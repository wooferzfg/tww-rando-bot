from racetime_bot import RaceHandler, monitor_cmd, can_moderate, can_monitor


class RandoHandler(RaceHandler):
    """
    RandoBot race handler. Generates seeds.
    """
    stop_at = ['pending', 'in_progress', 'cancelled', 'finished']

    def __init__(self, generator, **kwargs):
        super().__init__(**kwargs)

        self.generator = generator

    async def begin(self):
        """
        Send introduction messages.
        """
        if not self.state.get('intro_sent'):
            self.state['intro_sent'] = True
            self.state['locked'] = False
            self.state['seed_rolled'] = False

    @monitor_cmd
    async def ex_lock(self, args, message):
        """
        Handle !lock commands.

        Prevent seed rolling unless user is a race monitor.
        """
        self.state['locked'] = True
        await self.send_message(
            'Lock initiated. I will now only roll seeds for race monitors.'
        )

    @monitor_cmd
    async def ex_unlock(self, args, message):
        """
        Handle !unlock commands.

        Remove lock preventing seed rolling unless user is a race monitor.
        """
        self.state['locked'] = False
        await self.send_message(
            'Lock released. Anyone may now roll a seed.'
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
        reply_to = message.get('user', {}).get('name')

        if self.state.get('locked') and not can_monitor(message):
            await self.send_message(
                'Sorry %(reply_to)s, seed rolling is locked. Only race '
                'monitors may roll a seed for this race.'
                % {'reply_to': reply_to or 'friend'}
            )
            return
        if self.state.get('seed_rolled') and not can_moderate(message):
            await self.send_message(
                'Race already started!'
            )
            return

        await self.roll(
            reply_to=reply_to,
        )

    async def roll(self, reply_to):
        """
        Generate a seed and send it to the race room.
        """
        generated_seed = self.generator.generate_seed()

        await self.send_message(
            '%(reply_to)s, here is your seed: %(seed_uri)s'
            % {'reply_to': reply_to or 'Okay', 'seed_uri': generated_seed.get('spoiler_log_url')}
        )

        self.state['seed_rolled'] = True
