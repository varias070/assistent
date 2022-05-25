from django.db import models


class ParserState(models.Model):
    page_number = models.IntegerField(default=1)

    @staticmethod
    def reset():
        state = ParserState(page_number=1)
        state.save()
