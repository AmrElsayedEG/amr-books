from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from utils import isAdminUser, isVisitorUser
from rest_framework.permissions import IsAuthenticated
from books.serializers import BorrowBookSerializer, BorrowBookDetailsSerializer, UpdateBorrowBookSerializer
from books.models import BorrowRecord
from books.filters import BorrowFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class BorrowBookAPIView(ListCreateAPIView):
    queryset = BorrowRecord.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated, isAdminUser,]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = BorrowFilter

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST':
            mutable_data = self.request.data.copy()
            mutable_data['approved_by'] = self.request.user.id
            kwargs['data'] = mutable_data
        return super().get_serializer(*args, **kwargs)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BorrowBookDetailsSerializer
        return BorrowBookSerializer

class RetrieveUpdateBorrowRecordAPIView(RetrieveUpdateAPIView):
    queryset = BorrowRecord
    serializer_class = UpdateBorrowBookSerializer
    permission_classes = [IsAuthenticated, isAdminUser,]

class MyBorrowedBooks(ListAPIView):
    queryset = BorrowRecord
    serializer_class = BorrowBookDetailsSerializer
    permission_classes = (IsAuthenticated, isVisitorUser,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = BorrowFilter

    def get_queryset(self):
        return self.request.user.borrowed_books.order_by('-return_date')