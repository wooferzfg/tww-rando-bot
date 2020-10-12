import asyncio
from racetime_bot import RaceHandler, monitor_cmd, can_moderate, can_monitor

class RandoHandler(RaceHandler):
    """
    RandoBot race handler. Generates seeds.
    """
    stop_at = ["pending", "in_progress", "cancelled", "finished"]

    def __init__(self, generator, **kwargs):
        super().__init__(**kwargs)

        self.generator = generator
        self.loop = asyncio.get_event_loop()

    async def begin(self):
        self.state["locked"] = False
        self.state["seed_rolled"] = False
        self.state["finished_entrants"] = set()

    async def error(self, data):
        self.logger.info(data.get('errors'))
        await self.begin()

    async def race_data(self, data):
        self.data = data.get("race")

        finished_entrants = set(
            map(
                lambda entrant: entrant.get("user").get("name"),
                filter(
                    lambda entrant: entrant.get("status").get("value") == "done",
                    self.data.get("entrants")
                )
            )
        )

        new_finishers = list(finished_entrants - self.state["finished_entrants"])

        for finisher in new_finishers:
            await self.send_message(
                f"{finisher}, before you end your stream, please remember to advance to the second text box after defeating Ganondorf."
            )

        self.state["finished_entrants"] = finished_entrants

    @monitor_cmd
    async def ex_lock(self, args, message):
        """
        Handle !lock commands.

        Prevent seed rolling unless user is a race monitor.
        """
        self.state["locked"] = True
        await self.send_message(
            "Lock initiated. I will now only roll seeds for race monitors."
        )

    @monitor_cmd
    async def ex_unlock(self, args, message):
        """
        Handle !unlock commands.

        Remove lock preventing seed rolling unless user is a race monitor.
        """
        self.state["locked"] = False
        await self.send_message(
            "Lock released. Anyone may now roll a seed."
        )

    async def ex_startspoilerlograce(self, args, message):
        """
        Handle !startspoilerlograce commands.
        """
        await self.roll_and_send(args, message, True)

    async def roll_and_send(self, args, message, encrypt):
        """
        Read an incoming !seed or !race command, and generate a new seed if
        valid.
        """
        reply_to = message.get("user", {}).get("name")

        if self.state.get("locked") and not can_monitor(message):
            await self.send_message(
                "Sorry %(reply_to)s, seed rolling is locked. Only race "
                "monitors may roll a seed for this race."
                % {"reply_to": reply_to or "friend"}
            )
            return
        if self.state.get("seed_rolled"):
            await self.send_message(
                "Race already started!"
            )
            return

        self.loop.create_task(self.roll())

    async def roll(self):
        """
        Generate a seed and send it to the race room.
        """
        self.state["seed_rolled"] = True

        await self.send_message("Generating seed...")

        generated_seed = self.generator.generate_seed()
        spoiler_log_url = generated_seed.get("spoiler_log_url")
        permalink = generated_seed.get("permalink")
        file_name = generated_seed.get("file_name")

        self.logger.info(spoiler_log_url)
        self.logger.info(permalink)
        self.logger.info(file_name)

        await self.send_message("Seed generated! Preparation stage starts in 15 seconds...")

        await asyncio.sleep(10)
        await self.send_message("5...")
        await asyncio.sleep(1)
        await self.send_message("4...")
        await asyncio.sleep(1)
        await self.send_message("3...")
        await asyncio.sleep(1)
        await self.send_message("2...")
        await asyncio.sleep(1)
        await self.send_message("1...")
        await asyncio.sleep(1)

        await self.send_message("You have 50 minutes to prepare your route!")
        await self.send_message(f"Spoiler log: {spoiler_log_url}")

        await asyncio.sleep(2100) # 35 minutes

        await self.send_message("You have 15 minutes until the race starts!")
        await self.send_message(f"Permalink: {permalink}")

        await asyncio.sleep(840) # 14 minutes

        await self.send_message("You have 1 minute until the race starts!")
        await self.send_message(f"File name: {file_name}")

        await asyncio.sleep(45)

        await self.send_message("Starting race countdown!")
        await self.force_start()
