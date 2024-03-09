from django.db import models

class Slides(models.Model):
    photo = models.ImageField(upload_to="media/slides", null=True)
    title = models.CharField(max_length=200)
    caption = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    image = models.ImageField(upload_to='products/', default='') 
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=0)
    description = models.TextField()
    
    def __str__(self):
        return self.name
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=400, blank=True, null=True)
    # No user field for anonymous cart

class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=1)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='orders/', default='') 
    price = models.IntegerField(default=1)


class BuyNow2(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default='')
    product_id = models.CharField(max_length=255)
    product_brand = models.CharField(max_length=255, default='')
    product_category = models.CharField(max_length=255, default='')

    def __str__(self):
        return f"{self.name}'s Order for {self.product_name}"