import asyncio
from racetime_bot import RaceHandler, monitor_cmd, can_monitor

class RandoHandler(RaceHandler):
    stop_at = ["cancelled"]

    def __init__(self, generator, **kwargs):
        super().__init__(**kwargs)

        self.generator = generator
        self.loop = asyncio.get_event_loop()

    async def begin(self):
        self.state["seed_rolled"] = False
        self.state["tingle_tuner_banned"] = False
        self.state["finished_entrants"] = set()

    async def error(self, data):
        self.logger.info(data.get('errors'))
        self.state["seed_rolled"] = False

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

    async def ex_tingletuner(self, args, message):
        if self.state["tingle_tuner_banned"]:
            await self.send_message("The Tingle Tuner is banned in this race.")
        elif self.state.get("seed_rolled"):
            await self.send_message("The Tingle Tuner is allowed in this race.")
        else:
            await self.send_message(
                "Use !bantingletuner if you'd like the Tingle Tuner to be banned in this race. The "
                "ban will go into effect if at least one runner asks for the Tingle Tuner to be banned."
            )

    async def ex_bantingletuner(self, args, message):
        if self.state["tingle_tuner_banned"]:
            await self.send_message("The Tingle Tuner is already banned in this race.")
        elif self.state.get("seed_rolled") and not can_monitor(message):
            await self.send_message("The race has already started! The Tingle Tuner is allowed in this race.")
        else:
            self.state["tingle_tuner_banned"] = True
            await self.send_message("The Tingle Tuner is now banned in this race.")

    @monitor_cmd
    async def ex_unbantingletuner(self, args, message):
        if not self.state["tingle_tuner_banned"]:
            await self.send_message("The Tingle Tuner is already allowed in this race.")
        else:
            self.state["tingle_tuner_banned"] = False
            await self.send_message("The Tingle Tuner is now allowed in this race.")

    @monitor_cmd
    async def ex_startspoilerlograce(self, args, message):
        await self.roll_and_send(args, message)

    async def roll_and_send(self, args, message):
        if self.state.get("seed_rolled"):
            await self.send_message(
                "Race already started!"
            )
            return

        self.loop.create_task(self.roll())

    async def roll(self):
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
        await self.send_message(f"Spoiler Log: {spoiler_log_url}")

        await asyncio.sleep(2100) # 35 minutes

        await self.send_message("You have 15 minutes until the race starts!")
        await self.send_message(f"Permalink: {permalink}")

        await asyncio.sleep(840) # 14 minutes

        await self.send_message("You have 1 minute until the race starts!")
        await self.send_message(f"File Name: {file_name}")

        await asyncio.sleep(45)

        await self.force_start()
