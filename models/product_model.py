from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional
from enum import Enum

class ProductType(Enum):
    ELEC = "электроника"
    CLOTHES = "одежда"

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool
    type: ProductType


product = Product(name="Штаны", price=200.00, in_stock="True", type="одежда")

json_data = product.model_dump_json()
print(json_data)

new_product = Product.model_validate_json(json_data)
print(new_product)
