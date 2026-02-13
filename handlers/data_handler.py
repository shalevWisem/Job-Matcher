import pandas as pd
import os

class ExcelHandler:
    """
    A class to handle Excel file operations including reading, filtering columns, and filtering rows.
    """

    def __init__(self, file_path, header_row=7):
        """
        Initialize the ExcelHandler with a file path.

        Args:
            file_path (str): Path to the .xlsx file
            header_row (int): Row index where column names are located (default: 6 for row 7)
        """
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # If file_path is relative, make it relative to the script location
        if not os.path.isabs(file_path):
            self.file_path = os.path.join(current_dir, file_path)
        else:
            self.file_path = file_path
        self.header_row = header_row
        self.df = None

    def read_file(self):
        """
        Read the Excel file starting from the specified header row.

        Returns:
            pd.DataFrame: DataFrame containing the Excel data
        """
        self.df = pd.read_excel(self.file_path, header=self.header_row)
        print(self.df.columns.tolist())
        return self.df

    def filter_columns(self, column_names):
        """
        Filter DataFrame to include only specified columns.

        Args:
            column_names (list): List of column names to keep

        Returns:
            pd.DataFrame: DataFrame with only the specified columns
        """
        if self.df is None:
            raise ValueError("Please read the file first using read_file()")

        # Filter to only existing columns
        existing_cols = [col for col in column_names if col in self.df.columns]


        if len(existing_cols) < len(column_names):
            missing = [col for col in column_names if col not in self.df.columns]
            print(f"Missing columns: {missing}")

        self.df = self.df[existing_cols]
        return self.df

    def filter_rows_by_strings(self, search_strings):
        """
        Filter DataFrame to include only rows that contain at least one of the search strings in any column.

        Args:
            df (pd.DataFrame): The DataFrame to filter
            search_strings (list): List of strings to search for

        Returns:
            pd.DataFrame: DataFrame with only matching rows
        """
        # Create a boolean mask - starts as all False
        mask = pd.Series([False] * len(self.df))

        # For each search string, check all columns
        for search_str in search_strings:
            # Check each column for the search string
            for col in self.df.columns:
                # Convert column to string and check if search_str is in any cell
                mask |= self.df[col].astype(str).str.contains(search_str, case=False, na=False)

        filtered_df = self.df[mask]

        print(f"Search strings: {search_strings}")
        print(f"Rows found: {len(filtered_df)} out of {len(self.df)}")

        return filtered_df

    def get_dataframe(self):
        """
        Get the current DataFrame.

        Returns:
            pd.DataFrame: Current DataFrame
        """
        return self.df

    def reset(self):
        """
        Reset the DataFrame to the original data from the file.

        Returns:
            pd.DataFrame: Original DataFrame
        """
        return self.read_file()

    def save_to_excel(self, output_path):
        """
        Save the current DataFrame to an Excel file.

        Args:
            output_path (str): Path where to save the file
        """
        if self.df is None:
            raise ValueError("No data to save. Please read the file first.")

        self.df.to_excel(output_path, index=False)
