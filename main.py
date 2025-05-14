import os
import shutil
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

ARCHIVE_DIR = 'archive'
UNPROCESSED_DIR = 'unprocessed'

# Ensure archive and unprocessed directories exist
os.makedirs(ARCHIVE_DIR, exist_ok=True)
os.makedirs(UNPROCESSED_DIR, exist_ok=True)

class PipelineHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            log_action('Ignored', 'Incoming Directory', {'path': event.src_path})
            return
        log_action('Processing', 'Incoming file', {'path': event.src_path})
        self.process_file(event.src_path)

    def process_file(self, file_path):
        def process():
            file = FileProcessor(file_path)
            log_action("ETL", "Started The pipeline", {'filename': file_path})
            time.sleep(10)
            try:
                file.extract()
                if file.validate():
                    file.transform()
                    file.load()
                    log_action("[SUCCESS]", f"Processed {len(file.df)} rows from {file.file_name}")
                    archive_path = os.path.join(ARCHIVE_DIR, '/'.join(file.loading_path.split('/')[1:]))
                    os.makedirs(archive_path, exist_ok=True)
                    shutil.move(file_path, os.path.join(archive_path, file.file_name))
            except Exception as e:
                log_action("[ERROR]", f"Failed to process {file.file_name}: {e}")
                unprocessed_path = os.path.join(UNPROCESSED_DIR, '/'.join(file.loading_path.split('/')[1:]))
                os.makedirs(os.path.dirname(unprocessed_path), exist_ok=True)
                shutil.move(file_path, unprocessed_path)

        thread = threading.Thread(target=process)
        thread.start()

def process_existing_files():
    for file_name in os.listdir('incoming_data'):
        file_path = os.path.join('incoming_data', file_name)
        if os.path.isfile(file_path):
            log_action('Processing', 'Existing file', {'path': file_path})
            PipelineHandler().process_file(file_path)

if __name__ == "__main__":
    # Process existing files in the incoming_data directory
    process_existing_files()

    # Start monitoring for new files
    observer = Observer()
    observer.schedule(PipelineHandler(), path='incoming_data', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print('\nProcess Interrupted!')
    observer.join()
