import csv
from datetime import datetime
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from stock.models import Stock, Category

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
                stocks.append(Stock(
                    name=row[1],
                    symbol=row[0],
                    listing_date=datetime.strptime(row[3], "%d-%b-%Y").date(),
                    isin=row[6]
                ))

            Stock.objects.bulk_create(stocks)
            return redirect(reverse_lazy('admin:index'))

        return render(request, 'upload-stock-data.html', context)

admin.site.register(Stock, StockAdmin)
admin.site.register(Category, CategoryAdmin)