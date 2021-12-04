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
])

SPOILER_LOG_DEFAULT = ["preset-a", "preset-b", "preset-c", "preset-d", "preset-e", "preset-f"]
DEFAULT_PLANNING_TIME = 60
MINIMUM_PLANNING_TIME = 20

BANNABLE_PRESETS = SPOILER_LOG_DEFAULT
