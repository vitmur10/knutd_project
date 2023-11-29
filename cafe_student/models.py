from django.db import models


# Create your models here.

class Type_Product(models.Model):
    type = models.TextField()

    def __str__(self):
        return f"""{self.type}"""

    class Meta:
        verbose_name = 'Тип Продукту'
        verbose_name_plural = 'Тип Продукту'


class Product(models.Model):
    name = models.TextField()
    cost = models.IntegerField()
    type_product = models.ForeignKey(Type_Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"""|"""

    class Meta:
        verbose_name = 'Продукти'
        verbose_name_plural = 'Продукти'


class Order(models.Model):
    positions = models.TextField()
    cost = models.IntegerField()
    data = models.DateTimeField(auto_now=True)
    user_id = models.IntegerField()

    def __str__(self):
        return f"""|Кількість позицій = {self.positions}| Дата:  {self.data} Вартість {self.cost}"""

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
