import subprocess
import os
import pandas as pd
from Loaders.BaseLoader import BaseLoader
class HdfsLoader(BaseLoader):
    def load(self, dataframe, table_name, hdfs_path):
        """
        Save the given DataFrame to the specified HDFS path in Parquet format.
        """
        local_parquet_path = f"/tmp/{table_name}.parquet"
        dataframe.df.to_parquet(local_parquet_path, index=False)


        subprocess.run(["hdfs", "dfs", "-mkdir", "-p", os.path.dirname(hdfs_path)], check=True)
        subprocess.run(["hdfs", "dfs", "-put", "-f", local_parquet_path, hdfs_path], check=True)

        os.remove(local_parquet_path)
