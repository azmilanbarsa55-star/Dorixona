
from sqlalchemy import String, Text, Float, Integer, ForeignKey, Boolean, Column, Enum, DateTime
from sqlalchemy.orm import relationship
from enum import Enum as PyEnumClass
from datetime import datetime

from database.config import Base

class UserRole(PyEnumClass):
    ADMIN = "admin"
    CASHIER = "cashier"

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(length=50), unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String(length=50), nullable=True)

    role = Column(Enum(UserRole), nullable=False)

    checks = relationship("Check", back_populates="cashier")



class Drug(Base):
    __tablename__ = "drugs"

    id = Column(Integer, primary_key=True)

    name = Column(String(length=40), unique=True, nullable=False)
    amount = Column(Integer, default=0)
    description = Column(Text, nullable=False)
    base_price = Column(Float, default=0)
    sell_price = Column(Float, default=0)
    bar_code = Column(String(length=20))



class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True)

    check_num = Column(String, unique=True)
    date_create = Column(DateTime, nullable=False , default=datetime.now())

    cashier_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    cashier = relationship("Users", back_populates="checks")
    items = relationship("CheckItem", back_populates="check")

class CheckItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, default=1)

    drug_id = Column(Integer, ForeignKey("drugs.id"), nullable=False)

    check_id = Column(Integer, ForeignKey("checks.id"), nullable=False)
    check = relationship("Check", back_populates="items")


