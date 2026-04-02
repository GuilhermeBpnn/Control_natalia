from sqlalchemy.orm import Session, joinedload
from app.models import FinancialEntry, Product, StockMovement


class StockService:
    @staticmethod
    def list_movements(db: Session):
        return (
            db.query(StockMovement)
            .options(joinedload(StockMovement.product))
            .order_by(StockMovement.created_at.desc())
            .all()
        )

    @staticmethod
    def add_stock(db: Session, product: Product, quantity: int, reason: str, register_expense: bool = False, expense_amount: float = 0.0):
        if quantity <= 0:
            raise ValueError('A quantidade deve ser maior que zero.')
        product.stock_quantity += quantity
        movement = StockMovement(
            product_id=product.id,
            movement_type='entry',
            quantity=quantity,
            reason=reason or 'Entrada manual de estoque',
            reference_id=product.id,
        )
        db.add(movement)
        if register_expense and expense_amount > 0:
            db.add(
                FinancialEntry(
                    type='expense',
                    category='Compra de mercadoria',
                    amount=expense_amount,
                    description=f'Compra vinculada ao produto {product.name}',
                    origin='Estoque',
                    reference_id=product.id,
                )
            )
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def adjust_stock(db: Session, product: Product, new_quantity: int, reason: str):
        if new_quantity < 0:
            raise ValueError('O novo estoque não pode ser negativo.')
        difference = new_quantity - product.stock_quantity
        product.stock_quantity = new_quantity
        movement = StockMovement(
            product_id=product.id,
            movement_type='adjustment',
            quantity=difference,
            reason=reason or 'Ajuste manual',
            reference_id=product.id,
        )
        db.add(movement)
        db.commit()
        db.refresh(product)
        return product
