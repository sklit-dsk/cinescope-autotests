import random
from datetime import timedelta
from faker import Faker

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_password(length=12):
        if length < 8:
            raise ValueError("Password length must be at least 8 characters")

        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digits = "0123456789"
        special_chars = "?@#$%^&*()[]{}><\\/\\|\"'.,:;_-+"
        allowed_chars = letters + digits + special_chars

        password_chars = [
            random.choice(letters),
            random.choice(digits),
        ]
        password_chars.extend(random.choice(allowed_chars) for _ in range(length - 2))
        random.shuffle(password_chars)
        return "".join(password_chars)

    @staticmethod
    def generate_random_name():
        return faker.name()

    @staticmethod
    def generate_firstname():
        return faker.first_name()

    @staticmethod
    def generate_lastname():
        return faker.last_name()

    @staticmethod
    def generate_total_price():
        return random.randint(100, 5000)

    @staticmethod
    def generate_deposit_paid():
        return faker.boolean()

    @staticmethod
    def generate_checkin_date():
        return faker.date_between(start_date='today', end_date='+30d')

    @staticmethod
    def generate_checkout_date(checkin_date):
        return checkin_date + timedelta(days=random.randint(1, 14))

    @staticmethod
    def generate_additional_needs():
        options = ["Breakfast", "Lunch", "Dinner", "Late checkout", "Extra bed", ""]
        return random.choice(options)
