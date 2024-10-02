import httpx
from typing import Any

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View, ContextMixin
from django.core.paginator import Paginator

from home.views import MainViewsetMixin

from mailing.models import Subscribers
from mailing.forms import SubscribersForm


class SubscribersAdminView(View):
    """
        Viewset для подписчиков в админке
    """
    def get(self, request):
        subscribers_data = Subscribers.objects.all()
        page = request.GET.get("page")
        paginator = Paginator(subscribers_data, 50)   

        page_obj = paginator.get_page(page)

        return render(request, "mailing/index.html", context={"subscribers": page_obj, "paginator": paginator})


class SubscribersViewSet(ContextMixin):
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        form = SubscribersForm()
        return {"form": form}


class HandleSubscribersView(View, MainViewsetMixin):
    """
        Viewset для подписчиков в админке
    """    
    def get(self, request, subscribe_id=None, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        if 'success' in request.path:
            subscriber_id = subscribe_id
            try:
                subscriber = Subscribers.objects.get(id=subscriber_id)
                context.update(
                    {
                        'subscriber': {
                            'name': subscriber.name,
                            'email': subscriber.email
                        }
                    }
                )
                return render(request, "mailing/success.html", context=context)
            except Subscribers.DoesNotExist:
                return HttpResponseRedirect(reverse('subscribe_fail'))
        
        if 'fail' in request.path:
            return render(request, "mailing/fail.html", context=context)

    def post(self, request):
        """
            Обработка формы подписки на сайте
        """
        form = SubscribersForm(request.POST)
        
        if form.is_valid():
            clean_data_form = form.cleaned_data
            data_form = form.save()

            if settings.SUBSCRIBE_API_KEY:
                httpx.get(f'https://api.unisender.com/ru/api/subscribe?format=json&\
                            api_key={settings.SUBSCRIBE_API_KEY}&\
                            list_ids={settings.LISTS_SUBSCRIBE}&\
                            fields[email]={clean_data_form.get("email")}&\
                            fields[Name]={clean_data_form.get("name")}'
                        )
            
            return HttpResponseRedirect(reverse('subscribe_success', kwargs={'subscribe_id': data_form.id}))        
        else:
            return HttpResponseRedirect(reverse('subscribe_fail'))

            
            
            
        