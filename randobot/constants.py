from collections import OrderedDict

STANDARD_PERMALINKS = OrderedDict([
    ("s4",        "MS45LjAAQQAFCyIAD3DAAgAAAAAAAQAA"),
    ("beginner",  "MS45LjAAQQAFAwIADzDAAYAcQIFBATAA"),
    ("co-op",     "MS45LjAAQQAVCyYAD3DABAAAAAAAAQAA"),
    ("allsanity", "MS45LjAAQQD//3+CD3BABQAAAAAAAAAA"),
    ("s3",        "MS45LjAAQQAXAwQATjDAAwgAAAAAAQAA"),
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
    ("beginner",  """Start with Sword, 2 DRM, Puzzle Secret Caves,
 Free Gifts, Mail & Misc."""),
    ("co-op",     """
5 DRM, Puzzle Secret Caves, Free Gifts, Tingle Chests,
 Short Sidequests, Mail, Island Puzzles, Submarines & Misc."""),
    ("s1", """Start with Sword, 3 DRM, Puzzle Secret Caves, Great Fairies, Free Gifts,
 Tingle Chests, Short Sidequests, Mail & Misc."""),
    ("s3", """Start with Sword, 4 DRM, Puzzle Secret Caves, Great Fairies, Free Gifts,
 Tingle Chests, Short Sidequests, Mail."""),
    ("s4", """3 DRM, Puzzle Secret Caves, Island Puzzles,
 Free Gifts, Mail, Submarines & Misc."""),
    ("allsanity", "Everything enabled."),
    ("preset-a",  "Long Sidequests."),
    ("preset-b",  "Triforce Charts, Big Octos and Gunboats."),
    ("preset-c",  "Swordless."),
    ("preset-d",  "Lookout Platforms and Rafts."),
    ("preset-e",  "4 Dungeon Race Mode and Key-Lunacy."),
    ("preset-f",  "Combat Secret Caves, Submarines."),
])

SPOILER_LOG_DEFAULT = ["preset-a", "preset-b", "preset-c", "preset-d", "preset-e", "preset-f"]
DEFAULT_PLANNING_TIME = 60
MINIMUM_PLANNING_TIME = 20

BANNABLE_PRESETS = SPOILER_LOG_DEFAULT
