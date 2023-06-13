import sys
import json
from PyQt5.QtWidgets import QDialog , QFormLayout, QInputDialog ,QComboBox, QMessageBox, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget, QDateEdit, QSpinBox, QDoubleSpinBox
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Giriş")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(400, 200, 300, 150)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Kullanıcı Adı:", self.username)
        form_layout.addRow("Şifre:", self.password)

        self.login_button = QPushButton("Giriş")
        self.login_button.clicked.connect(self.login)

        layout.addLayout(form_layout)
        layout.addWidget(self.login_button)
        self.setLayout(layout)
    def login(self):
        username = self.username.text()
        password = self.password.text()

        if username == "purplonc" and password == "Parhesia19Oy.":
            self.accept()
        else:
            self.username.clear()
            self.password.clear()

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("C:/Users/onc20/OneDrive/Masaüstü/Codes/YZG/python/Musteritakipdeneme/app_icon.ico"))
        

        self.init_ui()
        self.load_data_json()
    def init_ui(self):
        self.setWindowTitle('Purplonc Store')

        layout = QVBoxLayout()

        input_layout = QHBoxLayout()

        self.date_label = QLabel('Tarih:')
        input_layout.addWidget(self.date_label)
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        input_layout.addWidget(self.date_input)

        self.discord_address_label = QLabel('Discord Adresi:')
        input_layout.addWidget(self.discord_address_label)
        self.discord_address_input = QLineEdit()
        input_layout.addWidget(self.discord_address_input)

        self.product_label = QLabel('Server:')
        input_layout.addWidget(self.product_label)
        self.product_input = QComboBox()
        self.product_input.setEditable(True)
        self.product_input.setInsertPolicy(QComboBox.NoInsert)
        input_layout.addWidget(self.product_input)

        self.quantity_label = QLabel('Miktar:')
        input_layout.addWidget(self.quantity_label)
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(99999)
        input_layout.addWidget(self.quantity_input)
        # self.delete_purchase_button = QPushButton('Satın Alma Sil')
        # layout.addWidget(self.delete_purchase_button)
        # self.delete_purchase_button.clicked.connect(lambda: self.delete_data('purchase'))

        # self.delete_sale_button = QPushButton('Satış Sil')
        # layout.addWidget(self.delete_sale_button)
        # self.delete_sale_button.clicked.connect(lambda: self.delete_data('sale'))
        self.remove_button = QPushButton('Seçilen Satırı Sil')
        layout.addWidget(self.remove_button)
        self.remove_button.clicked.connect(self.remove_selected_row)
        # self.add_product_button = QPushButton('Server Ekle')
        # layout.addWidget(self.add_product_button)
        # self.add_product_button.clicked.connect(self.add_product)

        # self.remove_product_button = QPushButton('Server Sil')
        # layout.addWidget(self.remove_product_button)
        # self.remove_product_button.clicked.connect(self.remove_product)

        self.price_label = QLabel('Fiyat:')
        input_layout.addWidget(self.price_label)
        self.price_input = QDoubleSpinBox()
        self.price_input.setMinimum(0.01)
        self.price_input.setMaximum(9999999.99)
        self.price_input.setDecimals(2)
        input_layout.addWidget(self.price_input)

        layout.addLayout(input_layout)
        self.profit_loss_label = QLabel('Kar/Zarar: 0.00')
        layout.addWidget(self.profit_loss_label)

        self.save_purchase_button = QPushButton('Satın Alma Kaydet')
        layout.addWidget(self.save_purchase_button)
        self.save_purchase_button.clicked.connect(lambda: self.save_data('purchase'))
        self.remove_stock_button = QPushButton('Stoktan Ürün Sil')
        layout.addWidget(self.remove_stock_button)
        self.remove_stock_button.clicked.connect(self.remove_product_from_stock)
        self.save_sale_button = QPushButton('Satış Kaydet')
        layout.addWidget(self.save_sale_button)
        self.save_sale_button.clicked.connect(lambda: self.save_data('sale'))


        self.tab_widget = QTabWidget()

        self.purchase_table = self.create_table()
        self.tab_widget.addTab(self.purchase_table, 'Satın Almalar')

        self.sale_table = self.create_table()
        self.tab_widget.addTab(self.sale_table, 'Satışlar')

        self.stock_table = self.create_stock_table()
        self.tab_widget.addTab(self.stock_table, 'Stok Takip')

        self.customer_table = self.create_party_table()
        self.tab_widget.addTab(self.customer_table, 'Müşteriler')

        self.supplier_table = self.create_party_table()
        self.tab_widget.addTab(self.supplier_table, 'Tedarikçiler')

        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['Tarih', 'Discord', 'Server', 'Miktar', 'Fiyat'])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        return table
    def closeEvent(self, event):
        self.save_data_json()
        event.accept()

    def save_data_json(self):
        data = {
            'purchase_table': self.serialize_table(self.purchase_table),
            'sale_table': self.serialize_table(self.sale_table),
            'stock_table': self.serialize_table(self.stock_table),
            'customer_table': self.serialize_table(self.customer_table),
            'supplier_table': self.serialize_table(self.supplier_table)
        }
        with open("data.json", "w") as f:
            json.dump(data, f)

    def load_data_json(self):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                self.deserialize_table(self.purchase_table, data["purchase_table"])
                self.deserialize_table(self.sale_table, data["sale_table"])
                self.deserialize_table(self.stock_table, data["stock_table"])
                self.deserialize_table(self.customer_table, data["customer_table"])
                self.deserialize_table(self.supplier_table, data["supplier_table"])
        except FileNotFoundError:
            pass
          


    def create_stock_table(self):
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(['Server', 'Miktar', 'Toplam Fiyat', 'Avg.Buy', 'Avg.Sell', 'Total Sales'])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        return table
    
    def calculate_profit_loss(self):
        purchase_table = self.purchase_table
        sale_table = self.sale_table

        total_purchase_cost = 0
        total_sales_revenue = 0

        for row in range(purchase_table.rowCount()):
            quantity = int(purchase_table.item(row, 3).text())
            price = float(purchase_table.item(row, 4).text())
            total_purchase_cost += quantity * price

        for row in range(sale_table.rowCount()):
            quantity = int(sale_table.item(row, 3).text())
            price = float(sale_table.item(row, 4).text())
            total_sales_revenue += quantity * price

        profit_loss = total_sales_revenue - total_purchase_cost
        result_text = f"Kar: {profit_loss:.2f}" if profit_loss >= 0 else f"Zarar: {abs(profit_loss):.2f}"
        self.profit_loss_label.setText(f"Kar/Zarar: {result_text}")
    def serialize_table(self, table):
        rows = table.rowCount()
        cols = table.columnCount()
        data = []

        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = table.item(row, col)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)

        return data
    def delete_data(self, category):
        if category == 'purchase':
            table = self.purchase_table
        else:
            table = self.sale_table

        selected_rows = sorted(set(index.row() for index in table.selectedIndexes()))
        
        if not selected_rows:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek istediğiniz satırı seçin.")
            return

        for row in reversed(selected_rows):
            product = table.item(row, 2).text()
            quantity = int(table.item(row, 3).text())
            price = float(table.item(row, 4).text())

            if category == 'purchase':
                new_category = 'sale'
            else:
                new_category = 'purchase'

            self.update_stock_table(product, quantity, price, new_category)
            table.removeRow(row)

        self.calculate_profit_loss()

    def deserialize_table(self, table, data):
        for row_data in data:
            row = table.rowCount()
            table.setRowCount(row + 1)
            for col, text in enumerate(row_data):
                table.setItem(row, col, QTableWidgetItem(text))

    def save_data(self, category):
        date = self.date_input.date().toString("yyyy-MM-dd")
        discord_address = self.discord_address_input.text()
        product = self.product_input.currentText()  # Değişiklik burada
        quantity = self.quantity_input.value()
        price = self.price_input.value()
        transaction_data = {
         "date": date,
         "product": product,
         "quantity": quantity,
         "price": price
        }

        if date and discord_address and product and quantity and price:
            if category == 'purchase':
                table = self.purchase_table
                party_table = self.supplier_table
            else:
                table = self.sale_table
                party_table = self.customer_table

            row = table.rowCount()
            table.setRowCount(row + 1)

            table.setItem(row, 0, QTableWidgetItem(date))
            table.setItem(row, 1, QTableWidgetItem(discord_address))
            table.setItem(row, 2, QTableWidgetItem(product))
            table.setItem(row, 3, QTableWidgetItem(str(quantity)))
            table.setItem(row, 4, QTableWidgetItem(f"{price:.2f}"))

            self.update_stock_table(product, quantity, price, category)
            transaction_data = {
            "date": date,
            "product": product,
            "quantity": quantity,
            "price": price 
             }
            self.update_party_table(discord_address, party_table, transaction_data, category)


            self.discord_address_input.clear()
            self.product_input.clear()
            self.quantity_input.setValue(1)
            self.price_input.setValue(0.01)
            self.calculate_profit_loss()
    def update_party_table(self, discord_address, table, transaction_data, category):
        row_count = table.rowCount()

        for row in range(row_count):
            if table.item(row, 0).text() == discord_address:
             current_details = table.item(row, 1).text()
             new_details = self.get_updated_details(current_details, transaction_data, category)
             table.setItem(row, 1, QTableWidgetItem(new_details))
             break
        else:
            table.setRowCount(row_count + 1)
            table.setItem(row_count, 0, QTableWidgetItem(discord_address))
            initial_details = self.get_initial_details(transaction_data, category)
            table.setItem(row_count, 1, QTableWidgetItem(initial_details))
            
    def get_initial_details(self, transaction_data, category):
        initial_details = f"{transaction_data['product']}"
        return initial_details

    def get_updated_details(self, current_details, transaction_data, category):
        updated_details = f"{current_details}, {transaction_data['product']}"
        return updated_details
    
    def add_product(self):
        product = self.product_input.currentText()
        if product:
            if product not in [self.product_input.itemText(i) for i in range(self.product_input.count())]:
                self.product_input.addItem(product)
            else:
                QMessageBox.warning(self, "Uyarı", "Bu Server zaten listede mevcut.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen geçerli bir Server adı girin.")

    def remove_product(self):
        product = self.product_input.currentText()
        if product:
            index = self.product_input.findText(product)
            if index >= 0:
                self.product_input.removeItem(index)
            else:
                QMessageBox.warning(self, "Uyarı", "Bu Server listede bulunamadı.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen geçerli bir Server adı girin.")
    def remove_selected_row(self):
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:
            table = self.purchase_table
        elif current_tab == 1:
            table = self.sale_table
        else:
            return

        row = table.currentRow()
        if row >= 0:
            # Eğer satış tablosunda satır siliyorsanız stoktan ürün silme işlemini de yapın
            if current_tab == 1:
                product_name = table.item(row, 0).text()
                quantity = int(table.item(row, 1).text())
                self.remove_from_stock(product_name, quantity)

            table.removeRow(row)
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek istediğiniz satırı seçin.")
    # def remove_from_stock(self, product_name, quantity):
    #     # Stoktan ürün silme işlemini burada gerçekleştirin
    #     found = False
    #     for row in range(self.stock_table.rowCount()):
    #         if self.stock_table.item(row, 0).text() == product_name:
    #             found = True
    #             current_quantity = int(self.stock_table.item(row, 1).text())
    #             new_quantity = current_quantity - quantity

    #             if new_quantity < 0:
    #                 QMessageBox.warning(self, "Uyarı", "Stok miktarı yetersiz.")
    #             else:
    #                 self.stock_table.setItem(row, 1, QTableWidgetItem(str(new_quantity)))

    #     if not found:
    #         QMessageBox.warning(self, "Uyarı", f"{product_name} adında ürün stokta bulunamadı.")
    def remove_product_from_stock(self):
        product_name, ok1 = QInputDialog.getText(self, "Ürün Adı", "Silinecek ürünün adını girin:")
        if ok1:
            quantity, ok2 = QInputDialog.getInt(self, "Miktar", "Silinecek ürünün miktarını girin:")
            if ok2:
                self.remove_from_stock(product_name, quantity)
            else:
                QMessageBox.warning(self, "Uyarı", "Geçerli bir miktar girin.")
        else:
            QMessageBox.warning(self, "Uyarı", "Geçerli bir ürün adı girin.")

    def get_total_sales(self, product):
        table = self.sale_table
        row_count = table.rowCount()
        total_sales = 0
        total_sales_value = 0
        for row in range(row_count):
            if table.item(row, 2).text() == product:
                quantity = int(table.item(row, 3).text())
                price = float(table.item(row, 4).text())
                total_sales += quantity
                total_sales_value += quantity * price

        return total_sales, total_sales_value
    
    def update_stock_table(self, product, quantity, price, category):
        total_sales, total_sales_value = self.get_total_sales(product)
        table = self.stock_table
        row_count = table.rowCount()

        for row in range(row_count):
            if table.item(row, 0).text() == product:
                current_quantity = int(table.item(row, 1).text())
                current_total_price = float(table.item(row, 2).text())

                if category == 'purchase':
                    new_quantity = current_quantity + quantity
                    new_total_price = current_total_price + (quantity * price)
                    avg_purchase_price = new_total_price / new_quantity
                    avg_sale_price = float(table.item(row, 4).text()) if table.item(row, 4) else 0.00

                else:
                    new_quantity = current_quantity - quantity
                    new_total_price = current_total_price - (quantity * price)
                    avg_purchase_price = float(table.item(row, 3).text())
                    total_sales_value += quantity * price
                    avg_sale_price = total_sales_value / total_sales if total_sales > 0 else 0.00

                table.setItem(row, 1, QTableWidgetItem(str(new_quantity)))
                table.setItem(row, 2, QTableWidgetItem(f"{new_total_price:.2f}"))
                table.setItem(row, 3, QTableWidgetItem(f"{avg_purchase_price:.2f}"))
                table.setItem(row, 4, QTableWidgetItem(f"{avg_sale_price:.2f}"))
                table.setItem(row, 5, QTableWidgetItem(str(total_sales)))
                break

        else:
            if category == 'purchase':
                table.setRowCount(row_count + 1)
                table.setItem(row_count, 0, QTableWidgetItem(product))
                table.setItem(row_count, 1, QTableWidgetItem(str(quantity)))
                table.setItem(row_count, 2, QTableWidgetItem(f"{quantity * price:.2f}"))
                table.setItem(row_count, 3, QTableWidgetItem(f"{price:.2f}"))
                table.setItem(row_count, 4, QTableWidgetItem("0.00"))


    def create_party_table(self):
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['Discord Adresi', 'Detaylar'])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        return table
    

    # Diğer fonksiyonlar burada devam ediyor

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = App()
    main_window.show()
    sys.exit(app.exec_())

