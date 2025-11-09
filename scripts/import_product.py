from myapp.models import Category, Product


def run():

    categories_names = ["Смартфоны", "Ноутбуки", "Планшеты", "Беспроводные наушники", "Фотоаппараты", "Экшн-камеры",
                        "Квадрокоптеры", "Телевизоры"]
    categories = {}
    for name in categories_names:
        category_obj, created = Category.objects.get_or_create(name=name)
        categories[name] = category_obj

    products_data = [
        {
            "name": "Apple iPhone 15",
            "description": "Последний флагманский смартфон Apple с новой камерой и процессором A16 Bionic.",
            "price": 999.00,
            "in_stock": True,
            "quantity": 25,
            "category": categories["Смартфоны"],
            "image": None
        },
        {
            "name": "Dell XPS 13",
            "description": "Ноутбук премиум-класса с высоким разрешением экрана и долгим временем работы.",
            "price": 1299.99,
            "in_stock": True,
            "quantity": 15,
            "category": categories["Ноутбуки"],
            "image": None
        },
        {
            "name": "Samsung Galaxy Tab S8",
            "description": "Планшет с ярким дисплеем и мощным процессором для работы и развлечений.",
            "price": 799.99,
            "in_stock": True,
            "quantity": 30,
            "category": categories["Планшеты"],
            "image": None
        },
        {
            "name": "Sony WH-1000XM5",
            "description": "Беспроводные наушники с активным шумоподавлением и длительным временем работы.",
            "price": 399.99,
            "in_stock": True,
            "quantity": 40,
            "category": categories["Беспроводные наушники"],
            "image": None
        },
        {
            "name": "Canon EOS R6",
            "description": "Профессиональная беззеркальная камера с высоким разрешением и стабилизацией.",
            "price": 2499.00,
            "in_stock": True,
            "quantity": 8,
            "category": categories["Фотоаппараты"],
            "image": None
        },
        {
            "name": "Microsoft Surface Laptop 4",
            "description": "Легкий и мощный ноутбук с Windows 10 и высоким разрешением экрана.",
            "price": 1099.99,
            "in_stock": True,
            "quantity": 12,
            "category": categories["Ноутбуки"],
            "image": None
        },
        {
            "name": "GoPro HERO11 Black",
            "description": "Экшн-камера для съемки в экстремальных условиях и походах.",
            "price": 499.99,
            "in_stock": True,
            "quantity": 20,
            "category": categories["Экшн-камеры"],
            "image": None
        },
        {
            "name": "Apple MacBook Pro 16\"",
            "description": "Мощный ноутбук для профессиональной работы с 16-дюймовым дисплеем и M1 Pro/M1 Max.",
            "price": 2499.00,
            "in_stock": True,
            "quantity": 10,
            "category": categories["Ноутбуки"],
            "image": None
        },
        {
            "name": "DJI Mavic Air 2",
            "description": "Дрон с высокой разрешающей способностью и дальностью полета.",
            "price": 799.00,
            "in_stock": True,
            "quantity": 5,
            "category": categories["Квадрокоптеры"],
            "image": None
        },
        {
            "name": "Roku Streaming Stick+",
            "description": "Гибкий потоковый гаджет для Smart TV с поддержкой 4K и HDR.",
            "price": 49.99,
            "in_stock": True,
            "quantity": 50,
            "category": categories["Телевизоры"],
            "image": None
        },
    ]

    products = [Product(**data) for data in products_data]
    Product.objects.bulk_create(products)

