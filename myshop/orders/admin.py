from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
from .admin_actions import export_to_csv
from django.urls import reverse

def order_pdf(obj: Order):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')

order_pdf.sort_description = 'Invoice'

def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


export_to_csv.short_description = 'Export to CSV'

def order_payment(obj: Order):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" trget="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''

order_payment.sort_description = 'Stripe payment'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "paid",
        order_payment,   
        "created",
        "updated",
        order_detail,
        order_pdf
    ]
    
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]