from django.shortcuts import render

# core/views.py
from django.shortcuts import render
from .models import Slider

from django.shortcuts import render
from .models import Slider, HomeContent


def home(request):

    # Active sliders
    slides = Slider.objects.filter(status='Active').order_by('id')

    # Active home contents
    home_contents = HomeContent.objects.filter(status=True).order_by('id')

    context = {
        'slides': slides,
        'home_contents': home_contents,
    }

    return render(request, 'home.html', context)

from .models import About
def about(request):
    abouts = About.objects.filter(status='Active')
    return render(request, 'about.html', {'abouts': abouts})

from collections import defaultdict
from .models import Service

def services(request):

    service_list = Service.objects.all().order_by('heading')

    grouped = defaultdict(list)

    for item in service_list:
        key = item.heading.strip()
        grouped[key].append(item)

    return render(request, 'services.html', {
        'grouped_services': dict(grouped)
    })

from django.shortcuts import render, redirect
from .models import Contact

def contact_page(request):
    return render(request, 'contact.html')

from django.shortcuts import render
from core.models import Hospital

from django.shortcuts import render
from core.models import Hospital

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Hospital, Contact, Service


# ================= HOSPITAL LIST =================
def hospital_list(request):

    hospitals = Hospital.objects.all()

    hospitals_by_category = {
        "General": [],
        "Specialty": [],
        "Emergency": [],
    }

    colors = {
        "General": "#6ee7b7",
        "Specialty": "#fbbf24",
        "Emergency": "#f87171"
    }

    for hospital in hospitals:
        category = hospital.category or "General"

        if category in hospitals_by_category:
            hospitals_by_category[category].append(hospital)

    for category, hospital_list in hospitals_by_category.items():
        for hospital in hospital_list:
            hospital.color = colors.get(category, "#6b7280")

    return render(request, 'hospital_list.html', {
        'hospitals_by_category': hospitals_by_category,
        'total_hospitals': hospitals.count()
    })


# ================= CONTACT SAVE =================
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Contact
from django.conf import settings


from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Contact


