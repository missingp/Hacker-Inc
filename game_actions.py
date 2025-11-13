from dataclasses import dataclass
from typing import Dict, Tuple

from game_constants import RESOURCE_GAIN_BASE


@dataclass(frozen=True)
class ActionInfo:
    key: str
    name: str
    description: str
    emphasis: Dict[str, float]
    success_bonus: float
    spread_range: Tuple[float, float]
    resource_gain: float
    resource_cost: float
    sector_exposure_range: Tuple[float, float]
    global_exposure_range: Tuple[float, float]
    defense_shift_range: Tuple[float, float] | None = None
    baseline_shift_range: Tuple[float, float] | None = None
    fail_sector_exposure_range: Tuple[float, float] = (4.0, 8.0)
    fail_global_exposure_range: Tuple[float, float] = (4.0, 8.0)


ACTION_DEFINITIONS: Dict[str, ActionInfo] = {
    "social_engineering": ActionInfo(
        key="social_engineering",
        name="社会工程学与钓鱼攻击",
        description="利用人性弱点获取凭证与舆论控制，适合渗透金融与媒体板块。",
        emphasis={
            "通信网络": 0.9,
            "金融系统": 1.2,
            "工业设施": 0.6,
            "舆论媒体": 1.4,
        },
        success_bonus=12.0,
        spread_range=(4.0, 8.0),
        resource_gain=RESOURCE_GAIN_BASE * 0.7,
        resource_cost=0.0,
        sector_exposure_range=(2.0, 5.0),
        global_exposure_range=(1.5, 3.5),
        defense_shift_range=(-2.0, -0.5),
    ),
    "network_intrusion": ActionInfo(
        key="network_intrusion",
        name="网络入侵与渗透测试",
        description="通过漏洞利用和横向移动控制核心网络，打击通信与工业设施。",
        emphasis={
            "通信网络": 1.4,
            "金融系统": 0.8,
            "工业设施": 1.2,
            "舆论媒体": 0.7,
        },
        success_bonus=6.0,
        spread_range=(6.0, 12.0),
        resource_gain=RESOURCE_GAIN_BASE * 0.9,
        resource_cost=4.0,
        sector_exposure_range=(3.0, 6.0),
        global_exposure_range=(3.0, 6.0),
        defense_shift_range=(-6.0, -3.0),
        baseline_shift_range=(-3.0, -1.0),
        fail_sector_exposure_range=(6.0, 10.0),
        fail_global_exposure_range=(5.0, 9.0),
    ),
    "malware": ActionInfo(
        key="malware",
        name="恶意软件与病毒传播",
        description="投放木马、勒索或蠕虫，实现快速扩散，风险与曝光同时大幅提升。",
        emphasis={
            "通信网络": 1.3,
            "金融系统": 0.9,
            "工业设施": 1.3,
            "舆论媒体": 0.8,
        },
        success_bonus=2.0,
        spread_range=(7.0, 14.0),
        resource_gain=RESOURCE_GAIN_BASE * 0.6,
        resource_cost=3.0,
        sector_exposure_range=(4.0, 8.0),
        global_exposure_range=(3.5, 7.0),
        defense_shift_range=(-4.0, -1.5),
        fail_sector_exposure_range=(6.0, 12.0),
        fail_global_exposure_range=(6.0, 10.0),
    ),
    "data_theft": ActionInfo(
        key="data_theft",
        name="数据泄露与身份盗窃",
        description="窃取高价值数据牟利或敲诈，对金融与媒体领域尤为有效。",
        emphasis={
            "通信网络": 0.8,
            "金融系统": 1.5,
            "工业设施": 0.7,
            "舆论媒体": 1.1,
        },
        success_bonus=10.0,
        spread_range=(3.0, 7.0),
        resource_gain=RESOURCE_GAIN_BASE * 1.8,
        resource_cost=2.0,
        sector_exposure_range=(2.5, 5.5),
        global_exposure_range=(2.0, 4.0),
        defense_shift_range=(-3.0, -1.0),
        fail_sector_exposure_range=(5.0, 9.0),
        fail_global_exposure_range=(5.0, 9.0),
    ),
}

ACTION_ORDER = list(ACTION_DEFINITIONS.keys())

