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
    size = models.ForeignKey('Size', on_delete=models.CASCADE, null=True)
    color = models.ForeignKey('Color', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='uploads')
    discount = models.IntegerField(default=0)
    is_new = models.BooleanField()
    is_best_seller = models.BooleanField()
    short_description = models.TextField(max_length=500)
    description = models.TextField(max_length=1000, null=True)
    details = models.TextField(max_length=1000, null=True)

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


class Cart(models.Model):
    title = models.CharField(max_length=300, blank=True, default='')
    email = models.CharField(max_length=200, blank=True, default='')
    last_name = models.CharField(max_length=200, blank=True, default='')
    first_name = models.CharField(max_length=200, blank=True, default='')
    zip_code = models.CharField(max_length=200, blank=True, default='')
    country = models.CharField(max_length=200, blank=True, default='')
    city = models.CharField(max_length=200, blank=True, default='')
    person = models.CharField(max_length=200, blank=True, default='')
    phone = models.CharField(max_length=200, blank=True, default='')
    address = models.CharField(max_length=200, blank=True, default='')
    payed = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    session_id = models.CharField(max_length=300, blank=True, null=True ,default='')
    amount = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    orig_price = models.FloatField(default=0)
    price = models.FloatField(default=0)
    is_accepted = models.BooleanField(default=False)
    

    def __str__(self):
        return self.session_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    product_price = models.IntegerField(default=0)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.product.title + ' | ' + str(self.cart.session_id)


