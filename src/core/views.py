from django.core.mail import send_mail
from django.core.mail.message import EmailMultiAlternatives
from django.shortcuts import render, reverse
from django.views import generic
from cart.models import Order

from .forms import ContactForm
from django.conf import settings
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name= 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            "orders": Order.objects.filter(user= self.request.user, ordered=True)
        })
        return context

class HomeView(generic.TemplateView):
    template_name = 'index.html'

class NosotrosView(generic.TemplateView):
    template_name = 'nosotros.html'

class ContactView(generic.FormView):
    form_class=ContactForm
    template_name='contact.html'

    def get_success_url(self):
        return reverse("contact")

    def form_valid(self, form):

        messages.info(
            self.request, "Hemos recibido tu mensaje")

        firstname = form.cleaned_data.get('nombre')
        lastname = form.cleaned_data.get('apellidos')
        email = form.cleaned_data.get('correo_electronico')
        phone = form.cleaned_data.get('celular')
        message = form.cleaned_data.get('mensaje')

        full_message = f"""
            Mensaje Recibido de {firstname} {lastname} ,
            Correo electrónico: {email}
            Celular: {phone}
            _________________________________________


            {message}
            """

        send_mail(
            subject="Mensaje de la página de Jardines, Paisajes y Bosques",
            message=full_message, 
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
        )

        return super(ContactView, self).form_valid(form)