from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    COURSE_TYPES = [
        ('qualification', 'Повышение квалификации'),
        ('retraining', 'Профессиональная переподготовка'),
        ('safety', 'Охрана труда'),
    ]

    name = models.CharField(max_length=200, verbose_name='Название курса')
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES, verbose_name='Тип курса')
    description = models.TextField(verbose_name='Описание')
    duration = models.CharField(max_length=100, verbose_name='Длительность')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['course_type']),
        ]


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Идет обучение'),
        ('completed', 'Обучение завершено'),
    ]

    PAYMENT_CHOICES = [
        ('bank', 'Банковский перевод'),
        ('card', 'Оплата картой'),
        ('online', 'Онлайн оплата'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    start_date = models.DateField(verbose_name='Дата начала обучения')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='Способ оплаты')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления', null=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.name}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['course', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name='Заявка')
    text = models.TextField(verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления', null=True)

    def __str__(self):
        return f'Отзыв от {self.user.username}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['application']),
            models.Index(fields=['created_at']),
        ]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления', null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['full_name']),
        ]