from django.db import models
from django.contrib.auth.models import User
import uuid

# Base model for common fields
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# ✅ Product Model (Main Product for all categories)
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # optional
    # category field agar delete kar diya ho toh koi dikkat nahi

    def __str__(self):
        return self.name

# ✅ Cart Model
class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="carts")
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart for {self.user.username} - Paid: {self.is_paid}"

# ✅ Cart Item Model
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# ✅ Order Model

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.product.pizza_name}"

class TableBooking(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    occasion = models.CharField(max_length=50, blank=True)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    table_preference = models.CharField(max_length=50, blank=True)
    message = models.TextField(blank=True)
    payment_method = models.CharField(max_length=50)
    is_paid = models.BooleanField(default=False)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"