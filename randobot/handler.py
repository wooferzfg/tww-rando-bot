import asyncio
import random
from datetime import datetime, timedelta, timezone

import isodate
from racetime_bot import RaceHandler, can_monitor, monitor_cmd

import randobot.constants as constants
from randobot.constants import SeedType
from randobot.generator import RandomizerPath


class RandoHandler(RaceHandler):
    stop_at = ["cancelled", "finished"]

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
        self.state["permalink"] = None
        self.state["example_permalink"] = None
        self.state["seed_hash"] = None
        self.state["spoiler_log_url"] = None
        self.state["planning_time"] = constants.DEFAULT_PLANNING_TIME
        self.state["file_name"] = None
        self.state["initialized"] = True
        self.state["finished_entrants"] = set()
        self.state["entrants"] = []
        self.state["bans"] = {}
        self.state["breaks_set"] = False
        self.state["break_duration"] = constants.MINIMUM_BREAK_DURATION
        self.state["break_interval"] = constants.MINIMUM_BREAK_INTERVAL
        self.state["break_warning_sent"] = False
        self.state["break_in_progress"] = False
        self.state["last_break_time"] = None
        self.state["15_warning_sent"] = False
        self.state["5_warning_sent"] = False
        self.state["1_warning_sent"] = False
        self.state["spoiler_log_race_started"] = False
        self.state["random_settings_spoiler_log_url"] = None
        self.state["random_settings_spoiler_log_unlocked"] = False
        self.state["locked"] = True

    def close_handler(self):
        self.loop_ended = True

    async def handle_scheduled_tasks(self):
        while not self.loop_ended:
            try:
                if self.state.get("spoiler_log_seed_rolled"):
                    seconds_remaining = self.seconds_remaining()
                    next_ten_minute_warning = self.state.get("next_ten_minute_warning")

                    # Warnings at multiples of 10 minutes
                    if seconds_remaining <= next_ten_minute_warning and next_ten_minute_warning > 0:
                        time_in_minutes = next_ten_minute_warning // 60
                        await self.send_message(f"You have {time_in_minutes} minutes until the race starts!")

                        if time_in_minutes == 10:
                            await self.send_message("Please start your stream if you haven't done so already!")

                        self.state["next_ten_minute_warning"] = next_ten_minute_warning - 600

                    if not self.state.get("15_warning_sent") and seconds_remaining < 900:
                        await self.send_message("You have 15 minutes until the race starts!")
                        self.state["15_warning_sent"] = True

                        permalink = self.state.get("permalink")
                        if permalink:
                            seed_hash = self.state.get("seed_hash")
                            await self.send_message(f"Permalink: {permalink}")
                            await self.send_message(f"Seed Hash: {seed_hash}")
                            race_info = f"{permalink} | Seed Hash: {seed_hash}"
                            await self.set_raceinfo(race_info, False, False)
                            self.state["permalink_available"] = True

                    if not self.state.get("5_warning_sent") and seconds_remaining < 300:
                        await self.send_message("You have 5 minutes until the race starts!")
                        self.state["5_warning_sent"] = True

                    if not self.state.get("1_warning_sent") and seconds_remaining < 60:
                        await self.send_message("You have 1 minute until the race starts!")
                        self.state["1_warning_sent"] = True

                        file_name = self.state.get("file_name")
                        if file_name:
                            await self.send_message(f"File Name: {file_name}")
                            self.state["file_name_available"] = True

                    if not self.state.get("spoiler_log_race_started") and seconds_remaining < 15:
                        await self.force_start()
                        self.state["spoiler_log_race_started"] = True

                if self.data.get("started_at") is not None and self.state.get("breaks_set"):
                    break_duration = self.state.get("break_duration")
                    break_interval = self.state.get("break_interval")

                    if self.state.get("last_break_time") is None:
                        self.state["last_break_time"] = isodate.parse_datetime(self.data.get("started_at"))
                    seconds_until_next_break = self._get_seconds_until_next_break()

                    if not self.state.get("break_warning_sent") and seconds_until_next_break < 300:
                        await self.send_message("@entrants Reminder: Next break in 5 minutes.")
                        self.state["break_warning_sent"] = True

                    if not self.state.get("break_in_progress") and seconds_until_next_break < 0:
                        await self.send_message(
                            f"@entrants Break time! Please pause your game for {break_duration} minutes."
                        )
                        self.state["break_in_progress"] = True

                    if self.state.get("break_in_progress") and seconds_until_next_break < break_duration * -60:
                        await self.send_message("@entrants Break ended. You may resume playing.")
                        self.state["break_warning_sent"] = False
                        self.state["break_in_progress"] = False
                        self.state["last_break_time"] = self.state.get("last_break_time") + timedelta(
                            0, 0, 0, 0, break_interval
                        )
            except Exception:
                pass
            finally:
                await asyncio.sleep(0.5)

    async def error(self, data):
        self.logger.info(data.get('errors'))

    async def race_data(self, data):
        self.data = data.get("race")

        self.state["entrants"] = [
            entrant.get("user").get("name")
            for entrant in self.data.get("entrants")
        ]

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

        num_finished_entrants = sum(
            entrant.get("status").get("value") in ("done", "dnf", "dq") for entrant in self.data.get("entrants")
        )
        if (
            self.state.get("random_settings_spoiler_log_url") is not None
            and not self.state.get("random_settings_spoiler_log_unlocked")
            and (
                self.data.get("status").get("value") == "finished"
                or (len(self.data.get("entrants")) == num_finished_entrants and num_finished_entrants > 0)
            )
        ):
            spoiler_log_url = self.state.get("random_settings_spoiler_log_url")
            await self.send_message(f"The race is now finished. The spoiler log can be found here: {spoiler_log_url}")
            self.state["random_settings_spoiler_log_unlocked"] = True

    async def ex_spoilerlogurl(self, args, message):
        spoiler_log_url = self.state.get("spoiler_log_url")
        if spoiler_log_url and (can_monitor(message) or self.state.get("spoiler_log_available")):
            await self.send_message(f"Spoiler Log: {spoiler_log_url}")
        else:
            await self.send_message("Spoiler Log is not available yet!")

    async def ex_permalink(self, args, message):
        permalink = self.state.get("permalink")
        if permalink and (can_monitor(message) or self.state.get("permalink_available")):
            await self.send_message(f"Permalink: {permalink}")
        else:
            await self.send_message("Permalink is not available yet!")

    async def ex_exampleperma(self, args, message):
        await self.print_example_permalink()

    async def ex_hash(self, args, message):
        seed_hash = self.state.get("seed_hash")
        if seed_hash:
            await self.send_message(f"Seed Hash: {seed_hash}")
        else:
            await self.send_message("Seed Hash is not available yet!")

    async def ex_filename(self, args, message):
        file_name = self.state.get("file_name")
        if file_name and (can_monitor(message) or self.state.get("file_name_available")):
            await self.send_message(f"File Name: {file_name}")
        else:
            await self.send_message("File Name is not available yet!")

    async def ex_time(self, args, message):
        if self._race_in_progress():
            await self.send_message("Race has already started!")
        elif not self.state.get("spoiler_log_seed_rolled"):
            await self.send_message("Seed has not been rolled yet!")
        else:
            duration = datetime.utcfromtimestamp(self.seconds_remaining())
            time_remaining = duration.strftime("%-H:%M:%S")
            await self.send_message(f"You have {time_remaining} until the race starts!")

    async def ex_presets(self, args, message):
        msg = "Available standard presets: "
        msg += ", ".join(constants.STANDARD_PERMALINKS.keys())
        await self.send_message(msg)

        msg = "Available spoiler log presets: "
        msg += ", ".join(constants.SPOILER_LOG_PERMALINKS.keys())
        await self.send_message(msg)

    async def ex_devpresets(self, args, message):
        msg = "Available dev presets: "
        msg += ", ".join(constants.DEV_PERMALINKS.keys())
        await self.send_message(msg)

        msg = "Available dev spoiler log presets: "
        msg += ", ".join(constants.DEV_SL_PERMALINKS.keys())
        await self.send_message(msg)

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
        msg = "The Permalink has been reset."
        if self.state.get("planning_time") != constants.DEFAULT_PLANNING_TIME:
            msg += f" The planning time has also been reset to {constants.DEFAULT_PLANNING_TIME} minutes."
        self.room_setup()
        await self.send_message(msg)

    async def ex_banorder(self, args, message):
        entrants = self.state.get("entrants").copy()

        if len(entrants) == 0:
            await self.send_message("The race has no entrants!")
            return

        random.shuffle(entrants)
        ban_order = ", ".join(entrants)

        await self.send_message(f"Ban Order: {ban_order}")

    async def ex_ban(self, args, message):
        bans = self.state.get("bans")
        preset_to_ban = args[0]
        bannable_presets = [
            preset
            for preset in constants.BANNABLE_PRESETS
            if preset not in bans.values()
        ]

        if preset_to_ban not in bannable_presets:
            bannable_presets_list = ", ".join(bannable_presets)
            await self.send_message(f"{preset_to_ban} is not a valid preset to ban!")
            await self.send_message(f"Available presets to ban: {bannable_presets_list}")
            return

        username = message.get('user', {}).get('name')

        bans[username] = preset_to_ban

        await self.print_banned_presets()

    async def ex_bans(self, args, message):
        await self.print_banned_presets()

    async def ex_setplanningtime(self, args, message):
        if self.state.get("spoiler_log_seed_rolled"):
            await self.send_message("Planning has already started!")
            return

        if len(args) == 0:
            await self.send_message("Please specify planning time (in minutes).")
            return

        planning_time = args[0]

        try:
            planning_time = max(constants.MINIMUM_PLANNING_TIME, int(planning_time))
            self.state["planning_time"] = planning_time
            await self.send_message(f"Planning time set to {planning_time} minutes.")
        except (TypeError, ValueError):
            await self.send_message(f"{planning_time} is not a valid time.")

    async def ex_rollseed(self, args, message):
        if not await self.can_roll_standard_seed(message):
            return

        await self.send_message("Rolling seed...")

        settings_permalink = await self.choose_permalink(
            constants.STANDARD_DEFAULT,
            constants.STANDARD_PERMALINKS,
            args
        )

        username = message.get('user', {}).get('name')
        generated_seed = await self._generate_seed(
            randomizer_path=RandomizerPath.WWRANDO,
            permalink=settings_permalink,
            prefix=username,
            generate_spoiler_log=False,
        )
        await self.update_race_room_with_generated_seed(settings_permalink, generated_seed, SeedType.STANDARD)

    async def ex_s8(self, args, message):
        if not await self.can_roll_standard_seed(message):
            return

        await self.send_message("Rolling seed...")

        settings_permalink = await self.choose_permalink(
            constants.S8_DEFAULT,
            constants.S8_PERMALINKS,
            args
        )

        username = message.get("user", {}).get("name")
        generated_seed = await self._generate_seed(
            randomizer_path=RandomizerPath.WWRANDO_S8,
            permalink=settings_permalink,
            prefix=username,
            generate_spoiler_log=False,
        )
        await self.update_race_room_with_generated_seed(settings_permalink, generated_seed, SeedType.STANDARD)
        await self.print_s8_build()

    async def ex_rolldevseed(self, args, message):
        if not await self.can_roll_standard_seed(message):
            return

        await self.send_message("Rolling seed...")

        settings_permalink = await self.choose_permalink(
            constants.DEV_DEFAULT,
            constants.DEV_PERMALINKS,
            args
        )

        username = message.get("user", {}).get("name")
        generated_seed = await self._generate_seed(
            randomizer_path=RandomizerPath.WWRANDO_DEV,
            permalink=settings_permalink,
            prefix=username,
            generate_spoiler_log=False,
        )
        await self.update_race_room_with_generated_seed(settings_permalink, generated_seed, SeedType.STANDARD)
        await self.print_dev_build()

    async def ex_miniblins(self, args, message):
        if not await self.can_roll_standard_seed(message):
            return

        await self.send_message("Rolling seed...")

        settings_permalink = await self.choose_permalink(
            constants.DEV_DEFAULT,
            constants.DEV_PERMALINKS,
            args
        )

        username = message.get("user", {}).get("name")
        generated_seed = await self._generate_seed(
            randomizer_path=RandomizerPath.WWRANDO_DEV,
            permalink=settings_permalink,
            prefix=username,
            generate_spoiler_log=False,
        )
        await self.update_race_room_with_generated_seed(settings_permalink, generated_seed, SeedType.STANDARD)
        await self.print_miniblins_build()

    async def ex_randomsettings(self, args, message):
        if not await self.can_roll_standard_seed(message):
            return

        await self.send_message("Rolling seed...")

        settings_permalink = await self.choose_permalink(
            constants.RS_DEFAULT,
            constants.RS_PERMALINKS,
            args
        )

        username = message.get('user', {}).get('name')
        generated_seed = await self._generate_seed(
            randomizer_path=RandomizerPath.WWRANDO_RANDOM_SETTINGS,
            permalink=settings_permalink,
            prefix=username,
            generate_spoiler_log=True,
        )

        await self.update_race_room_with_generated_seed(settings_permalink, generated_seed, SeedType.RANDOM_SETTINGS)

        await self.send_message(
            f"Please note that this seed uses the Random Settings {constants.RS_VERSION} build of the randomizer. "
            f"Download: {constants.RS_DOWNLOAD} "
            f"Tracker: {constants.RS_TRACKER}"
        )

    async def can_roll_standard_seed(self, message):
        if self.state.get("locked") and not can_monitor(message):
            await self.send_message(
                "Seed rolling is locked. "
                "Only the creator of this room, a race monitor, or a moderator can roll a seed. "
                "(Use !unlock to unlock seed rolling.)"
            )
            return False

        if self.state.get("spoiler_log_seed_rolled"):
            await self.send_message("Seed rolling is disabled in spoiler log races!")
            return False

        if self.state.get("permalink_available"):
            permalink = self.state.get("permalink")
            seed_hash = self.state.get("seed_hash")
            await self.send_message("Seed already rolled!")
            await self.send_message(f"Permalink: {permalink}")
            await self.send_message(f"Seed Hash: {seed_hash}")
            return False

        return True

    async def can_start_spoiler_log_race(self, message):
        if self.state.get("locked") and not can_monitor(message):
            await self.send_message(
                "Seed rolling is locked. Only the creator of this room, a race monitor, "
                "or a moderator can roll a seed. (Use !unlock to unlock seed rolling.)"
            )
            return False

        if self.state.get("spoiler_log_seed_rolled"):
            await self.send_message("Seed already rolled!")
            return False

        return True

    async def update_race_room_with_generated_seed(self, settings_permalink, generated_seed, type):
        permalink = generated_seed.get("permalink")
        seed_hash = generated_seed.get("seed_hash")

        self.logger.info(permalink)

        self.state["example_permalink"] = settings_permalink
        self.state["permalink"] = permalink
        self.state["seed_hash"] = seed_hash

        if type == SeedType.SPOILER_LOG:
            spoiler_log_url = generated_seed.get("spoiler_log_url")
            file_name = generated_seed.get("file_name")

            self.logger.info(spoiler_log_url)
            self.logger.info(file_name)

            self.state["spoiler_log_url"] = spoiler_log_url
            self.state["file_name"] = file_name

            await self.send_message("Seed rolled!")
        else:
            self.state["permalink_available"] = True
            if type == SeedType.RANDOM_SETTINGS:
                self.state["random_settings_spoiler_log_url"] = generated_seed.get("spoiler_log_url")

            await self.send_message(f"Permalink: {permalink}")
            await self.send_message(f"Seed Hash: {seed_hash}")

            race_info = f"{permalink} | Seed Hash: {seed_hash}"
            await self.set_raceinfo(race_info, False, False)

    async def ex_startspoilerlogtimer(self, args, message):
        if self.state.get("locked") and not can_monitor(message):
            await self.send_message(
                "Race starting is locked. Only the creator of this room, a race monitor, "
                "or a moderator can start a race. (Use !unlock to unlock race starting.)"
            )
            return

        if self.state.get("spoiler_log_seed_rolled"):
            await self.send_message("Race already started!")
            return

        self.loop.create_task(self.start_spoiler_log_race())

    async def ex_startspoilerlograce(self, args, message):
        if not await self.can_start_spoiler_log_race(message):
            return

        settings_permalink = await self.choose_permalink(
            constants.SPOILER_LOG_DEFAULT,
            constants.SPOILER_LOG_PERMALINKS,
            args
        )
        username = message.get('user', {}).get('name')

        await self.send_message("Rolling seed...")
        generated_seed = await self._generate_seed(
            randomizer_path=RandomizerPath.WWRANDO,
            permalink=settings_permalink,
            prefix=username,
            generate_spoiler_log=True,
        )
        await self.update_race_room_with_generated_seed(settings_permalink, generated_seed, SeedType.SPOILER_LOG)

        self.loop.create_task(self.start_spoiler_log_race())

    async def ex_starts8spoilerlograce(self, args, message):
        if not await self.can_start_spoiler_log_race(message):
            return

        settings_permalink = await self.choose_permalink(
            constants.S8_SL_DEFAULT,
            constants.S8_SL_PERMALINKS,
            args
        )
        username = message.get('user', {}).get('name')

        await self.send_message("Rolling seed...")
        generated_seed = await self._generate_seed(
            randomizer_path=RandomizerPath.WWRANDO_S8,
            permalink=settings_permalink,
            prefix=username,
            generate_spoiler_log=True,
        )
        await self.update_race_room_with_generated_seed(settings_permalink, generated_seed, SeedType.SPOILER_LOG)
        await self.print_s8_build()

        self.loop.create_task(self.start_spoiler_log_race())

    async def ex_startdevspoilerlograce(self, args, message):
        if not await self.can_start_spoiler_log_race(message):
            return

        settings_permalink = await self.choose_permalink(
            constants.DEV_SL_DEFAULT,
            constants.DEV_SL_PERMALINKS,
            args
        )
        username = message.get('user', {}).get('name')

        await self.send_message("Rolling seed...")
        generated_seed = await self._generate_seed(
            randomizer_path=RandomizerPath.WWRANDO_DEV,
            permalink=settings_permalink,
            prefix=username,
            generate_spoiler_log=True,
        )
        await self.update_race_room_with_generated_seed(settings_permalink, generated_seed, SeedType.SPOILER_LOG)
        await self.print_dev_build()

        self.loop.create_task(self.start_spoiler_log_race())

    async def start_spoiler_log_race(self):
        self.state["spoiler_log_seed_rolled"] = True

        planning_time = self.state.get("planning_time")

        time_to_next_warning = planning_time % 10
        if time_to_next_warning == 0:
            time_to_next_warning = 10

        self.state["race_start_time"] = datetime.now() + timedelta(0, 15, 0, 0, planning_time)
        self.state["next_ten_minute_warning"] = (planning_time - time_to_next_warning) * 60

        await self.send_message("Preparation stage starts in 15 seconds...")

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

        await self.send_message(f"You have {planning_time} minutes to prepare your route!")

        spoiler_log_url = self.state["spoiler_log_url"]
        if spoiler_log_url:
            await self.send_message(f"Spoiler Log: {spoiler_log_url}")
            self.state["spoiler_log_available"] = True
            await self.print_example_permalink()

    async def choose_permalink(self, default_settings, presets, args):
        # Use default settings if no arguments are provided to the command
        settings_list = args if len(args) > 0 else default_settings

        # Split args into permalinks and presets
        permalink_args = []
        preset_args = []
        for settings in settings_list:
            if self._is_permalink(settings):
                permalink_args.append(settings)
            else:
                # Convert all non-permalink settings to lowercase
                preset_args.append(settings.lower())

        # Remove any settings that are banned
        banned_presets = self.state.get("bans").values()
        unbanned_presets = [
            preset for preset in preset_args if preset not in banned_presets
        ]

        # Raise exception if all settings are banned
        if len(permalink_args) + len(unbanned_presets) == 0:
            msg = "There were no valid settings to choose from after bans!"
            await self.send_message(msg)
            raise Exception(msg)

        # Raise exception if any of the presets are invalid
        invalid_presets = set(
            f'"{settings}"'
            for settings in unbanned_presets
            if settings not in presets.keys()
        )
        if len(invalid_presets) > 0:
            msg = f"Invalid preset{'s' if len(invalid_presets) != 1 else ''}: {', '.join(invalid_presets)}"
            await self.send_message(msg)
            raise Exception(msg)

        # Select a settings key at random from the list of valid settings
        valid_settings = permalink_args + unbanned_presets
        settings_idx = int(random.random() * len(valid_settings))
        settings_key = valid_settings[settings_idx]

        # If a selection was made from more than one option, update race room chat and info
        if len(valid_settings) > 1:
            settings_text = f"Settings: {settings_key}"
            settings_description = constants.SETTINGS_DESCRIPTIONS.get(settings_key)
            if settings_description:
                settings_text += f" ({settings_description})"
            await self.send_message(settings_text)
            await self.set_raceinfo(settings_text, False, False)

        # Determine the permalink for the settings
        if self._is_permalink(settings_key):
            settings_permalink = settings_key
        else:
            # Get base permalink
            settings_permalink = presets.get(settings_key)

        return settings_permalink

    async def print_banned_presets(self):
        banned_presets = self.state.get("bans").values()

        if len(banned_presets) == 0:
            await self.send_message("No presets are banned yet!")
        else:
            bannable_presets_list = ", ".join(banned_presets)
            await self.send_message(f"Banned Presets: {bannable_presets_list}")

    def seconds_remaining(self):
        return (self.state.get("race_start_time") - datetime.now()).total_seconds()

    async def print_s8_build(self):
        await self.send_message("Please note that this seed uses the S8 Tournament build of the randomizer.")
        await self.send_message(f"Download: {constants.S8_DOWNLOAD}")
        await self.send_message(f"Tracker: {constants.S8_TRACKER}")

    async def print_dev_build(self):
        await self.send_message("Please note that this seed uses the dev build of the randomizer.")
        await self.send_message(f"Download: {constants.DEV_DOWNLOAD}")
        await self.send_message(f"Tracker: {constants.DEV_TRACKER}")

    async def print_miniblins_build(self):
        await self.send_message("Please note that this seed uses the dev build of the randomizer.")
        await self.send_message(f"Download: {constants.DEV_DOWNLOAD}")
        await self.send_message(f"Tracker: {constants.MINIBLINS_TRACKER}")

    async def print_example_permalink(self):
        example_permalink = self.state.get("example_permalink")
        if example_permalink:
            await self.send_message(f"Example Permalink: {example_permalink}")
            await self.send_message("Warning: The seed from this permalink does not match the actual permalink!")
        else:
            await self.send_message("Example Permalink is not available yet!")

    async def ex_breaks(self, args, message):
        if self._race_in_progress():
            if self.state.get("breaks_set"):
                seconds_until_next_break = self._get_seconds_until_next_break()
                if not self.state.get("break_in_progress"):
                    await self.send_message(
                        f"The next break is in {self._get_formatted_duration_str(seconds_until_next_break)}."
                    )
                else:
                    # During a break, `seconds_until_next_break` = - seconds_since_break_started
                    seconds_until_break_ends = (self.state.get("break_duration") * 60) + seconds_until_next_break
                    await self.send_message(
                        f"The break ends in {self._get_formatted_duration_str(seconds_until_break_ends)}."
                    )
            else:
                await self.send_message("Breaks have not been set.")
        elif len(args) == 0:
            if self.state.get("breaks_set"):
                break_duration = self.state.get("break_duration")
                break_interval = self.state.get("break_interval")
                await self.send_message(f"Breaks are set for {break_duration} minutes every {break_interval} minutes.")
            else:
                await self.send_message(
                    'Breaks are off. Example usage is "!breaks 5 60" for 5-minute breaks every 60 minutes.'
                )
        elif len(args) == 1:
            if args[0] == "off":
                if self.state.get("breaks_set"):
                    self.state["breaks_set"] = False
                    self.state["break_duration"] = constants.MINIMUM_BREAK_DURATION
                    self.state["break_interval"] = constants.MINIMUM_BREAK_INTERVAL
                    await self.send_message("Breaks have been turned off.")
                else:
                    await self.send_message("Breaks are already off.")
            else:
                await self.send_message(
                    'Error parsing command. Example usage is "!breaks 5 60" for 5-minute breaks every 60 minutes.'
                )
        else:
            break_duration, break_interval = args

            try:
                break_duration = max(constants.MINIMUM_BREAK_DURATION, int(break_duration))
            except (TypeError, ValueError):
                await self.send_message(f"{break_duration} is not a valid time.")
                return

            try:
                break_interval = max(constants.MINIMUM_BREAK_INTERVAL, int(break_interval))
            except (TypeError, ValueError):
                await self.send_message(f"{break_interval} is not a valid time.")
                return

            # Ensure that there's a valid amount of time in-between breaks
            if break_interval <= break_duration + 5:
                await self.send_message("Error. Please ensure there are more than 5 minutes in-between breaks.")
                return

            self.state["breaks_set"] = True
            self.state["break_duration"] = break_duration
            self.state["break_interval"] = break_interval
            await self.send_message(
                f"Breaks have been set for {break_duration} minutes every {break_interval} minutes."
            )

    def _get_seconds_until_next_break(self):
        if self.state.get("last_break_time") is None:
            return 0

        seconds_since_last_break = (datetime.now(timezone.utc) - self.state.get("last_break_time")).total_seconds()
        return (self.state.get("break_interval") * 60) - seconds_since_last_break

    def _get_formatted_duration_str(self, duration_in_seconds):
        if duration_in_seconds < 0:
            return "Invalid time"
        if duration_in_seconds == 0:
            return "0 seconds"

        hours = duration_in_seconds // 3600
        minutes = (duration_in_seconds - (hours * 3600)) // 60
        seconds = duration_in_seconds - (hours * 3600) - (minutes * 60)

        formatted_str = []
        if hours != 0:
            hours_string = f"{hours} hour"
            if hours > 1:
                hours_string += "s"
            formatted_str.append(hours_string)
        if minutes != 0:
            minutes_string = f"{minutes} minute"
            if minutes > 1:
                minutes_string += "s"
            formatted_str.append(minutes_string)
        if seconds != 0:
            seconds_string = f"{seconds} second"
            if seconds > 1:
                seconds_string += "s"
            formatted_str.append(seconds_string)

        if len(formatted_str) == 3:
            formatted_str[2] = f"and {formatted_str[2]}"
            return ", ".join(formatted_str)
        elif len(formatted_str) == 2:
            return f"{formatted_str[0]} and {formatted_str[1]}"
        else:
            return formatted_str[0]

    def _race_in_progress(self):
        return self.data.get("status").get("value") in ("pending", "in_progress")

    def _is_permalink(self, permalink_or_preset):
        for prefix in constants.PERMALINK_PREFIXES:
            if permalink_or_preset.startswith(prefix):
                return True
        return False

    async def _generate_seed(
        self,
        randomizer_path: RandomizerPath,
        permalink: str,
        prefix: str,
        generate_spoiler_log: bool,
    ):
        try:
            return self.generator.generate_seed(
                randomizer_path=randomizer_path,
                permalink=permalink,
                prefix=prefix,
                generate_spoiler_log=generate_spoiler_log,
            )
        except Exception:
            await self.send_message("Failed to generate seed!")
            raise Exception("Failed to generate seed")
