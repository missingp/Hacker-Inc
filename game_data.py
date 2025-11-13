from typing import List

from game_models import Region, Sector


def create_initial_regions() -> List[Region]:
    return [
        Region(
            "北美",
            (320, 220),
            population=580,
            baseline_defense=68.0,
            sectors=[
                Sector("通信网络", defense=75.0, value=1.2),
                Sector("金融系统", defense=82.0, value=1.6),
                Sector("工业设施", defense=70.0, value=1.2),
                Sector("舆论媒体", defense=65.0, value=1.0),
            ],
        ),
        Region(
            "南美",
            (420, 420),
            population=430,
            baseline_defense=55.0,
            sectors=[
                Sector("通信网络", defense=60.0, value=1.0),
                Sector("金融系统", defense=58.0, value=1.3),
                Sector("工业设施", defense=52.0, value=1.1),
                Sector("舆论媒体", defense=50.0, value=0.9),
            ],
        ),
        Region(
            "欧洲",
            (650, 220),
            population=750,
            baseline_defense=72.0,
            sectors=[
                Sector("通信网络", defense=78.0, value=1.3),
                Sector("金融系统", defense=85.0, value=1.7),
                Sector("工业设施", defense=72.0, value=1.3),
                Sector("舆论媒体", defense=70.0, value=1.1),
            ],
        ),
        Region(
            "非洲",
            (650, 440),
            population=1300,
            baseline_defense=48.0,
            sectors=[
                Sector("通信网络", defense=52.0, value=1.1),
                Sector("金融系统", defense=50.0, value=1.0),
                Sector("工业设施", defense=55.0, value=1.2),
                Sector("舆论媒体", defense=45.0, value=0.9),
            ],
        ),
        Region(
            "中东",
            (770, 310),
            population=300,
            baseline_defense=62.0,
            sectors=[
                Sector("通信网络", defense=65.0, value=1.1),
                Sector("金融系统", defense=68.0, value=1.4),
                Sector("工业设施", defense=60.0, value=1.2),
                Sector("舆论媒体", defense=58.0, value=1.0),
            ],
        ),
        Region(
            "南亚",
            (870, 360),
            population=1800,
            baseline_defense=52.0,
            sectors=[
                Sector("通信网络", defense=60.0, value=1.2),
                Sector("金融系统", defense=55.0, value=1.3),
                Sector("工业设施", defense=58.0, value=1.4),
                Sector("舆论媒体", defense=50.0, value=1.0),
            ],
        ),
        Region(
            "东亚",
            (950, 260),
            population=1600,
            baseline_defense=78.0,
            sectors=[
                Sector("通信网络", defense=82.0, value=1.3),
                Sector("金融系统", defense=80.0, value=1.6),
                Sector("工业设施", defense=76.0, value=1.4),
                Sector("舆论媒体", defense=75.0, value=1.2),
            ],
        ),
        Region(
            "大洋洲",
            (1120, 520),
            population=50,
            baseline_defense=65.0,
            sectors=[
                Sector("通信网络", defense=68.0, value=1.1),
                Sector("金融系统", defense=70.0, value=1.3),
                Sector("工业设施", defense=62.0, value=1.0),
                Sector("舆论媒体", defense=60.0, value=0.9),
            ],
        ),
    ]

