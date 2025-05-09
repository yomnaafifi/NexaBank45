import pandas as pd
import BaseExtractor
class TextExtractor(BaseExtractor):
    def __init__(self, file: str):
        super.__init__(file)

    def extract(self, source):
        """
        Extract data from a plain text file using pandas.
        """
        data = pd.read_csv(source, header=None, names=["line"], sep="\n")
        return data["line"].tolist()
