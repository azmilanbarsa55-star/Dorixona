
from typing import Optional
from pydantic import BaseModel
from database.models import UserRole

class UserData(BaseModel):
    username: str
    password: str
    role: UserRole
    full_name: Optional[str] = None
class Medicine(BaseModel):
    name: str
    amount: int
    description: int
    base_price: float
    sell_price: float
    bar_code: Optional[str] = None