import asyncio
import unittest
from unittest.mock import call, patch

from randobot.handler import RandoHandler


class MockGenerator():
    def generate_seed(self, randomizer_path, permalink, username, generate_spoiler_log):
        raise Exception("Method not properly mocked")


def mock_generate_seed_standard(randomizer_path, permalink, username, generate_spoiler_log):
    return {
        "file_name": "FILENAME",
        "permalink": f"PERMA_{permalink}",
        "seed_hash": "SEED HASH",
        "spoiler_log_url": None,
    }


class MockLogger():
    def info(self, data):
        pass


def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f


def create_rando_handler(generator, state):
    handler = RandoHandler(generator, logger=MockLogger(), conn=None, state=state)
    handler.room_setup()
    return handler


def get_mock_message_data():
    return {"user": {"name": "test_user"}}


class TestHandler(unittest.IsolatedAsyncioTestCase):
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_ra_command(self, mock_send_message):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_ra([], get_mock_message_data())

        mock_send_message.assert_has_calls([
            call(
                "Runners\' agreements (RAs) may be used to modify S6 seeds. Example usage: \"s6+4drm+nosword\""
                ". Valid RA modifiers: 4drm (4-Dungeon Race Mode), nosword (No Starting Sword), der (Randomized "
                "Dungeon Entrances), keys (Key-Lunacy), tingle (Tingle Chests), expen (Expensive Purchases), "
                "subs (Submarines), minis (Minigames), combat (Combat Secret Caves)"
            )
        ])

    @patch.object(MockGenerator, "generate_seed", side_effect=mock_generate_seed_standard)
    @patch.object(RandoHandler, "set_raceinfo", return_value=async_return(None))
    @patch.object(RandoHandler, "send_message", return_value=async_return(None))
    async def test_rollseed_s6(self, mock_send_message, mock_set_raceinfo, mock_generate_seed):
        generator = MockGenerator()
        state = {}
        handler = create_rando_handler(generator, state)
        await handler.ex_rollseed(["s6"], get_mock_message_data())

        self.assertEqual(mock_send_message.call_count, 3)
        mock_send_message.assert_has_calls([
            call("Rolling seed..."),
            call("Permalink: PERMA_MS4xMC4wAEEAFwMiAHPowgMMsACCcQ8AAMkHAAAA"),
            call("Seed Hash: SEED HASH"),
        ])

        self.assertEqual(mock_set_raceinfo.call_count, 1)
        mock_set_raceinfo.assert_has_calls([
            call("PERMA_MS4xMC4wAEEAFwMiAHPowgMMsACCcQ8AAMkHAAAA | Seed Hash: SEED HASH", False, False)
        ])

        self.assertEqual(mock_generate_seed.call_count, 1)
        mock_generate_seed.assert_has_calls([
            call("wwrando", "MS4xMC4wAEEAFwMiAHPowgMMsACCcQ8AAMkHAAAA", "test_user", False)
        ])


if __name__ == "__main__":
    unittest.main()
