from .models import Profile
import pdfkit
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader


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
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        summary = request.POST.get("summary", "")
        degree = request.POST.get("degree", "")
        school = request.POST.get("school", "")
        university = request.POST.get("university", "")
        previous_work = request.POST.get("previous_work", "")
        skills = request.POST.get("skills", "")
        employed = request.POST.get("employed", "") == "on"

        profile = Profile(
            name=name, email=email, phone=phone, summary=summary,
            degree=degree, school=school, university=university,
            previous_work=previous_work, skills=skills, employed=employed
        )
        profile.save()
    return render(request, 'pdf/accept.html')
