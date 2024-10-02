# 🎓 Library Management System

This project is a Django-based Library Management System. It allows users (both admin and clients) to manage books and authors, handle transactions (buying, renting, and returning books), and perform user authentication and registration.

## 🌐 Live Demo

[My website](https://yousefhani.pythonanywhere.com/)

## Features

- **Authentication**: Users can sign up, log in, and log out.
- **User Roles**: Admin users can manage books and authors, while clients can only rent or buy books.
- **Book & Author Management**:
  - Admins can add, edit, and delete books and authors.
  - Clients can search for available books and authors.
- **Transactions**: Clients can buy or rent books and return rented books. 
- **Search Functionality**: Admin can search for books by title or authors by name.
- **Session Management**: Sessions expire after 7 days of inactivity.

## Installation

Follow the steps below to set up and run the project locally:

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL
- **Version Control:** Git/GitHub

### Prerequisites

- Python 3.x
- Django 4.x
- PostgreSQL (or any other preferred database)

### 🛠️ Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/youseifMahmoud/library-management-system.git
    cd library-management-system
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    Ensure PostgreSQL is running and create a database for the project. Then configure `DATABASES` in `settings.py` with your database credentials.

5. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser** (admin account):
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the server**:
    ```bash
    python manage.py runserver
    ```

8. **Access the application**:
    - Admin interface: `http://127.0.0.1:8000/admin`
    - Application home: `http://127.0.0.1:8000`

## Usage

- **Admin Dashboard**: Admins can log in and manage books and authors, view all transactions, and handle user registrations.
- **Client Interface**: Clients can search, rent, or buy books and view available authors. They can also return rented books.
- **Authentication**: Users need to log in to access any part of the app, with different views depending on their role (admin or client).

## Key Views

- `home(request)`: Admin home page where books and authors can be added or searched.
- `client_page(request)`: Client page where clients can search for books.
- `buy_or_rent_book(request, book_id, transaction_type)`: Handle book purchase or rental.
- `return_book(request, book_id)`: Handle the return of rented books.
- `login_view(request)`: User login functionality.
- `signup(request)`: User registration functionality.
- `logout_view(request)`: Log out a user.

## Models

- `Book`: Represents books in the system.
- `Author`: Represents authors.
- `Transaction`: Tracks book transactions (buying and renting).

## Forms

- `BookForm`: Form to create or edit books.
- `AuthorForm`: Form to create or edit authors.
- `CustomUserCreationForm`: Form for user registration.

## Templates

Templates are located in the `library/templates/library/` directory. The key templates include:

- `index.html`: Landing page.
- `home.html`: Admin home page.
- `client.html`: Client page for searching and interacting with books.
- `login.html`: Login form.
- `signup.html`: Sign-up form.

## 📦 Folder Structure

```bash
   📦 library-management-system/
   ├── 📁 library/                     # Django app directory
   │   ├── 📁 migrations/              # Database migration files
   │   ├── 📁 templates/
   │   │   └── 📁 library/             # HTML templates
   │   │       ├── base.html           # Base template for the app
   │   │       ├── index.html          # Landing page
   │   │       ├── home.html           # Admin dashboard page
   │   │       ├── client.html         # Client page
   │   │       ├── login.html          # Login form
   │   │       ├── signup.html         # Sign-up form
   │   │       ├── edit_book.html      # Edit book page
   │   │       ├── delete_book.html    # Delete book confirmation page
   │   │       ├── edit_author.html    # Edit author page
   │   │       └── delete_author.html  # Delete author confirmation page
   │   ├── 📁 static/                  # Static files (CSS, JS)
   │   │   ├── 📁 css/                 # CSS files
   │   │   │    └── styles.css          # General stylesheet
   │   │   └── 📁 js/                  # JS files
   │   │       └── main.js              # General 
   │   ├── 📄 admin.py                 # Admin configurations
   │   ├── 📄 apps.py                  # Application settings
   │   ├── 📄 forms.py                 # Form definitions (BookForm, AuthorForm, CustomUserCreationForm)
   │   ├── 📄 models.py                # Model definitions (Book, Author, Transaction)
   │   ├── 📄 urls.py                  # URL configurations for this app
   │   ├── 📄 views.py                 # View functions (home, login, client_page, etc.)
   │   └── 📄 tests.py                 # Unit tests for the app
   ├── 📁 library_project/             # Main Django project directory
   │   ├── 📄 __init__.py              # Project initialization
   │   ├── 📄 settings.py              # Project settings
   │   ├── 📄 urls.py                  # Root URL configurations
   │   ├── 📄 wsgi.py                  # WSGI config for deployment
   │   └── 📄 asgi.py                  # ASGI config for deployment
   ├── 📄 .gitignore                   # Files and directories to be ignored by Git
   ├── 📄 manage.py                    # Django's command-line utility
   ├── 📄 README.md                    # Project documentation
   └── 📄 requirements.txt             # Python dependencies

```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


