from abc import ABC, abstractmethod
import pandas as pd
import subprocess
import os

class BaseWriter(ABC):
    def __init__(self, dataframe: pd.DataFrame, local_path: str):
        self.dataframe = dataframe
        self.local_path = local_path

    @abstractmethod
    def write(self) -> str:
        """Write the dataframe to a destination and return the path written."""
        pass


class LocalParquetWriter(BaseWriter):
    """transform dataframe into parquet file and save it locally"""
    def write(self) -> str:
        self.dataframe.to_parquet(self.local_path, index=False)
        return self.local_path


class BaseLoader(ABC):
    """Base class for loaders that handle the loading of dataframes to different destinations."""
    def __init__(self, dataframe: pd.DataFrame, local_path: str, loading_path: str):
        self.dataframe = dataframe
        self.local_path = local_path
        self.loading_path = loading_path

    @abstractmethod
    def load(self) -> bool:
        pass


class HdfsLoader(BaseLoader):
    """Load dataframe to HDFS using parquet writer"""
    def load(self) -> bool:
        try:
            writer = LocalParquetWriter(self.dataframe, self.local_path)
            local_file = writer.write()

            subprocess.run(["hdfs", "dfs", "-mkdir", "-p", os.path.dirname(self.loading_path)], check=True)
            subprocess.run(["hdfs", "dfs", "-put", "-f", local_file, self.loading_path], check=True)

            os.remove(local_file)
            return True
        
        except Exception as e:
            print(f"[ERROR] Failed to load to HDFS: {e}")
            return False
