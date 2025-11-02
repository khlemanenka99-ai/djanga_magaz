from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Product, Category, ProductImage, Orders, OrderItem


def export_selected_to_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "Данные"
    headers = ['ID', 'name', 'description', 'price']
    ws.append(headers)
    for obj in queryset:
        ws.append([obj.id, obj.name, obj.description, obj.price])
    response = HttpResponse(
            content_type='application/vnd.openpyxl.spreadsheetml.sheet',
        )
    response['Content-Disposition'] = 'attachment; filename=exported_data.xlsx'
    wb.save(response)
    return response
export_selected_to_excel.short_description = "Экспортировать выбранные в Excel"

class ProductImageInline(admin.TabularInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'price', 'quantity', 'in_stock',)
    list_filter = ('in_stock', 'category',)
    search_fields = ('name',)
    actions = [export_selected_to_excel]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('user', 'status', 'phone', 'address',)
    list_filter = ('status',)


