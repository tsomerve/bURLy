from django.db import models


class ShortURL(models.Model):
    url = models.URLField()
    code = models.CharField(max_length=8, primary_key=True, editable=False)

    def __str__(self):
        return f'{self.code}: {self.url}'


class Click(models.Model):
    ip = models.GenericIPAddressField(blank=True, null=True)
    referer = models.URLField(blank=True, null=True)

    short_url = models.ForeignKey(ShortURL, on_delete=models.CASCADE, related_name='clicks')
