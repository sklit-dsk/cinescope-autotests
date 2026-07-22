from typing import List, Optional, Union

def multiply(a: int, b: int) -> int:
    return a * b

# multiply("das", "dasda")

def sum_numbers(numbers: List[int]) -> int:
    return sum(numbers)

# sum_numbers(["one", "two", "three"])

def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None

# print(find_user(5))

def process_input(value: Union[int, str]):
    return f"Ты передал: {value}"

# print(process_input(5))

class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, меня зовут {self.name}!"
    
# new_user = User("Artem", 5)
# print(new_user.greet())

def get_even_numbers(numbers: List[int]) -> List[int]:
    return [num for num in numbers if num % 2 == 0]

print(get_even_numbers([1,2,3,4,5,6]))