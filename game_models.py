from dataclasses import dataclass, field
from typing import Dict, List, Optional

from game_tech import TECH_ORDER


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass
class ResearchTask:
    tech_key: str
    target_level: int
    remaining_turns: int


@dataclass
class Sector:
    name: str
    defense: float
    value: float = 1.0
    control: float = 0.0
    exposure: float = 0.0

    def control_percent(self) -> float:
        return clamp(self.control, 0.0, 100.0)

    def defense_level(self) -> float:
        return max(0.0, self.defense)

    def exposure_level(self) -> float:
        return max(0.0, self.exposure)


@dataclass
class Region:
    name: str
    position: tuple[int, int]
    population: int
    baseline_defense: float
    sectors: List[Sector] = field(default_factory=list)
    exposure: float = 0.0

    def overall_control_percent(self) -> float:
        if not self.sectors:
            return 0.0
        total_value = sum(sector.value for sector in self.sectors)
        if total_value <= 0:
            return 0.0
        weighted = sum(sector.control_percent() * sector.value for sector in self.sectors)
        return weighted / total_value

    def defense_level(self) -> float:
        return max(0.0, self.baseline_defense)

    def exposure_level(self) -> float:
        return max(0.0, self.exposure)

    def recalc_exposure(self) -> None:
        if not self.sectors:
            self.exposure = 0.0
            return
        avg = sum(sector.exposure_level() for sector in self.sectors) / len(self.sectors)
        self.exposure = clamp(avg, 0, 100)

    def get_sector(self, index: int) -> Sector:
        return self.sectors[index]

    def get_sector_by_name(self, name: str) -> Optional[Sector]:
        for sector in self.sectors:
            if sector.name == name:
                return sector
        return None


@dataclass
class GameState:
    regions: List[Region] = field(default_factory=list)
    resources: float = 5.0
    exposure: float = 0.0
    turn: int = 0
    selected_index: int = 0
    selected_sector_index: int = 0
    message: str = "选择一个行动开始入侵。"
    running: bool = True
    game_over: bool = False
    victory: bool = False
    archetype_key: str = "economic"
    available_actions: List[str] = field(default_factory=list)
    tech_levels: Dict[str, int] = field(default_factory=lambda: {key: 0 for key in TECH_ORDER})
    tech_selection_index: int = 0
    research_task: Optional[ResearchTask] = None
    selecting_archetype: bool = True
    archetype_selection_index: int = 0

    def total_influence_percent(self) -> float:
        if not self.regions:
            return 0.0
        total_population = sum(r.population for r in self.regions)
        weighted = sum(r.population * (r.overall_control_percent() / 100.0) for r in self.regions)
        return (weighted / total_population) * 100.0

    def add_message(self, text: str) -> None:
        self.message = text

