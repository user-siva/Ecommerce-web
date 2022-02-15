from django.db import models

class Subscibers(models.Model):
	email = models.EmailField(max_length=255)
	date_added = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.email


