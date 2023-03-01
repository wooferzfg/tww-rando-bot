from collections import OrderedDict
from enum import Enum


class SeedType(Enum):
    STANDARD = 1
    SPOILER_LOG = 2
    DEV = 3
    RANDOM_SETTINGS = 4
    S5 = 5


STANDARD_PERMALINKS = OrderedDict([
    ("s5",        "MS4xMC4wAEEAFQMiAJPowAMMsACCcQ8AAMkHAQAA"),
    ("s4",        "MS4xMC4wAEEABQsiAAUAvgMcsAACAAAAAAGAIAAA"),
    ("beginner",  "MS4xMC4wAEEABQMCAHOGwAMMcADC+Q8AAskPKQAG"),
    ("co-op",     "MS4xMC4wAEEAFQsmANsMwQMcMAECAAAAAAmAAAAA"),
    ("allsanity", "MS4xMC4wAEEA//9/gtsMwQMcUAECAAAAAAkAAAAA"),
    ("s3",        "MS4xMC4wAEEAFwMEAAQAvhMM8AADAAAAAAGAIAAA"),
])

STANDARD_DEFAULT = ["s5"]
STANDARD_PATH = "wwrando"

SPOILER_LOG_PERMALINKS = OrderedDict([
    ("preset-a",  "MS4xMC4wAEEANwMmAgEAoAMUsAACAAAAAAGAAAAA"),
    ("preset-b",  "MS4xMC4wAEEAF2MmggEAoAMUsAACAAAAAAGAAAAA"),
    ("preset-c",  "MS4xMC4wAEEAFwMmAgEAoAMksAACAAAAAAGAAAAA"),
    ("preset-d",  "MS4xMC4wAEEAFwcmAgEAoAMUsAACAAAAAAGAAAAA"),
    ("preset-e",  "MS4xMC4wAEEAFwNmAgEAoAMU8AACAAAAAAGAAAAA"),
    ("preset-f",  "MS4xMC4wAEEAHwsmAgEAoAMUsAACAAAAAAGAAAAA"),
    ("s1",        "MS4xMC4wAEEAFwMGAgEAoAMEsAACAAAAAAGAIAAA"),
    ("allsanity", "MS4xMC4wAEEA//9/ggMAoAMUUAECAAAAAAEAAAAA"),
])

SETTINGS_DESCRIPTIONS = OrderedDict([
    ("preset-a",  "Long Sidequests"),
    ("preset-b",  "Triforce Charts, Big Octos and Gunboats"),
    ("preset-c",  "Swordless"),
    ("preset-d",  "Lookout Platforms and Rafts"),
    ("preset-e",  "4 Dungeon Race Mode, Key-Lunacy"),
    ("preset-f",  "Combat Secret Caves, Submarines"),
])

SPOILER_LOG_DEFAULT = ["preset-a", "preset-b", "preset-c", "preset-d", "preset-e", "preset-f"]
DEFAULT_PLANNING_TIME = 60
MINIMUM_PLANNING_TIME = 20

DEV_PERMALINKS = OrderedDict([
    ("default", "eJwz1LPUMzSIT0ktY3BkYGdkZigwYXjAWMDAKMUABg0MJAAAZlcFog=="),
])

DEV_DEFAULT = ["default"]
DEV_PATH = "wwrando-dev-tanjo3"
DEV_VERSION = "1.9.10_dev"
DEV_DOWNLOAD = "https://github.com/tanjo3/wwrando/releases"

RS_PATH = "wwrando-random-settings"
RS_VERSION = "v1.3.1"
RS_DOWNLOAD = "https://github.com/tanjo3/wwrando/releases/tag/RS_v1.3.1"
RS_TRACKER = "https://jaysc.github.io/tww-rando-tracker-rs/"

S5_PERMALINKS = OrderedDict([
    ("default", "UzUuMABTNQAVAyIAJ3l8gAEWAIx7AIE+AAAA"),
])

S5_DEFAULT = ["default"]
S5_PATH = "wwrando-s5-tournament"
S5_VERSION = "S5.0"
S5_DOWNLOAD = "https://github.com/wooferzfg/wwrando/releases/tag/s5.0"

BANNABLE_PRESETS = SPOILER_LOG_DEFAULT

MINIMUM_BREAK_DURATION = 5
MINIMUM_BREAK_INTERVAL = 60
