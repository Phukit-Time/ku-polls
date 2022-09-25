"""Create question, choice, vote."""
import datetime


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Create Question models."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True, blank=True)

    def was_published_recently(self):
        """If poll published in one day, this function will return true."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return true when pass the published date."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """To check that the poll can vote or not, will return true when can vote."""
        now = timezone.now()
        if self.end_date is None:
            return self.pub_date <= now
        return self.pub_date <= now <= self.end_date

    def __str__(self):
        """Print question."""
        return self.question_text


class Choice(models.Model):
    """Create Choice models."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def vote(self):
        """Count the number of votes for this choice."""
        return Vote.objects.filter(choice=self).count()

    def __str__(self):
        """Print choice."""
        return self.choice_text


class Vote(models.Model):
    """A vote by a uer for a question."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    @property
    def question(self):
        """Create Question property."""
        return self.question


def get_client_ip(request):
    """Get the visitor's IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARD_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
