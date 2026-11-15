from pydantic import BaseModel, Field, ConfigDict


class ProductCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
        description="Product name must contain 2–100 characters"
    )

    description: str | None = Field(
        default=None,
        max_length=500
    )

    price: float = Field(
        gt=0,
        description="Price must be greater than zero"
    )

    quantity: int = Field(
        ge=0,
        description="Quantity cannot be negative"
    )


class ProductResponse(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
