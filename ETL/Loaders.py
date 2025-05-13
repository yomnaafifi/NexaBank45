from abc import ABC, abstractmethod
import pandas as pd
import subprocess
import os
import pandas as pd

class BaseLoader(ABC):
    def __init__(self, data: pd.DataFrame):
        """
        Constructor to initialize the BaseLoader with a data attribute.

        Args:
            data (pandas.DataFrame): The data to be loaded, represented as a pandas DataFrame.
        """
        self.data = data

    @abstractmethod
    def load(self) -> bool:
        """
        Abstract method to load the data to be implemented by subclasses.

        Returns:
            bool: True if the data is successfully loaded, False otherwise.
        """
        pass


class HdfsLoader(BaseLoader):

    def load(self, dataframe, file_name, hdfs_path):
        """
        Save the given DataFrame to the specified HDFS path in Parquet format.
        """
        local_parquet_path = f"/tmp/{file_name}.parquet"
        dataframe.df.to_parquet(local_parquet_path, index=False)


        subprocess.run(["hdfs", "dfs", "-mkdir", "-p", os.path.dirname(hdfs_path)], check=True)
        subprocess.run(["hdfs", "dfs", "-put", "-f", local_parquet_path, hdfs_path], check=True)

        os.remove(local_parquet_path)
