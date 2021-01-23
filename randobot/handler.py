import asyncio
from datetime import datetime, timedelta
from racetime_bot import RaceHandler, monitor_cmd, can_monitor

class RandoHandler(RaceHandler):
    stop_at = ["cancelled", "finished"]

    CURRENT_STANDARD_RACE_GOAL = "Standard Race - Defeat Ganondorf"
    CURRENT_STANDARD_RACE_PERMALINK = "MS44LjAAU3RhbmRhcmRSYWNlRXhhbXBsZQAXAwQATjDADAAAAAAAAAA="
    CURRENT_SPOILER_LOG_GOAL = "Spoiler Log"
    CURRENT_SPOILER_LOG_PERMALINK = "MS44LjAARXhhbXBsZVNwb2lsZXJMb2cAFwMGAg8QwAwAAAAAAAAA"


    def __init__(self, generator, **kwargs):
        super().__init__(**kwargs)

        self.generator = generator
        self.loop = asyncio.get_event_loop()
        self.loop_ended = False

    async def begin(self):
        if not self.state.get("initialized"):
            self.state["initialized"] = True
            self.state["finished_entrants"] = set()
            self.state["race_delay"] = timedelta(0, 5)

        self.loop.create_task(self.handle_scheduled_tasks())

    async def race_data(self, data):
        self.data = data.get('race')
        if not self.data.goal.custom:
            if self.data.goal.name == CURRENT_STANDARD_RACE_GOAL:
                self.state["standard_race"] = True
                self.state["spoiler_log"] = False
                self.state["force_filename"] = False
                self.state["race_delay"] = timedelta(0, 5)
            elif self.data.goal.name == CURRENT_SPOILER_LOG_GOAL:
                self.state["standard_race"] = False
                self.state["spoiler_log"] = True
                self.state["force_filename"] = True
                self.state["race_delay"] = timedelta(0, 5, 0, 0, 50)
            else:
                self.state["standard_race"] = False
                self.state["spoiler_log"] = False
                self.state["force_filename"] = False

    def close_handler(self):
        self.loop_ended = True

    async def handle_scheduled_tasks(self):
        while not self.loop_ended:
            try:
                if self.state.get("seed_rolled"):
                    seconds_remaining = self.seconds_remaining(False)

                    if not self.state.get("60_warning_sent") and seconds_remaining < 3600: # 60 minutes
                        await self.send_message("You have an hour until the race starts!")
                        self.state["60_warning_sent"] = True

                    if not self.state.get("50_warning_sent") and seconds_remaining < 3000: # 50 minutes
                        await self.send_message("You have 50 minutes until the race starts!")
                        self.state["50_warning_sent"] = True

                    if not self.state.get("40_warning_sent") and seconds_remaining < 2400: # 40 minutes
                        await self.send_message("You have 40 minutes until the race starts!")
                        self.state["40_warning_sent"] = True

                    if not self.state.get("30_warning_sent") and seconds_remaining < 1800: # 30 minutes
                        await self.send_message("You have 30 minutes until the race starts!")
                        self.state["30_warning_sent"] = True

                    if not self.state.get("20_warning_sent") and seconds_remaining < 1200: # 20 minutes
                        await self.send_message("You have 20 minutes until the race starts!")
                        self.state["20_warning_sent"] = True

                    if not self.state.get("permalink_available") and seconds_remaining < 900: # 15 minutes
                        await self.send_message("You have 15 minutes until the race starts!")
                        permalink = self.state.get("permalink")
                        await self.send_message(f"Permalink: {permalink}")
                        self.state["permalink_available"] = True

                    if not self.state.get("10_warning_sent") and seconds_remaining < 600: # 10 minutes
                        await self.send_message("You have 10 minutes until the race starts!")
                        if not self.state.get("custom_race"):
                            await self.send_message("Please start your stream if you haven't done so already!")
                        self.state["10_warning_sent"] = True

                    if not self.state.get("5_warning_sent") and seconds_remaining < 300: # 5 minutes
                        await self.send_message("You have 5 minutes until the race starts!")
                        self.state["5_warning_sent"] = True

                    if not self.state.get("file_name_available") and seconds_remaining < 60: # 1 minute
                        await self.send_message("You have 1 minute until the race starts!")
                        if self.state.get("force_filename"):
                            file_name = self.state.get("file_name")
                            await self.send_message(f"File Name: {file_name}")
                            self.state["file_name_available"] = True

                    if not self.state.get("race_started") and seconds_remaining < 15 and not self.state.get("standard_race") and not self.state.get("custom_race"):
                        await self.force_start()
                        self.state["race_started"] = True
            finally:
                await asyncio.sleep(0.5)

    async def error(self, data):
        self.logger.info(data.get('errors'))

    async def race_data(self, data):
        self.data = data.get("race")

        if self.state.get("seed_rolled"):
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
                if self.state.get("spoiler_log"):
                    await self.send_message(
                        f"{finisher}, before you end your stream, please remember to advance to the second text box after defeating Ganondorf."
                    )
                else:
                    await self.send_message(f"{finisher}, great job!")

            self.state["finished_entrants"] = finished_entrants

