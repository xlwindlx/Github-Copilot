from django.db import models
from django.conf import settings


class Memo(models.Model):
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="memos",
	)
	title = models.CharField(max_length=200)
	body = models.TextField()
	is_public = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-updated_at", "-created_at"]

	def __str__(self) -> str:
		return f"{self.title}"

# Create your models here.
