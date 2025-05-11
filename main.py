import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PipelineHandler(FileSystemEventHandler):
    def on_created(self, event):
        print('hi ya big data')


if __name__ == "__main__":
    observer = Observer()
    observer.schedule(PipelineHandler(), path='incoming_data', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print('\n process Interrupted!')
    observer.join()
