from django.db import models
import uuid

class Products(models.Model):
    name = models.CharField(max_length=100)
    product_id = models.IntegerField(null=False)
    price = models.FloatField(max_length=10)
    sku = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.sku = uuid.uuid1()
        self.sku = str(self.sku)
        self.sku = self.sku[:8]
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"Product-Id: {self.product_id}, Name: {self.name}, Price: {self.price}, date: {self.date}"
    

