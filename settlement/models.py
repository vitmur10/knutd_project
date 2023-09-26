from django.db import models


class Hostel(models.Model):
    hostel_number = models.CharField(max_length=10, verbose_name="Номер гуртожитка")
    residents = models.CharField(max_length=255, verbose_name="Хто проживає")
    address = models.CharField(max_length=255, verbose_name="Адреса")
    mobile_number = models.CharField(max_length=20, verbose_name="Мобільний номер")

    def __str__(self):
        return self.hostel_number

    class Meta:
        verbose_name = "Гуртожиток"
        verbose_name_plural = "Гуртожитки"


class StudentParens(models.Model):
    IPIF = models.CharField(max_length=255, verbose_name="ПіП Батьків")
    passport_series_f = models.CharField(max_length=10, verbose_name="Паспорт батьків серія")
    passport_number_f = models.CharField(max_length=20, verbose_name="Паспорт батьків номер")
    passport_issued_f = models.CharField(max_length=255, verbose_name="Паспорт батьків виданий")

    def __str__(self):
        return self.IPIF

    class Meta:
        verbose_name = "Батьки Студентів"
        verbose_name_plural = "Студенти"


class Student(models.Model):
    COURSE_CHOICES = [
        (1, '1 курс'),
        (2, '2 курс'),
        (3, '3 курс'),
        (4, '4 курс'),
        (5, '5 курс'),
    ]
    IPI = models.CharField(max_length=255, verbose_name="ПІП")
    date_of_birth = models.DateField(verbose_name="Дата народження")
    parents = models.ForeignKey(StudentParens, on_delete=models.CASCADE, verbose_name="Батьки")
    group = models.CharField(max_length=10, verbose_name="Група")
    street = models.CharField(max_length=255, verbose_name="Вулиця")
    house = models.CharField(max_length=10, verbose_name="Дім")
    room = models.CharField(max_length=10, verbose_name="Кімната")
    hostel = models.PositiveSmallIntegerField(verbose_name="Гуртожиток")
    faculty = models.CharField(max_length=255, verbose_name="Факультет")
    course = models.IntegerField(choices=COURSE_CHOICES, verbose_name="Курс")
    bloc = models.CharField(max_length=10, verbose_name="Блок")
    learning_from = models.PositiveSmallIntegerField(verbose_name="Початок навчання")
    training_to = models.PositiveSmallIntegerField(verbose_name="Закінчення")
    passport_series = models.CharField(max_length=10, verbose_name="Паспорт серія")
    passport_number = models.CharField(max_length=20, verbose_name="Паспорт номер")
    passport_issued = models.CharField(max_length=255, verbose_name="Паспорт виданий")
    identification_code = models.CharField(max_length=20, verbose_name="Індифікаційний код")

    def __str__(self):
        return self.IPI

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенти"
