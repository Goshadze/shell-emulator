import tkinter as tk

from shell import Shell, ShellError, ShellExit
from vfs import Vfs, load

PROMPT = "$ "


class App(tk.Tk):
    def __init__(self, args):
        super().__init__()
        self.output = tk.Text(self, state="disabled", height=24, width=80)
        self.output.tag_config("error", foreground="red")
        self.output.pack(fill="both", expand=True)
        self.entry = tk.Entry(self)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()
        for name, value in vars(args).items():
            self.print(f"[debug] {name}={value}")
        self.shell = Shell(self.load_vfs(args.vfs))
        self.title(f"Shell Emulator - [{self.shell.vfs.name}]")
        if args.script:
            self.after(100, self.run_script, args.script)

    def print(self, text, tag=None):
        self.output.config(state="normal")
        self.output.insert("end", text + "\n", tag)
        self.output.config(state="disabled")
        self.output.see("end")

    def load_vfs(self, path):
        if path is None:
            return Vfs()
        try:
            return load(path)
        except ShellError as err:
            self.print(str(err), "error")
            return Vfs()

    def run(self, line):
        self.print(PROMPT + line)
        try:
            result = self.shell.execute(line)
        except ShellError as err:
            self.print(str(err), "error")
            return False
        if result:
            self.print(result)
        return True

    def on_enter(self, _event):
        line = self.entry.get()
        self.entry.delete(0, "end")
        try:
            self.run(line)
        except ShellExit:
            self.destroy()

    def run_script(self, path):
        try:
            with open(path, encoding="utf-8") as file:
                lines = file.read().splitlines()
            for number, line in enumerate(lines, 1):
                if line.strip() and not self.run(line):
                    self.print(f"script: error at line {number}", "error")
                    return
        except (OSError, ValueError) as err:
            self.print(f"script: {err}", "error")
        except ShellExit:
            self.destroy()
