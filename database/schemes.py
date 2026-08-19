
from typing import Optional
from pydantic import BaseModel
from database.models import UserRole
from typing import Text

class UserData(BaseModel):
    username: str
    password: str
    role: UserRole
    full_name: Optional[str] = None

class UsersUpdateData(BaseModel):
    id: int
    username: str | None = None
    passwors: str | None = None
    full_name: str | None = None
    role: UserRole | None = None
class DrugData(BaseModel):
    name: str
    amount: int
    description: Text
    base_price: float
    sell_price: float
    bar_code: Optional[str] = None