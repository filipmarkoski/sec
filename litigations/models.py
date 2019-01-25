from django.db import models


# Create your models here.

class Litigation(models.Model):
    release_no = models.CharField(max_length=25, unique=True)
    date = models.DateField()
    respondents = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    subtitle = models.CharField(max_length=256)
    contents = models.TextField()

    def __str__(self):
        return "{release_no} - {date} - {respondents}".format(release_no=self.release_no,
                                                              date=self.date,
                                                              respondents=self.respondents)


class Reference(models.Model):
    litigation = models.ForeignKey(Litigation, on_delete=models.SET_NULL, blank=True, null=True)
    reference = models.CharField(max_length=2000)
    reference_text = models.CharField(max_length=256)
