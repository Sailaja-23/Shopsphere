from pydantic import BaseModel, Field, ConfigDict


class OrderItemCreate(BaseModel):
    product_id: int = Field(gt=0)

    quantity: int = Field(
        gt=0,
        description="Order quantity must be greater than zero"
    )


class OrderCreate(BaseModel):
    customer_id: int = Field(gt=0)

    items: list[OrderItemCreate] = Field(
        min_length=1,
        description="An order must contain at least one item"
    )


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    status: str
    total_amount: float
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)
