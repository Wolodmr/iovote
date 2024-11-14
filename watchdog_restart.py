import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class RestartServerHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py") or event.src_path.endswith(".html"):
            print(f"Change detected in {event.src_path}, restarting server...")
            subprocess.run(["daphne", "library_voting.asgi:application"])

if __name__ == "__main__":
    path = "."  # Directory to watch, typically the project directory
    event_handler = RestartServerHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()
    print("Watching for changes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
