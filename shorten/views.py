import random
import string

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from ipware import get_client_ip

from shorten.models import ShortURL, Click


def generate_code(length=8):
    return ''.join([
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length)
    ])

class ShortURLIndexView(View):
    def get(self, request):
        return render(request, 'shorten/index.html', {})

    def post(self, request):
        model = ShortURL()
        model.url = request.POST['url']
        model.code = generate_code()
        model.save()

        return redirect('detail', pk=model.pk)

class ShortURLDetailView(DetailView):
    model = ShortURL
    template_name = 'shorten/detail.html'
    context_object_name = 'url'

class ShortURLRedirectView(View):
    def get(self, request, pk):
        model = get_object_or_404(ShortURL, pk=pk)

        click = Click()
        click.short_url = model

        ip, _ = get_client_ip(request)
        if ip:
            click.ip = ip

        click.referer = request.META['HTTP_REFERER']
        click.save()

        return HttpResponseRedirect(model.url)