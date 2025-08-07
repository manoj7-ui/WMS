from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sku = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    @property
    def current_stock(self):
        ins = self.stockmovement_set.filter(movement_type='IN').aggregate(models.Sum('quantity'))['quantity__sum'] or 0
        outs = self.stockmovement_set.filter(movement_type='OUT').aggregate(models.Sum('quantity'))['quantity__sum'] or 0
        return ins - outs

class StockMovement(models.Model):
    MOVEMENT_CHOICES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_CHOICES)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.movement_type == 'OUT' and self.quantity > self.product.current_stock:
            raise ValidationError("Not enough stock for this operation.")

    def __str__(self):
        return f"{self.movement_type} - {self.product.name} ({self.quantity})"
