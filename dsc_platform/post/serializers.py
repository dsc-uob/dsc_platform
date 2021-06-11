from rest_framework import serializers

from .models import Article,ArticleComment,Enquiry,EnquiryComment 
from user.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Article
        read_only = ('id','created_date','updated_date',)
        fields = '__all__'
    

class ArticleCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ArticleComment
        read_only = ('id','created_date','updated_date')
        exclude = ['article']

class EnquirySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Enquiry
        read_only = ('id','created_date','updated_date',)
        fields = '__all__'

class EnquiryCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = EnquiryComment
        read_only = ('id','created_date','updated_date',)
        exclude = ['enquiry']