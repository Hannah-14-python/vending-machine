class VendingMachine:
    def __init__(self):
        self.menu = {
            'Hot Drinks': {
                '1': {'item': 'Espresso', 'price': 1.50, 'stock': 10},
                '2': {'item': 'Cappuccino', 'price': 2.00, 'stock': 8},
                '3': {'item': 'Latte', 'price': 2.50, 'stock': 6},
            },
            'Snacks': {
                '4': {'item': 'Biscuits', 'price': 1.20, 'stock': 15},
                '5': {'item': 'Chocolate Bar', 'price': 1.00, 'stock': 12},
                '6': {'item': 'Cookies', 'price': 1.50, 'stock': 10},
            },
            'Baked Goods': {
                '7': {'item': 'Croissant', 'price': 1.80, 'stock': 8},
                '8': {'item': 'Bagel with Cream Cheese', 'price': 2.00, 'stock': 10},
                '9': {'item': 'Assorted Muffins', 'price': 1.50, 'stock': 12},
            },
        }
        self.wallet_limit = 20.0  # Limit the amount of money a user can have in their wallet
        self.user_balance = 0.0
        self.current_order = []
        self.purchase_history = []

    def display_menu(self):
        print("\n=== Vending Machine Menu ===")
        for category, products in self.menu.items():
            print(f"\n{category}:")
            for code, product in products.items():
                print(f"{code}: {product['item']} - ${product['price']:.2f} - Stock: {product['stock']}")
        print("===========================")

    def get_user_input(self):
        return input("Enter the code of the item you want to add (or 'F' to finish): ").upper()

    def accept_money(self):
        try:
            amount = float(input("Insert money: $"))
            if self.user_balance + amount <= self.wallet_limit:
                self.user_balance += amount
            else:
                print(f"Wallet limit reached. You cannot insert more than ${self.wallet_limit - self.user_balance:.2f}.")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

    def add_to_order(self, code):
        found = False
        for category, products in self.menu.items():
            if code in products:
                found = True
                if products[code]['stock'] > 0 and self.user_balance >= products[code]['price']:
                    self.current_order.append(products[code])
                    print(f"{products[code]['item']} added to your order.")
                    self.update_purchase_history(products[code]['item'])
                    self.update_stock(products[code], 1)
                    self.user_balance -= products[code]['price']
                elif products[code]['stock'] == 0:
                    print(f"Sorry, {products[code]['item']} is out of stock.")
                else:
                    print("Insufficient funds. Please insert more money or choose a cheaper item.")
                break

        if not found:
            print("Invalid code. Please enter a valid code.")

    def update_stock(self, product, quantity):
        product['stock'] -= quantity

    def update_purchase_history(self, item):
        self.purchase_history.append(item)

    def suggest_purchase(self):
        if len(self.purchase_history) >= 2:
            last_purchase = self.purchase_history[-1]
            second_last_purchase = self.purchase_history[-2]

            # Dynamic suggestion based on the user's purchase history
            if last_purchase in ['Espresso', 'Cappuccino', 'Latte'] and second_last_purchase in ['Biscuits', 'Cookies']:
                print(f"\nHow about trying our {self.get_complementary_snack(last_purchase)} to go with your {last_purchase.lower()}?")
            elif last_purchase in ['Biscuits', 'Cookies'] and second_last_purchase in ['Espresso', 'Cappuccino', 'Latte']:
                print(f"\nEnjoy your {last_purchase.lower()}! You might also like our {self.get_complementary_hot_drink(last_purchase)}.")

    def get_complementary_snack(self, hot_drink):
        # Returns a complementary snack based on the type of hot drink purchased
        if hot_drink.lower() == 'espresso':
            return 'Biscuits'
        elif hot_drink.lower() == 'cappuccino':
            return 'Cookies'
        elif hot_drink.lower() == 'latte':
            return 'Chocolate Bar'

    def get_complementary_hot_drink(self, snack):
        # Returns a complementary hot drink based on the type of snack purchased
        if snack.lower() == 'biscuits':
            return 'Espresso'
        elif snack.lower() == 'cookies':
            return 'Cappuccino'
        elif snack.lower() == 'chocolate bar':
            return 'Latte'

    def view_current_order(self):
        if self.current_order:
            print("\n=== Current Order ===")
            for product in self.current_order:
                print(f"{product['item']} - ${product['price']:.2f}")
            print("=====================")
        else:
            print("Your order is empty.")

    def return_change(self):
        print(f"\nTotal cost of your order: ${sum(item['price'] for item in self.current_order):.2f}")
        print(f"Change returned: ${self.user_balance:.2f}")

    def run(self):
        while True:
            self.display_menu()
            selected_code = self.get_user_input()

            if selected_code == 'F':
                break

            if selected_code == 'V':
                self.view_current_order()
                continue

            self.accept_money()
            self.add_to_order(selected_code)
            self.suggest_purchase()

        self.view_current_order()
        self.return_change()


# Main Program
if __name__ == "__main__":
    vending_machine = VendingMachine()
    vending_machine.run()
