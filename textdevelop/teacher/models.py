from django.db import models

# Create your models here.
# Create your models here.
class Teacher(models.Model):
    username = models.CharField(max_length=32, 
    verbose_name="이름")
    major = models.CharField(max_length=128,verbose_name="전공")
    

    def __str__(self):
        return self.username


    class Meta:
        db_table = 'teacher'
        verbose_name = "대학원 교수"
        verbose_name_plural = "대학원 교수"