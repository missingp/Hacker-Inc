from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class TechLevel:
    cost: float
    duration: int
    description: str


@dataclass(frozen=True)
class TechDefinition:
    key: str
    name: str
    description: str
    levels: Tuple[TechLevel, ...]


TECH_DEFINITIONS: List[TechDefinition] = [
    TechDefinition(
        key="stealth",
        name="隐蔽性",
        description="降低曝光风险，提升入侵成功率。",
        levels=(
            TechLevel(cost=6, duration=2, description="曝光降低 15%，成功率 +6%"),
            TechLevel(cost=9, duration=3, description="曝光降低 30%，成功率 +12%"),
            TechLevel(cost=13, duration=4, description="曝光降低 45%，成功率 +18%"),
        ),
    ),
    TechDefinition(
        key="sabotage",
        name="破坏性",
        description="强化攻坚与资源掠夺能力。",
        levels=(
            TechLevel(cost=6, duration=3, description="资源收益 +20%，防御削弱 +15%"),
            TechLevel(cost=10, duration=4, description="资源收益 +40%，防御削弱 +30%"),
            TechLevel(cost=15, duration=5, description="资源收益 +60%，防御削弱 +45%"),
        ),
    ),
    TechDefinition(
        key="propagation",
        name="传播性",
        description="扩大渗透范围，加速邻域感染。",
        levels=(
            TechLevel(cost=7, duration=3, description="扩散强度 +25%，被动传播提升"),
            TechLevel(cost=11, duration=4, description="扩散强度 +50%，被动传播进一步提升"),
            TechLevel(cost=16, duration=5, description="扩散强度 +75%，被动传播显著强化"),
        ),
    ),
]

TECH_MAP: Dict[str, TechDefinition] = {tech.key: tech for tech in TECH_DEFINITIONS}
TECH_ORDER: List[str] = [tech.key for tech in TECH_DEFINITIONS]


def get_next_level_info(tech_key: str, current_level: int) -> Optional[TechLevel]:
    tech = TECH_MAP.get(tech_key)
    if not tech:
        return None
    if current_level >= len(tech.levels):
        return None
    return tech.levels[current_level]


def max_level(tech_key: str) -> int:
    tech = TECH_MAP.get(tech_key)
    return len(tech.levels) if tech else 0

