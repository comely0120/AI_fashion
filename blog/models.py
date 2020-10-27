from django.db import models
from django.urls import reverse_lazy
from django.shortcuts import reverse
# Create your models here.

cloth_category = {
    ('Shirt', 'Shirt'),
    ('Blouse', 'Blouse'),
    ('Pants', 'Pants'),
    ('Skirt', 'Skirt')
}

cloth_label = (
    ('T', 'Top'),
    ('B', 'Bottom'),
    ('D', 'Dress'),
)

class Cloth(models.Model):
    closet = models.ImageField(upload_to='clothes/closets/',null=True,blank=True)
    category = models.CharField(max_length=50 , null=True, default='self')
    label = models.CharField(choices=cloth_label, max_length=1, null=True, default="T")
    category_num = models.IntegerField(default=0)

class Recommend(models.Model):
    index = models.IntegerField(default=0, primary_key=True)
    Path = models.CharField(max_length=100)
    label_T = models.IntegerField(default=0)
    label_B = models.IntegerField(default=0)

class Selection(models.Model):
    v_id = models.IntegerField(default=0)
    v_up = models.IntegerField(default=0)
    v_down = models.IntegerField(default=0)

    def __int__(self):
        return self.v_up


