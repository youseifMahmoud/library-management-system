from django.db import models

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
    image = models.ImageField(upload_to='photos/', null=True, blank=True)

    def __str__(self):
        return self.title

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('rent', 'Rent')])
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.book.title}"
