from django.contrib import admin
from .models import Stock, Position, Quote, Balance

# import json
import finnhub
# from alpha_vantage.timeseries import TimeSeries

# Setup client
finnhub_client = finnhub.Client(api_key="buhih2748v6seskai4n0")
# alpha_vantage = TimeSeries(key='GSG7BQGSGDY9PASO')

# Register your models here.
class StockAdmin(admin.ModelAdmin):
    list_display = ('companyName', 'symbol', 'description')
    search_fields = ['companyName',  'symbol']

    class Media:
        js = ("js/prefillstockdata.js",)

class PositionAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'size', 'price', 'open', 'datetime')
    search_fields = ['symbol__symbol']

    autocomplete_fields = ['symbol']

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'datetime', 'price')
    search_fields = ['symbol__symbol']

    autocomplete_fields = ['symbol']


class BlanceAdmin(admin.ModelAdmin):
    list_display = ('datetime',)
    search_fields = ['datetime']


admin.site.register(Stock, StockAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Balance, BlanceAdmin)

