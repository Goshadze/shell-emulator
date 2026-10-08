import shlex


class ShellError(Exception):
    pass


class ShellExit(Exception):
    pass


def parse(line):
    try:
        return shlex.split(line)
    except ValueError as err:
        raise ShellError(f"parse error: {err}")


class Shell:
    def __init__(self, vfs):
        self.vfs = vfs
        self.commands = {
            "ls": self.stub,
            "cd": self.stub,
            "exit": self.exit,
            "vfs-info": self.vfs_info,
        }

    def stub(self, name, args):
        return f"{name}: args={args}"

    def exit(self, name, args):
        if args:
            raise ShellError(f"{name}: too many arguments")
        raise ShellExit()

    def vfs_info(self, name, args):
        if args:
            raise ShellError(f"{name}: too many arguments")
        return f"name: {self.vfs.name}\nsha256: {self.vfs.sha256}"

    def execute(self, line):
        tokens = parse(line)
        if not tokens:
            return ""
        name, args = tokens[0], tokens[1:]
        if name not in self.commands:
            raise ShellError(f"{name}: command not found")
        return self.commands[name](name, args)
