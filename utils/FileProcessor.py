import os
import glob
import traceback
from datetime import datetime
from ETL.Extractors import *
from ETL.Transformer import *
from ETL.Loaders import *
from utils.SchemaRegistry import *

class FileProcessor:
    def __init__(self, incoming_dir: str):
        self.incoming_dir = incoming_dir

    def process_files(self):
        files = glob.glob(f"{self.incoming_dir}/**/*", recursive=True)

        for file_path in files:
            if not os.path.isfile(file_path):
                continue

            file_name = os.path.basename(file_path)
            name_without_ext, ext = os.path.splitext(file_name)

            extractor_cls = EXTRACTOR_REGISTRY.get(ext.lower())
            transformer_cls = TRANSFORMER_REGISTRY.get(name_without_ext.lower())

            if not extractor_cls or not transformer_cls:
                print(f"[SKIPPED] No handler for: {file_path}")
                continue

            print(f"[INFO] Processing file: {file_path}")
            try:
                extractor = extractor_cls(file_path)
                df = extractor.extract()

                transformer = transformer_cls(df)
                transformed_df = transformer.transform()

                # load the dataframe
                loader = LocalLoader(transformed_df, "tmp", name_without_ext)
                loader.load()
                
                print(f"[SUCCESS] Processed {len(transformed_df)} rows from {file_name}")


            except Exception as e:
                print(f"[ERROR] Failed to process {file_name}: {e}")
                traceback.print_exc()
