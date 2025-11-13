from typing import List

import pygame

from game_archetypes import ARCHETYPES, get_archetype
from game_constants import FPS, HEIGHT, REGION_CONNECTIONS, TECH_HEIGHT, TECH_WIDTH, WIDTH
from game_models import GameState
from game_systems import find_region
from game_tech import TECH_MAP, TECH_ORDER, get_next_level_info


def render(screen: pygame.Surface, background: pygame.Surface, state: GameState, font: pygame.font.Font) -> None:
    if state.selecting_archetype:
        render_archetype_selection(screen, state, font)
    else:
        render_main_view(screen, background, state, font)


def render_main_view(screen: pygame.Surface, background: pygame.Surface, state: GameState, font: pygame.font.Font) -> None:
    screen.blit(background, (0, 0))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))

    info_panel = pygame.Surface((460, HEIGHT), pygame.SRCALPHA)
    info_panel.fill((0, 0, 0, 160))
    screen.blit(info_panel, (0, 0))

    title = font.render("黑客公司", True, (0, 255, 180))
    screen.blit(title, (20, 20))

    archetype = get_archetype(state.archetype_key)
    stats = [
        f"回合: {state.turn}",
        f"资源: {state.resources:.1f}",
        f"全球曝光: {state.exposure:.1f}",
        f"全球控制力: {state.total_influence_percent():.1f}%",
        "",
        f"身份: {archetype.name}",
        f"动机: {archetype.description}",
        "",
        "操作说明:",
        "左右键 切换区域 / 上下键 切换模块",
        "Space 发动攻击",
        "T 打开科技树",
        "Esc 退出游戏",
    ]

    if state.research_task:
        tech_def = TECH_MAP.get(state.research_task.tech_key)
        if tech_def:
            stats.append("")
            stats.append(
                f"研发中: {tech_def.name} Lv{state.research_task.target_level} "
                f"剩余 {state.research_task.remaining_turns} 回合"
            )
    else:
        stats.append("")
        stats.append("研发中: 空闲 (按 T 打开科技树)")

    for i, line in enumerate(stats):
        color = (180, 240, 255) if i < 4 else (160, 200, 220)
        text = font.render(line, True, color)
        screen.blit(text, (20, 60 + i * 28))

    selected_region = state.regions[state.selected_index]
    detail_start_y = 360
    detail_lines = [
        f"[{selected_region.name}]",
        f"综合防御: {selected_region.defense_level():.1f}",
        f"综合控制: {selected_region.overall_control_percent():.1f}%",
        f"平均曝光: {selected_region.exposure_level():.1f}",
    ]

    for i, line in enumerate(detail_lines):
        color = (255, 230, 150) if i == 0 else (220, 220, 220)
        text = font.render(line, True, color)
        screen.blit(text, (20, detail_start_y + i * 26))

    sector_start_y = detail_start_y + len(detail_lines) * 26 + 16
    for i, sector in enumerate(selected_region.sectors):
        marker = ">" if i == state.selected_sector_index else " "
        line = (
            f"{marker}{sector.name}: 控制 {sector.control_percent():.1f}% "
            f"| 防御 {sector.defense_level():.1f} | 曝光 {sector.exposure_level():.1f}"
        )
        color = (190, 255, 190) if i == state.selected_sector_index else (200, 200, 200)
        text = font.render(line, True, color)
        screen.blit(text, (20, sector_start_y + i * 24))

    tech_summary_start = sector_start_y + len(selected_region.sectors) * 24 + 16
    tech_lines: List[str] = []
    for key in TECH_ORDER:
        definition = TECH_MAP[key]
        level = state.tech_levels.get(key, 0)
        line = f"{definition.name}: Lv{level}"
        if state.research_task and state.research_task.tech_key == key:
            line += f" (研发中 剩余 {state.research_task.remaining_turns} 回合)"
        tech_lines.append(line)

    for i, line in enumerate(tech_lines):
        text = font.render(line, True, (180, 220, 200))
        screen.blit(text, (20, tech_summary_start + i * 24))

    message_start_y = tech_summary_start + len(tech_lines) * 24 + 18
    message_lines = state.message.split(" | ")
    for i, line in enumerate(message_lines[:6]):
        text = font.render(line, True, (210, 210, 230))
        screen.blit(text, (20, message_start_y + i * 24))

    drawn_connections: set[tuple[str, str]] = set()
    for region in state.regions:
        for neighbor_name in REGION_CONNECTIONS.get(region.name, []):
            neighbor = find_region(state, neighbor_name)
            if not neighbor:
                continue
            key = tuple(sorted((region.name, neighbor.name)))
            if key in drawn_connections:
                continue
            drawn_connections.add(key)

            influence_avg = (region.overall_control_percent() + neighbor.overall_control_percent()) / 200.0
            line_color = (
                int(40 + 120 * influence_avg),
                int(120 + 80 * influence_avg),
                int(200 + 40 * influence_avg),
            )
            line_width = 2 + int(4 * influence_avg)
            pygame.draw.line(screen, line_color, region.position, neighbor.position, line_width)

    for idx, region in enumerate(state.regions):
        x, y = region.position
        radius = 18
        influence_ratio = region.overall_control_percent() / 100.0
        color = (
            int(40 + 180 * influence_ratio),
            int(80 + 140 * (1 - influence_ratio)),
            180,
        )
        pygame.draw.circle(screen, color, (x, y), radius)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), radius, 2)

        if idx == state.selected_index:
            pygame.draw.circle(screen, (255, 255, 255), (x, y), radius + 6, 2)

        name_text = font.render(region.name, True, (255, 255, 255))
        screen.blit(name_text, (x - name_text.get_width() // 2, y + radius + 4))


def render_archetype_selection(screen: pygame.Surface, state: GameState, font: pygame.font.Font) -> None:
    screen.fill((8, 14, 24))

    panel_width = WIDTH - 240
    panel_height = HEIGHT - 200
    panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel.fill((18, 32, 44, 235))
    screen.blit(panel, (120, 100))

    title = font.render("选择黑客身份", True, (0, 255, 220))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 130))

    hint_lines = [
        "↑↓ 切换身份",
        "Enter / Space 确认",
        "Esc 退出游戏",
    ]
    for i, line in enumerate(hint_lines):
        text = font.render(line, True, (180, 210, 240))
        screen.blit(text, (140, 180 + i * 26))

    list_start_y = 240
    for idx, archetype in enumerate(ARCHETYPES):
        selected = idx == state.archetype_selection_index
        prefix = ">" if selected else " "
        line = f"{prefix}{archetype.name}  — {archetype.description}"
        color = (120, 240, 200) if selected else (210, 220, 230)
        text = font.render(line, True, color)
        screen.blit(text, (160, list_start_y + idx * 36))

    message_lines = state.message.split(" | ")
    for i, line in enumerate(message_lines[:4]):
        text = font.render(line, True, (200, 210, 230))
        screen.blit(text, (140, HEIGHT - 140 + i * 26))


