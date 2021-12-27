from django.db import models


class ParserState(models.Model):
    page_number = models.IntegerField(default=1)

    def reset(self):
        a = ParserState(page_number=1)
        a.save()
