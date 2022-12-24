import requests
import pandas as pd

class ScriptData:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.data = {}

    def fetch_intraday_data(self, script: str):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={script}&interval=5min&apikey={self.api_key}"
        response = requests.get(url)
        data = response.json()
        self.data[script] = data

    def convert_intraday_data(self, script: str):
        data = self.data[script]["Time Series (5min)"]
        df = pd.DataFrame.from_dict(data, orient="index", columns=["open", "high", "low", "close", "volume"])
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        self.data[script] = df

    def __getitem__(self, script: str):
        return self.data[script]

    def __setitem__(self, script: str, value):
        self.data[script] = value

    def __contains__(self, script: str):
        return script in self.data