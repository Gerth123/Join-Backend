from rest_framework import serializers
from tasks_app.models import Task, Subtask, AssignedContact
from contacts_app.models import Contact

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'title', 'checked']

class TaskSerializer(serializers.ModelSerializer):
    subtasks = serializers.SerializerMethodField()  
    assigned = serializers.SerializerMethodField() 
    subtasks_data = serializers.ListField(child=serializers.DictField(), write_only=True) 
    assigned_data = serializers.ListField(child=serializers.DictField(), write_only=True)  

    class Meta:
        model = Task
        fields = '__all__'

    def get_subtasks(self, obj):
        subtasks = Subtask.objects.filter(task=obj)
        return [{'id': subtask.id, 'title': subtask.title, 'checked': subtask.checked} for subtask in subtasks]

    def get_assigned(self, obj):
        return [
            {"name": contact.name, "color": assigned_contact.color}
            for assigned_contact in AssignedContact.objects.filter(task=obj)
            for contact in [assigned_contact.contact]
        ]

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks_data', [])  
        assigned_data = validated_data.pop('assigned_data', []) 
        task = Task.objects.create(**validated_data)
        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)
        for assigned in assigned_data:
            contact_name = assigned.get('name')
            contact_color = assigned.get('color')
            try:
                contact = Contact.objects.get(name=contact_name)
                AssignedContact.objects.create(task=task, contact=contact, color=contact_color)
            except Contact.DoesNotExist:
                raise serializers.ValidationError(f"Contact '{contact_name}' does not exist.")
        return task
    
    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks_data', [])
        assigned_data = validated_data.pop('assigned_data', [])
        self.update_task_fields(instance, validated_data)
        self.update_or_create_subtasks(instance, subtasks_data)
        self.update_or_create_assignments(instance, assigned_data)
        return instance

    def update_task_fields(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

    def update_or_create_subtasks(self, instance, subtasks_data):
        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get('id')
            if subtask_id:
                Subtask.objects.filter(id=subtask_id).update(
                    title=subtask_data.get('title'),
                    checked=subtask_data.get('checked')
                )
            else:
                Subtask.objects.create(task=instance, **subtask_data)

    def update_or_create_assignments(self, instance, assigned_data):
        for assigned in assigned_data:
            contact_name = assigned.get('name')
            contact_color = assigned.get('color')
            try:
                contact = Contact.objects.get(name=contact_name)
                AssignedContact.objects.update_or_create(
                    task=instance,
                    contact=contact,
                    defaults={'color': contact_color}
                )
            except Contact.DoesNotExist:
                raise serializers.ValidationError(
                    f"Contact '{contact_name}' does not exist."
                )


