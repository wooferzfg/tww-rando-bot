import asyncio
import unittest
from unittest.mock import call, patch

from randobot.generator import ArgFormat
from randobot.handler import RandoHandler


class MockGenerator():
    def generate_seed(self, randomizer_path, permalink, username, generate_spoiler_log):
        raise Exception("Method not properly mocked")


def mock_generate_seed_standard(randomizer_path, permalink, username, generate_spoiler_log,
                                modifiers="", args_format=ArgFormat.V110):
    return {
        "file_name": "FILENAME",
        "permalink": f"PERMA_{permalink}",
        "seed_hash": "SEED HASH",
        "spoiler_log_url": None,
    }


def mock_generate_seed_spoiler_log(randomizer_path, permalink, username, generate_spoiler_log,
                                   modifiers="", args_format=ArgFormat.V110):
    if not generate_spoiler_log:
        raise Exception("Did not generate spoiler log")

    return {
        "file_name": "FILENAME",
        "permalink": f"PERMA_{permalink}",
        "seed_hash": "SEED HASH",
        "spoiler_log_url": "SPOILER_LOG_URL",
    }


class MockLogger():
    def info(self, data):
        pass


def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f


async def wait_for_all_async_tasks():
    tasks = [
        t for t in asyncio.all_tasks() if t is not asyncio.current_task()
    ]
    await asyncio.gather(*tasks)


def create_rando_handler(generator, state):
    handler = RandoHandler(generator, logger=MockLogger(), conn=None, state=state)
    handler.room_setup()
    return handler


def get_mock_message_data():
    return {
        "is_monitor": True,
        "user": {"name": "test_user"},
    }