def render_tech_screen(screen: pygame.Surface, state: GameState, font: pygame.font.Font) -> None:
    screen.fill((12, 20, 32))

    panel = pygame.Surface((TECH_WIDTH - 120, TECH_HEIGHT - 120), pygame.SRCALPHA)
    panel.fill((18, 30, 44, 235))
    screen.blit(panel, (60, 60))

    title = font.render("科技树", True, (0, 255, 220))
    screen.blit(title, (TECH_WIDTH // 2 - title.get_width() // 2, 90))

    info_lines = [
        f"当前资源: {state.resources:.1f}",
        "操作: ↑↓选择 | 回车/空格 开始研发 | T / ESC 返回",
    ]
    for i, line in enumerate(info_lines):
        text = font.render(line, True, (200, 220, 240))
        screen.blit(text, (90, 130 + i * 26))

    list_start_y = 190
    for idx, tech_key in enumerate(TECH_ORDER):
        definition = TECH_MAP[tech_key]
        level = state.tech_levels.get(tech_key, 0)
        next_level = get_next_level_info(tech_key, level)
        selected = idx == state.tech_selection_index
        prefix = ">" if selected else " "
        status = "已满级"
        if next_level:
            status = f"成本 {next_level.cost:.0f} | 时长 {next_level.duration} 回合"
        if state.research_task and state.research_task.tech_key == tech_key:
            status = f"研发中 剩余 {state.research_task.remaining_turns} 回合"

        line = f"{prefix}{definition.name}  Lv{level}  — {status}"
        color = (120, 240, 200) if selected else (200, 210, 220)
        text = font.render(line, True, color)
        screen.blit(text, (110, list_start_y + idx * 34))

        if selected:
            desc_lines = [
                definition.description,
            ]
            if next_level:
                desc_lines.append(f"下一等级: {next_level.description}")
            else:
                desc_lines.append("下一等级: 已达最大等级。")
            for j, desc in enumerate(desc_lines):
                desc_text = font.render(desc, True, (190, 200, 230))
                screen.blit(desc_text, (120, list_start_y + len(TECH_ORDER) * 34 + 20 + j * 26))

    message_lines = state.message.split(" | ")
    for i, line in enumerate(message_lines[:4]):
        text = font.render(line, True, (210, 210, 230))
        screen.blit(text, (90, TECH_HEIGHT - 110 + i * 24))


def summary_screen(
    screen: pygame.Surface,
    state: GameState,
    font: pygame.font.Font,
    clock: pygame.time.Clock,
    background: pygame.Surface,
) -> None:
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
                break

        screen.blit(background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        result_text = "胜利！全球网络被你掌控。" if state.victory else "失败。全球防线联合封锁。"
        result = font.render(result_text, True, (255, 240, 180))
        screen.blit(result, (WIDTH // 2 - result.get_width() // 2, HEIGHT // 2 - 60))

        stats: List[str] = [
            f"最终回合: {state.turn}",
            f"全球控制力: {state.total_influence_percent():.1f}%",
            f"全球曝光: {state.exposure:.1f}",
            "按任意键退出。",
        ]

        for i, line in enumerate(stats):
            text = font.render(line, True, (220, 220, 220))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + i * 30))

        pygame.display.flip()
        clock.tick(FPS)

