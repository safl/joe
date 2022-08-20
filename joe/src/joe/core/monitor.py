import re
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Handler(FileSystemEventHandler):
    """Monitor workflow for creation of 'cmd*.output files"""

    def __init__(self, cmdlogs, match="cmd\d+\.output", do_print=True):
        self.cmdlogs = cmdlogs
        self.match = match
        self.do_print = do_print

    def on_created(self, event):

        path = Path(event.src_path).resolve()
        if path.is_dir() or not re.match(self.match, str(path.name)):
            return

        self.cmdlogs.append(path)
        if self.do_print:
            print(f"{path}")


class WorkflowMonitor(object):
    def __init__(self, path):
        self.path = path
        self.cmdlogs = []
        self.handler = Handler(self.cmdlogs, "cmd")
        self.observer = Observer()

    def latest_cmdlog(self):
        """Returns the last created 'cmd*.output' file; if any."""

        if not self.cmdlogs:
            return None

        return self.cmdlogs[-1]

    def start(self):
        self.observer.schedule(self.handler, self.path, recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
