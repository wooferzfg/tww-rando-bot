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

S8_PERMALINKS = OrderedDict([
    ("s8",          "eJwLtlAIyS8tykvMTc0rUSgzYnBkuPu5iKPBmEHAwZEBCBqAqJ9RAMSUYLJzrjf4KL/hf7YJAxjc8WjgcHlyWt3GVp5BwOMfE1CNA4MIgytjhQYXAGZ7Fso="),  # noqa: E501
    ("mixed-pools", "eJwLtlAIyS8tykvMTc0rUSgzYnBkuL8hgYFI8ObgfI6O5CPqBhbSDAweb0BCDlApDgDv9w36"),  # noqa: E501
])
S8_DEFAULT = ["s8"]

S8_SL_PERMALINKS = OrderedDict([
    ("s8-sl",          "eJwLtlAIyS8tykvMTc0rUSgzYnBkuPu5iKPBmEHAwZEBCBqAqJ9RAMSUYLJzrjf4KL/hf7YJAxjc8WjgcHlyWt3GVp5BwOMfE1CNA4MIgytjhQYTAGZzFsI="),  # noqa: E501
    ("mixed-pools-sl", "eJwLtlAIyS8tykvMTc0rUSgzYnBkuL8hgYFI8ObgfI6O5CPqBhbSDAweb0BCDjA5AO/vDfI="),  # noqa: E501
])
S8_SL_DEFAULT = ["s8-sl"]

MINIBLINS_PERMALINKS = OrderedDict([
    ("miniblins",      "eJwz1DM00DOIN0xNszAySmRwZOg0SBBgZ2DjYMAKBBgYWOAcHwYHFqGN/hZz2RlYJukvYWhQAgB6WwmT"),
    ("miniblins-2024", "eJwz1DM00DOIN0xNszAySmRwZPA1cGAgEvgwOLAIXfS3uMvOwDJJfwlDgxIAXkYJXg=="),
])
MINIBLINS_DEFAULT = ["miniblins"]

S8_DOWNLOAD = "https://github.com/tanjo3/wwrando/releases/tag/s8-v2"
S8_TRACKER = "https://www.wooferzfg.me/tww-rando-tracker/s8-tournament"

MINIBLINS_DOWNLOAD = "https://github.com/tanjo3/wwrando/releases/tag/miniblins-2025"
MINIBLINS_TRACKER = "https://wooferzfg.me/tww-rando-tracker/miniblins"

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
