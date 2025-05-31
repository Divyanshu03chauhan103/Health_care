import pandas as pd

class CSVReaderTool:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.name = "csv_reader_tool"
        self.description = "A tool to read and process CSV files."

    def read_csv(self):
        """Read the CSV file and return a DataFrame."""
        try:
            df = pd.read_csv(self.csv_path)
            return df
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None

    def get_column_names(self):
        """Get the column names of the CSV file."""
        df = self.read_csv()
        if df is not None:
            return list(df.columns)
        return []

    def filter_data(self, column_name, value):
        """Filter the CSV data based on a column and value."""
        df = self.read_csv()
        if df is not None:
            return df[df[column_name] == value]
        return None

    def __call__(self, query):
        """Make the tool callable. This is the function that will be invoked by the agent."""
        # Example: Return column names for now
        return self.get_column_names()

    # Add a 'func' attribute to make the tool compatible with the Agent class
    @property
    def func(self):
        return self.__call__