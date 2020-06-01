from django.db import models


class Word(models.Model):
    """
      @Description: unfamiliar english words
    """
    word = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)
    definition = models.CharField(max_length=256, null=True)
    uk_audio = models.CharField(max_length=128, null=True)
    us_audio = models.CharField(max_length=128, null=True)
    detail_url = models.CharField(max_length=128, null=True)
    en_definition = models.CharField(max_length=512, null=True)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ['word']
