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
    gene = models.TextField(verbose_name='Gene')
    date = models.DateTimeField(auto_now_add=True)
    gene_len = models.IntegerField(verbose_name='gene_len')
    pools = models.IntegerField(verbose_name='pools')
    min_len = models.IntegerField(verbose_name='min_len')
    max_len = models.IntegerField(verbose_name='max_len')


# # 访问网站的ip地址和次数
# class Userip(models.Model):
#     ip = models.CharField(verbose_name='IP地址', max_length=30)  # ip地址
#     count = models.IntegerField(verbose_name='访问次数', default=0)  # 该ip访问次数
#
#     class Meta:
#         verbose_name = '访问用户信息'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.ip
#
#
# # 网站总访问次数
# class VisitNumber(models.Model):
#     count = models.IntegerField(verbose_name='网站访问总次数', default=0)  # 网站访问总次数
#
#     class Meta:
#         verbose_name = '网站访问总次数'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return str(self.count)
#
#
# # 单日访问量统计
# class DayNumber(models.Model):
#     day = models.DateField(verbose_name='日期', default=timezone.now)
#     count = models.IntegerField(verbose_name='网站访问次数', default=0)  # 网站访问总次数
#
#     class Meta:
#         verbose_name = '网站日访问量统计'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return str(self.day)
