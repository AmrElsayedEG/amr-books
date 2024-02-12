from django.db import models
from users.models import User

def book_image_location(instance, filename):
    return f"books/{instance.title}_{filename}"

class Book(models.Model):
    title = models.CharField(max_length=300)
    author_name = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to=book_image_location)
    amount_available = models.BigIntegerField()
    active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    @property
    def borrow_available(self):
        return self.active and self.amount_available > 0