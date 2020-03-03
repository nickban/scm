from django.contrib import admin
from .models import (Sample, User, Style, Brand, Merchandiser, Designer,
                     Factory, Shipping, Qc, Finance, Office, Admin,
                     Merchandiser_Manager, Post, PostAttachment,
                     Sample_os_avatar, Order, Order_color_ratio_qty,
                     Order_size_specs, Invoice, Order_fitting_sample,
                     Mainlabel, Maintag, Addtiontag, Packingtype, Order_packing_ctn,
                     Order_packing_status)

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
admin.site.register(Order_size_specs)
admin.site.register(Invoice)
admin.site.register(Order_fitting_sample)
admin.site.register(Mainlabel)
admin.site.register(Maintag)
admin.site.register(Addtiontag)
admin.site.register(Packingtype)
admin.site.register(Order_packing_ctn)
admin.site.register(Order_packing_status)

