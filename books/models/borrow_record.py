from django.db import models
from .book import Book
from users.models import User

class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_borrows')
    borrow_date = models.DateTimeField()
    return_date = models.DateTimeField()
    returned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Borrow Record'
        verbose_name_plural = 'Borrow Records'