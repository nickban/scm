from django.contrib import admin
from .models import (Sample, User, Style, Brand, Merchandiser, Designer,
                     Factory, Shipping, Qc, Finance, Office, Admin,
                     Merchandiser_Manager, Post, PostAttachment,
                     Sample_os_avatar, Order, Order_color_ratio_qty)

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
admin.site.register(PostAttachment)
admin.site.register(Sample_os_avatar)
admin.site.register(Order)
admin.site.register(Order_color_ratio_qty)
