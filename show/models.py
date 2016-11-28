from django.db import models

# Create your models here.

class Keyword(models.Model):
    word = models.CharField('词名',max_length=100)
    freq = models.DecimalField('词频',max_digits=12,decimal_places=10)
    releate = models.IntegerField('相关文章数',default=0)

class Dept(models.Model):
    dept = models.CharField('公众号',max_length=100)

class Passage(models.Model):
    title = models.CharField('标题',max_length=200)
    publish_time = models.DateField('发表时间')
    dianzan = models.IntegerField('点赞数')
    yuedu = models.IntegerField('阅读数')
    text = models.TextField('文章内容')
    department = models.ForeignKey(Dept)
    aboutwords = models.ManyToManyField(Keyword)
    passagehot = models.FloatField('热度',default=0)
    departmentname = models.CharField('部门名',max_length=100,default='null')

    class Meta:
        verbose_name_plural = "文章"
        verbose_name = verbose_name_plural

    def __str__(self):
        return self.title


# class Datetest(models.Model):
#     date = models.DateField()

class Relate(models.Model):
    word1 = models.CharField(max_length=100)
    word2 = models.CharField(max_length=100)
    relation = models.IntegerField(default=0)