def contact_save(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        # SAVE TO DATABASE
        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        # =====================================================
        # ADMIN EMAIL
        # =====================================================

        admin_subject = f"🚨 New Contact Request From {name}"

        admin_html = f"""

        <div style="
            font-family: Arial;
            max-width: 700px;
            margin: auto;
            background: #f4f7fb;
            padding: 40px;
            border-radius: 15px;
        ">

            <div style="
                background: linear-gradient(135deg,#000,#444);
                padding: 25px;
                border-radius: 12px;
                color: white;
                text-align: center;
            ">
                <h1>📩 New Contact Request</h1>
            </div>

            <div style="
                background: white;
                padding: 30px;
                margin-top: 20px;
                border-radius: 12px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            ">

                <h2 style="color:#111;">Customer Details</h2>

                <table style="width:100%;border-collapse:collapse;">

                    <tr>
                        <td style="padding:12px;font-weight:bold;">👤 Name</td>
                        <td style="padding:12px;">{name}</td>
                    </tr>

                    <tr style="background:#f7f7f7;">
                        <td style="padding:12px;font-weight:bold;">📧 Email</td>
                        <td style="padding:12px;">{email}</td>
                    </tr>

                    <tr>
                        <td style="padding:12px;font-weight:bold;">📞 Phone</td>
                        <td style="padding:12px;">{phone}</td>
                    </tr>

                </table>

                <div style="
                    margin-top:25px;
                    padding:20px;
                    background:#f9f9f9;
                    border-left:5px solid black;
                    border-radius:8px;
                ">
                    <h3>📝 Message</h3>
                    <p style="line-height:1.7;color:#333;">
                        {message}
                    </p>
                </div>

            </div>

            <div style="
                text-align:center;
                margin-top:25px;
                color:#666;
                font-size:14px;
            ">
                INNSURE HEALTH SERVICES
            </div>

        </div>

        """

        admin_email = EmailMultiAlternatives(
            admin_subject,
            "",
            settings.EMAIL_HOST_USER,
            ['innsurehealth@gmail.com']
        )

        admin_email.attach_alternative(admin_html, "text/html")
        admin_email.send()

        # =====================================================
        # USER CONFIRMATION EMAIL
        # =====================================================

        user_subject = "✅ Your Request Has Been Submitted "

        user_html = f"""

        <div style="
            font-family: Arial;
            max-width: 700px;
            margin: auto;
            background: #f4f7fb;
            padding: 40px;
            border-radius: 15px;
        ">

            <div style="
                background: linear-gradient(135deg,#000,#555);
                padding: 35px;
                border-radius: 15px;
                color: white;
                text-align: center;
            ">

                <h1>🎉 Thank You {name}</h1>

                <p style="
                    font-size:18px;
                    margin-top:10px;
                    opacity:0.9;
                ">
                    Your contact request has been received successfully.</p>

            </div>

            <div style="
                background:white;
                margin-top:25px;
                padding:35px;
                border-radius:15px;
                box-shadow:0 5px 15px rgba(0,0,0,0.08);
            ">

                <h2 style="color:#111;">
                    We Will Contact You Shortly
                </h2>

                <p style="
                    line-height:1.8;
                    color:#444;
                    font-size:16px;
                ">
                    Thank you for contacting
                    <b>INNSURE HEALTH SERVICES</b>.

                    Our support team has received your request and
                    will get back to you as soon as possible.
                </p>

                <div style="
                    margin-top:25px;
                    padding:20px;
                    background:#f7f7f7;
                    border-radius:10px;
                ">

                    <h3>Your Submitted Details</h3>

                    <p><b>Name:</b> {name}</p>
                    <p><b>Email:</b> {email}</p>
                    <p><b>Phone:</b> {phone}</p>

                </div>

                <div style="
                    margin-top:30px;
                    text-align:center;
                ">

                    <a href=""
                       style="
                        display:inline-block;
                        padding:14px 30px;
                        background:black;
                        color:white;
                        text-decoration:none;
                        border-radius:8px;
                        font-weight:bold;
                       ">
                        Visit Website
                    </a>

                </div>

            </div>

            <div style="
                text-align:center;
                margin-top:30px;
                color:#777;
                font-size:14px;
            ">
                © INNSURE HEALTH SERVICES
            </div>

        </div>

        """

        user_email = EmailMultiAlternatives(
            user_subject,
            "",
            settings.EMAIL_HOST_USER,
            [email]
        )
        user_email.attach_alternative(user_html, "text/html")
        user_email.send()
        return render(request, 'contact.html', {'success': True})
    return redirect('contact_page')


# ================= LOGIN =================
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages


def login_view(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')


from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render


from django.contrib import messages
from django.contrib.auth.models import User

def forgot_password(request):

    if request.method == "POST":

        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "forgot_password.html")

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            messages.success(request, "Password updated successfully!")

        except User.DoesNotExist:
            messages.error(request, "Username not found")

    return render(request, "forgot_password.html")


# ================= DASHBOARD =================
@login_required(login_url='login')
def dashboard_view(request):

    context = {
        'services_count': Service.objects.count(),
        'hospitals_count': Hospital.objects.count(),
        'contacts_count': Contact.objects.count(),
        'recent_contacts': Contact.objects.order_by('-id')[:5]
    }

    return render(request, 'dashboard.html', context)


# ================= LOGOUT =================
from django.contrib.auth import logout
from django.shortcuts import redirect

def admin_logout(request):
    logout(request)
    return redirect('login')   # ya home page


from django.shortcuts import render, redirect
from .models import Service, Hospital
from django.contrib import messages
from django.http import HttpResponse

# Manage Services
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Service, Hospital


# ================= SERVICES =================

@login_required
def manage_services(request):

    heading = request.GET.get('heading')

    services = Service.objects.all()

    if heading:
        services = services.filter(heading=heading)

    headings = Service.objects.values('heading').distinct()

    return render(request, 'manage_services.html', {
        'services': services,
        'headings': headings,
        'selected_heading': heading
    })


@login_required
def add_service(request):
    if request.method == 'POST':
        heading = request.POST['heading']
        name = request.POST['name']
        description = request.POST['description']

        Service.objects.create(
            heading=heading,
            name=name,
            description=description
        )

        messages.success(request, "Service added successfully!")
        return redirect('manage_services')

    return render(request, 'add_service.html')


@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        service.heading = request.POST['heading']
        service.name = request.POST['name']
        service.description = request.POST['description']
        service.save()

        messages.success(request, "Service updated successfully!")
        return redirect('manage_services')

    return render(request, 'edit_service.html', {'service': service})


@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    messages.success(request, "Service deleted successfully!")
    return redirect('manage_services')


# ================= HOSPITALS =================

@login_required
def manage_hospitals(request):

    hospitals = Hospital.objects.all()
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    if query:
        hospitals = hospitals.filter(name__icontains=query)
    if category:
        hospitals = hospitals.filter(category=category)

    return render(request, 'manage_hospitals.html', {
        'hospitals': hospitals
    })


@login_required
def add_hospital(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        category = request.POST['category']

        Hospital.objects.create(
            name=name,
            address=address,
            category=category
        )

        messages.success(request, "Hospital added successfully!")
        return redirect('manage_hospitals')

    return render(request, 'add_hospital.html')


@login_required
def edit_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    if request.method == 'POST':
        hospital.name = request.POST['name']
        hospital.address = request.POST['address']
        hospital.category = request.POST['category']
        hospital.save()
        messages.success(request, "Hospital updated successfully!")
        return redirect('manage_hospitals')

    return render(request, 'edit_hospital.html', {'hospital': hospital})


@login_required
def delete_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    hospital.delete()
    messages.success(request, "Hospital deleted successfully!")
    return redirect('manage_hospitals')


from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Contact


# ================= Manage Contacts =================
@login_required
def manage_contacts(request):

    search = request.GET.get('search')

    contacts = Contact.objects.all().order_by('-id')

    if search:
        contacts = contacts.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    contacts_page = paginator.get_page(page_number)

    context = {
        'contacts': contacts_page,
        'search': search
    }

    return render(request, 'manage_contacts.html', context)


# ================= Delete Contact =================
@login_required
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    contact.delete()
    messages.success(request, "Contact deleted successfully!")
    return redirect('manage_contacts')




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Slider

# ================= Manage Slider =================
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# ================= Manage Slider =================
@login_required
def manage_slider(request):
    slides = Slider.objects.all()
    return render(request, 'manage_slider.html', {'slides': slides})


# ================= Add Slider =================
@login_required
def add_slider(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        image = request.FILES.get('image')

        if title and image and status:
            Slider.objects.create(
                title=title,
                description=description,
                status=status,
                image=image
            )
            messages.success(request, "Slide added successfully!")
            return redirect('manage_slider')
        else:
            messages.error(request, "Please fill all required fields.")

    return render(request, 'add_slider.html')


# ================= Edit Slider =================
@login_required
def edit_slider(request, slide_id):
    slide = get_object_or_404(Slider, id=slide_id)

    if request.method == "POST":
        slide.title = request.POST.get('title')
        slide.description = request.POST.get('description')
        slide.status = request.POST.get('status')

        if 'image' in request.FILES:
            slide.image = request.FILES['image']

        slide.save()
        messages.success(request, "Slide updated successfully!")
        return redirect('manage_slider')

    return render(request, 'edit_slider.html', {'slide': slide})

# ================= Delete Slider =================
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required
def delete_slider(request, slide_id):
    slide = get_object_or_404(Slider, id=slide_id)
    slide.delete()
    messages.success(request, "Slide deleted successfully!")
    return redirect('manage_slider')


@login_required
def profile_view(request):
    return render(request, "profile.html")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def edit_profile(request):

    user = request.user

    if request.method == "POST":

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()

        # profile image update (if model exists)
        if hasattr(user, "userprofile") and "profile_image" in request.FILES:
            user.userprofile.profile_image = request.FILES["profile_image"]
            user.userprofile.save()

        messages.success(request, "Profile updated successfully")
        return redirect("profile")

    return render(request, "edit_profile.html")



from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


@login_required
def change_password(request):

    if request.method == "POST":

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect")
            return redirect("change_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("change_password")

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, "Password changed successfully")
        return redirect("profile")

    return render(request, "change_password.html")


# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import HomeContent


# ===============================
# Manage Home Content
# ===============================
def manage_home_content(request):
    home_contents = HomeContent.objects.all().order_by('-id')

    context = {
        'home_contents': home_contents
    }

    return render(request, 'manage_home_content.html', context)


# ===============================
# Add Home Content
# ===============================
def add_home_content(request):

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')

        HomeContent.objects.create(
            title=title,
            description=description,
            status=True if status == "on" else False
        )

        return redirect('manage_home_content')

    return render(request, 'add_home_content.html')


# ===============================
# Edit Home Content
# ===============================
def edit_home_content(request, id):

    content = get_object_or_404(HomeContent, id=id)

    if request.method == "POST":
        content.title = request.POST.get('title')
        content.description = request.POST.get('description')
        content.status = True if request.POST.get('status') == "on" else False

        content.save()

        return redirect('manage_home_content')

    context = {
        'content': content
    }

    return render(request, 'edit_home_content.html', context)


# ===============================
# Delete Home Content
# ===============================
def delete_home_content(request, id):

    content = get_object_or_404(HomeContent, id=id)

    content.delete()

    return redirect('manage_home_content')


from django.shortcuts import render, redirect, get_object_or_404
from .models import About

def manage_about(request):
    abouts = About.objects.all()
    return render(request, 'manage_about.html', {'abouts': abouts})


def add_about(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        status = request.POST['status']

        About.objects.create(
            title=title,
            description=description,
            status=status
        )
        return redirect('manage_about')

    return render(request, 'add_about.html')


from django.shortcuts import render, get_object_or_404, redirect
from .models import About

def edit_about(request, id):
    about = get_object_or_404(About, id=id)

    if request.method == "POST":
        about.title = request.POST.get('title')
        about.description = request.POST.get('description')
        about.status = request.POST.get('status')
        about.save()
        return redirect('manage_about')

    return render(request, 'edit_about.html', {'about': about})


def delete_about(request, id):
    about = get_object_or_404(About, id=id)
    about.delete()
    return redirect('manage_about')