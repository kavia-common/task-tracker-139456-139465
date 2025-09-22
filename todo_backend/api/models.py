from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base model with created/updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the record was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the record was last updated")

    class Meta:
        abstract = True


class Todo(TimeStampedModel):
    """Todo item owned by a user."""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="todos",
        help_text="User who owns this todo",
    )
    title = models.CharField(max_length=255, help_text="Short title for the todo")
    description = models.TextField(blank=True, help_text="Optional longer description")
    is_completed = models.BooleanField(default=False, help_text="Completion status")
    due_date = models.DateTimeField(null=True, blank=True, help_text="Optional due date/time")

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "is_completed"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.title} ({'done' if self.is_completed else 'open'})"
