from typing import Optional
from pydantic import BaseModel

class UIUserDemoQA(BaseModel):
    userName: Optional[str]
    firstName: str
    lastName: str
    userEmail: str
    userAge: Optional[int]
    userSalary: Optional[int]
    userDepartament: Optional[str]
    userPhoneNumber: Optional[str]
    password: Optional[str]
    
class UIUserCinescope(BaseModel):
    password: str
    userName: str
    userEmail: str