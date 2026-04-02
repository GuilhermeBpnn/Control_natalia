from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import FinancialEntry


class FinanceService:
    @staticmethod
    def list_entries(db: Session, entry_type: str | None = None):
        query = db.query(FinancialEntry)
        if entry_type in {'income', 'expense'}:
            query = query.filter(FinancialEntry.type == entry_type)
        return query.order_by(FinancialEntry.created_at.desc()).all()

    @staticmethod
    def create_entry(db: Session, data: dict):
        if data['type'] not in {'income', 'expense'}:
            raise ValueError('Tipo inválido.')
        if data['amount'] <= 0:
            raise ValueError('O valor precisa ser maior que zero.')
        entry = FinancialEntry(**data)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def current_month_totals(db: Session):
        now = datetime.utcnow()
        month_start = datetime(now.year, now.month, 1)
        income = (
            db.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0))
            .filter(FinancialEntry.type == 'income', FinancialEntry.created_at >= month_start)
            .scalar()
        )
        expense = (
            db.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0))
            .filter(FinancialEntry.type == 'expense', FinancialEntry.created_at >= month_start)
            .scalar()
        )
        return {'income': float(income or 0), 'expense': float(expense or 0)}

    @staticmethod
    def totals(db: Session):
        income = db.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0)).filter(FinancialEntry.type == 'income').scalar()
        expense = db.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0)).filter(FinancialEntry.type == 'expense').scalar()
        return {'income': float(income or 0), 'expense': float(expense or 0), 'balance': float((income or 0) - (expense or 0))}
