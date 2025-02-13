from .models import Profile
import pdfkit
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .forms import ProfileForm
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings


def share_cv_email(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    recipient_email = request.POST.get('email')

    if recipient_email:
        subject = f"{profile.name}'s CV"

        # Проверяем, есть ли загруженное изображение
        if profile.profile_picture:
            profile_picture_url = request.build_absolute_uri(profile.profile_picture.url)
        else:
            profile_picture_url = request.build_absolute_uri('/')  # Ссылка на главную страницу или другой URL

        message = f"Check out {profile.name}'s CV at {profile_picture_url}"
        sender_email = settings.EMAIL_HOST_USER

        try:
            send_mail(subject, message, sender_email, [recipient_email])
            messages.success(request, "CV shared successfully via email.")
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")

    else:
        messages.error(request, "Please provide a valid email.")

    return redirect('list_profiles')
def generate_pdf(request, id):
    user_profile = get_object_or_404(Profile, pk=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({'user_profile': user_profile})

    # Указываем путь к wkhtmltopdf
    path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }

    pdf = pdfkit.from_string(html, False, options=options, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response


def list_profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf/list.html', {'profiles': profiles})


def resume(request, id):
    user_profile = get_object_or_404(Profile, pk=id)
    return render(request, 'pdf/resume.html', {'user_profile': user_profile})


def accept(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_profiles')
    else:
        form = ProfileForm()

    return render(request, 'pdf/accept.html', {'form': form})

