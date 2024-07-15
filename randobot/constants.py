from collections import OrderedDict
from enum import Enum


class SeedType(Enum):
    STANDARD = 1
    SPOILER_LOG = 2
    RANDOM_SETTINGS = 3


STANDARD_PERMALINKS = OrderedDict([
    ("s6",           "MS4xMC4wAEEAFwMiAHPowgMMsACCcQ8AAMkHAAAA"),
    ("s5",           "MS4xMC4wAEEAFQMiAJPowAMMsACCcQ8AAMkHAQAA"),
    ("s4",           "MS4xMC4wAEEABQsiAAUAvgMcsAACAAAAAAGAIAAA"),
    ("miniblins-s1", "MS4xMC4wAEEABwMCAHOGwAMMcADC+Q8AAskPKQAG"),
    ("co-op",        "MS4xMC4wAEEAFQsmANsMwQMcMAGCcQ8AAMkHAAAA"),
    ("allsanity",    "MS4xMC4wAEEA//9/gtsMwQMcUAECAAAAAAkAAAAA"),
    ("s3",           "MS4xMC4wAEEAFwMEAAQAvhMM8AADAAAAAAGAIAAA"),
])

STANDARD_DEFAULT = ["s6"]
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

S7_PERMALINKS = OrderedDict([
    ("s7",   "eJwz1DM00DOIt7RITrQwM2VwZLhrVMTF0czAwMDCAAUcIEKAgYGJg3GlykMQAyoRwuLAsmajv8G85QwMk/iB6jUB5s8MHw=="),
])
S7_DEFAULT = ["s7"]

S7_SL_PERMALINKS = OrderedDict([
    ("s7-sl", "eJwz1DM00DOIt7RITrQwM2VwZLhrVMTF0czAwMDCAAUcIEKAgYGJg3GlykMQAyoRwuLAsmajv8G85QwMk/iB6jkB5q8L/w=="),
])
S7_SL_DEFAULT = ["s7-sl"]

RUNNER_AGREEMENTS = OrderedDict([
    ("4rbm",     "4-Required Bosses Mode"),
    ("nosword",  "No Starting Sword"),
    ("der",      "Randomized Dungeon Entrances"),
    ("ber",      "Randomized Boss Entrances"),
    ("keys",     "Key-Lunacy"),
    ("tingle",   "Tingle Chests replacing Dungeon Secrets"),
    ("expen",    "Expensive Purchases"),
    ("subs",     "Submarines"),
    ("minis",    "Minigames"),
    ("plats",    "Lookout Platforms on Islet of Steel, Southern Fairy, and Seven-Star"),
])

S7_PATH = "wwrando-s7"
S7_DOWNLOAD = "https://github.com/tanjo3/wwrando/releases/tag/s7-v1"
S7_TRACKER = "https://wooferzfg.me/tww-rando-tracker/s7-tournament"

DEV_PERMALINKS = OrderedDict([
    ("default", "eJwz1LPUMzSIT0ktY3BkYGdkZigwYXjAWMDAKMUABg0MJAAAZlcFog=="),
])

DEV_DEFAULT = ["default"]
DEV_PATH = "wwrando-dev-tanjo3"
DEV_VERSION = "1.9.10_dev"
DEV_DOWNLOAD = "https://github.com/tanjo3/wwrando/releases"

MP_PERMALINKS = OrderedDict([
    ("miniblins",   "MS4xMC4wXzVmMWJhZTYAQQBNMEBMAEAEEvETzn8AEEh+SAEAIw=="),
    ("mixed-pools", "MS4xMC4wXzVmMWJhZTYAQQDfsGDs4E8ExPETjHsAAEg+AAAAIA=="),
])
MP_DEFAULT = ["mixed-pools"]

MP_SL_PERMALINKS = OrderedDict([
    ("mixed-pools-sl", "MS4xMC4wXzVmMWJhZTYAQQDfsGDs4E8ExPETjHsAAEg+AAAAAA=="),
])
MP_SL_DEFAULT = ["mixed-pools-sl"]

MP_PATH = "wwrando-mixed-pools"
MP_DOWNLOAD = "https://github.com/wooferzfg/wwrando/releases/tag/mixed-pools-build"

RS_PATH = "wwrando-random-settings"
RS_VERSION = "RS1.4.0-dev3"
RS_DOWNLOAD = "https://github.com/Aelire/wwrando/releases/tag/RS1.4.0-dev3"
RS_TRACKER = "https://jaysc.github.io/tww-rando-tracker-rs/"
RS_DEFAULT = ["random-settings"]
RS_PERMALINKS = OrderedDict([
    ("random-settings", "UlMxLjQuMC1kZXYzAEEAgQU="),
])

BANNABLE_PRESETS = SPOILER_LOG_DEFAULT

MINIMUM_BREAK_DURATION = 5
MINIMUM_BREAK_INTERVAL = 60

PERMALINK_PREFIXES = ["MS4", "eJw", "UlM"]
