from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, StockMovement
from .forms import StockMovementForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    movements = product.stockmovement_set.all().order_by('-timestamp')
    return render(request, 'inventory/product_detail.html', {
        'product': product, 'movements': movements
    })

def stock_movement_create(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = StockMovementForm()
    return render(request, 'inventory/stock_movement_form.html', {'form': form})
