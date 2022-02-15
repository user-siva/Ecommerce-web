from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User,related_name='userprofile',on_delete=models.CASCADE)
	address = models.CharField(max_length=255,blank=True,null=True)
	zip_code = models.IntegerField(blank=True,null=True)
	place = models.CharField(max_length=255,blank=True,null=True)
	phone = models.IntegerField(blank=True,null=True)

	def __str__(self):
		return '%s' % self.user.username

User.UserProfile = property(lambda self:UserProfile.objects.get_or_create(user=self)[0])