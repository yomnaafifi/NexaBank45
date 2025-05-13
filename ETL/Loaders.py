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
    def __init__(self, dataframe: pd.DataFrame, loading_path:str, file_name:str):
        self.dataframe = dataframe
        self.loading_path = loading_path
        self.file_name = file_name
        self.full_path = os.path.join(self.loading_path, self.file_name) 

    @abstractmethod
    def load(self) -> bool:
        pass

class LocalLoader(BaseLoader):
    """Load dataframe to local file system using parquet writer"""
    def load(self) -> bool:
        try:
            writer = LocalParquetWriter(self.dataframe, self.full_path)
            writer.write()
            return True
        except Exception as e:
            print(f"[ERROR] Failed to load to local: {e}")
            return False


class HdfsLoader(BaseLoader):
    """Load dataframe to HDFS using parquet writer"""
    def load(self) -> bool:
        try:
            LocalLoader(self.dataframe, "tmp", self.file_name).load()

            subprocess.run(["hdfs", "dfs", "-mkdir", "-p", self.loading_path], check=True)
            subprocess.run(["hdfs", "dfs", "-put", "-f", self.full_path, self.loading_path], check=True)

            os.remove(self.full_path)
            return True
        
        except Exception as e:
            print(f"[ERROR] Failed to load to HDFS: {e}")
            return False
