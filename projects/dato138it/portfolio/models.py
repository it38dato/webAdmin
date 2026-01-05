from django.db import models
#from ckeditor_uploader.fields import RichTextUploadingField
from django_ckeditor_5.fields import CKEditor5Field
class Place(models.Model):
    title = models.CharField(max_length=255, verbose_name="Место работы")
    spec = models.CharField(max_length=255, verbose_name="Должность")
    years = models.CharField(max_length=25, blank=True, null=True)
    description = models.TextField(verbose_name="Обязанности")
    progress = models.TextField(verbose_name="Достижения")
    doc=models.FileField(upload_to="uploads/%Y/%m/%d/", verbose_name="Файлы", blank=True, null=True)
    begin=models.DateField(blank=True, null=True, verbose_name="Начало работы")
    finish=models.DateField(blank=True, null=True, verbose_name="Конец работы")
    is_published=models.BooleanField(default=True, verbose_name="Публикация")
    cat=models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Категории")
    ordinal = models.IntegerField()
class Portfolio(models.Model):
    begin=models.DateField(blank=True, null=True, verbose_name="Начало работы")
    finish=models.DateField(blank=True, null=True, verbose_name="Конец работы")
    location = models.CharField(max_length=255, verbose_name="Место работы")
    specialization = models.CharField(max_length=255, verbose_name="Специальность")
    #responsibilities = CKEditor5Field(verbose_name="Обязанности", config_name='extends')
    responsibilities = models.CharField(blank=True, null=True, max_length=500, verbose_name="Обязанности")
    progress = models.CharField(max_length=500, verbose_name="Достижения")
    #progress = CKEditor5Field(verbose_name="Достижение", config_name='extends')
    #doc=models.FileField(upload_to="uploads/%Y/%m/%d/", verbose_name="Файлы", blank=True, null=True)
    description = CKEditor5Field(blank=True, null=True, verbose_name="Описание", config_name='extends')
    #image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    #url = models.URLField(blank=True, null=True)
    #is_published=models.BooleanField(default=True, verbose_name="Публикация")
    cat=models.ForeignKey('Category', on_delete=models.PROTECT, blank=True, null=True, verbose_name="Категории")
class Category(models.Model):
    name=models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    ordinal = models.IntegerField()
