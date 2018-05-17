from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Dinner_platter(models.Model):
    name = models.CharField(max_length=64)
    price_small = models.DecimalField(max_digits=5, decimal_places=2)
    price_large = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} (small - {self.price_small}, large - {self.price_large})"


class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} (price - {self.price})"


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} (price - {self.price})"


class Sub_addon(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.id} - {self.name} (price - {self.price})"


class Sub(models.Model):

    name = models.CharField(max_length=64)
    price_small = models.DecimalField(max_digits=5, decimal_places=2)
    price_large = models.DecimalField(max_digits=5, decimal_places=2)
    amount_addons = models.PositiveSmallIntegerField(default=1)
   
    def __str__(self):
        return f"{self.name} (price for small - {self.price_small}, price for large - {self.price_large}, amount of addons - {self.amount_addons})"


class Topping(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"


class Reg_Pizza(models.Model):
    kind = models.CharField(max_length=64)
    price_small = models.DecimalField(max_digits=5, decimal_places=2)
    price_large = models.DecimalField(max_digits=5, decimal_places=2)
    amount_toppings = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.kind} (price for small - {self.price_small}, price for large - {self.price_large}, amount of toppings - {self.amount_toppings})"


class Syc_Pizza(models.Model):
    kind = models.CharField(max_length=64)
    price_small = models.DecimalField(max_digits=5, decimal_places=2)
    price_large = models.DecimalField(max_digits=5, decimal_places=2)
    amount_toppings = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.kind} (price for small - {self.price_small}, price for large - {self.price_large}, amount of toppings - {self.amount_toppings})"


class Size(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"



STATUS_CHOICES = (
    ('d', 'Declined'),
    ('c', 'Completed'),
    ('p', 'Pending'),
)


class Order(models.Model):
    consumer = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.CharField(max_length=64)
    kind = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    topping =  models.ManyToManyField(Topping, blank=True, related_name="pizza")
    addon =  models.ManyToManyField(Sub_addon, blank=True, related_name="sub")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="p")
    ordered = models.BooleanField(default=False)

    def __str__(self):
        if self.ordered:
            if self.dish == "Sub" or self.dish == "Dinner platter":
                addons = ""
                for i in self.addon.all():
                    addons += " + "+ i.name

                return f"{self.dish} : {self.kind} {addons} ({self.size.name}) - ${self.price} by {self.consumer.username}"
            
            elif self.dish == "Regular pizza" or self.dish == "Sicilian pizza":
                toppings = ""
                for i in self.topping.all():
                    toppings += " + "+ i.name

                return f"{self.dish} : {self.kind} {toppings} ({self.size.name}) - ${self.price} by {self.consumer.username}"

            else:
                return f"{self.dish}: {self.kind} ({self.price}) by {self.consumer.username}"
        else:
            return "Waiting for confirmation"