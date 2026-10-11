import calendar
import datetime
import posixpath
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
        self.cwd = "/"
        self.commands = {
            "ls": self.ls,
            "cd": self.cd,
            "cal": self.cal,
            "cat": self.cat,
            "chown": self.chown,
            "exit": self.exit,
            "vfs-info": self.vfs_info,
        }

    def resolve(self, name, path):
        full = posixpath.normpath(posixpath.join(self.cwd, path))
        if full not in self.vfs.nodes:
            raise ShellError(f"{name}: {path}: no such file or directory")
        return full

    def children(self, path):
        return sorted(
            p for p in self.vfs.nodes
            if p != "/" and posixpath.dirname(p) == path
        )

    def entry(self, path, long):
        name = posixpath.basename(path)
        if not long:
            return name
        node = self.vfs.nodes[path]
        kind = "d" if node.kind == "dir" else "-"
        return f"{kind} {node.owner} {name}"

    def ls(self, name, args):
        long = "-l" in args
        match [arg for arg in args if arg != "-l"]:
            case []:
                target = "."
            case [target]:
                pass
            case _:
                raise ShellError(f"{name}: too many arguments")
        path = self.resolve(name, target)
        if self.vfs.nodes[path].kind == "dir":
            paths = self.children(path)
        else:
            paths = [path]
        return "\n".join(self.entry(p, long) for p in paths)

    def cd(self, name, args):
        match args:
            case []:
                target = "/"
            case [target]:
                pass
            case _:
                raise ShellError(f"{name}: too many arguments")
        path = self.resolve(name, target)
        if self.vfs.nodes[path].kind != "dir":
            raise ShellError(f"{name}: {target}: not a directory")
        self.cwd = path
        return ""

    def cat(self, name, args):
        if not args:
            raise ShellError(f"{name}: missing operand")
        parts = []
        for arg in args:
            node = self.vfs.nodes[self.resolve(name, arg)]
            if node.kind != "file":
                raise ShellError(f"{name}: {arg}: is a directory")
            parts.append(node.data.decode("utf-8", errors="replace"))
        return "".join(parts).rstrip("\n")

    def chown(self, name, args):
        if not args[1:]:
            raise ShellError(f"{name}: missing operand")
        owner, *paths = args
        targets = [self.resolve(name, path) for path in paths]
        for path in targets:
            self.vfs.nodes[path] = self.vfs.nodes[path]._replace(owner=owner)
        return ""

    def cal(self, name, args):
        try:
            nums = [int(arg) for arg in args]
        except ValueError:
            raise ShellError(f"{name}: invalid argument")
        today = datetime.date.today()
        match nums:
            case []:
                year, month = today.year, today.month
            case [year]:
                month = None
            case [month, year]:
                pass
            case _:
                raise ShellError(f"{name}: too many arguments")
        text = calendar.TextCalendar(calendar.SUNDAY)
        try:
            if month is None:
                return text.formatyear(year).rstrip()
            return text.formatmonth(year, month).rstrip()
        except ValueError as err:
            raise ShellError(f"{name}: {err}")

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
