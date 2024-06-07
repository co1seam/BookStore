from modules.order_manager import *
from utils.date_utils import parse_date

def main():
    validator = DataValidator()
    order_manager = OrderManager(validator)

    buyer_pup = order_manager.load_data('Buyer_pup.txt')
    order_list = order_manager.load_data('Список заказов.txt')
    current_pup = order_manager.load_data('current PUP.txt')
    new_orders = order_manager.load_data('Заказы новые.txt')

    date_input = input("Введите дату в формате 'дд/мм/гггг': ")
    date1 = datetime.strptime(date_input, '%d/%m/%Y')

    distributed_orders = order_manager.distribute_orders(new_orders, buyer_pup, date1)

    updated_orders = order_manager.update_orders_table(order_list, date1)

    order_manager.save_to_excel(distributed_orders, 'Book 1.xlsx')
    order_manager.save_to_excel(updated_orders, 'Список заказов.txt')


if __name__ == "__main__":
    main()