#Note on Commands. Please adhere to the following order when making commands
#1. Initial Calling/State Handling. Pertaining only to the Bot
#2. Game State Changing, IE Tingle Tuner, Permalink changes, Requests for things related to that
#3. Race Commands, such as time related commands
#4. Seed Rolling
#If it can't apply to the above, feature might not be suitable

    @monitor_cmd
    async def ex_summonbot(self, args, message):
        await self.send_message("Hey everyone!"):
        race_delay = (self.state.get["race_delay"] - timedelta.(0,5)).total_minutes()
        if self.state.get("standard_race"):
            await self.send_message("Please use command !startrace to get a permalink.")
            self.state["permalink"] = CURRENT_STANDARD_RACE_PERMALINK
        elif self.state.get("spoiler_log"):
            await self.send_message(f"Please use command !startrace to get a link to the spoiler log, race is set to start {race_delay} minutes after that.")
            self.state["permalink"] = CURRENT_SPOILER_LOG_PERMALINK
        else:
            self.state["custom_race"] = True
            await self.send_message("You've summoned me to a custom room! Feel free to use !newperma <Permalink> to give me a permalink!")
        self.set_time_states(self.seconds_remaining(True))

    @monitor_cmd
    async def ex_removebot(self, args, message):
        self.state["remove_bot"] = True
        await self.send_message("This will remove the bot and it will forget all currently set settings, use !confirm to do this, otherwise use !cancel")

    async def ex_confirm(self, args, message):
        if self.state.get("remove_bot"):
            self.should_stop()

    async def ex_cancel(self, args, message):
        if self.state.get("remove_bot"):
            await self.send_message("Command Cancelled")
            self.state["remove_bot"] = False

    async def ex_newperma(self, args, message):
        if self.state.get("seed_rolled"):
            await self.send_message("Too late! Permalink was made!")
        elif self.state.get("standard_race"):
            await self.send_message("Sorry, standard races have a set permalink")
        elif self.state.get("spoiler_log"):
            await self.send_message("Please keep in mind that this permalink needs to have Generated Spoiler Log enabled!")
            CURRENT_PERMALINK = args
            self.state["custom_race"] = True
        else:
            CURRENT_PERMALINK = args
            self.state["custom_race"] = True

    @monitor_cmd
    async def ex_setfilename(self, args, message):
        if self.state.get("race_started"):
            await self.send_message("Too late! Race is started!")
        elif args == "True" or args == "true":
            self.state["force_filename"] = True
            self.state["file_name_available"] = False
            await.send_message("Custom Filenames are not allowed for this race!")
        elif args == "False" or args == "false":
            self.state["file_name_available"] = True
            self.state["forse_filename"] = False
            await.send_message("Custom Filenames are allowed! FeelsCustomMan")
        else:
            await.send_message("Error, I speak English, not Hylian")

    @monitor_cmd
    async def ex_confirmaspoilerlog(self, args, message):
        if self.state.get("seed_rolled"):
            await self.send_message("Too late! Seed has been rolled!")
        elif args == "True" or args == "true":
            self.state["spoiler_log"] = True
            await self.send_message("A spoiler log will be generated from this race.")
        elif args == "False" or args == "false":
            self.state["custom_race"] = True
            self.state["spoiler_log"] = False
            await self.send_message("No spoilers this time! Mode set to Custom.")
        else:
            await self.send_message("Error, I speak English, not Hylian!")

    async def ex_tingletuner(self, args, message):
        if self.state.get("tingle_tuner_banned"):
            await self.send_message("The Tingle Tuner is banned in this race.")
        elif self.state.get("seed_rolled"):
            await self.send_message("The Tingle Tuner is allowed in this race.")
        else:
            await self.send_message(
                "Use !bantingletuner if you'd like the Tingle Tuner to be banned in this race. The "
                "ban will go into effect if at least one runner asks for the Tingle Tuner to be banned."
            )

    async def ex_bantingletuner(self, args, message):
        if self.state.get("tingle_tuner_banned"):
            await self.send_message("The Tingle Tuner is already banned in this race.")
        elif self.state.get("seed_rolled") and not can_monitor(message):
            await self.send_message("The race has already started! The Tingle Tuner is allowed in this race.")
        else:
            self.state["tingle_tuner_banned"] = True
            await self.send_message("The Tingle Tuner is now banned in this race.")

    async def ex_unbantingletuner(self, args, message):
        if not self.state.get("tingle_tuner_banned"):
            await self.send_message("The Tingle Tuner is already allowed in this race.")
        else:
            self.state["tingle_tuner_banned"] = False
            await self.send_message("The Tingle Tuner is now allowed in this race.")

    async def ex_spoilerlogurl(self, args, message):
        if self.state.get("seed_rolled") and (can_monitor(message) or self.state.get("spoiler_log_available")):
            spoiler_log_url = self.state.get("spoiler_log_url")
            await self.send_message(f"Spoiler Log: {spoiler_log_url}")

    async def ex_permalink(self, args, message):
        permalink = self.state.get("permalink")
        if self.state.get("seed_rolled") and (can_monitor(message) or self.state.get("permalink_available")):
            await self.send_message(f"Permalink: {permalink}")
        else:
            await self.send_message(f"Permalink is not available! Current Settings {permalink}")

    async def ex_filename(self, args, message):
        if self.state.get("seed_rolled") and (can_monitor(message) or self.state.get("file_name_available") and self.state.get("force_filename")):
            file_name = self.state.get("file_name")
            await self.send_message(f"File Name: {file_name}")
        elif not self.state.get("force_filename"):
            await self.send_message("I mean if you want one so bad, I hear Cubsrule is a decent one.")
        else:
            await self.send_message("File Name is not available yet!")

    @monitor_cmd
    async def ex_setplanningtime(self, args, message):
        if not isinstance(args, int):
            await.self.send_message("Please send a time in minutes!")
            return

        if self.state.get("spoiler_log"):
            self.state["race_delay"] = timedelta(0, 5, 0, 0, args)
            await self.set_time_states(self.seconds_remaining(True))
            await self.send_message(f"You adjusted the planning time, it is now {args} minutes long!")
        else:
            await self.send_message("Sorry, only Spoiler Log races have a planning time.")

    async def ex_time(self, args, message):
        if not self.state.get("seed_rolled"):
            await self.send_message("Seed has not been generated yet!")
        elif self.state.get("race_started"):
            await self.send_message("Race has already started!")
        else:
            duration = datetime.utcfromtimestamp(self.seconds_remaining())
            time_remaining = duration.strftime("%M:%S")
            await self.send_message(f"You have {time_remaining} until the race starts!")

    def seconds_remaining(self, args):
        if(args == True):
            return (self.state.get("race_delay") - timedelta(0,5)).total_seconds()
        if not self.state.get("time_paused"):
            return (self.state.get("race_start_time") - datetime.now()).total_seconds()
        else:
            return 9999

    #Note to self, find a better solution
    async def set_time_states(self, waitTime):
        if waitTime > 3600: # 60 minutes
            self.state["60_warning_sent"] = False
        else:
            self.state["60_warning_sent"] = True

        if waitTime > 3000: # 50 minutes
            self.state["50_warning_sent"] = False
        else:
            self.state["50_warning_sent"] = True

        if waitTime > 2400: # 40 minutes
            self.state["40_warning_sent"] = False
        else:
            self.state["40_warning_sent"] = True

        if waitTime > 1800: # 30 minutes
            self.state["30_warning_sent"] = False
        else:
            self.state["30_warning_sent"] = True

        if waitTime > 1200: # 20 minutes
            self.state["20_warning_sent"] = False
        else:
            self.state["20_warning_sent"] = True

        if waitTime > 900: # 15 minutes
            self.state["15_warning_sent"] = False
        else:
            self.state["15_warning_sent"] = True

        if waitTime > 600: # 10 minutes
            self.state["10_warning_sent"] = False
        else:
            self.state["10_warning_sent"] = True

        if waitTime > 300: # 5 minutes
            self.state["5_warning_sent"] = False
        else:
            self.state["5_warning_sent"] = True

    @monitor_cmd
    async def ex_startrace(self, args, message):
        if self.state.get("spoiler_log"):
            await self.startspoilerlograce(args, message)
        elif self.state.get("standard_race"):
            await self.startstandardrace(args, message)
        else:
            await self.startcustomrace(args, message)

    async def startcustomrace(self, args, message):
        if not self.state.get("seed_rolled")
            await self.send_message("Starting up this custom race!")
            await self.roll_and_send(args, message)

    async def startstandardrace(self, args, message):
        if not self.state.get("seed_rolled"):
            await self.roll_and_send(arge, message)

    async def startspoilerlograce(self, args, message):
        if not self.state.get("seed_rolled"):
            await self.roll_and_send(args, message)


    async def roll_and_send(self, args, message):
        if self.state.get("seed_rolled"):
            await self.send_message(
                "Seed already generated!"
            )
            return

        self.loop.create_task(self.roll())

    async def roll(self):
        self.state["seed_rolled"] = True

        await self.send_message("Generating seed...")

        permalink = self.state.get("permalink")
        generated_seed = self.generator.generate_seed(permalink, self.state.get("spoiler_log"))
        spoiler_log_url = generated_seed.get("spoiler_log_url")
        permalink = generated_seed.get("permalink")
        file_name = generated_seed.get("file_name")

        self.logger.info(spoiler_log_url)
        self.logger.info(permalink)
        self.logger.info(file_name)

        self.state["spoiler_log_url"] = spoiler_log_url
        self.state["permalink"] = permalink
        self.state["file_name"] = file_name
        self.state["race_start_time"] = datetime.now() + self.state.get("race_delay")

        await self.send_message("Seed generated! Lets see how this turned out......")
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

        if self.state.get("spoiler_log"):
            race_delay_in_minutes = seconds_remaining(True).total_minutes()
            await self.send_message(f"You have {race_delay_in_minutes} minutes to prepare your route!")
            await self.send_message(f"Spoiler Log: {spoiler_log_url}")
            self.state["spoiler_log_available"] = True

        elif self.state.get("standard_race") or self.state.get("custom_race"):
            await self.send_message(f"Here is the permalink! {permalink}")
            await self.send_message("Make sure to ready up and start the race!")
