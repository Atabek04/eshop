from django.db import models

class Category(models.Model):
	title = models.CharField(max_length=300)
	logo = models.ImageField(upload_to='uploads')
	is_main = models.BooleanField()

	def __str__(self):
		return self.title

class Size(models.Model):
	title = models.CharField(max_length=300)

	def __str__(self):
		return self.title


class Color(models.Model):
	title = models.CharField(max_length=300)
	code = models.CharField(max_length=300)

	def __str__(self):
		return self.title

class Product(models.Model):
	title = models.CharField(max_length=300)
	views = models.IntegerField(default=0)
	rating = models.FloatField(default=0.0)
	old_price = models.IntegerField(default=0)
	new_price = models.IntegerField(default=0)
	size = models.ForeignKey('Size', on_delete=models.CASCADE, null = True)
	color = models.ForeignKey('Color', on_delete=models.CASCADE, null = True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	logo = models.ImageField(upload_to='uploads')
	discount = models.IntegerField(default=0)
	is_new = models.BooleanField()
	is_best_seller = models.BooleanField()
	short_description = models.TextField(max_length=500)
	description = models.TextField(max_length=1000, null = True)
	details = models.TextField(max_length=1000, null = True)

	def __str__(self):
		return self.title

class ProductImage(models.Model):
	product = models.ForeignKey('Product', on_delete=models.CASCADE)
	title = models.CharField(max_length=300)
	image = models.ImageField(upload_to='uploads')

	def __str__(self):
		return self.title

class CommentItem(models.Model):
	product = models.ForeignKey('Product', on_delete=models.CASCADE)
	text = models.TextField(max_length=500)
	author_name = models.CharField(max_length=300)
	author_email = models.CharField(max_length=300)
	rating = models.FloatField(default=0.0)
	pub_date = models.DateField()

	def __str__(self):
		return self.author_name



