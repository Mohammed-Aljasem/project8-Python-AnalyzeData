from django.db import models
from django.utils import timezone




class Data_source(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "managestore_data_source"


class Manage_store(models.Model):
    data_source_name = models.TextField(max_length=30)
    file_name = models.TextField(max_length=30)
    execution_time = models.TextField(default=None, max_length=30)
    number_of_records = models.IntegerField(default=None)
    data_source = models.ForeignKey(Data_source, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Manage_store, self).save(*args, **kwargs)

    class Meta:
        db_table = "managestore_manage_store"


class Data(models.Model):
    customer_idd = models.CharField(max_length=30)
    customer_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    country = models.TextField(max_length=30)
    city = models.TextField(max_length=50)
    state = models.TextField(max_length=50)
    category = models.TextField(max_length=100)
    sub_category = models.TextField(max_length=100)
    product_name = models.TextField(max_length=100)
    sales = models.FloatField()
    quantity = models.IntegerField()
    discount = models.FloatField()
    profit = models.FloatField()
    manage_store = models.ForeignKey(Manage_store, on_delete=models.CASCADE)

    class Meta:
        db_table = "managestore_data"
