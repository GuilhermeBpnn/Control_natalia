from sqlalchemy.orm import Session, joinedload
from app.models import FinancialEntry, Product, Sale, SaleItem, StockMovement


class SaleService:
    @staticmethod
    def list_sales(db: Session):
        return db.query(Sale).order_by(Sale.created_at.desc()).all()

    @staticmethod
    def get_sale(db: Session, sale_id: int):
        return (
            db.query(Sale)
            .options(joinedload(Sale.items).joinedload(SaleItem.product))
            .filter(Sale.id == sale_id)
            .first()
        )

    @staticmethod
    def create_sale(db: Session, customer_name: str | None, payment_method: str, notes: str | None, items_payload: list[dict]):
        if not items_payload:
            raise ValueError('Adicione pelo menos um item na venda.')

        validated_items = []
        total = 0.0
        for item in items_payload:
            product = db.query(Product).filter(Product.id == item['product_id']).first()
            if not product:
                raise ValueError(f"Produto com ID {item['product_id']} não encontrado.")
            quantity = int(item['quantity'])
            if quantity <= 0:
                raise ValueError(f'Quantidade inválida para o produto {product.name}.')
            if product.stock_quantity < quantity:
                raise ValueError(f'Estoque insuficiente para o produto {product.name}.')
            subtotal = product.sale_price * quantity
            total += subtotal
            validated_items.append((product, quantity, subtotal))

        sale = Sale(
            customer_name=customer_name or None,
            payment_method=payment_method,
            total_amount=total,
            notes=notes or None,
        )
        db.add(sale)
        db.flush()

        for product, quantity, subtotal in validated_items:
            product.stock_quantity -= quantity
            db.add(
                SaleItem(
                    sale_id=sale.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.sale_price,
                    subtotal=subtotal,
                )
            )
            db.add(
                StockMovement(
                    product_id=product.id,
                    movement_type='sale',
                    quantity=-quantity,
                    reason=f'Venda #{sale.id}',
                    reference_id=sale.id,
                )
            )

        db.add(
            FinancialEntry(
                type='income',
                category='Venda',
                amount=total,
                description=f'Entrada automática da venda #{sale.id}',
                origin='Vendas',
                reference_id=sale.id,
            )
        )

        db.commit()
        db.refresh(sale)
        return sale
