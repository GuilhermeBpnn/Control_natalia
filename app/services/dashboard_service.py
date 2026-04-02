from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import FinancialEntry, Product, Sale, StockMovement


class DashboardService:
    @staticmethod
    def get_summary(db: Session):
        now = datetime.utcnow()
        day_start = datetime(now.year, now.month, now.day)
        month_start = datetime(now.year, now.month, 1)

        sold_today = db.query(func.coalesce(func.sum(Sale.total_amount), 0.0)).filter(Sale.created_at >= day_start).scalar() or 0.0
        sold_month = db.query(func.coalesce(func.sum(Sale.total_amount), 0.0)).filter(Sale.created_at >= month_start).scalar() or 0.0
        expense_month = db.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0)).filter(FinancialEntry.type == 'expense', FinancialEntry.created_at >= month_start).scalar() or 0.0
        income_total = db.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0)).filter(FinancialEntry.type == 'income').scalar() or 0.0
        expense_total = db.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0)).filter(FinancialEntry.type == 'expense').scalar() or 0.0
        estimated_cost_stock = db.query(func.coalesce(func.sum(Product.cost_price * Product.stock_quantity), 0.0)).scalar() or 0.0
        total_stock_items = db.query(func.coalesce(func.sum(Product.stock_quantity), 0)).scalar() or 0
        low_stock_products = db.query(Product).filter(Product.stock_quantity <= Product.minimum_stock).order_by(Product.stock_quantity.asc()).limit(8).all()
        recent_sales = db.query(Sale).order_by(Sale.created_at.desc()).limit(5).all()
        recent_movements = db.query(StockMovement).order_by(StockMovement.created_at.desc()).limit(5).all()

        return {
            'sold_today': float(sold_today),
            'sold_month': float(sold_month),
            'expense_month': float(expense_month),
            'balance': float(income_total - expense_total),
            'estimated_profit_month': float(sold_month - expense_month),
            'estimated_cost_stock': float(estimated_cost_stock),
            'total_stock_items': int(total_stock_items or 0),
            'low_stock_products': low_stock_products,
            'recent_sales': recent_sales,
            'recent_movements': recent_movements,
        }
