from django.db import models
from django.template.defaultfilters import slugify
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.contrib.auth.models import User

class Category(models.Model):
	title = models.CharField(max_length=300)
	ordering = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = 'categories'
		ordering = ('ordering',)  #To oreder categories

	def slug(self):
		return slugify(self.title)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return '/category/%s/' %(self.pk)

class Product(models.Model):
	''' foreignkey = ManytoOne,related_name is replacement for _set.all() Here , category.products.all() '''

	category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
	variant = models.ForeignKey('self',related_name='variants',on_delete=models.CASCADE,blank=True,null=True)
	title = models.CharField(max_length=300)
	description = models.TextField(blank=True,null=True)
	price = models.FloatField()
	is_featured = models.BooleanField(default=False)
	num_available = models.IntegerField(default=1)

	date_added = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='uploads/',blank=True,null=True)
	thumbnail = models.ImageField(upload_to='uploads/',blank=True,null=True)



	class Meta:
		ordering = ('-date_added',)

	@property
	def slug(self):
		return slugify(self.title)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return '/%s/' %(self.pk)

	def make_thumbnail(self,image,size=(300,200)):
		img = Image.open(image)
		img.convert('RGB')
		img.thumbnail(size)

		thumb_io = BytesIO()
		img.save(thumb_io,'JPEG',quality=85)
		thumbnail = File(thumb_io,name=image.name)

		return thumbnail

	def get_thumbnail(self):
		if self.thumbnail:
			return self.thumbnail.url
		else:
			if self.image:
				self.thumbnail = self.make_thumbnail(self.image)
				self.save()
                
				return self.thumbnail.url
			else:
				return ''

	def save(self,*args,**kwargs):
		print('saved at',self.image.path)
		self.thumbnail = self.make_thumbnail(self.image)
		super().save(*args,**kwargs)

class ProductImage(models.Model):
	product = models.ForeignKey(Product,related_name='images',on_delete=models.CASCADE)

	image = models.ImageField(upload_to='uploads/',blank=True,null=True)
	thumbnail = models.ImageField(upload_to='uploads/',blank=True,null=True)

	def make_thumbnail(self,image,size=(300,200)):
		img = Image.open(image)
		img.convert('RGB')
		img.thumbnail(size)

		thumb_io = BytesIO()
		img.save(thumb_io,'JPEG',quality=85)
		thumbnail = File(thumb_io,name=image.name)

		return thumbnail

	def save(self,*args,**kwargs):
		print('saved at',self.image.path)
		self.thumbnail = self.make_thumbnail(self.image)
		super().save(*args,**kwargs)

class ProductReview(models.Model):

	product = models.ForeignKey(Product,related_name='reviews',on_delete=models.CASCADE)
	user = models.ForeignKey(User,related_name='reviews',on_delete=models.CASCADE)
	heading = models.CharField(max_length=100,blank=True,null=True)
	content = models.TextField(blank=True,null=True)
	date_added = models.DateTimeField(auto_now_add=True)
	stars = models.IntegerField()	

