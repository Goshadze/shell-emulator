import tkinter as tk

from shell import ShellError, ShellExit, execute

VFS_NAME = "vfs"
PROMPT = "$ "


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"Shell Emulator - [{VFS_NAME}]")
        self.output = tk.Text(self, state="disabled", height=24, width=80)
        self.output.tag_config("error", foreground="red")
        self.output.pack(fill="both", expand=True)
        self.entry = tk.Entry(self)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

    def print(self, text, tag=None):
        self.output.config(state="normal")
        self.output.insert("end", text + "\n", tag)
        self.output.config(state="disabled")
        self.output.see("end")

    def on_enter(self, _event):
        line = self.entry.get()
        self.entry.delete(0, "end")
        self.print(PROMPT + line)
        try:
            result = execute(line)
        except ShellExit:
            self.destroy()
            return
        except ShellError as err:
            self.print(str(err), "error")
            return
        if result:
            self.print(result)
