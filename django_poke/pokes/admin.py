from django.contrib import admin
from pokes.models import User, Poke

class PokeAdmin(admin.ModelAdmin):
  list_display = ('send_user', 'receive_user', 'poke_date', 'was_poked_recently')
  list_filter = ['poke_date']
  search_fields = ['send_user', 'receive_user']

  fieldsets = [
    ('Poke sender', {'fields': ['send_user']}),
    ('Poke receiver', {'fields': ['receive_user']}),
    ('Date information', {'fields': ['poke_date'], 'classes': ['collapse']}),
  ]
    

admin.site.register(Poke, PokeAdmin)