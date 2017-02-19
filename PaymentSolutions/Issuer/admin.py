from django.contrib import admin

from .models import Account, CardInstrument, Transaction, Transfer, Currency, Merchant

admin.site.register(Account)
admin.site.register(CardInstrument)
admin.site.register(Transaction)
admin.site.register(Transfer)
admin.site.register(Currency)
admin.site.register(Merchant)
