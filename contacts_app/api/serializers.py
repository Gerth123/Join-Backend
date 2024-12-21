from rest_framework import serializers
from contacts_app.models import Contact

def validate_no_html(value):
        errors = []

        if '<' in value:
            errors.append('No HTML tag < allowed.')
        if '>' in value:
            errors.append('No HTML tag > allowed.')
        if errors:
            raise serializers.ValidationError(errors)
        return value

class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, validators=[validate_no_html])
    email = serializers.CharField(max_length=100, validators=[validate_no_html])
    phone = serializers.CharField(max_length=15, validators=[validate_no_html])
    color = serializers.CharField(max_length=7, validators=[validate_no_html])

    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'phone', 'color')

    def create(self, validated_data):
        return Contact.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.color = validated_data.get('color', instance.color)
        instance.save()
        return instance

