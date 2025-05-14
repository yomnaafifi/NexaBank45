import time
import traceback
from ETL.Extractors import *
from ETL.Transformer import *
from ETL.Loaders import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.logger import setup_logger
from utils.logger import log_action
from utils.FileProcessor import FileProcessor
setup_logger()

class PipelineHandler(FileSystemEventHandler):
    def on_created(self, event):
        print('hi ya big data')

        print(event.src_path.split('/')[0])

        if event.is_directory:
            return

        file = FileProcessor(event.src_path)

        log_action("ETL","Started The pipline",{'filename':event.src_path})
        try:
            file.extract()
            if file.validate():
                file.transform()
                file.load()
                print(f"[SUCCESS] Processed {len(file.df)} rows from {file.file_name}")
        except Exception as e:
            print(f"[ERROR] Failed to process {file.file_name}: {e}")
            traceback.print_exc()


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
