"""Django View page."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """Index page."""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Get list of question filtered by timezone."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Detail page."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Filter question by timezone."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def dispatch(self, request, *args, **kwargs):
        """
        If someone navigates to a poll detail page when voting is not allowed,
        redirect them to the polls index page and show an error message on the page.
        """
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        if not question.can_vote():
            messages.error(request, "Can't Vote")
            return redirect(reverse('polls:index'))
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    """Results page."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Login before voting."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        try:
            user_vote = Vote.objects.get(user=request.user, choice__question=question)
            user_vote.choice = selected_choice
            user_vote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(choice=selected_choice, user=request.user)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
