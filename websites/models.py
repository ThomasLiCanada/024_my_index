# websites/models.py

from django.db import models


class IndexCategory(models.Model):
    category_name = models.CharField(max_length=255, null=True)
    category_order_num = models.IntegerField(default=99, null=True)

    def __str__(self):
        return self.category_name


class Index(models.Model):
    key_words = models.CharField(max_length=2083, null=True)
    address = models.CharField(max_length=2083, null=True)
    category1 = models.ForeignKey(IndexCategory, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_click_date = models.DateTimeField(null=True)
    click_times = models.IntegerField(default=0, null=True)

    def get_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}


class ToDoTask(models.Model):
    task_name = models.CharField(max_length=2083, null=True)
    task_reminder1_date = models.DateTimeField(blank=True, null=True)
    task_reminder2_date = models.DateTimeField(blank=True, null=True)
    task_due_date = models.DateTimeField(blank=True, null=True)
    task_done = models.BooleanField(default=False)
    task_created_date = models.DateTimeField(auto_now_add=True, null=True)

    def get_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}
