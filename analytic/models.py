from django.db import models


# Create your models here.


class Analytics_User(models.Model):
    quantity_user = models.IntegerField()
    data = models.DateTimeField(auto_now=True)
    nickname = models.TextField()
    chat_id = models.IntegerField(default=000)
    user_id = models.IntegerField(default=000)
    phone = models.IntegerField(default=000000000)

    def __str__(self):
        return f"""|Кількість користувачів = {self.quantity_user}| Дата:  {self.data} Нікнейм {self.nickname}"""

    class Meta:
        verbose_name = 'Аналітика користувачі'
        verbose_name_plural = 'Аналітика користувачі'


class Analytics_actions(models.Model):
    clicks_quantity = models.IntegerField()
    button_clicks = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"""|Дія/Клік = {self.button_clicks}| Дата кліку: {self.data}"""

    class Meta:
        verbose_name = 'Аналітика дії'
        verbose_name_plural = 'Аналітика дії'
