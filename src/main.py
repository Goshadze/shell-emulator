import argparse

from gui import App

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs", help="path to VFS file")
    parser.add_argument("--script", help="path to startup script")
    App(parser.parse_args()).mainloop()
