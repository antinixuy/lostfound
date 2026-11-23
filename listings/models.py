from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField('Название категории', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Listing(models.Model):
    TYPE_CHOICES = [
        ('lost', 'Потерял'),
        ('found', 'Нашёл'),
    ]
    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('matched', 'Пара найдена'),
        ('closed', 'Закрыто'),
        ('hidden', 'Скрыто модератором'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='listings',
        verbose_name='Автор'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='listings',
        verbose_name='Категория'
    )
    type = models.CharField('Тип объявления', max_length=10, choices=TYPE_CHOICES)
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    location = models.CharField('Место', max_length=200, blank=True)
    event_date = models.DateField('Дата события', null=True, blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        db_table = 'listings'
        ordering = ['-created_at']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return f'{self.title} ({self.get_type_display()})'

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images', verbose_name='Объявление')
    image = models.ImageField('Изображение', upload_to='listings/')
    created_at = models.DateTimeField('Загружено', auto_now_add=True)

    class Meta:
        db_table = 'listing_images'
        verbose_name = 'Изображение объявления'
        verbose_name_plural = 'Изображения объявлений'