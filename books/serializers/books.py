from rest_framework import serializers
from books.models import Book, BorrowRecord
from django.db.transaction import atomic
from users.serializers import UserSerializer
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author_name', 'cover_image', 'borrow_available',)
        # extra_kwargs = {'active' : {'write_only':True}}

class AdminBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author_name', 'cover_image', 'borrow_available', 'active', 'amount_available', 'added_by')

class BorrowBookSerializer(serializers.ModelSerializer):

    error_msg = {
        "already_borrowed" : {
            "error" : "This user already borrowed that book and not returned it yet!"
        },
        "borrow_unavailable" : {
            "error" : "Sorry, This book can\'t be borrowed due to low quantity or not active"
        },
        "date_in_past" : {
            "error" : "Please check the dates"
        }
    }

    class Meta:
        model = BorrowRecord
        fields = '__all__'

    def validate(self, attrs):
        print(self.context['view'].kwargs.get('pk'))
        product = BorrowRecord.objects.filter(book=attrs['book'], borrower=attrs['borrower'], returned=False)

        if product.exists():
            raise serializers.ValidationError(self.error_msg['already_borrowed'])
        
        if not attrs['book'].borrow_available:
            raise serializers.ValidationError(self.error_msg['borrow_unavailable'])
        
        if attrs['borrow_date'] > attrs['return_date']:
            raise serializers.ValidationError(self.error_msg['date_in_past'])

        return attrs
    
    @atomic
    def create(self, validated_data):
        new_obj = super().create(validated_data)
        book = new_obj.book
        book.amount_available -= 1
        book.save()
        return new_obj
    
class BorrowBookDetailsSerializer(serializers.ModelSerializer):
    borrower = UserSerializer()
    book = BookSerializer()

    class Meta:
        model = BorrowRecord
        fields = '__all__'

class UpdateBorrowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ('returned', 'return_date',)

    @atomic
    def update(self, instance, validated_data):
        returned = validated_data.get('returned', None)
        if returned is not None:
            book = instance.book
            if instance.returned != returned:
                book.amount_available += 1 if returned and not instance.returned else -1
                book.save()
        return super().update(instance, validated_data)