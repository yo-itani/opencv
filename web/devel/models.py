import os
from django.db import models

# Create your models here.
class Image(models.Model):
    UNAVAILABLE = 0
    AVAILABLE = 1
    STATUS_CHOICES = (
        (UNAVAILABLE, 'not available'),
        (AVAILABLE, 'available'),
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

    def change_status(self, status):
        if isinstance(status, int) or status.isdigit():
            status = int(status)
            if status == Image.UNAVAILABLE:
                self.ng()
            elif status == Image.AVAILABLE:
                self.ok()

    def ng(self):
        self.status = self.STATUS_CHOICES[0][0]
        self.save()

    def ok(self):
        self.status = self.STATUS_CHOICES[1][0]
        self.save()
