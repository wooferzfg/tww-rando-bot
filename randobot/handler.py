import asyncio
from datetime import datetime, timedelta
from racetime_bot import RaceHandler, monitor_cmd, can_monitor


class RandoHandler(RaceHandler):
    stop_at = ["cancelled", "finished"]

    STANDARD_RACE_PERMALINK = "MS44LjAAU3RhbmRhcmRSYWNlRXhhbXBsZQAXAwQATjDADAAAAAAAAAA="
    SPOILER_LOG_PERMALINK = "MS44LjAARXhhbXBsZVNwb2lsZXJMb2cAFwMGAg8QwAwAAAAAAAAA"

    def __init__(self, generator, **kwargs):
        super().__init__(**kwargs)

        self.generator = generator
        self.loop = asyncio.get_event_loop()
        self.loop_ended = False

    async def begin(self):
        if not self.state.get("initialized"):
            self.room_setup()
        self.loop.create_task(self.handle_scheduled_tasks())

    def room_setup(self):
        self.state["spoiler_log_seed_rolled"] = False
        self.state["permalink_available"] = False
        self.state["file_name_available"] = False
        self.state["tingle_tuner_banned"] = False
        self.state["permalink"] = None
        self.state["spoiler_log_url"] = None
        self.state["file_name"] = None
        self.state["initialized"] = True
        self.state["finished_entrants"] = set()

    def close_handler(self):
        self.loop_ended = True

    async def handle_scheduled_tasks(self):
        while not self.loop_ended:
            try:
                if self.state.get("spoiler_log_seed_rolled"):
                    seconds_remaining = self.seconds_remaining()
                    next_ten_minute_warning = self.state.get("next_ten_minute_warning")

                    # Warnings at 40, 30, 20, and 10 minutes
                    if seconds_remaining <= next_ten_minute_warning and next_ten_minute_warning > 0:
                        time_in_minutes = next_ten_minute_warning // 60
                        await self.send_message(f"You have {time_in_minutes} minutes until the race starts!")

                        if time_in_minutes == 10:
                            await self.send_message("Please start your stream if you haven't done so already!")

                        self.state["next_ten_minute_warning"] = next_ten_minute_warning - 600

                    if not self.state.get("permalink_available") and seconds_remaining < 900:
                        await self.send_message("You have 15 minutes until the race starts!")
                        permalink = self.state.get("permalink")
                        await self.send_message(f"Permalink: {permalink}")
                        await self.set_raceinfo(permalink, False, False)
                        self.state["permalink_available"] = True

                    if not self.state.get("5_warning_sent") and seconds_remaining < 300:
                        await self.send_message("You have 5 minutes until the race starts!")
                        self.state["5_warning_sent"] = True

                    if not self.state.get("file_name_available") and seconds_remaining < 60:
                        await self.send_message("You have 1 minute until the race starts!")
                        file_name = self.state.get("file_name")
                        await self.send_message(f"File Name: {file_name}")
                        self.state["file_name_available"] = True

                    if not self.state.get("race_started") and seconds_remaining < 15:
                        await self.force_start()
                        self.state["race_started"] = True
            finally:
                await asyncio.sleep(0.5)

    async def error(self, data):
        self.logger.info(data.get('errors'))

    async def race_data(self, data):
        self.data = data.get("race")

        if self.state.get("spoiler_log_seed_rolled"):
            finished_entrants = {
                entrant.get("user").get("name")
                for entrant in self.data.get("entrants")
                if entrant.get("status").get("value") == "done"
            }

            new_finishers = list(finished_entrants - self.state["finished_entrants"])

            for finisher in new_finishers:
                await self.send_message(
                    f"{finisher}, before you end your stream, please remember to "
                    "advance to the second text box after defeating Ganondorf."
                )

            self.state["finished_entrants"] = finished_entrants

    async def ex_tingletuner(self, args, message):
        if self.state.get("tingle_tuner_banned"):
            await self.send_message("The Tingle Tuner is banned in this race.")
        elif self.state.get("spoiler_log_seed_rolled"):
            await self.send_message("The Tingle Tuner is allowed in this race.")
        else:
            await self.send_message(
                "Use !bantingletuner if you'd like the Tingle Tuner to be banned in this race. The "
                "ban will go into effect if at least one runner asks for the Tingle Tuner to be banned."
            )

    async def ex_bantingletuner(self, args, message):
        if self.state.get("tingle_tuner_banned"):
            await self.send_message("The Tingle Tuner is already banned in this race.")
        elif self.state.get("spoiler_log_seed_rolled") and not can_monitor(message):
            await self.send_message("The race has already started! The Tingle Tuner is allowed in this race.")
        else:
            self.state["tingle_tuner_banned"] = True
            await self.send_message("The Tingle Tuner is now banned in this race.")

    @monitor_cmd
    async def ex_unbantingletuner(self, args, message):
        if not self.state.get("tingle_tuner_banned"):
            await self.send_message("The Tingle Tuner is already allowed in this race.")
        else:
            self.state["tingle_tuner_banned"] = False
            await self.send_message("The Tingle Tuner is now allowed in this race.")

    async def ex_spoilerlogurl(self, args, message):
        if (
            self.state.get("spoiler_log_seed_rolled")
            and (can_monitor(message) or self.state.get("spoiler_log_available"))
        ):
            spoiler_log_url = self.state.get("spoiler_log_url")
            await self.send_message(f"Spoiler Log: {spoiler_log_url}")
        else:
            await self.send_message("Spoiler Log is not available yet!")

    async def ex_permalink(self, args, message):
        if self.state.get("permalink") and (can_monitor(message) or self.state.get("permalink_available")):
            permalink = self.state.get("permalink")
            await self.send_message(f"Permalink: {permalink}")
        else:
            await self.send_message("Permalink is not available yet!")

    async def ex_filename(self, args, message):
        if (
            self.state.get("spoiler_log_seed_rolled")
            and (can_monitor(message) or self.state.get("file_name_available"))
        ):
            file_name = self.state.get("file_name")
            await self.send_message(f"File Name: {file_name}")
        else:
            await self.send_message("File Name is not available yet!")

    async def ex_time(self, args, message):
        if not self.state.get("spoiler_log_seed_rolled"):
            await self.send_message("Seed has not been rolled yet!")
        elif self.state.get("race_started"):
            await self.send_message("Race has already started!")
        else:
            duration = datetime.utcfromtimestamp(self.seconds_remaining())
            time_remaining = duration.strftime("%M:%S")
            await self.send_message(f"You have {time_remaining} until the race starts!")

    def seconds_remaining(self):
        return (self.state.get("race_start_time") - datetime.now()).total_seconds()

    @monitor_cmd
    async def ex_lock(self, args, message):
        self.state["locked"] = True
        await self.send_message("Seed rolling is now locked.")

    @monitor_cmd
    async def ex_unlock(self, args, message):
        self.state["locked"] = False
        await self.send_message("Seed rolling is now unlocked.")

    @monitor_cmd
    async def ex_reset(self, args, message):
        self.room_setup()
        await self.send_message("The Permalink has been reset, and the Tingle Tuner is now allowed in this race.")

    async def ex_rollseed(self, args, message):
        if self.state.get("locked") and not can_monitor(message):
            await self.send_message(
                "Seed rolling is locked. Only the creator of this room, a race monitor, or a moderator can roll a seed."
            )
            return

        if self.state.get("spoiler_log_seed_rolled"):
            await self.send_message("Seed rolling is disabled in spoiler log races!")
            return

        if self.state.get("permalink_available"):
            permalink = self.state.get("permalink")
            await self.send_message("Seed already rolled!")
            await self.send_message(f"Permalink: {permalink}")
            return

        await self.send_message("Rolling seed...")

        settings_permalink = self.STANDARD_RACE_PERMALINK
        if len(args) > 0:
            settings_permalink = args[0]

        generated_seed = self.generator.generate_seed(settings_permalink, False)
        permalink = generated_seed.get("permalink")

        self.logger.info(permalink)

        self.state["permalink"] = permalink
        self.state["permalink_available"] = True

        await self.send_message(f"Permalink: {permalink}")
        await self.set_raceinfo(permalink, False, False)

    async def ex_startspoilerlograce(self, args, message):
        if self.state.get("locked") and not can_monitor(message):
            await self.send_message(
                "Seed rolling is locked. Only the creator of this room, a race monitor, or a moderator can roll a seed."
            )
            return

        if self.state.get("spoiler_log_seed_rolled"):
            await self.send_message("Seed already rolled!")
            return

        settings_permalink = self.SPOILER_LOG_PERMALINK
        if len(args) > 0:
            settings_permalink = args[0]

        self.loop.create_task(self.start_spoiler_log_race(settings_permalink))

    async def start_spoiler_log_race(self, settings_permalink):
        self.state["spoiler_log_seed_rolled"] = True

        await self.send_message("Rolling seed...")

        generated_seed = self.generator.generate_seed(settings_permalink, True)
        spoiler_log_url = generated_seed.get("spoiler_log_url")
        permalink = generated_seed.get("permalink")
        file_name = generated_seed.get("file_name")

        self.logger.info(spoiler_log_url)
        self.logger.info(permalink)
        self.logger.info(file_name)

        self.state["spoiler_log_url"] = spoiler_log_url
        self.state["permalink"] = permalink
        self.state["file_name"] = file_name
        self.state["race_start_time"] = datetime.now() + timedelta(0, 15, 0, 0, 50)
        self.state["next_ten_minute_warning"] = 2400

        await self.send_message("Seed rolled! Preparation stage starts in 15 seconds...")

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
        self.state["spoiler_log_available"] = True
