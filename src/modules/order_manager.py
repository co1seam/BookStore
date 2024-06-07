import pandas as pd
from datetime import datetime, timedelta
from modules.data_validator import DataValidator

class OrderManager:
    def __init__(self, validator):
        self.validator = validator
    
    def load_data(self, file_path, file_type = 'txt'):
        if file_path == 'txt':
            self.validator.validate_file_format(file_path, '.txt')
            data = pd.read_csv(file_path, sep='\t', encoding='utf-8')
        elif file_type == 'xlsx':
            self.validator.validate_file_format(file_path, '.xlsx')
            data = pd.read_excel(file_path)
        else:
            raise ValueError("Неподдерживаемый формат файла. Допустимые типы: 'txt', 'xlsx'")
        self.validator.validate_column_headers(data, ['ID товара', 'Дата совершения заказа', 'Value'])
        self.validator.validate_data_types(data, {'ID товара': int, 'Дата совершения заказа': str, 'Value': float})
        self.validator.validate_unique_values(data, 'ID товара')
        self.validator.validate_positive_values(data, 'Value')
        self.validator.validate_missing_values(data, 'Дата совершения заказа')

        return data

    def distribute_orders(self, orders, buyers, date1):
        distributed_orders = orders.copy()

        orders_to_distribute = distributed_orders[distributed_orders['Дата совершения заказа'] == date1.strftime('%d/%m/%Y')]

        results = pd.DataFrame(columns=orders.columns)

        buyer_order_counts = {buyer_id: 0 for buyer_id in buyers['ID Buyer'].unique()}

        for index, order in orders_to_distribute.iterrows():
            ordered_product_ids = results['ID товара'].unique()

            date_21_days_ago = date1 - timedelta(days=21)

            eligible_buyers = buyers[~buyers['ID Buyer'].isin(
                orders[(orders['ID товара'] == order['ID товара']) &
                    (orders['Дата завершения заказа'] >= date_21_days_ago.strftime('%d/%m/%Y')) &
                    (orders['Дата завершения заказа'] < date1.strftime('%d/%m/%Y'))]['ID Buyer']
            )]

            if not eligible_buyers.empty():
                unique_pup_orders = results.drop_duplicate(subset=['ID товара', 'ID pick-up point'])
                unique_pup_buyers = eligible_buyers[~eligible_buyers['ID pick-up point'].isin(unique_pup_orders['ID pick-ip point'])]

                if not unique_pup_buyers.empty:
                    unique_pup_buyers['order_count'] = unique_pup_buyers['ID Buyer'].map(buyer_order_counts)
                    buyer = unique_pup_buyers.loc[eligible_buyers['order_count'].idxmin()]
                else:
                    eligible_buyers['order_count'] = eligible_buyers['ID Buyer'].map(buyer_order_counts)
                    buyer = eligible_buyers.loc[eligible_buyers['order_count'].idxmin()]
            else:
                buyers['order_count'] = buyers['ID Buyer'].map(buyer_order_counts)
                buyer = buyers.loc[buyers['order_count'].idxmin()]
            
            order['ID Buyer'] = buyer['ID Buyer']
            order['Name Buyer'] = buyer['Name Buyer']

            buyer_order_counts[buyer['ID Buyer']] += 1

            results = results.append(order)
        return results


    def update_orders_date(self, orders, date1):
        str_date = date1.strftime('%d/%m/%Y')
        self.validator.validate_date_format(str_date)
        update_orders = orders[orders['Дата совершения заказа'] != str_date]
        return update_orders

    def save_to_excel(data, file_path):
        try:
            data.to_excel(file_path, index=False)
            print(f"Данные успешно сохранены в файл по пути: '{file_path}'.")
        except Exception as e:
            print(f"Ошибка при сохранение данных в файл '{file_path}': {e}")