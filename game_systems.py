import math
import random
from typing import List, Optional

from game_constants import EXPOSURE_THRESHOLD, REGION_CONNECTIONS, VICTORY_INFLUENCE
from game_models import GameState, Region, Sector, ResearchTask, clamp
from game_tech import TECH_MAP, get_next_level_info


def get_tech_level(state: GameState, tech_key: str) -> int:
    return state.tech_levels.get(tech_key, 0)


def find_region(state: GameState, name: str) -> Optional[Region]:
    for region in state.regions:
        if region.name == name:
            return region
    return None


def spread_influence(state: GameState) -> List[str]:
    spread_events: List[str] = []
    propagation_level = get_tech_level(state, "propagation")
    stealth_level = get_tech_level(state, "stealth")
    chance_bonus = propagation_level * 5.0
    spread_multiplier = 1.0 + propagation_level * 0.3
    exposure_multiplier = max(0.45, 1.0 - stealth_level * 0.18)
    secondary_multiplier = 1.0 + propagation_level * 0.25

    for origin in state.regions:
        comms = origin.get_sector_by_name("通信网络")
        if not comms:
            continue
        origin_ratio = comms.control_percent() / 100.0
        if origin_ratio <= 0:
            continue

        neighbors = REGION_CONNECTIONS.get(origin.name, [])
        for neighbor_name in neighbors:
            neighbor = find_region(state, neighbor_name)
            if not neighbor:
                continue
            neighbor_comms = neighbor.get_sector_by_name("通信网络")
            if not neighbor_comms:
                continue
            if neighbor_comms.control_percent() >= 100:
                continue

            base_chance = 10 + origin_ratio * 60 - neighbor_comms.defense_level() * 0.25
            base_chance += chance_bonus
            base_chance -= neighbor.defense_level() * 0.1
            base_chance = clamp(base_chance, 5, 80)
            roll = random.random() * 100
            if roll > base_chance:
                continue

            spread_amount = random.uniform(3, 7) * origin_ratio * spread_multiplier
            neighbor_comms.control = clamp(neighbor_comms.control + spread_amount, 0, 100)
            neighbor_comms.exposure = clamp(
                neighbor_comms.exposure + random.uniform(1, 3) * exposure_multiplier,
                0,
                100,
            )
            neighbor.recalc_exposure()
            state.exposure = clamp(
                state.exposure + random.uniform(0.5, 1.2) * exposure_multiplier,
                0,
                999,
            )
            spread_events.append(f"{origin.name} 的感染向 {neighbor.name} 蔓延 (+{spread_amount:.1f}%)")

            for secondary_name in ("金融系统", "工业设施"):
                secondary = neighbor.get_sector_by_name(secondary_name)
                if not secondary:
                    continue
                leverage = comms.control_percent() / 100.0
                bonus = random.uniform(1.0, 2.5) * leverage * secondary_multiplier
                secondary.control = clamp(secondary.control + bonus, 0, 100)
                secondary.exposure = clamp(
                    secondary.exposure + random.uniform(0.5, 1.5) * exposure_multiplier,
                    0,
                    100,
                )
            neighbor.recalc_exposure()

    return spread_events


