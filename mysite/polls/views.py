# -*- coding: utf-8 -*-
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import *
from django.contrib.messages.views import SuccessMessageMixin
from polls.models import Question, Choice, Tag
from django.http import HttpRequest, HttpResponse, JsonResponse
from accounts.models import User
from polls.utils import (
    update_vote_data_choice_id,
)
from django.contrib.auth.forms import UserCreationForm
from typing import Any
import json
from polls.forms import CreatePoll, UserGroupEdit
from polls.constants import (
    HOME_TEMPLATE,
    QUESTION_CONTEXT,
    CREATE_POLLS_TEMPLATE,
    HOME_URL,
    POLLS_LIST_TEMPLATE,
)
from django.core.mail import (
    send_mail,
    send_mass_mail,
    EmailMessage,
    EmailMultiAlternatives,
)
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

# class InputForm(FormView):
#     template_name = "Temp.html"
#     form_class = NameForm
#     success_url = "/polls"

#     def form_valid(self, form):
#         username = self.request.POST["username"]
#         password = self.request.POST["password"]
#         validate_password = validate(password)
#         if not validate_password:
#             form.add_error(None, PASSWORD_VALIDATION_ERROR)
#             return super().form_invalid(form)
#         return super().form_valid(form)


class IndexView(ListView):
    model = Question
    context_object_name = QUESTION_CONTEXT
    template_name = HOME_TEMPLATE
    paginate_by = 10

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        return the filterd queryset

        :return:
        """
        from django.db.models import Q

        query = Q()
        order_by = self.request.GET.get("orderby", "-created")
        tag = self.request.GET.get("tag", "")
        if tag:
            query = Q(tag__title=tag)
        return (
            Question.objects.prefetch_related("choice")
            .filter(query & Q(created__lte=timezone.now()))
            .order_by(order_by)
        )

    def get_template_names(self):
        if self.request.htmx:  # type: ignore
            return POLLS_LIST_TEMPLATE
        else:
            return self.template_name

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        if cache.get("key"):
            value = cache.get("key")
            print("True")
        else:
            print("False")
            cache.set("key", "value", 10)
            value = cache.get("key")
        context["value"] = value
        return context


def vote(request) -> JsonResponse:
    """
    handles the ajax request to update model and send serialize data for javascript in json format

    :param request: question_id
    :return: JsonResponse
    """
    data = json.loads(request.POST["data"])
    updated_data = update_vote_data_choice_id(data)
    return JsonResponse(updated_data)


class PollsCreate(FormView, SuccessMessageMixin):
    template_name = CREATE_POLLS_TEMPLATE
    form_class = CreatePoll
    success_url = HOME_URL
    success_message = "Polls is Successfully Created"

    def form_valid(self, form) -> HttpResponse:
        """
        saves the question objects received from form & get choices list and create choices objects for same question

        :param form: unknown
        :return: HttpResponse
        """
        # Save the question
        question = form.save()

        # Process choices
        choices = self.request.POST.getlist("choices")
        for choice_text in choices:
            if choice_text:
                Choice.objects.create(question=question, title=choice_text)
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["test"] = _("Hello Brother")
        return context


def handler404(request, exception=None):
    response_error = {}
    response_error["status_code"] = 500
    print(response_error)
    return render(request, "stock/error.html", response_error)


class QuestionYearArchiveView(YearArchiveView):
    queryset = Question.objects.all()
    date_field = "created"
    make_object_list = True
    paginate_by = 10


class QuestionMonthArchiveView(MonthArchiveView):
    queryset = Question.objects.all()
    date_field = "created"
    paginate_by = 10


class PollsUsers(ListView, FormView):
    template_name = "users.html"
    model = User
    context_object_name = "users"
    form_class = UserGroupEdit
    success_url = "/polls/users"

    def form_valid(self, form):
        id = self.request.POST.get("id")
        user = User.objects.get(id=id)
        groups = form.cleaned_data["groups"]
        for group in groups:
            user.groups.add(group)
        print(groups, id)
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response
