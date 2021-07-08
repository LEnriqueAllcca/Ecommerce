from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse

class Administrador(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE)
    dirreccion = models.CharField(max_length=100)
    dia_creacion = models.DateField(auto_now_add=True, null=True)

    def _str_(self):
        return str(self.id)

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    @property
    def first_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def is_staff(self):
        return self.user.is_staff

    @property
    def is_active(self):
        return self.user.is_active

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def _str_(self):
        return self.name

class Proveedores(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    celular = models.CharField(max_length=150)
    correo = models.CharField(max_length=150)

    def _str_(self):
        return self.nombre
    
    
class Address(models.Model):
    ADDRESS_CHOICES = (

        ('S','Shipping'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.address_line_1},{self.address_line_2},{self.city},{self.zip_code}"

    class Meta:
        verbose_name_plural = 'Addresses'

class Product(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='product_images')
    description = models.TextField()
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False,  help_text='Activar/Desactivar', )
    primary_category = models.ForeignKey(Category, related_name='primary_products', on_delete=models.CASCADE)
    secondary_categories = models.ManyToManyField(Category, blank=True)
    stock = models.IntegerField(default=0)

    def _str_(self):
        return self.title

    def get_absolute_url(self):
        return reverse("cart:product-detail", kwargs={'slug': self.slug})

    def get_price(self):
        return "{:.2f}".format(self.price / 100)

    @property
    def in_stock(self):
        return self.stock > 0

class OrderItem(models.Model):
    order = models.ForeignKey("Order", related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default= 1)

    def _str_(self) :
        return f"{self.quantity} x {self.product.title}"

    def get_raw_total_item_price(self):
        return self.quantity * self.product.price/3.92

    def get_total_item_price(self):
        price = self.get_raw_total_item_price() #1000
        return "{:.2f}".format(price / 100)


class Order(models.Model):
    user = models.ForeignKey(User,blank=True, null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)

    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', blank=True, null=True, on_delete=models.SET_NULL)

    def _str_(self) :
        return self.reference_number

    @property
    def get_direccion(self):
        return self.shipping_address.address_line_1 + " " + self.shipping_address.address_line_2 +" (" + self.shipping_address.city +") "

    @property
    def get_name(self):
        return self.user.username + " " + self.user.last_name

    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"

    def get_raw_subtotal(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_raw_total_item_price()
        return total

    def get_subtotal(self):
        subtotal = self.get_raw_subtotal()
        return "{:.2f}".format(subtotal / 100)

    def get_raw_total(self):
        subtotal = self.get_raw_subtotal()
        #agregar suma de IGV, Delivery, Descuentos
        #total = subtotal - discounts + tax + delivery
        return subtotal

    def get_total(self):
        total = self.get_raw_total()
        return "{:.2f}".format(total / 100)



class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=(
        ('Paypal','Paypal'),
    ))
    timestamp = models.DateTimeField(auto_now_add=True)
    succesful = models.BooleanField(default=False)
    amount = models.FloatField()
    raw_response = models.TextField()

    def _str_(self) :
        return self.reference_number

    @property
    def reference_number(self):
        return f"PAYMENT-{self.order}-{self.pk}"


class Dolar_price(models.Model):
    price = models.FloatField()

    def _str_(self) :
        return self.price

    def pre_save_product_receiver(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = slugify(instance.title)

    pre_save.connect(pre_save_product_receiver, sender=Product)