class TestHandler(unittest.IsolatedAsyncioTestCase):
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_ra_command(self, mock_send_message):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_ra([], get_mock_message_data())

        self.assertEqual(mock_send_message.call_count, 1)
        mock_send_message.assert_has_calls([
            call(
                "Runners' agreements (RAs) may be used to modify S7 seeds. Example usage: \"!s7 4drm+nosword\". "
                "Valid RA modifiers: 4rbm (4-Required Bosses Mode), nosword (No Starting Sword), "
                "der (Randomized Dungeon Entrances), ber (Randomized Boss Entrances), keys (Key-Lunacy), "
                "tingle (Tingle Chests replacing Dungeon Secrets), expen (Expensive Purchases), subs (Submarines), "
                "minis (Minigames), plats (Lookout Platforms on Islet of Steel, Southern Fairy, and Seven-Star)"
            ),
        ])

    @patch.object(MockGenerator, "generate_seed", side_effect=mock_generate_seed_standard)
    @patch.object(RandoHandler, "set_raceinfo", return_value=async_return(None))
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_rollseed_s7(self, mock_send_message, mock_set_raceinfo, mock_generate_seed):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_s7([], get_mock_message_data())

        self.assertEqual(mock_send_message.call_count, 6)
        permalink = "eJwz1DM00DOIt7RITrQwM2VwZLhrVMTF0czAwMDCAAUcIEKAgYGJg3GlykMQAyoRwuLAsmajv8G85QwMk/iB6jUB5s8MHw=="
        mock_send_message.assert_has_calls([
            call("Rolling seed..."),
            call(f"Permalink: PERMA_{permalink}"),
            call("Seed Hash: SEED HASH"),
            call('Please note that this seed uses the S7 Tournament build of the randomizer.'),
            call("Download: https://github.com/tanjo3/wwrando/releases/tag/s7-v1"),
            call("Tracker: https://wooferzfg.me/tww-rando-tracker/s7-tournament"),
        ])

        self.assertEqual(mock_set_raceinfo.call_count, 1)
        mock_set_raceinfo.assert_has_calls([
            call(f"PERMA_{permalink} | Seed Hash: SEED HASH", False, False),
        ])

        self.assertEqual(mock_generate_seed.call_count, 1)
        mock_generate_seed.assert_has_calls([
            call("wwrando-s7", permalink, "test_user", generate_spoiler_log=False,
                 modifiers="", args_format=ArgFormat.VS7),
        ])

    @patch.object(MockGenerator, "generate_seed", side_effect=mock_generate_seed_standard)
    @patch.object(RandoHandler, "set_raceinfo", return_value=async_return(None))
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_rollseed_s7_with_ra(self, mock_send_message, mock_set_raceinfo, mock_generate_seed):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_s7(["4rbm+nosword"], get_mock_message_data())

        self.assertEqual(mock_send_message.call_count, 7)
        permalink = "eJwz1DM00DOIt7RITrQwM2VwZLhrVMTF0czAwMDCAAUcIEKAgYGJg3GlykMQAyoRwuLAsmajv8G85QwMk/iB6jUB5s8MHw=="
        mock_send_message.assert_has_calls([
            call("Rolling seed..."),
            call("Settings: s7+4rbm+nosword"),
            call(f"Permalink: PERMA_{permalink}"),
            call("Seed Hash: SEED HASH"),
            call('Please note that this seed uses the S7 Tournament build of the randomizer.'),
            call("Download: https://github.com/tanjo3/wwrando/releases/tag/s7-v1"),
            call("Tracker: https://wooferzfg.me/tww-rando-tracker/s7-tournament"),
        ])

        self.assertEqual(mock_set_raceinfo.call_count, 2)
        mock_set_raceinfo.assert_has_calls([
            call("Settings: s7+4rbm+nosword", False, False),
            call(f"PERMA_{permalink} | Seed Hash: SEED HASH", False, False),
        ])

        self.assertEqual(mock_generate_seed.call_count, 1)
        mock_generate_seed.assert_has_calls([
            call("wwrando-s7", permalink, "test_user", generate_spoiler_log=False,
                 modifiers="4rbm,nosword", args_format=ArgFormat.VS7),
        ])

    @patch("random.random", return_value=0.6123)
    @patch.object(MockGenerator, "generate_seed", side_effect=mock_generate_seed_standard)
    @patch.object(RandoHandler, "set_raceinfo", return_value=async_return(None))
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_multiple_presets(self, mock_send_message, mock_set_raceinfo, mock_generate_seed, mock_random):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_rollseed(["S4", "S5", "S6"], get_mock_message_data())

        self.assertEqual(mock_send_message.call_count, 4)
        mock_send_message.assert_has_calls([
            call("Rolling seed..."),
            call("Settings: s5"),
            call("Permalink: PERMA_MS4xMC4wAEEAFQMiAJPowAMMsACCcQ8AAMkHAQAA"),
            call("Seed Hash: SEED HASH"),
        ])

        self.assertEqual(mock_set_raceinfo.call_count, 2)
        mock_set_raceinfo.assert_has_calls([
            call("Settings: s5", False, False),
            call("PERMA_MS4xMC4wAEEAFQMiAJPowAMMsACCcQ8AAMkHAQAA | Seed Hash: SEED HASH", False, False),
        ])

        self.assertEqual(mock_generate_seed.call_count, 1)
        mock_generate_seed.assert_has_calls([
            call("wwrando", "MS4xMC4wAEEAFQMiAJPowAMMsACCcQ8AAMkHAQAA", "test_user", False),
        ])

    @patch("random.random", return_value=0.6123)
    @patch.object(MockGenerator, "generate_seed", side_effect=mock_generate_seed_standard)
    @patch.object(RandoHandler, "set_raceinfo", return_value=async_return(None))
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_presets_and_permalinks_preset_chosen(
        self,
        mock_send_message,
        mock_set_raceinfo,
        mock_generate_seed,
        mock_random,
    ):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_rollseed([
            "s4",
            "s5",
            "MS4xMC4wAEEAFQsmANsMwQMcMAGCcQ8AAMkHAAAA",
            "MS4xMC4wAEEA//9/gtsMwQMcUAECAAAAAAkAAAAA",
        ], get_mock_message_data())

        self.assertEqual(mock_send_message.call_count, 4)
        mock_send_message.assert_has_calls([
            call("Rolling seed..."),
            call("Settings: s4"),
            call("Permalink: PERMA_MS4xMC4wAEEABQsiAAUAvgMcsAACAAAAAAGAIAAA"),
            call("Seed Hash: SEED HASH"),
        ])

        self.assertEqual(mock_set_raceinfo.call_count, 2)
        mock_set_raceinfo.assert_has_calls([
            call("Settings: s4", False, False),
            call("PERMA_MS4xMC4wAEEABQsiAAUAvgMcsAACAAAAAAGAIAAA | Seed Hash: SEED HASH", False, False),
        ])

        self.assertEqual(mock_generate_seed.call_count, 1)
        mock_generate_seed.assert_has_calls([
            call("wwrando", "MS4xMC4wAEEABQsiAAUAvgMcsAACAAAAAAGAIAAA", "test_user", False),
        ])

    @patch("random.random", return_value=0.2789)
    @patch.object(MockGenerator, "generate_seed", side_effect=mock_generate_seed_standard)
    @patch.object(RandoHandler, "set_raceinfo", return_value=async_return(None))
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_presets_and_permalinks_permalink_chosen(
        self,
        mock_send_message,
        mock_set_raceinfo,
        mock_generate_seed,
        mock_random,
    ):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_rollseed([
            "s4",
            "s5",
            "MS4xMC4wAEEAFQsmANsMwQMcMAGCcQ8AAMkHAAAA",
            "MS4xMC4wAEEA//9/gtsMwQMcUAECAAAAAAkAAAAA",
        ], get_mock_message_data())

        self.assertEqual(mock_send_message.call_count, 4)
        mock_send_message.assert_has_calls([
            call("Rolling seed..."),
            call("Settings: MS4xMC4wAEEA//9/gtsMwQMcUAECAAAAAAkAAAAA"),
            call("Permalink: PERMA_MS4xMC4wAEEA//9/gtsMwQMcUAECAAAAAAkAAAAA"),
            call("Seed Hash: SEED HASH"),
        ])

        self.assertEqual(mock_set_raceinfo.call_count, 2)
        mock_set_raceinfo.assert_has_calls([
            call("Settings: MS4xMC4wAEEA//9/gtsMwQMcUAECAAAAAAkAAAAA", False, False),
            call("PERMA_MS4xMC4wAEEA//9/gtsMwQMcUAECAAAAAAkAAAAA | Seed Hash: SEED HASH", False, False),
        ])

        self.assertEqual(mock_generate_seed.call_count, 1)
        mock_generate_seed.assert_has_calls([
            call("wwrando", "MS4xMC4wAEEA//9/gtsMwQMcUAECAAAAAAkAAAAA", "test_user", False),
        ])

    @patch("random.random", return_value=0.6123)
    @patch.object(MockGenerator, "generate_seed", side_effect=mock_generate_seed_standard)
    @patch.object(RandoHandler, "set_raceinfo", return_value=async_return(None))
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_presets_and_permalinks_with_ra(
        self,
        mock_send_message,
        mock_set_raceinfo,
        mock_generate_seed,
        mock_random,
    ):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_s7([
            "4rbm",
            "nosword",
            "4rbm+nosword",
            "eJwz1DM00DOIt7RITrQwM2VwZPAUCGAgEkgwMPxmOuENZjMxNDEwMAIAROIG7Q==",
        ], get_mock_message_data())

        self.assertEqual(mock_send_message.call_count, 7)
        permalink = "eJwz1DM00DOIt7RITrQwM2VwZLhrVMTF0czAwMDCAAUcIEKAgYGJg3GlykMQAyoRwuLAsmajv8G85QwMk/iB6jUB5s8MHw=="
        mock_send_message.assert_has_calls([
            call("Rolling seed..."),
            call("Settings: s7+nosword"),
            call(f"Permalink: PERMA_{permalink}"),
            call("Seed Hash: SEED HASH"),
            call('Please note that this seed uses the S7 Tournament build of the randomizer.'),
            call("Download: https://github.com/tanjo3/wwrando/releases/tag/s7-v1"),
            call("Tracker: https://wooferzfg.me/tww-rando-tracker/s7-tournament"),
        ])

        self.assertEqual(mock_set_raceinfo.call_count, 2)
        mock_set_raceinfo.assert_has_calls([
            call("Settings: s7+nosword", False, False),
            call(f"PERMA_{permalink} | Seed Hash: SEED HASH", False, False),
        ])

        self.assertEqual(mock_generate_seed.call_count, 1)
        mock_generate_seed.assert_has_calls([
            call("wwrando-s7", permalink, "test_user", generate_spoiler_log=False,
                 modifiers="nosword", args_format=ArgFormat.VS7),
        ])

    @patch("random.random", return_value=0.6123)
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_invalid_preset(
        self,
        mock_send_message,
        mock_random,
    ):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        with self.assertRaises(Exception):
            await handler.ex_rollseed([
                "s6",
                "invalidpreset",
                "s4",
            ], get_mock_message_data())

        self.assertEqual(mock_send_message.call_count, 2)
        mock_send_message.assert_has_calls([
            call("Rolling seed..."),
            call("Invalid preset: \"invalidpreset\""),
        ])

    @patch("random.random", return_value=0.6123)
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_multiple_invalid_presets(
        self,
        mock_send_message,
        mock_random,
    ):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        with self.assertRaises(Exception):
            await handler.ex_rollseed([
                "s6",
                "invalidpreset",
                "invalidpreset2",
                "s4",
            ], get_mock_message_data())

        self.assertEqual(mock_send_message.call_count, 2)
        mock_send_message.assert_has_calls([
            call("Rolling seed..."),
        ])

        second_message = mock_send_message.call_args_list[1][0][0]
        self.assertTrue("Invalid presets: " in second_message)
        self.assertTrue("\"invalidpreset2\"" in second_message)
        self.assertTrue("\"invalidpreset\"" in second_message)

    @patch("random.random", return_value=0.6123)
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_invalid_ra(
        self,
        mock_send_message,
        mock_random,
    ):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        with self.assertRaises(Exception):
            await handler.ex_s7([
                "s7+garbage",
                "s7",
            ], get_mock_message_data())

        self.assertEqual(mock_send_message.call_count, 2)
        mock_send_message.assert_has_calls([
            call("Rolling seed..."),
            call("Invalid preset: \"s7+garbage\" - Invalid runners' agreement modifier!"),
        ])

    @patch.object(MockGenerator, "generate_seed", side_effect=mock_generate_seed_standard)
    @patch.object(RandoHandler, "set_raceinfo", return_value=async_return(None))
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_miniblins(self, mock_send_message, mock_set_raceinfo, mock_generate_seed):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_miniblins([], get_mock_message_data())

        self.assertEqual(mock_send_message.call_count, 6)
        permalink = "eJwz1DM00DOIt7RITrQwM2VwZOg0SBBgZ2DjYMAKBBgYWOAcHwYHFqGN/hZz2RlYJukvYWhQAgBxyAly"
        mock_send_message.assert_has_calls([
            call("Rolling seed..."),
            call(f"Permalink: PERMA_{permalink}"),
            call("Seed Hash: SEED HASH"),
            call('Please note that this seed uses the S7 Tournament build of the randomizer.'),
            call("Download: https://github.com/tanjo3/wwrando/releases/tag/s7-v1"),
            call("Tracker: https://wooferzfg.me/tww-rando-tracker/miniblins"),
        ])

        self.assertEqual(mock_set_raceinfo.call_count, 1)
        mock_set_raceinfo.assert_has_calls([
            call(f"PERMA_{permalink} | Seed Hash: SEED HASH", False, False),
        ])

        self.assertEqual(mock_generate_seed.call_count, 1)
        mock_generate_seed.assert_has_calls([
            call("wwrando-s7", permalink, "test_user", generate_spoiler_log=False,
                 modifiers="", args_format=ArgFormat.VS7),
        ])

    @patch("asyncio.sleep", return_value=async_return(None))
    @patch("random.random", return_value=0.6123)
    @patch.object(MockGenerator, "generate_seed", side_effect=mock_generate_seed_spoiler_log)
    @patch.object(RandoHandler, "set_raceinfo", return_value=async_return(None))
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_startspoilerlograce(
        self,
        mock_send_message,
        mock_set_raceinfo,
        mock_generate_seed,
        mock_random,
        mock_sleep,
    ):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_startspoilerlograce([], get_mock_message_data())

        await wait_for_all_async_tasks()

        self.assertEqual(mock_send_message.call_count, 13)
        mock_send_message.assert_has_calls([
            call("Settings: preset-d (Lookout Platforms and Rafts)"),
            call("Rolling seed..."),
            call("Seed rolled!"),
            call("Preparation stage starts in 15 seconds..."),
            call("5..."),
            call("4..."),
            call("3..."),
            call("2..."),
            call("1..."),
            call("You have 60 minutes to prepare your route!"),
            call("Spoiler Log: SPOILER_LOG_URL"),
            call("Example Permalink: MS4xMC4wAEEAFwcmAgEAoAMUsAACAAAAAAGAAAAA"),
            call("Warning: The seed from this permalink does not match the actual permalink!")
        ])

        self.assertEqual(mock_set_raceinfo.call_count, 1)
        mock_set_raceinfo.assert_has_calls([
            call("Settings: preset-d (Lookout Platforms and Rafts)", False, False),
        ])

        self.assertEqual(mock_generate_seed.call_count, 1)
        mock_generate_seed.assert_has_calls([
            call("wwrando", "MS4xMC4wAEEAFwcmAgEAoAMUsAACAAAAAAGAAAAA", "test_user", True),
        ])

        self.assertEqual(state["spoiler_log_seed_rolled"], True)
        self.assertEqual(state["example_permalink"], "MS4xMC4wAEEAFwcmAgEAoAMUsAACAAAAAAGAAAAA")
        self.assertEqual(state["permalink"], "PERMA_MS4xMC4wAEEAFwcmAgEAoAMUsAACAAAAAAGAAAAA")
        self.assertEqual(state["spoiler_log_url"], "SPOILER_LOG_URL")
        self.assertEqual(state["seed_hash"], "SEED HASH")
        self.assertEqual(state["file_name"], "FILENAME")

    @patch("asyncio.sleep", return_value=async_return(None))
    @patch.object(MockGenerator, "generate_seed", side_effect=mock_generate_seed_spoiler_log)
    @patch.object(RandoHandler, "set_raceinfo", return_value=async_return(None))
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_startspoilerlogtimer(self, mock_send_message, mock_set_raceinfo, mock_generate_seed, mock_sleep):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_startspoilerlogtimer([], get_mock_message_data())

        await wait_for_all_async_tasks()

        self.assertEqual(mock_send_message.call_count, 7)
        mock_send_message.assert_has_calls([
            call("Preparation stage starts in 15 seconds..."),
            call("5..."),
            call("4..."),
            call("3..."),
            call("2..."),
            call("1..."),
            call("You have 60 minutes to prepare your route!"),
        ])

        mock_set_raceinfo.assert_not_called()
        mock_generate_seed.assert_not_called()

        self.assertEqual(state["spoiler_log_seed_rolled"], True)
        self.assertEqual(state["example_permalink"], None)
        self.assertEqual(state["permalink"], None)
        self.assertEqual(state["spoiler_log_url"], None)
        self.assertEqual(state["seed_hash"], None)
        self.assertEqual(state["file_name"], None)

    @patch("asyncio.sleep", return_value=async_return(None))
    @patch.object(MockGenerator, "generate_seed", side_effect=mock_generate_seed_spoiler_log)
    @patch.object(RandoHandler, "set_raceinfo", return_value=async_return(None))
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_starts7spoilerlograce(self, mock_send_message, mock_set_raceinfo, mock_generate_seed, mock_sleep):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_starts7spoilerlograce([], get_mock_message_data())

        await wait_for_all_async_tasks()

        self.assertEqual(mock_send_message.call_count, 15)
        permalink = "eJwz1DM00DOIt7RITrQwM2VwZLhrVMTF0czAwMDCAAUcIEKAgYGJg3GlykMQAyoRwuLAsmajv8G85QwMk/iB6jkB5q8L/w=="
        mock_send_message.assert_has_calls([
            call("Rolling seed..."),
            call("Seed rolled!"),
            call('Please note that this seed uses the S7 Tournament build of the randomizer.'),
            call("Download: https://github.com/tanjo3/wwrando/releases/tag/s7-v1"),
            call("Tracker: https://wooferzfg.me/tww-rando-tracker/s7-tournament"),
            call("Preparation stage starts in 15 seconds..."),
            call("5..."),
            call("4..."),
            call("3..."),
            call("2..."),
            call("1..."),
            call("You have 60 minutes to prepare your route!"),
            call("Spoiler Log: SPOILER_LOG_URL"),
            call(f"Example Permalink: {permalink}"),
            call("Warning: The seed from this permalink does not match the actual permalink!")
        ])

        mock_set_raceinfo.assert_not_called()

        self.assertEqual(mock_generate_seed.call_count, 1)
        mock_generate_seed.assert_has_calls([
            call("wwrando-s7", permalink, "test_user", generate_spoiler_log=True,
                 modifiers="", args_format=ArgFormat.VS7),
        ])

        self.assertEqual(state["spoiler_log_seed_rolled"], True)
        self.assertEqual(state["example_permalink"], permalink)
        self.assertEqual(state["permalink"], f"PERMA_{permalink}")
        self.assertEqual(state["spoiler_log_url"], "SPOILER_LOG_URL")
        self.assertEqual(state["seed_hash"], "SEED HASH")
        self.assertEqual(state["file_name"], "FILENAME")

    @patch("asyncio.sleep", return_value=async_return(None))
    @patch.object(MockGenerator, "generate_seed", side_effect=mock_generate_seed_spoiler_log)
    @patch.object(RandoHandler, "set_raceinfo", return_value=async_return(None))
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_randomsettings(self, mock_send_message, mock_set_raceinfo, mock_generate_seed, mock_sleep):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_randomsettings([], get_mock_message_data())

        await wait_for_all_async_tasks()

        self.assertEqual(mock_send_message.call_count, 4)
        mock_send_message.assert_has_calls([
            call("Rolling seed..."),
            call("Permalink: PERMA_UlMxLjQuMC1kZXYzAEEAgQU="),
            call("Seed Hash: SEED HASH"),
            call(
                "Please note that this seed uses the Random Settings RS1.4.0-dev3 "
                "build of the randomizer. "
                "Download: https://github.com/Aelire/wwrando/releases/tag/RS1.4.0-dev3 "
                "Tracker: https://jaysc.github.io/tww-rando-tracker-rs/"
            ),

        ])

        self.assertEqual(mock_set_raceinfo.call_count, 1)
        mock_set_raceinfo.assert_has_calls([
            call("PERMA_UlMxLjQuMC1kZXYzAEEAgQU= | Seed Hash: SEED HASH", False, False),
        ])

        self.assertEqual(mock_generate_seed.call_count, 1)
        mock_generate_seed.assert_has_calls([
            call(
                "wwrando-random-settings",
                "UlMxLjQuMC1kZXYzAEEAgQU=",
                "test_user",
                generate_spoiler_log=True,
                args_format=ArgFormat.RS14,
            ),
        ])

        self.assertEqual(state["example_permalink"], "UlMxLjQuMC1kZXYzAEEAgQU=")
        self.assertEqual(state["permalink"], "PERMA_UlMxLjQuMC1kZXYzAEEAgQU=")
        self.assertEqual(state["random_settings_spoiler_log_url"], "SPOILER_LOG_URL")
        self.assertEqual(state["random_settings_spoiler_log_unlocked"], False)
        self.assertEqual(state["seed_hash"], "SEED HASH")


if __name__ == "__main__":
    unittest.main()
