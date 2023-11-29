from django.db import models


# Create your models here.


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    instagram_link = models.URLField(blank=True)
    tg_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    website_link = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультети'


class Question(models.Model):
    TYPE_CHOICES = (
        ('Найчастіші запитання', 'Найчастіші запитання'),
        ('Питання щодо навчання', 'Питання щодо навчання'),
        ('Фінанси', 'Фінанси'),
        ('Питання щодо вступу', 'Питання щодо вступу'),
    )
    text = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f"""Питання: {self.text}      Відповідь: {self.answer}   Факультет: {self.faculty}  Тип: {self.type}"""

    class Meta:
        verbose_name = 'Питання'
        verbose_name_plural = 'Питання'
