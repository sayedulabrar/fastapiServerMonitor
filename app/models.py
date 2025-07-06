from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True , autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Integer, nullable=False)
