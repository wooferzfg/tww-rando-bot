from collections import OrderedDict

STANDARD_PERMALINKS = OrderedDict([
    ("s4",        "MS45LjAAQQAFCyIAD3DAAgAAAAAAAQAA"),
    ("beginner",  "MS45LjAAQQAFAwIADzDAAYAcQIFBATAA"),
    ("co-op",     "MS45LjAAQQAVCyYAD3DABAAAAAAAAAAA"),
    ("allsanity", "MS45LjAAQQD//3+CD3BABQAAAAAAAAAA"),
    ("s3",        "MS45LjAAQQAXAwQATjDAAwgAAAAAAQAA"),
    ("rsi-preset-1", "MS45LjAAQQAFCyIAD3DAAggAAAAAAQAA"),
    ("rsi-preset-2", "MS45LjAAQQAFCyIAD3DAAhAAAAAAAQAA"),
    ("rsi-preset-3", "MS45LjAAQQAFCyIAD3DAAiAAAAAAAQAA"),
    ("rsi-preset-4", "MS45LjAAQQAFCyIAD3DAAgABAAAAAQAA"),
    ("rsi-preset-5", "MS45LjAAQQAFCyIAD3DAAgCAAAAAAQAA"),
    ("rsi-preset-6", "MS45LjAAQQAFCyIAD3DAAgAAAgAAAQAA"),
    ("rsi-preset-7", "MS45LjAAQQAFCyIAD3DAAgAAAAQAAQAA"),
    ("rsi-preset-8", "MS45LjAAQQAFCyIAD3DAAgAAAAAEAQAA"),
    ("rsi-preset-9", "MS45LjAAQQAFCyIAD3DAAgAAAAgAAQAA"),
])

RANDOM_STARTING_ITEM_PRESETS = [
    "rsi-preset-1", "rsi-preset-2", "rsi-preset-3", "rsi-preset-4",
    "rsi-preset-5", "rsi-preset-6", "rsi-preset-7", "rsi-preset-8",
    "rsi-preset-9"
]

STANDARD_DEFAULT = ["s4"]

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
    ("rsi-preset-1", "Bait Bag"),
    ("rsi-preset-2", "Bombs"),
    ("rsi-preset-3", "Boomerang"),
    ("rsi-preset-4", "Deku Leaf"),
    ("rsi-preset-5", "Grappling Hook"),
    ("rsi-preset-6", "Hookshot"),
    ("rsi-preset-7", "Power Bracelets"),
    ("rsi-preset-8", "Progressive Bow"),
    ("rsi-preset-9", "Skull Hammer"),
])

SPOILER_LOG_DEFAULT = ["preset-a", "preset-b", "preset-c", "preset-d", "preset-e", "preset-f"]
DEFAULT_PLANNING_TIME = 60
MINIMUM_PLANNING_TIME = 20

DEV_PERMALINKS = OrderedDict([
    ("default", "eJwz1LPUMzSIT0ktY3BkYGdkZigwYXjAWMDAKMUABg0MJAAAZlcFog=="),
])

DEV_DEFAULT = ["default"]
DEV_VERSION = "1.9.10_dev"
DEV_DOWNLOAD = "https://github.com/tanjo3/wwrando/releases"

BANNABLE_PRESETS = SPOILER_LOG_DEFAULT + RANDOM_STARTING_ITEM_PRESETS
