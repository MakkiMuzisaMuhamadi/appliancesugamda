from django.db import models

class Slides(models.Model):
    photo = models.ImageField(upload_to="media/slides", null=True)
    title = models.CharField(max_length=200)
    caption = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/')  # Assuming you want to upload category images

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    image = models.ImageField(upload_to='products/', default='')  # Assuming you want to upload category images
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=0)
    description = models.TextField()
    def __str__(self):
        return self.name
