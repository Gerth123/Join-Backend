from contacts_app.models import Contact
from users_app.models import UserProfile
from rest_framework import serializers
from contacts_app.api.serializers import ContactSerializer
from django.contrib.auth.models import User
from utils.validators import validate_no_html
from users_app.dummy_data import test_contacts, test_tasks
from tasks_app.models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        exclude = ('user',)


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, validators=[validate_no_html])
    email = serializers.CharField(
        max_length=100, validators=[validate_no_html])
    phone = serializers.CharField(max_length=15, validators=[validate_no_html])
    color = serializers.CharField(max_length=7, validators=[validate_no_html])
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email', 'phone', 'color', 'contacts']

#     def validate_contacts(self, value):
#         contacts = Contact.objects.filter(id__in=value)
#         if len(contacts) != len(set(value)):
#             raise serializers.ValidationError("One or more contacts not found.")
#         return value

#     def create(self, validated_data):
#         contact_ids = validated_data.pop('contacts')
#         user = UserProfile.objects.create(**validated_data)
#         test_contact_instances = Contact.objects.filter(id__in=test_contacts)
#         user.contacts.set(test_contact_instances)
#         if contact_ids:
#             additional_contacts = Contact.objects.filter(id__in=contact_ids)
#             user.contacts.add(*additional_contacts)
#         return user


# class RegistrationSerializer(serializers.Serializer):

#     repeated_password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'repeated_password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def save(self):
#         pw = self.validated_data['password']
#         repeated_pw = self.validated_data['repeated_password']
#         if pw != repeated_pw:
#             raise serializers.ValidationError("Passwords don't match.")

#         account = User(username=self.validated_data['username'], email=self.validated_data['email'])
#         account.set_password(pw)
#         account.save()
#         return account

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self):
        password = self.validated_data['password']
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        user.set_password(password)
        user.save()

        user_profile = UserProfile.objects.create(user=user)

        for contact_data in test_contacts:
            contact, created = Contact.objects.get_or_create(
                name=contact_data['name'],
                email=contact_data['email'],
                phone=contact_data['phone'],
                color=contact_data['color'],
                user_id = user.id
            )
            user_profile.contacts.add(contact)

        # for task_group in test_tasks:
        #     for task_data in task_group['items']:
        #         category_name = task_data['category'] 
        
        #         category, created = Category.objects.get_or_create(
        #             name=category_name
        #         )

        #         task = Task.objects.create(
        #             title=task_data['title'],
        #             description=task_data['description'],
        #             category=category, 
        #             date=task_data['date'],
        #             priority=task_data['priority']
        #         )
        
        #         for subtask in task_data.get('subtasks', []):
        #             subtask_instance = Subtask.objects.create(
        #                 task=task, 
        #                 title=subtask['task'],
        #                 checked=subtask['checked']
        #             )
        
        #         user_profile.tasks.add(task)
                # for assigned_user_data in task_data['assigned']:
                #     user_profile = UserProfile.objects.get(name=assigned_user_data['name'])
        return user
    

class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                username = user.username 
            except User.DoesNotExist:
                raise serializers.ValidationError("Benutzer mit dieser E-Mail existiert nicht.")

            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Ungültige Anmeldedaten.")
        else:
            raise serializers.ValidationError("E-Mail und Passwort sind erforderlich.")

        attrs['user'] = user
        return attrs
