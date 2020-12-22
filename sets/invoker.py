class Invoker:
    def __init__(self):
        self._commands = []
        self.result = None

    def store_command(self, command):
        self._commands.append(command)

    def execute_commands(self):
        for command in self._commands:
            self.result = command.execute()
