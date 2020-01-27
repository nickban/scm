from django.contrib import admin
from .models import (Sample, User, Style, Brand, Merchandiser, Designer,
                     Factory, Shipping, Qc, Finance, Office, Admin, Merchandiser_Manager, Post)

admin.site.register(User)
admin.site.register(Sample)
admin.site.register(Style)
admin.site.register(Brand)
admin.site.register(Merchandiser)
admin.site.register(Designer)
admin.site.register(Factory)
admin.site.register(Finance)
admin.site.register(Office)
admin.site.register(Admin)
admin.site.register(Shipping)
admin.site.register(Qc)
admin.site.register(Merchandiser_Manager)
admin.site.register(Post)
