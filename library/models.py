from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13)
    is_for_sale = models.BooleanField(default=True)
    is_for_rent = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    is_rented = models.BooleanField(default=False)
    count = models.PositiveIntegerField(default=0)  # For number of copies
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='photos/', null=True, blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Ensure this field is set to a positive integer
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} rated {self.rating}/5"

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('rent', 'Rent')])
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.book.title}"
