from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y') 
    except Exception as e:
        print(f"Ошибка при преобразовании даты: {e}")
        return None