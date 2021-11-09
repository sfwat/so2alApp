from django.db import models

# Create your models here.


class Submitter(models.Model):
    MALE = "M"
    FEMALE = "F"
    GENDER_CHOICES = [
        (MALE, "M"),
        (FEMALE, "F"),
    ]

    name = models.CharField(max_length=100, unique=True)
    nationality = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.CharField(max_length=100)

    def already_submitted(self, submitter_id):
        """
        Return True if user already submitted
        """
        answer = self.answer.filter(submitter=submitter_id)
        if answer:
            return True
        return False

    def answer_count(self):
        return self.answer.count()

    def choice_percent(self):
        answer_count = self.answer_count()
        result = {}
        for choice in self.choice.all():
            if not answer_count:
                answer_count = 1
            result[choice.choice_text] = (choice.answer_count() / answer_count) * 100
        return result

    @classmethod
    def retrieve_question(cls, qs_id=None):
        if not qs_id:
            return cls.objects.first()
        else:
            return cls.objects.exclude(pk__in=qs_id).first()

    def __str__(self):
        return self.question


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choice')
    choice_text = models.CharField(max_length=100)

    def answer_count(self):
        return self.answer.count()

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    submitter = models.ForeignKey(Submitter, on_delete=models.CASCADE, related_name='answer')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='answer')

    def __str__(self):
        return f"{self.submitter} {self.question}: {self.choice}"
