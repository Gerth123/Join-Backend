from rest_framework import serializers

def validate_no_html(value):
        errors = []

        if '<' in value:
            errors.append('No HTML tag < allowed.')
        if '>' in value:
            errors.append('No HTML tag > allowed.')
        if errors:
            raise serializers.ValidationError(errors)
        return value