from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class HackerArchetype:
    key: str
    name: str
    description: str
    action_keys: Tuple[str, ...]


ARCHETYPES: List[HackerArchetype] = [
    HackerArchetype(
        key="economic",
        name="经济利益型",
        description="以牟利为目标，擅长钓鱼诈骗与高价值数据窃取。",
        action_keys=("social_engineering", "data_theft"),
    ),
    HackerArchetype(
        key="corporate",
        name="竞争优势型",
        description="为竞争优势渗透对手系统，侧重网络入侵与情报窃取。",
        action_keys=("network_intrusion", "data_theft"),
    ),
    HackerArchetype(
        key="sabotage",
        name="破坏与报复型",
        description="以破坏为主，重视渗透关键基础设施并投放恶意软件。",
        action_keys=("network_intrusion", "malware"),
    ),
    HackerArchetype(
        key="activist",
        name="社会/政治诉求型",
        description="通过社会工程与大规模传播揭露事件或施压政府。",
        action_keys=("social_engineering", "malware"),
    ),
]

ARCHETYPE_MAP: Dict[str, HackerArchetype] = {arch.key: arch for arch in ARCHETYPES}
ARCHETYPE_KEYS: List[str] = [arch.key for arch in ARCHETYPES]
DEFAULT_ARCHETYPE_KEY = ARCHETYPE_KEYS[0]


def get_archetype(key: str) -> HackerArchetype:
    return ARCHETYPE_MAP[key]


def get_next_archetype_key(current_key: str, delta: int = 1) -> str:
    if current_key not in ARCHETYPE_MAP:
        return DEFAULT_ARCHETYPE_KEY
    index = ARCHETYPE_KEYS.index(current_key)
    new_index = (index + delta) % len(ARCHETYPE_KEYS)
    return ARCHETYPE_KEYS[new_index]

