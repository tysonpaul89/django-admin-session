from django.db import models

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Stock Category")

    def __str__(self):
        return self.name

class MarketCapitalization(models.TextChoices):
    UNKNOWN = ("U", "Unknown")
    SMALL = ("S", "Smallcap")
    MID = ("M", "Midcap")
    LARGE = ("L", "Largecap")

class Stock(models.Model):
    name = models.CharField(max_length=100, verbose_name="Company Name")
    symbol = models.CharField(max_length=10, verbose_name="Stock Symbol")
    listing_date = models.DateField(verbose_name="Stock Listing Date")
    isin = models.CharField(max_length=20, unique=True, verbose_name="ISIN Number")
    market_cap = models.CharField(
        max_length=1,
        choices=MarketCapitalization.choices,
        default=MarketCapitalization.UNKNOWN,
        verbose_name="Market Capitalization"
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)


    def __str__(self):
        return f"{self.name}({self.symbol})"
