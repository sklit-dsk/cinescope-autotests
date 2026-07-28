import random
from datetime import timedelta
from faker import Faker

faker = Faker()

class DataGenerator:
    VALID_GENRE_IDS = [4, 6, 7, 8, 9]

    @staticmethod
    def generate_random_email() -> str:
        random_string = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8)
        )
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_password(length: int = 12) -> str:
        if length < 8:
            raise ValueError("Password length must be at least 8 characters")

        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digits = "0123456789"
        special_chars = "?@#$%^&*()[]"
        allowed_chars = letters + digits + special_chars

        password_chars = [
            random.choice(letters),
            random.choice(digits),
        ]
        password_chars.extend(random.choice(allowed_chars) for _ in range(length - 2))
        random.shuffle(password_chars)
        return "".join(password_chars)

    @staticmethod
    def generate_random_name() -> str:
        return faker.name()

    @staticmethod
    def generate_firstname() -> str:
        return faker.first_name()

    @staticmethod
    def generate_lastname() -> str:
        return faker.last_name()

    @staticmethod
    def generate_min_price() -> int:
        return random.randint(100, 1000)

    @staticmethod
    def generate_max_price(minPrice: int) -> int:
        return random.randint(minPrice, 10000)

    @staticmethod
    def generate_location() -> str:
        options = ["SPB", "MSK"]
        return random.choice(options)

    @staticmethod
    def generate_published() -> bool:
        options = [True, False]
        return random.choice(options)

    @staticmethod
    def generate_genre_id() -> int:
        return random.choice(DataGenerator.VALID_GENRE_IDS)

    @staticmethod
    def generate_created_at() -> str:
        options = ["asc", "desc"]
        return random.choice(options)

    @staticmethod
    def generate_bad_location() -> str:
        options = ["SRG", "NSK"]
        return random.choice(options)

    @staticmethod
    def generate_movie_name() -> str:
        random_string = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=8))
        return f"{random_string}"

    @staticmethod
    def generate_movie_image_url() -> str:
        random_string = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8)
        )
        return f"https://{random_string}.url"

    @staticmethod
    def generate_movie_description() -> str:
        random_string = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=20)
        )
        return f"{random_string}"

    @staticmethod
    def generate_movie_data() -> dict[str, object]:
        return {
            "name": DataGenerator.generate_movie_name(),
            "imageUrl": DataGenerator.generate_movie_image_url(),
            "price": DataGenerator.generate_min_price(),
            "description": DataGenerator.generate_movie_description(),
            "location": DataGenerator.generate_location(),
            "published": DataGenerator.generate_published(),
            "genreId": DataGenerator.generate_genre_id(),
        }

    @staticmethod
    def generate_movie_params() -> dict[str, object]:
        min_price = DataGenerator.generate_min_price()
        return {
            "minPrice": min_price,
            "maxPrice": DataGenerator.generate_max_price(min_price),
            "locations": DataGenerator.generate_location(),
            "published": DataGenerator.generate_published(),
            "genreId": DataGenerator.generate_genre_id(),
            "createdAt": DataGenerator.generate_created_at(),
        }

    @staticmethod
    def generate_bad_movie_params() -> dict[str, object]:
        min_price = DataGenerator.generate_min_price()
        return {
            "minPrice": min_price,
            "maxPrice": DataGenerator.generate_max_price(min_price),
            "locations": DataGenerator.generate_bad_location(),
            "published": DataGenerator.generate_published(),
            "genreId": DataGenerator.generate_genre_id(),
            "createdAt": DataGenerator.generate_created_at(),
        }

    @staticmethod
    def generate_verification() -> bool:
        options = [True, False]
        return random.choice(options)

    @staticmethod
    def generate_user_data() -> dict[str, object]:
        password = DataGenerator.generate_random_password()
        return {
            "email": DataGenerator.generate_random_email(),
            "fullName": DataGenerator.generate_random_name(),
            "password": password,
            "passwordRepeat": password,
            "verified": DataGenerator.generate_verification(),
            "banned": False,
        }

    @staticmethod
    def generate_page_size() -> int:
        return random.randint(1, 10)

    @staticmethod
    def generate_roles() -> list[str]:
        options = [
            ["USER"],
            ["ADMIN"],
            ["SUPER_ADMIN"],
            ["USER", "ADMIN"],
            ["USER", "SUPER_ADMIN"],
            ["ADMIN", "SUPER_ADMIN"],
        ]
        return random.choice(options)

    @staticmethod
    def generate_user_params() -> dict[str, object]:
        return {
            "pageSize": DataGenerator.generate_page_size(),
            "page": DataGenerator.generate_page_size(),
            "roles": DataGenerator.generate_roles(),
            "createdAt": DataGenerator.generate_created_at(),
        }
