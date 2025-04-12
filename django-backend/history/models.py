from django.db import models
from guardian.models import Child  # Make sure this is the correct import

class History(models.Model):
    child = models.ForeignKey(Child, related_name="histories", on_delete=models.CASCADE)
    visited_url = models.URLField()  # Store the URL that was visited
    title = models.CharField(max_length=255, blank=True, null=True)  # Store the title of the page
    visit_time = models.DateTimeField(auto_now_add=True)  # When the URL was visited

    def __str__(self):
        return f"History of {self.child.name} - {self.visited_url}"
