import datetime


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True, blank=True)

    def was_published_recently(self):
        """if poll published in one day, this function will return true"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """return true when pass the published date"""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """to check that the poll can vote or not, will return true when can vote"""
        now = timezone.now()
        if self.end_date is None:
            return self.pub_date <= now
        return self.pub_date <= now <= self.end_date

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)

    @property
    def vote(self):
        """count the number of votes for this choice."""
        #TODO - one line of code!
        return 0

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    """A vote by a uer for a question."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
