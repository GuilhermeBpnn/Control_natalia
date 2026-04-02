from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER

from app.database import get_db
from app.models import Product
from app.services.dashboard_service import DashboardService
from app.services.finance_service import FinanceService
from app.services.product_service import ProductService
from app.services.sale_service import SaleService
from app.services.stock_service import StockService

router = APIRouter()


def render(request: Request, template: str, context: dict):
    templates = request.app.state.templates
    base_context = {'request': request, 'active_page': context.get('active_page', '')}
    base_context.update(context)
    return templates.TemplateResponse(template, base_context)


@router.get('/')
def home(request: Request, db: Session = Depends(get_db)):
    summary = DashboardService.get_summary(db)
    return render(request, 'dashboard.html', {'active_page': 'dashboard', 'summary': summary})


@router.get('/products')
def products_page(request: Request, search: str | None = None, db: Session = Depends(get_db)):
    products = ProductService.list_products(db, search)
    edit_id = request.query_params.get('edit')
    edit_product = ProductService.get_product(db, int(edit_id)) if edit_id and edit_id.isdigit() else None
    return render(request, 'products.html', {'active_page': 'products', 'products': products, 'edit_product': edit_product, 'search': search or ''})


@router.post('/products')
def create_product(
    request: Request,
    name: str = Form(...),
    sku: str = Form(...),
    category: str = Form(''),
    cost_price: float = Form(...),
    sale_price: float = Form(...),
    stock_quantity: int = Form(...),
    minimum_stock: int = Form(0),
    description: str = Form(''),
    db: Session = Depends(get_db),
):
    try:
        ProductService.create_product(
            db,
            {
                'name': name.strip(),
                'sku': sku.strip(),
                'category': category.strip() or None,
                'cost_price': cost_price,
                'sale_price': sale_price,
                'stock_quantity': stock_quantity,
                'minimum_stock': minimum_stock,
                'description': description.strip() or None,
            },
        )
        return RedirectResponse('/products?success=Produto+cadastrado+com+sucesso', status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        products = ProductService.list_products(db)
        return render(request, 'products.html', {'active_page': 'products', 'products': products, 'error': str(e), 'search': ''})


@router.post('/products/{product_id}/update')
def update_product(
    product_id: int,
    request: Request,
    name: str = Form(...),
    sku: str = Form(...),
    category: str = Form(''),
    cost_price: float = Form(...),
    sale_price: float = Form(...),
    stock_quantity: int = Form(...),
    minimum_stock: int = Form(0),
    description: str = Form(''),
    db: Session = Depends(get_db),
):
    product = ProductService.get_product(db, product_id)
    if not product:
        return RedirectResponse('/products?error=Produto+nao+encontrado', status_code=HTTP_303_SEE_OTHER)
    try:
        ProductService.update_product(
            db,
            product,
            {
                'name': name.strip(),
                'sku': sku.strip(),
                'category': category.strip() or None,
                'cost_price': cost_price,
                'sale_price': sale_price,
                'stock_quantity': stock_quantity,
                'minimum_stock': minimum_stock,
                'description': description.strip() or None,
            },
        )
        return RedirectResponse('/products?success=Produto+atualizado+com+sucesso', status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        products = ProductService.list_products(db)
        return render(request, 'products.html', {'active_page': 'products', 'products': products, 'edit_product': product, 'error': str(e), 'search': ''})


@router.post('/products/{product_id}/delete')
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService.get_product(db, product_id)
    if not product:
        return RedirectResponse('/products?error=Produto+nao+encontrado', status_code=HTTP_303_SEE_OTHER)
    try:
        ProductService.delete_product(db, product)
        return RedirectResponse('/products?success=Produto+excluido+com+sucesso', status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        return RedirectResponse(f'/products?error={str(e).replace(" ", "+")}', status_code=HTTP_303_SEE_OTHER)


@router.get('/sales')
def sales_page(request: Request, db: Session = Depends(get_db)):
    products = ProductService.list_products(db)
    sales = SaleService.list_sales(db)
    return render(request, 'sales.html', {'active_page': 'sales', 'products': products, 'sales': sales})


@router.post('/sales')
def create_sale(
    request: Request,
    customer_name: str = Form(''),
    payment_method: str = Form(...),
    notes: str = Form(''),
    product_id: list[int] = Form(...),
    quantity: list[int] = Form(...),
    db: Session = Depends(get_db),
):
    try:
        items = []
        for pid, qty in zip(product_id, quantity):
            if qty > 0:
                items.append({'product_id': pid, 'quantity': qty})
        SaleService.create_sale(db, customer_name, payment_method, notes, items)
        return RedirectResponse('/sales?success=Venda+registrada+com+sucesso', status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        products = ProductService.list_products(db)
        sales = SaleService.list_sales(db)
        return render(request, 'sales.html', {'active_page': 'sales', 'products': products, 'sales': sales, 'error': str(e)})


@router.get('/sales/{sale_id}')
def sale_detail(request: Request, sale_id: int, db: Session = Depends(get_db)):
    sale = SaleService.get_sale(db, sale_id)
    if not sale:
        return RedirectResponse('/sales?error=Venda+nao+encontrada', status_code=HTTP_303_SEE_OTHER)
    return render(request, 'sale_detail.html', {'active_page': 'sales', 'sale': sale})


@router.get('/finance')
def finance_page(request: Request, entry_type: str | None = None, db: Session = Depends(get_db)):
    entries = FinanceService.list_entries(db, entry_type)
    totals = FinanceService.totals(db)
    return render(request, 'finance.html', {'active_page': 'finance', 'entries': entries, 'totals': totals, 'entry_type': entry_type or ''})


@router.post('/finance')
def create_finance_entry(
    request: Request,
    type: str = Form(...),
    category: str = Form(...),
    amount: float = Form(...),
    description: str = Form(''),
    origin: str = Form(''),
    db: Session = Depends(get_db),
):
    try:
        FinanceService.create_entry(
            db,
            {
                'type': type,
                'category': category.strip(),
                'amount': amount,
                'description': description.strip() or None,
                'origin': origin.strip() or None,
            },
        )
        return RedirectResponse('/finance?success=Lancamento+registrado+com+sucesso', status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        entries = FinanceService.list_entries(db)
        totals = FinanceService.totals(db)
        return render(request, 'finance.html', {'active_page': 'finance', 'entries': entries, 'totals': totals, 'error': str(e), 'entry_type': ''})


@router.get('/stock')
def stock_page(request: Request, db: Session = Depends(get_db)):
    products = ProductService.list_products(db)
    movements = StockService.list_movements(db)
    return render(request, 'stock.html', {'active_page': 'stock', 'products': products, 'movements': movements})


@router.post('/stock/entry')
def stock_entry(
    product_id: int = Form(...),
    quantity: int = Form(...),
    reason: str = Form(''),
    register_expense: str | None = Form(None),
    expense_amount: float = Form(0),
    db: Session = Depends(get_db),
):
    product = ProductService.get_product(db, product_id)
    if not product:
        return RedirectResponse('/stock?error=Produto+nao+encontrado', status_code=HTTP_303_SEE_OTHER)
    try:
        StockService.add_stock(db, product, quantity, reason, register_expense == 'on', expense_amount)
        return RedirectResponse('/stock?success=Entrada+de+estoque+registrada+com+sucesso', status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        return RedirectResponse(f'/stock?error={str(e).replace(" ", "+")}', status_code=HTTP_303_SEE_OTHER)


@router.post('/stock/adjust')
def stock_adjust(
    product_id: int = Form(...),
    new_quantity: int = Form(...),
    reason: str = Form(''),
    db: Session = Depends(get_db),
):
    product = ProductService.get_product(db, product_id)
    if not product:
        return RedirectResponse('/stock?error=Produto+nao+encontrado', status_code=HTTP_303_SEE_OTHER)
    try:
        StockService.adjust_stock(db, product, new_quantity, reason)
        return RedirectResponse('/stock?success=Ajuste+de+estoque+registrado+com+sucesso', status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        return RedirectResponse(f'/stock?error={str(e).replace(" ", "+")}', status_code=HTTP_303_SEE_OTHER)
