from collections import OrderedDict

STANDARD_PERMALINKS = OrderedDict([
    ("tourney",   "MS45LjAAQQAFCyIAD3DAAgAAAAAAAQAA"),
    ("beginner",  "MS45LjAAQQAFAwIADzDAAYAcQIFBATAA"),
    ("co-op",     "MS45LjAAQQAVCyYAD3DABAAAAAAAAQAA"),
    ("allsanity", "MS45LjAAQQD//3+CD3BABQAAAAAAAAAA"),
    ("s3",        "MS45LjAAQQAXAwQATjDAAwgAAAAAAQAA"),
])
STANDARD_ALIASES = {
    "s4":   "tourney",
    "coop": "co-op",
}
STANDARD_DEFAULT = ["tourney"]

SPOILER_LOG_PERMALINKS = OrderedDict([
    ("tourney",   "MS45LjAAQQAXAwYCDxDAAgAAAAAAAQAA"),
    ("allsanity", "MS45LjAAQQD//3+CD1BABQAAAAAAAAAA"),
])
SPOILER_LOG_ALIASES = {
    "s1": "tourney",
}
SPOILER_LOG_DEFAULT = ["tourney"]
DEFAULT_PLANNING_TIME = 50
MINIMUM_PLANNING_TIME = 20

BANNABLE_PRESETS = ["preset-a", "preset-b", "preset-c", "preset-d", "preset-e", "preset-f"]
