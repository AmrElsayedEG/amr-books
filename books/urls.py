from django.urls import path
from .views import *

app_name = 'books'

urlpatterns = [
    # Get - Create Product Endpoint
   path('', ListCreateBookAPIView.as_view(), name='get_create_books'),

   # Retrieve - Update - Delete Book Endpoint
   path('<int:pk>/', RetrieveUpdateDeleteBookAPIView.as_view(), name='crud_books'),

   # Borrow Book List - Create
   path('borrow/', BorrowBookAPIView.as_view(), name='borrow_book'),

   # Update - Retrieve Borrow Record
   path('borrow/<int:pk>/', RetrieveUpdateBorrowRecordAPIView.as_view(), name='retrieve_update_book'),

   # List my borrowed books
   path('borrow/me/', MyBorrowedBooks.as_view(), name='list_my_borrowed_books')
]