import pandas as pd
from datetime import datetime

class DataValidator:
    def __init__(self):
        pass

    def validate_file_format(self, file_path, expected_extension):
        if not file_path.endswith(expected_extension):
            raise ValueError(f"Файл {file_path} не имеет ожидаемого расширения {expected_extension}.")
    
    def validate_column_headers(self, data, expected_headers):
        missing_columns = set(expected_headers) - set(data.columns)
        if missing_columns:
            raise ValueError(f"В данных отсутствуют ожидаемые столбцы: {missing_columns}.")
    
    def validate_date_format(self, date_str, date_format='%d/%m/%Y'):
        try:
            datetime.strptime(date_str, date_format)
        except ValueError:
            raise ValueError(f"Дата {date_str} не соответствует формату {date_format}.")
    
    def validate_unique_values(self, data, column):
        if data[column].duplicated().any():
            raise ValueError(f"В столбце {column} обнаружены дублирующиеся значения.")

    def validate_positive_values(self, data, column):
        if(data[column] < 0).any():
            raise ValueError(f"В столбце {column} обнаружены отрицательные значения.")

    def validate_missing_values(self, data, column):
        if data[column].isnull().any():
            raise ValueError(f"В столбце {column} обнаружены пропущенные значения.")        

