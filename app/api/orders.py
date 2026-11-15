import logging

logger = logging.getLogger("shopsphere")
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.customer import Customer
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderResponse


router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"]
)


@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):

    try:
        # Verify customer exists
        customer = db.query(Customer).filter(
            Customer.id == order_data.customer_id
        ).first()

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        # Validate products and stock before creating order
        validated_items = []
        total_amount = 0

        for item in order_data.items:

            product = db.query(Product).filter(
                Product.id == item.product_id
            ).first()

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product {item.product_id} not found"
                )

            if product.quantity < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for {product.name}"
                )

            validated_items.append((product, item.quantity))

            total_amount += product.price * item.quantity

        # Create order
        new_order = Order(
            customer_id=customer.id,
            total_amount=total_amount,
            status="pending"
        )

        db.add(new_order)
        db.flush()

        # Create order items and reduce stock
        for product, quantity in validated_items:

            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price
            )

            product.quantity -= quantity

            db.add(order_item)

        db.commit()
        db.refresh(new_order)
        logger.info(
            "Order created | order_id=%s | customer_id=%s | total=%s",
            new_order.id,
            new_order.customer_id,
            new_order.total_amount
        )
        return new_order

    except Exception:
        db.rollback()
        raise


@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):

    return db.query(Order).all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order
