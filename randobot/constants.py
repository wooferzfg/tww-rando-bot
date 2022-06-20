from collections import OrderedDict

STANDARD_PERMALINKS = OrderedDict([
    ("s4",        "MS45LjAAQQAFCyIAD3DAAgAAAAAAAQAA"),
    ("beginner",  "MS45LjAAQQAFAwIADzDAAYAcQIFBATAA"),
    ("co-op",     "MS45LjAAQQAVCyYAD3DABAAAAAAAAAAA"),
    ("allsanity", "MS45LjAAQQD//3+CD3BABQAAAAAAAAAA"),
    ("s3",        "MS45LjAAQQAXAwQATjDAAwgAAAAAAQAA"),
])

STANDARD_DEFAULT = ["s4"]
STANDARD_PATH = "wwrando"

SPOILER_LOG_PERMALINKS = OrderedDict([
    ("preset-a",  "MS45LjAAQQA3AyYCD1DAAgAAAAAAAAAA"),
    ("preset-b",  "MS45LjAAQQAXYyaCD1DAAgAAAAAAAAAA"),
    ("preset-c",  "MS45LjAAQQAXAyYCD5DAAgAAAAAAAAAA"),
    ("preset-d",  "MS45LjAAQQAXByYCD1DAAgAAAAAAAAAA"),
    ("preset-e",  "MS45LjAAQQAXA2YCD1DAAwAAAAAAAAAA"),
    ("preset-f",  "MS45LjAAQQAfCyYCD1DAAgAAAAAAAAAA"),
    ("s1",        "MS45LjAAQQAXAwYCDxDAAgAAAAAAAQAA"),
    ("allsanity", "MS45LjAAQQD//3+CD1BABQAAAAAAAAAA"),
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

S5_PERMALINKS = OrderedDict([
    ("default", "UzUuMABTNQAVAyIAJ3l8gAEWAIx7AIE+AAAA"),
])

S5_DEFAULT = ["default"]
S5_PATH = "wwrando-s5-tournament"
S5_VERSION = "S5.0"
S5_DOWNLOAD = "https://github.com/wooferzfg/wwrando/releases/tag/s5.0"

BANNABLE_PRESETS = SPOILER_LOG_DEFAULT