def apply_passive_effects(state: GameState) -> str:
    income = 0.0
    cover = 0.0
    defense_breaks = 0
    stealth_level = get_tech_level(state, "stealth")
    sabotage_level = get_tech_level(state, "sabotage")

    for region in state.regions:
        finance = region.get_sector_by_name("金融系统")
        if finance:
            ratio = finance.control_percent() / 100.0
            income += finance.value * ratio * 0.9

        media = region.get_sector_by_name("舆论媒体")
        if media:
            ratio = media.control_percent() / 100.0
            cover += media.value * ratio * 0.6

        comms = region.get_sector_by_name("通信网络")
        if comms and comms.control_percent() > 60:
            region.baseline_defense = clamp(region.baseline_defense - 0.6, 20, 95)
            defense_breaks += 1

        region.recalc_exposure()

    if income > 0:
        income *= 1.0 + sabotage_level * 0.3
        state.resources = clamp(state.resources + income, 0, 999)
    if cover > 0:
        cover *= 1.0 + stealth_level * 0.4
        state.exposure = clamp(state.exposure - cover, 0, 999)

    messages: List[str] = []
    if income > 0:
        messages.append(f"金融抽取 +{income:.1f} 资源")
    if cover > 0:
        messages.append(f"舆论掩护 降低曝光 {cover:.1f}")
    if defense_breaks > 0:
        bonus_note = " (破坏性加成)" if sabotage_level > 0 else ""
        messages.append(f"通信控制削弱防线{bonus_note}")

    return " | ".join(messages)


def start_research(state: GameState, tech_key: str) -> None:
    definition = TECH_MAP.get(tech_key)
    if not definition:
        state.add_message("未知科技。")
        return

    current_level = state.tech_levels.get(tech_key, 0)
    if current_level >= len(definition.levels):
        state.add_message(f"{definition.name} 已达到最高等级。")
        return

    if state.research_task:
        state.add_message("已有科技正在研究中。")
        return

    next_level = get_next_level_info(tech_key, current_level)
    if not next_level:
        state.add_message(f"{definition.name} 已达到最高等级。")
        return

    if state.resources < next_level.cost:
        state.add_message("资源不足，无法研发该科技。")
        return

    state.resources = clamp(state.resources - next_level.cost, 0, 999)
    state.research_task = ResearchTask(
        tech_key=tech_key,
        target_level=current_level + 1,
        remaining_turns=next_level.duration,
    )
    state.add_message(
        f"开始研究 {definition.name} Lv{current_level + 1}，需要 {next_level.duration} 回合完成。"
    )


def advance_research(state: GameState) -> str:
    task = state.research_task
    if not task:
        return ""

    task.remaining_turns -= 1
    if task.remaining_turns <= 0:
        definition = TECH_MAP.get(task.tech_key)
        state.tech_levels[task.tech_key] = task.target_level
        state.research_task = None
        if definition:
            return f"{definition.name} Lv{task.target_level} 研发完成。"
        return "科技研发完成。"

    definition = TECH_MAP.get(task.tech_key)
    if definition:
        return f"{definition.name} 研发剩余 {task.remaining_turns} 回合。"
    return "研发进度推进。"


