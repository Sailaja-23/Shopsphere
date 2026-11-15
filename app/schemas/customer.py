from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

    email: EmailStr

    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=15
    )


class CustomerResponse(CustomerCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
