async function addProduct() {
  const data = {
    name: document.getElementById('prodName').value,
    category: document.getElementById('prodCategory').value,
    price: parseFloat(document.getElementById('prodPrice').value),
    stock_quantity: parseInt(document.getElementById('prodStock').value)
  };
  const res = await fetch('/inventory/api/products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (res.ok) { location.reload(); }
  else { alert('Error adding product'); }
}

async function deleteProduct(id) {
  if (!confirm('Delete this product?')) return;
  const res = await fetch('/inventory/api/products/' + id, { method: 'DELETE' });
  if (res.ok) { document.getElementById('row-' + id).remove(); }
}

async function editProduct(id, name, price, stock) {
  const newStock = prompt('Update stock for ' + name + ':', stock);
  if (newStock === null) return;
  await fetch('/inventory/api/products/' + id, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ stock_quantity: parseInt(newStock) })
  });
  location.reload();
}

async function updateStatus(id, status) {
  await fetch('/orders/api/orders/' + id + '/status', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: status })
  });
  location.reload();
}
