from sqlalchemy.orm import Session
from app.models import Product, StockMovement


class ProductService:
    @staticmethod
    def list_products(db: Session, search: str | None = None):
        query = db.query(Product)
        if search:
            like = f'%{search.strip()}%'
            query = query.filter((Product.name.ilike(like)) | (Product.sku.ilike(like)))
        return query.order_by(Product.name.asc()).all()

    @staticmethod
    def get_product(db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def sku_exists(db: Session, sku: str, exclude_id: int | None = None) -> bool:
        query = db.query(Product).filter(Product.sku == sku)
        if exclude_id:
            query = query.filter(Product.id != exclude_id)
        return db.query(query.exists()).scalar()

    @staticmethod
    def create_product(db: Session, data: dict):
        if ProductService.sku_exists(db, data['sku']):
            raise ValueError('Já existe um produto com esse SKU.')
        product = Product(**data)
        db.add(product)
        db.flush()
        if product.stock_quantity > 0:
            db.add(
                StockMovement(
                    product_id=product.id,
                    movement_type='entry',
                    quantity=product.stock_quantity,
                    reason='Estoque inicial',
                    reference_id=product.id,
                )
            )
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def update_product(db: Session, product: Product, data: dict):
        if ProductService.sku_exists(db, data['sku'], exclude_id=product.id):
            raise ValueError('Já existe um produto com esse SKU.')
        if data['stock_quantity'] < 0:
            raise ValueError('O estoque não pode ser negativo.')
        for key, value in data.items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete_product(db: Session, product: Product):
        if product.sale_items:
            raise ValueError('Não é possível excluir um produto que já possui vendas registradas.')
        db.delete(product)
        db.commit()
