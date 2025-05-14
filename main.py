import time
import threading
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

        if event.is_directory:
            log_action('Incoming','Ignored Directory' ,{'path':event.src_path})
            return
        log_action('Incoming','File' ,{'path':event.src_path})


        
        def process_file():
            file = FileProcessor(event.src_path)
            log_action("ETL","Started The pipline",{'filename':event.src_path})
            try:
                file.extract()
                if file.validate():
                    file.transform()
                    file.load()
                    log_action("[SUCCESS]", f"Processed {len(file.df)} rows from {file.file_name}")

            except Exception as e:
                log_action("[ERROR]", f"Failed to process {file.file_name} in : {e}")
        
        thread = threading.Thread(target=process_file)
        thread.start()


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
