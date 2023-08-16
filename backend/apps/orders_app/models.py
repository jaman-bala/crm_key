from django.db import models
from datetime import datetime


class Device(models.Model):
    """Отдел"""

    class Meta:
        db_table = "devices"
        verbose_name = "Отдел"
        verbose_name_plural = "Отдел"

    manufacturer = models.CharField(verbose_name="Отдел", max_length=200)

    def __str__(self):
        return f"{self.manufacturer}"


class Customer(models.Model):
    """Город"""

    class Meta:
        db_table = "customers"
        verbose_name = "Добавить город"
        verbose_name_plural = "Город"

    customer_city = models.CharField(verbose_name="Город", max_length=200)

    def __str__(self):
        return self.customer_city


class DeviceInField(models.Model):
    """Оборудование в полях"""

    class Meta:
        db_table = "devices_in_fields"
        verbose_name = "Оборудование в полях"
        verbose_name_plural = "Оборудование в полях"

    equipment = models.CharField(verbose_name="Наимеование", max_length=200)
    serial_number = models.CharField(verbose_name="Серийный номер", max_length=200)
    owner_status = models.TextField(verbose_name="Примичание")

    def __str__(self):
        return f"{self.equipment} с/н {self.serial_number}"


class Order(models.Model):
    """Класс для описания заявки"""

    class Meta:
        db_table = "orders"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    statuses = (("open", "открыта"),
                ("closed", "закрыта"),
                ("in progress", "в работе"),
                ("need info", "нужна информация"))

    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Город/Область")
    analyzer = models.ForeignKey(Device, on_delete=models.RESTRICT, verbose_name="Отдел")
    device = models.ForeignKey(DeviceInField, verbose_name="Оборудование", on_delete=models.RESTRICT)
    order_description = models.TextField(verbose_name="Описание")
    created_dt = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    last_updated_dt = models.DateTimeField(verbose_name="Последнее изменение", blank=True, null=True)
    order_status = models.TextField(verbose_name="Статус заявки", choices=statuses)

    def __str__(self):
        return f"Заявка №{self.id} для {self.device}"

    def save(self, *args, **kwargs):
        self.last_updated_dt = datetime.now()
        super().save(*args, **kwargs)