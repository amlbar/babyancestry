from django.db import models

class IPToken(models.Model):
    ip = models.CharField(max_length=18)
    access_token = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.ip
