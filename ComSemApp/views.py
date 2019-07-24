from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from .models import Admin, Teacher, Student
from ComSemApp.administrator.forms import SignupForm, ContactForm

# TODO - these are the sort of extra views that don't exactly fit into one of the existing "apps"
# and should be reorganized

# home page
def about(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # send a message to us
            email = form.cleaned_data['email']

            message = "Somebody has requested to join Communications Seminar!\nHere is their info:\n\n"

            for key in form.cleaned_data.keys():
                if form.cleaned_data[key]:
                    message += "\t" + key + ": " + form.cleaned_data[key] + "\n"

            recipients = ['hunter@gonzaga.edu', 'zekehuntergreen@gmail.com']

            send_mail("Request to join ComSem", message, email, recipients)

            # send them a confirmation message ?

            form = SignupForm() # clear the form

            messages.success(request, 'Your request has been sent successfully! '
                                      'We will contact you shortly to set up an account.')
        else:
            messages.error(request, 'Please correct the above error.')
    else:
        form = SignupForm()

    return render(request, 'ComSemApp/about/home.html', {
        'form': form,
    })


class Contact(FormView):
    template_name = 'ComSemApp/about/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy("about")

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Your message has been sent successfully!')
        return super().form_valid(form)


class AboutTeacher(TemplateView):
    template_name = "ComSemApp/about/teacher.html"


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('initiate_roles')
        else:
            messages.error(request, 'Please correct the above error.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ComSemApp/standard_form.html', {
        'form': form,
        'page_title': 'Change Password'
    })


# called when user logs in, puts current role in session
@login_required
def initiate_roles(request):
    if Admin.objects.filter(user=request.user).exists():
        return redirect('/administrator/')

    if Teacher.objects.filter(user=request.user).exists():
        return redirect('/teacher/')

    if Student.objects.filter(user=request.user).exists():
        return redirect('/student/')
