import pandas as pd
import BaseExtractor
class JSONExtractor(BaseExtractor):
    def __init__(self, file: str):
        super.__init__(file)

    def extract(self, source):
        """
        Extract data from a JSON file using pandas.
        """
        data = pd.read_json(source)
        return data
