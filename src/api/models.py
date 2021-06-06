from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model

import json


class PaymentMethod(models.Model):
    SUPPORTED_METHODS = (
        ('stripe', 'Stripe'),
    )

    name = models.CharField(max_length=15, choices=SUPPORTED_METHODS)
    customer_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return '%s : %s' % (self.name, str(self.customer_id))


class KSUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    username = models.CharField(max_length=20)
    payment_method = models.OneToOneField(
        PaymentMethod, on_delete=models.CASCADE)

    def __str__(self):
        return '%s : %s' % (self.username, str(self.user.id))


class GameCategory(models.Model):
    CATEGORIES = (
        ('fps', 'FPS'),
        ('rpg', 'RPG'),
        ('racing', 'Racing'),
        ('sports', 'Sports')
    )
    name = models.CharField(max_length=20, choices=CATEGORIES)

    def __str__(self):
        return '%s' % (self.name)


class Price(models.Model):
    SUPPORTED_CURRENCIES = json.loads(
        open('./api/supported_currency.json').read())

    SUPPORTED_CURRENCIES_CHOICES = (
        (data.lower(), data.lower()) for data in SUPPORTED_CURRENCIES.get('supported'))

    amount = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(
        max_length=10, choices=SUPPORTED_CURRENCIES_CHOICES)
    price_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return '%f: %s' % (self.amount, self.currency)


class Game(models.Model):
    name = models.CharField(max_length=20)
    publisher = models.CharField(max_length=20)
    category = models.ForeignKey('GameCategory', on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'publisher']

    def __str__(self):
        return '%s: %s: %f: %s' % (self.name, self.publisher, self.price.amount, self.price.currency)


class Order(models.Model):
    ksuser = models.ForeignKey(KSUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['ksuser', 'game']

    def __str__(self):
        return '%s: %s' % (self.ksuser.username, self.game.name)


class Wishlist(models.Model):
    ksuser = models.ForeignKey(KSUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['ksuser', 'game']

    def __str__(self):
        return '%s: %s' % (self.ksuser.username, self.game.name)


class Library(models.Model):
    ksuser = models.ForeignKey(KSUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['ksuser', 'game', 'order']

    def __str__(self):
        return '%d: %s' % (self.order.id, self.game.name)
