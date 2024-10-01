from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author , Transaction , Review
from .forms import BookForm, AuthorForm , CustomUserCreationForm , ReviewForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q  
from django.contrib import messages
from django.http import JsonResponse

def index(request):
    return render(request, 'library/index.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        book_form = BookForm(request.POST, request.FILES)  # Ensure you're handling file uploads
        author_form = AuthorForm(request.POST)
        
        if book_form.is_valid():
            book_form.save()
            return redirect('home')
        
        if author_form.is_valid():
            author_form.save()
            return redirect('home')
    else:
        book_form = BookForm()
        author_form = AuthorForm()

    query_books = request.GET.get('q_books', '')
    books = Book.objects.filter(Q(title__icontains=query_books)) if query_books else Book.objects.all()

    query_authors = request.GET.get('q_authors', '')
    authors = Author.objects.filter(Q(name__icontains=query_authors)) if query_authors else Author.objects.all()

    return render(request, 'library/home.html', {
        'username': request.user.username,
        'book_form': book_form,
        'author_form': author_form,
        'books': books,
        'authors': authors,
        'query_books': query_books,
        'query_authors': query_authors,
    })

def client_page(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login')

    query_books = request.GET.get('q_books', '')  

    if query_books:
        books = Book.objects.filter(Q(title__icontains=query_books))
    else:
        books = Book.objects.none()

    return render(request, 'library/client.html', {
        'username': request.user.username,
        'books': books,
        'query_books': query_books,
    })

def buy_or_rent_book(request, book_id, transaction_type):
    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(Book, id=book_id)

    if transaction_type == 'buy':
        if book.count > 0:
            book.is_sold = True
            book.is_for_sale = False
            book.is_for_rent = False
            book.count -= 1  # Decrease count after purchase
            messages.success(request, f"You have successfully bought '{book.title}'.")
        else:
            messages.warning(request, f"'{book.title}' is not available for sale.")
            return redirect('client_page')


    book.save()

    # Create a transaction
    transaction = Transaction(book=book, user=request.user, transaction_type=transaction_type)
    transaction.save()

    return redirect('client_page')


def return_book(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(Book, id=book_id)

    # Check if the book is currently rented
    if book.is_rented:
        book.is_rented = False  # Mark the book as not rented
        book.count += 1  # Increment available copies
        book.save()

        # Optionally, delete the transaction record if needed
        Transaction.objects.filter(book=book, user=request.user, transaction_type='rent').delete()

        messages.success(request, f"You have successfully returned '{book.title}'.")
    else:
        messages.warning(request, f"'{book.title}' was not rented.")

    return redirect('client_page')


def rent_book(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(Book, id=book_id)

    # Check if the book is available for rent
    if book.is_for_rent and book.count > 0:
        if not book.is_rented:  # Check if it's already rented
            book.is_rented = True  # Mark the book as rented
            book.count -= 1  # Decrement available copies
            book.save()

            # Create a transaction record for the rental
            Transaction.objects.create(book=book, user=request.user, transaction_type='rent')

            messages.success(request, f"You have successfully rented '{book.title}'.")
        else:
            messages.warning(request, f"'{book.title}' is already rented.")
    else:
        messages.warning(request, f"'{book.title}' is not available for rent.")

    return redirect('client_page')

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(book=book)  # Get all reviews for the book

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Assign the review to the current user
            review.book = book  # Assign the review to the current book
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('book_detail', book_id=book_id)
    else:
        form = ReviewForm()

    context = {
        'book': book,
        'reviews': reviews,
        'form': form
    }

    return render(request, 'library/book_detail.html', context)

def process_payment(request, book_id):
    # Get the book object based on the book_id
    book = get_object_or_404(Book, id=book_id)

    # Render the payment page, passing the book information
    return render(request, 'library/payment.html', {'book': book})

def complete_payment(request, book_id):
    # Fetch the book object based on the book_id
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        # Extract the card information from the request (you could add validation here)
        card_number = request.POST.get('card_number')
        card_name = request.POST.get('card_name')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        
        # Simple validation to check if the card details are filled (expand this for real-world use)
        if card_number and card_name and expiry_date and cvv:
            # Assuming payment is successful, update the book's status
            if book.count > 0:
                book.count -= 1
                book.is_sold = True  # Mark the book as sold
                book.save()
                
                messages.success(request, 'Payment completed successfully!')
                return render(request, 'library/payment_success.html', {'book': book})
            else:
                messages.error(request, 'Book is out of stock.')
                return redirect('client_page')  # Redirect if out of stock
        else:
            # Handle payment failure (missing information)
            return render(request, 'library/payment.html', {
                'book': book,
                'error': 'Please provide all payment details.'
            })

    # If the request is not POST, render the payment form again
    return render(request, 'library/payment.html', {'book': book})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Set session to expire in 7 days
            request.session.set_expiry(7 * 24 * 60 * 60)  

            if user.is_staff:
                return redirect('home')  # Redirect to admin home
            else:
                return redirect('client_page')  # Redirect to client page
    else:
        form = AuthenticationForm()
    
    return render(request, 'library/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            if user_type == 'admin':
                user.is_staff = True
            else:
                user.is_staff = False
            user.save()
            return redirect('login')  # Redirect to login after signup
    else:
        form = CustomUserCreationForm()  # Create a new form instance for GET requests

    return render(request, 'library/signup.html', {'form': form}) 

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('home')  # Redirect to admin home
            else:
                return redirect('client_page')  # Redirect to client page
    else:
        form = AuthenticationForm()
    return render(request, 'library/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to login after logout
    
def book_list(request):
    """
    Retrieves all books from the database and renders the book list page.

    Returns:
        book list page with a list of books.
    """
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def author_list(request):
    """
    Retrieves all authors from the database and renders the author list page.

    Returns:
        HttpResponse: The rendered author list page with a list of authors.
    """
    authors = Author.objects.all()
    return render(request, 'library/author_list.html', {'authors': authors})

def edit_book(request, pk):
    """
    To edit book and redirect to home after editing.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after successful edit
    else:
        form = BookForm(instance=book)
    return render(request, 'library/edit_book.html', {'form': form})

def delete_book(request, pk):
    """
    To deleting book and redirect to home after deleting.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        return redirect('home')  # Redirect to the home page after deletion

    return render(request, 'library/delete_book.html', {'book': book})

def edit_author(request, pk):
    """
    To edit author and redirect to home after editing.
    """
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after saving changes
    else:
        form = AuthorForm(instance=author)
    return render(request, 'library/edit_author.html', {'form': form})

def delete_author(request, pk):
    """
    To deleting author and redirect to home after deleting.
    """
    author = get_object_or_404(Author, pk=pk)
    
    if request.method == 'POST':
        author.delete()
        return redirect('home')  # Redirect to the home page after deletion

    return render(request, 'library/delete_author.html', {'author': author})
