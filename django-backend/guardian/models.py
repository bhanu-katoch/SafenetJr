from django.db import models
from django.contrib.auth.models import User
import uuid


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link parent to user for authentication
    parent_id = models.CharField(max_length=50, unique=True, blank=True)  # Unique Parent ID

    def save(self, *args, **kwargs):
        if not self.parent_id:
            self.parent_id = str(uuid.uuid4())[:8]  # Generate unique ID
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} ({self.parent_id})'

class Child(models.Model):
    parent = models.ForeignKey(Parent, related_name="children", on_delete=models.CASCADE)
    child_number = models.PositiveIntegerField()
    child_id = models.CharField(max_length=50, unique=True, blank=True)  # Child's unique ID
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.child_id:
            self.child_id = f"{self.parent.parent_id}-{self.child_number}"  # Generate child ID based on parent_id and child_number
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.child_id})'