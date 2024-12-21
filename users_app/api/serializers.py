from contacts_app.models import Contact
from users_app.models import UserProfile
from rest_framework import serializers
from contacts_app.api.serializers import ContactSerializer
from django.contrib.auth.models import User
from utils.validators import validate_no_html

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']

# class UsersSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=100, validators=[validate_no_html])
#     email = serializers.CharField(max_length=100, validators=[validate_no_html])
#     phone = serializers.CharField(max_length=15, validators=[validate_no_html])
#     color = serializers.CharField(max_length=7, validators=[validate_no_html])
#     contacts = ContactSerializer(many=True, read_only=True)

class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, validators=[validate_no_html])
    email = serializers.CharField(max_length=100, validators=[validate_no_html])
    phone = serializers.CharField(max_length=15, validators=[validate_no_html])
    color = serializers.CharField(max_length=7, validators=[validate_no_html])
    contacts = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    
    def validate_contacts(self, value):
        contacts = Contact.objects.filter(id__in=value)
        if len(contacts) != len(set(value)):
            raise serializers.ValidationError("One or more contacts not found.")    
        return value
    
    def create(self, validated_data):
        contact_ids = validated_data.pop('contacts')
        user = UserProfile.objects.create(**validated_data)
        contacts = Contact.objects.filter(id__in=contact_ids)
        user.contacts.set(contacts)
        return user
    
class RegistrationSerializer(serializers.Serializer):

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password'] 
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        if pw != repeated_pw:
            raise serializers.ValidationError("Passwords don't match.")
        
        account = User(username=self.validated_data['username'], email=self.validated_data['email'])
        account.set_password(pw)
        account.save()
        return account
