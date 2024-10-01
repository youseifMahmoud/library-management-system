"""
Registering the Book and Author models to make them manageable 
through the Django admin interface.

"""
from django.contrib import admin
from .models import Book, Author


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ('title', 'author', 'isbn', 'price', 'count', 'is_for_sale', 'is_for_rent', 'is_sold', 'is_rented')
    
    # Add filters to the right sidebar for these fields
    list_filter = ('is_for_sale', 'is_for_rent', 'is_sold', 'is_rented', 'author')
    
    # Add search functionality for title, author, and ISBN
    search_fields = ('title', 'author__name', 'isbn')
    
    # Specify the fields to be editable directly from the list view
    list_editable = ('price', 'count', 'is_for_sale', 'is_for_rent', 'is_sold', 'is_rented')

# Register the Author model without customization
admin.site.register(Author)
