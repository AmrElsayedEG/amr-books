from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils import canUpdateBooks, UserRoleChoices
from books.models import Book
from books.serializers import BookSerializer, AdminBookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class BookSerializerMixin:
    def get_serializer_class(self):
        if self.request.user.role == UserRoleChoices.ADMIN:
            return AdminBookSerializer
        return BookSerializer

class ListCreateBookAPIView(BookSerializerMixin, ListCreateAPIView):
    queryset = Book.objects.all()
    # Only Admin can Create Books
    permission_classes = (IsAuthenticated, canUpdateBooks,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields   = ['author_name', 'active']
    search_fields = ['title', 'author_name']

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST':
            mutable_data = self.request.data.copy()
            mutable_data['added_by'] = self.request.user.id
            kwargs['data'] = mutable_data
        return super().get_serializer(*args, **kwargs)
    
class RetrieveUpdateDeleteBookAPIView(BookSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = Book
    serializer_class = BookSerializer
    # Only Admin can Update or Delete Book
    permission_classes = (IsAuthenticated, canUpdateBooks,)