import os
from django.db import models

# Create your models here.
class Image(models.Model):
    STATUS_CHOICES = (
        (0, 'not available'),
        (1, 'available'),
    )
    name = models.CharField(max_length=1000)
    directory = models.CharField(max_length=1000)
    hash = models.CharField(max_length=40, db_index=True)
    status = models.IntegerField(choices=STATUS_CHOICES)

    def get_image_path(self):
        index = self.directory.find('image_data')
        if index >= 0:
            dirctory_path = self.directory[index:]
        else:
            dirctory_path = self.directory
        return os.path.join(dirctory_path, self.name)
