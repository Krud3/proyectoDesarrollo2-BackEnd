from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Auction(models.Model):
    auction_id = models.AutoField(primary_key=True)
    auction_name = models.CharField(max_length=255, verbose_name=_("Nombre de la subasta"))
    auction_description = models.TextField()
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False, default=timezone.now)
    status = models.CharField(max_length=20, choices=(('active', _('Active')), ('inactive', _('Inactive'))), default='active')

    class Meta:
        db_table = 'auctions'
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
        ]

    def __str__(self):
        return self.auction_name

    def clean(self):
        super().clean()
        if self.end_date and self.start_date and self.end_date <= self.start_date:
            raise ValidationError(_("La fecha de finalización debe ser posterior a la fecha de inicio."))

class Artwork(models.Model):
    artwork_id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    year_created = models.IntegerField()
    dimensions = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    minimum_bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    status = models.CharField(max_length=20, choices=(('active', _('Active')), ('inactive', _('Inactive'))), default='active')

    class Meta:
        db_table = 'artworks'

    def __str__(self):
        return self.title

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    document_type = models.CharField(max_length=50, blank=False, null=False, default='ID')
    document_number = models.CharField(max_length=50, blank=False, null=False, default='')

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.full_name

class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bid_value = models.DecimalField(max_digits=10, decimal_places=2)
    bid_timestamp = models.DateTimeField(null=False)

    class Meta:
        db_table = 'bids'

    def __str__(self):
        return f"Bid #{self.bid_id} - {self.customer.full_name} - {self.artwork.title}"

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)  # Campo para indicar si el usuario es administrador

    class Meta:
        db_table = 'admins'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
