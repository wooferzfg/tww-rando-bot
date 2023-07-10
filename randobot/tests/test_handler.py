import asyncio
import unittest
from unittest.mock import call, patch

from randobot.handler import RandoHandler


class MockGenerator():
    def generate_seed(self, randomizer_path, permalink, username, generate_spoiler_log):
        raise Exception("Method not properly mocked")


def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f


def create_rando_handler(generator, state):
    return RandoHandler(generator, logger=None, conn=None, state=state)


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


if __name__ == '__main__':
    unittest.main()
