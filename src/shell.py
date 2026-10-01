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


def stub(name, args):
    return f"{name}: args={args}"


def run_exit(name, args):
    if args:
        raise ShellError("exit: too many arguments")
    raise ShellExit()


COMMANDS = {
    "ls": stub,
    "cd": stub,
    "exit": run_exit,
}


def execute(line):
    tokens = parse(line)
    if not tokens:
        return ""
    name, args = tokens[0], tokens[1:]
    if name not in COMMANDS:
        raise ShellError(f"{name}: command not found")
    return COMMANDS[name](name, args)
