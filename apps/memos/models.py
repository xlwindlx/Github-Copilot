from django.db import models
from django.conf import settings


class Memo(models.Model):
	class MemoCategory(models.TextChoices):
		DAILY = "daily", "일상"
		WORK = "work", "업무"
		PERSONAL = "personal", "개인"

	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="memos",
	)
	title = models.CharField(max_length=200)
	body = models.TextField()
	category = models.CharField(
		max_length=20,
		choices=MemoCategory.choices,
		null=True,
		blank=True,
		db_index=True,
	)
	is_public = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-updated_at", "-created_at"]

	def __str__(self) -> str:
		return f"{self.title}"

# Create your models here.
