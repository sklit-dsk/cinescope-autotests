# CinescopeFork\Modul_4\PydanticExamples\test_pydantic.py
from pydantic import BaseModel
from venv import logger


class User(BaseModel):  # Создается класс User с помощью BaseModel от pydantic и указывается
    name: str       # что имя должно быть строкой
    age: int        # возраст должен быть числом
    adult: bool     # поле совершенолетие должно быть булевым значением


def get_user() -> (
    dict[str, object]
):  # функция get_user возвращает обьект dict с следущими полями
    return {"name": "Alice", "age": 25, "adult": "true"}


def test_user_data() -> None:
    user = User(
        name="Alice", age=25, adult=True
    )  # Проверяем возможность конвертации данных и соответствия типов данных с помощью Pydantic
    assert user.name == "Alice"  # Возможность дополнительных проверок
    logger.info(
        f"{user.name=} {user.age=} {user.adult=}"
    )  # а также возможность удобного взаимодействия


# CinescopeFork\Modul_4\PydanticExamples\test_pydantic.py
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from venv import logger


class ProductType(str, Enum):
    NEW = "new"
    PREVIOUS_USE = "previous_use"


class Manufacturer(BaseModel):
    name: str
    city: Optional[str] = None
    street: Optional[str] = None


class Product(BaseModel):
    # поле name может иметь длину в диапазоне от 3 до 50 символов и является строкой
    name: str = Field(..., min_length=3, max_length=50, description="Название продукта")
    # поле price должно быть больше 0
    price: float = Field(..., gt=0, description="Цена продукта")
    # поле in_stock принимает булево значение и установится по умолчанию = False
    in_stock: bool = Field(default=False, description="Есть ли в наличии")
    # поле colorдолжно быть строкой и принимает значение "black" по умолчанию
    color: str = "black"
    # поле year не обязательное. можно не указывать при создании обьекта
    year: Optional[int] = None
    # поле product принимает тип Enum (может содержать только 1 из его значений)
    product: ProductType
    # поле manufacturer принимает тип другой BaseModel
    manufacturer: Manufacturer


def test_product() -> None:
    # Пример создания обьекта + в поле price передаём строку вместо числа
    product = Product(
        name="Laptop",
        price="999.99",
        product=ProductType.NEW,
        manufacturer=Manufacturer(name="MSI"),
    )
    logger.info(f"{product=}")
    # Output: product=Product(name='Laptop', price=999.99, in_stock=False, color='black', year=None, product=<ProductType.NEW: 'new'>, manufacturer=Manufacturer(name='MSI', city=None, street=None))

    # Пример конвертации обьекта в json
    json_data = product.model_dump_json(exclude_unset=True)
    logger.info(f"{json_data=}")
    # Output: json_data='{"name":"Laptop","price":999.99,"product":"new","manufacturer":{"name":"MSI"}}'

    # Пример конвертации json в обьект
    new_product = Product.model_validate_json(json_data)
    logger.info(f"{new_product=}")
    # Output: new_product=Product(name='Laptop', price=999.99, in_stock=False, color='black', year=None, product=<ProductType.NEW: 'new'>, manufacturer=Manufacturer(name='MSI', city=None, street=None))


from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional
from venv import logger


class PostgresClient:  # Mock - заглушка вмето реального сервиса. делающего запрос в базу данных
    @staticmethod
    def get(key: str) -> None:  # Всегда возвращает None
        return None


class Card(BaseModel):
    pan: str = Field(..., min_length=16, max_length=16, description="Номер карты")
    cvc: str = Field(...,  min_length=3, max_length=3)

    @field_validator("pan")  # кастомный валидатор для проверки поля pan
    def check_pan(cls, value: str) -> str:
        """
            не самый лучший пример. не стоит добавлять в валидаторы сложновесную логику
            но данным приером хочется показать что кастомные валидаторы лучше использоват
            для ситуаций которые невозможно проверить доступной логикой Field
        """
        # Проверяем, существует ли карта в Redis
        if PostgresClient.get(f'card_by_pan_{value}') is None:
            raise ValueError("Такой карты не существует")
        return value

# def test_field_validator() -> None:
# # Попытка создать объект с данными. отсутствующими в базе данных
#     try:
#         card = Card(pan="1111222233334444", cvc="123")
#         logger.info(card)
#     except ValidationError as e:
#         logger.info(f"Ошибка валидации: {e}")
#         raise
