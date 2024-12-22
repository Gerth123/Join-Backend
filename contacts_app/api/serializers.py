from rest_framework import serializers
from contacts_app.models import Contact
from utils.validators import validate_no_html

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'phone', 'color', 'user_id')
        extra_kwargs = {
            'name': {'validators': [validate_no_html]},
            'email': {'validators': [validate_no_html]},
            'phone': {'validators': [validate_no_html]},
            'color': {'validators': [validate_no_html]},
        }

    def create(self, validated_data):
        return Contact.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.color = validated_data.get('color', instance.color)
        instance.save()
        return instance

