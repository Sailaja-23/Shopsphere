from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.database import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    description = Column(String, nullable=True)

    price = Column(Float, nullable=False)

    quantity = Column(Integer, nullable=False)

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )
