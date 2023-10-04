from django.contrib import admin
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Order, Device, Customer, DeviceInField


# @admin.register(User)
# class CustomUserAdmin(User):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_responsible_orders')
#     list_filter = ('is_staff', 'is_superuser', 'groups', 'responsible_orders')
#
#     def get_responsible_orders(self, obj):
#         orders = obj.responsible_orders.all()
#         return format_html(', '.join([str(order) for order in orders]))
#
#     get_responsible_orders.short_description = "Ответственные задачи"


class ForeignKeyWithNameRawIdWidget(ForeignKeyRawIdWidget):
    def label_and_url_for_value(self, value):
        key = self.rel.get_related_field().name
        try:
            obj = self.rel.model._default_manager.get(**{key: value})
            return str(obj), reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        except self.rel.model.DoesNotExist:
            return super().label_and_url_for_value(value)

    def render(self, name, value, attrs=None, renderer=None):
        label, url = self.label_and_url_for_value(value)
        html = super().render(name, value, attrs, renderer)
        return format_html('{} <strong><a href="{}">{}</a></strong>', html, url, label)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    # todo на случай работы с запчастями можно добавить и поиск по id
    search_fields = ('manufacturer', )  # поля по которым будет осуществляться поиск
    list_display = ('manufacturer', )  # поля, которые будут отображаться в админке


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    # задаём методы для получения полей из связанных таблиц
    def my_customer(self, obj):
        return obj.device.customer.customer_city

    def my_serial_number(self, obj):
        return obj.device.serial_number

    # def my_device_manufacturer(self, obj):
    #     return obj.device.analyzer.manufacturer

    # задаём отображаемое название полей в админке
    my_customer.short_description = 'Пользователь'
    my_serial_number.short_description = 'Серийный номер'
    # my_device_manufacturer.short_description = 'Производитель'
    filter_horizontal = ('responsible_users',)



    # поля для отображения
    list_display = ( 'my_serial_number',
                    'order_description', 'created_dt', 'last_updated_dt', 'order_status')
    list_filter = ('order_status', 'deadline', 'responsible_users')
    # поля для поиска
    search_fields = ('device__customer__customer_city', 'device__id', 'device__serial_number',
                     'device__analyzer__model', 'device__analyzer__manufacturer')
    # поля для того, чтобы заменить выпадашку на ввод информации и делать поиск
    autocomplete_fields = ('device', 'customer', 'analyzer')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in self.raw_id_fields:
            kwargs['widget'] = ForeignKeyWithNameRawIdWidget(db_field.remote_field, self.admin_site)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ('customer_city', )
    list_display = ('customer_city',)


@admin.register(DeviceInField)
class DeviceInFieldAdmin(admin.ModelAdmin):
    # def my_customer(self, obj):
    #     return obj.customer.customer_city

    # def my_device_manufacturer(self, obj):
    #     return obj.analyzer.manufacturer

    # todo сделать поиск по контрагентам
    search_fields = ('equipment', 'serial_number',  'owner_status')
    list_display = ('equipment', 'serial_number',  'owner_status')


# admin.site.register(Order, OrderAdmin)
# admin.site.register(Device, DeviceAdmin)
# admin.site.register(Customer, CustomerAdmin)
# admin.site.register(DeviceInField, DeviceInFieldAdmin)