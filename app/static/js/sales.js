document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('sale-items');
  const addButton = document.getElementById('add-sale-item');
  const totalBox = document.getElementById('sale-total');
  if (!container || !addButton) return;

  function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value || 0);
  }

  function updateRowSubtotal(row) {
    const select = row.querySelector('select[name="product_id"]');
    const quantityInput = row.querySelector('input[name="quantity"]');
    const subtotalEl = row.querySelector('.item-subtotal');
    const selectedOption = select?.selectedOptions?.[0];
    const price = Number(selectedOption?.dataset?.price || 0);
    const stock = Number(selectedOption?.dataset?.stock || 0);
    const quantity = Number(quantityInput?.value || 0);

    if (quantityInput && stock > 0) {
      quantityInput.max = stock;
    } else if (quantityInput) {
      quantityInput.removeAttribute('max');
    }

    const subtotal = price * quantity;
    if (subtotalEl) subtotalEl.textContent = formatCurrency(subtotal);
    return subtotal;
  }

  function updateTotal() {
    const rows = container.querySelectorAll('.sale-item-row');
    let total = 0;
    rows.forEach((row) => {
      total += updateRowSubtotal(row);
    });
    if (totalBox) totalBox.textContent = formatCurrency(total);
  }

  function createRow() {
    const firstRow = container.querySelector('.sale-item-row');
    const row = firstRow.cloneNode(true);
    row.querySelector('select').value = '';
    row.querySelector('input[name="quantity"]').value = 1;
    const subtotalEl = row.querySelector('.item-subtotal');
    if (subtotalEl) subtotalEl.textContent = formatCurrency(0);
    return row;
  }

  addButton.addEventListener('click', () => {
    const row = createRow();
    container.appendChild(row);
    updateTotal();
  });

  container.addEventListener('click', (event) => {
    if (!event.target.classList.contains('remove-item')) return;
    const rows = container.querySelectorAll('.sale-item-row');
    if (rows.length === 1) {
      alert('A venda precisa ter pelo menos um item.');
      return;
    }
    event.target.closest('.sale-item-row').remove();
    updateTotal();
  });

  container.addEventListener('change', (event) => {
    if (event.target.matches('select[name="product_id"], input[name="quantity"]')) {
      updateTotal();
    }
  });

  container.addEventListener('input', (event) => {
    if (event.target.matches('input[name="quantity"]')) {
      updateTotal();
    }
  });

  updateTotal();
});
