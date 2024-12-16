from django.db import models
from django.db import models
from django.contrib.auth.models import User
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField


class Meal(models.Model):
    CATEGORY = (
        ('Break fast', 'Break fast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),


    )
    name = models.CharField(max_length=190, null=True)
    price = models.FloatField( null=True)
    category = models.CharField(max_length=190, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(blank=True, null=True, default="preson.png")

    def __str__(self):
         return self.name


class Customer(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=190, null=True)
    email = models.CharField(max_length=190, null=True)
    phone = models.CharField(max_length=190, null=True)
    age = models.CharField(max_length=190, null=True)
    image = models.ImageField(blank=True, null=True, default="preson.png")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Employe(models.Model):
    JOP_TITLE = (
        ('cooking chef', 'cooking chef'),
        ('presta', 'presta'),
        ('stafe', 'stafe'),
        ('manager', 'manager'),

    )
    first_name = models.CharField(max_length=190, null=True)
    last_name = models.CharField(max_length=190, null=True)
    title = models.CharField(max_length=190, null=True)
    jop_title = models.CharField(max_length=190, null=True, choices=JOP_TITLE)
    salary = models.FloatField( null=True)
    email = models.CharField(max_length=190, null=True)
    phone = models.CharField(max_length=190, null=True)
    age = models.CharField(max_length=190, null=True)
    image = models.ImageField(blank=True, null=True, default="preson.png")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    details = models.ManyToManyField(Meal, through='OrderDetail')
    is_finished = models.BooleanField()
    total = 0
    items_count = 0

    def __str__(self):
        return 'User: ' + self.user.username + 'Order id' + str(self.id)


class OrderDetail(models.Model):
    product = models.ForeignKey(Meal, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return 'Order: {}, Book: {}, Order id: {}'.format(self.order.user.username, self.product.name, self.order.id)

    class Meta:
        ordering=['id']


class BookTable(models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField()
        date_reservation =models.EmailField()
        num_people = models.IntegerField()
        message = models.TextField()

        def __str__(self):
            return f"{self.name}'s Booking at {self.date_reservation}"



class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=190, null=True)
    email = models.CharField(max_length=190, null=True)
    subject = models.CharField(max_length=190, null=True)
    message = models.CharField(max_length=190, null=True)

    def __str__(self):
        return self.subject


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_address = models.CharField(max_length=150)
    shipment_phone = models.CharField(max_length=50)
    card_number = CardNumberField()
    expire = CardExpiryField()
    security_code = SecurityCodeField()

    def __str__(self):
        return self.order


class CashPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_address = models.CharField(max_length=150)
    shipment_phone = models.CharField(max_length=50)

    def __str__(self):
        return f"Cash Payment for Order {self.order.id}"  # أو استخدم أي معلومة نصية مرتبطة بالطلب