def execute_attack(state: GameState) -> None:
    if not state.regions:
        state.add_message("暂无可攻击目标。")
        return

    region = state.regions[state.selected_index]
    sector = region.get_sector(state.selected_sector_index)
    stealth_level = get_tech_level(state, "stealth")
    sabotage_level = get_tech_level(state, "sabotage")
    propagation_level = get_tech_level(state, "propagation")

    base_chance = 50.0
    base_chance += stealth_level * 6.0
    base_chance += propagation_level * 1.5
    base_chance -= sector.defense_level() * 0.32
    base_chance -= region.defense_level() * 0.14
    base_chance += math.log1p(max(state.resources, 0.1)) * 5.2
    base_chance = clamp(base_chance, 5, 92)

    success = random.random() * 100 <= base_chance
    if success:
        spread_base = random.uniform(5, 10)
        spread_multiplier = 1.0 + propagation_level * 0.25
        spread_gain = spread_base * spread_multiplier
        sector.control += spread_gain

        resource_gain = 2.5 + sabotage_level * 1.6
        state.resources = clamp(state.resources + resource_gain, 0, 999)

        exposure_gain = max(0.0, random.uniform(2.5, 5.5) - stealth_level * 1.3)
        state.exposure = clamp(state.exposure + exposure_gain, 0, 999)
        sector.exposure = clamp(
            sector.exposure + exposure_gain * (0.8 + propagation_level * 0.1),
            0,
            100,
        )

        defense_reduction = random.uniform(1.5, 3.5) * (1.0 + sabotage_level * 0.45)
        sector.defense = clamp(sector.defense - defense_reduction, 20, 95)
        region.baseline_defense = clamp(region.baseline_defense - defense_reduction * 0.4, 20, 95)

        action_message = (
            f"{region.name} 的{sector.name} 被成功渗透，控制 +{spread_gain:.1f}%，资源 +{resource_gain:.1f}。"
        )
    else:
        exposure_penalty = max(2.5, random.uniform(4.0, 8.0) - stealth_level * 1.0)
        state.exposure = clamp(state.exposure + exposure_penalty, 0, 999)
        sector.exposure = clamp(sector.exposure + exposure_penalty + 1.5, 0, 100)
        sector.defense = clamp(sector.defense + random.uniform(1.5, 3.0), 20, 95)
        region.baseline_defense = clamp(region.baseline_defense + random.uniform(0.5, 1.5), 20, 95)
        action_message = f"{region.name} 的{sector.name} 加固防线，曝光上升 {exposure_penalty:.1f}。"

    sector.control = clamp(sector.control, 0, 100)
    sector.exposure = clamp(sector.exposure, 0, 100)
    region.recalc_exposure()
    state.resources = clamp(state.resources, 0, 999)

    spread_events = spread_influence(state)
    passive_message = apply_passive_effects(state)
    state.turn += 1
    research_message = advance_research(state)

    combined_messages = [
        msg
        for msg in (
            action_message,
            " | ".join(spread_events) if spread_events else "",
            passive_message,
            research_message,
        )
        if msg
    ]
    if combined_messages:
        state.add_message(" | ".join(combined_messages))
    else:
        state.add_message("行动完成。")

    security_response(state)


def security_response(state: GameState) -> None:
    global_exposure = state.exposure
    stealth_level = get_tech_level(state, "stealth")
    sabotage_level = get_tech_level(state, "sabotage")
    backlash_multiplier = max(0.35, 1.0 - stealth_level * 0.2)
    defense_recovery_multiplier = max(0.55, 1.0 - sabotage_level * 0.12)

    for region in state.regions:
        for sector in region.sectors:
            control_ratio = sector.control_percent() / 100.0
            if control_ratio > 0:
                backlash = (
                    (sector.defense_level() / 90 + region.defense_level() / 120)
                    * random.uniform(1.0, 2.2)
                    * backlash_multiplier
                )
                sector.control = clamp(sector.control - backlash, 0, 100)
                sector.exposure = clamp(
                    sector.exposure + random.uniform(0.5, 2.0) * backlash_multiplier,
                    0,
                    100,
                )

            defense_boost = (global_exposure / 100) * random.uniform(0.4, 1.4) * defense_recovery_multiplier
            sector.defense = clamp(sector.defense + defense_boost, 20, 95)

            if sector.exposure_level() > 35:
                sector.defense = clamp(
                    sector.defense + random.uniform(1, 4) * defense_recovery_multiplier,
                    20,
                    95,
                )

        region.baseline_defense = clamp(
            region.baseline_defense
            + (global_exposure / 100) * random.uniform(0.5, 1.8) * defense_recovery_multiplier,
            25,
            95,
        )

        if region.exposure_level() > 30:
            region.baseline_defense = clamp(
                region.baseline_defense + random.uniform(0.5, 1.5) * defense_recovery_multiplier,
                25,
                95,
            )

        region.recalc_exposure()

    if global_exposure > EXPOSURE_THRESHOLD:
        state.game_over = True
        state.victory = False
        state.add_message("全球网络警戒，行动失败。")
        state.running = False

    if state.total_influence_percent() >= VICTORY_INFLUENCE:
        state.game_over = True
        state.victory = True
        state.add_message("世界网络尽在掌握！胜利！")
        state.running = False

