from django.db import models
from django.utils import timezone


# Create your models here.

class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class GeneInfo(models.Model):
    email = models.EmailField(verbose_name='email')
    # gene = models.TextField(verbose_name='Gene')
    date = models.DateTimeField(auto_now_add=True)
    gene_len = models.IntegerField(verbose_name='gene_len')
    pools = models.IntegerField(verbose_name='pools')
    min_len = models.IntegerField(verbose_name='min_len')
    max_len = models.IntegerField(verbose_name='max_len')
