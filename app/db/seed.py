
import sys
from app.config.dependencies import get_db
from app.models.product import Product
from app.models.inventory import Inventory
from faker import Faker

def seed_data():
    db = next(get_db())

    if db.query(Product).first():
        print("Data already exists, no new information will be inserted!")
        return

    print("Adding data ...")

    fake = Faker()
    products_data = []
    inventory_data = []
    unique_skus = set()
    quantity_digits = 3
    min_stock_digits = 2
    
    for index in range(50):

        while True:
            sku = f"SKU{fake.random_int(min=1000, max=9999)}"
            if sku not in unique_skus:
                unique_skus.add(sku)
                break 
        product = Product(
            id = f"prod{index+1}",
            name = fake.word().capitalize() + " " + fake.word().capitalize(),
            description = fake.sentence(),
            category = fake.random_element(["Electronics", "Wearables", "Home", "Gaming", "Kitchen", "Outdoors"]),
            price = round(fake.random_number(digits=2) + fake.random.random(), 2),
            sku = sku
        )

        products_data.append(product)

        if index == 44:
            quantity_digits = 2
            min_stock_digits = 3

        inventory = Inventory(
            id = f"inv{index+1}",
            product_id = f"prod{index+1}",
            store_id = fake.random_element(["store001", "store002", "store003", "store004", "store005"]),
            quantity = fake.random_number(digits=quantity_digits),
            min_stock = fake.random_number(digits=min_stock_digits),
        )
    
        inventory_data.append(inventory)
        

    db.add_all(products_data)
    db.add_all(inventory_data)
    db.commit()
    print("Data loaded correctly!")

if __name__ == "__main__":
    seed_data()
    sys.exit(0)
