import csv
from datetime import datetime
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from stock.models import MarketCapitalization, Stock, Category

class CategoryAdmin(admin.ModelAdmin):
    pass

class StockAdmin(admin.ModelAdmin):
    list_display = ("symbol", "name", "market_cap", "category", "isin")
    search_fields = ("name", "symbol", "isin")
    list_filter = ("market_cap", "category")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload-stock-data/', self.admin_site.admin_view(self.upload_stock_data), name="upload"),
        ]
        return my_urls + urls

    def upload_stock_data(self, request):
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
        )

        if request.method == "POST":
            stocks = []

            file = request.FILES['stock_data']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            next(reader) # Skipping header rows
            for row in reader:
                stock = Stock(
                    symbol=row[0],
                    name=row[1],
                    listing_date=datetime.strptime(row[2], "%d-%b-%Y").date(),
                    isin=row[3]
                )

                market_cap = row[4].strip().lower()
                if market_cap == 'smallcap':
                    stock.market_cap = MarketCapitalization.SMALL
                elif market_cap == 'midcap':
                    stock.market_cap = MarketCapitalization.MID
                elif market_cap == 'largecap':
                    stock.market_cap = MarketCapitalization.LARGE
                else:
                    stock.market_cap = MarketCapitalization.UNKNOWN

                category, created = Category.objects.get_or_create(name__iexact=row[5], defaults={'name': row[5]})
                stock.category = category

                stocks.append(stock)

            Stock.objects.bulk_create(stocks)
            return redirect(reverse_lazy('admin:index'))

        return render(request, 'upload-stock-data.html', context)

admin.site.register(Stock, StockAdmin)
admin.site.register(Category, CategoryAdmin)
