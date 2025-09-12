from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm
from .models import Profile
from authentication.models import ProductCode
from django.contrib.auth.models import User
import qrcode
import base64
from io import BytesIO
import qrcode, base64, zipfile
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date


# ---------------------------
# Signup view
# ---------------------------
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # inactive until approved
            user.save()  # triggers post_save signal to create Profile

            messages.info(request, "Signup successful! Await admin approval.")
            return redirect('accounts:login')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


# ---------------------------
# Login view
# ---------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            # Profile always exists due to signal
            profile = user.profile

            if profile.approved:
                login(request, user)
                return redirect('accounts:dashboard')
            else:
                messages.error(request, "Your account is not approved yet.")
        else:
            messages.error(request, "Invalid credentials.")
    
    return render(request, 'accounts/login.html')


# ---------------------------
# Dashboard view
# ---------------------------
@login_required
def dashboard_view(request):
    codes = ProductCode.objects.filter(user=request.user)
    return render(request, 'accounts/dashboard.html', {
        'codes': codes,
        'count': codes.count(),
        'user': request.user
    })


# ---------------------------
# Logout view
# ---------------------------
def logout_view(request):
    logout(request)
    return redirect('accounts:login')



@login_required
def dashboard_view(request):
    # --- Handle Date Filters ---
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    codes_qs = ProductCode.objects.filter(user=request.user)

    if start_date and end_date:
        codes_qs = codes_qs.filter(
            created_at__date__gte=parse_date(start_date),
            created_at__date__lte=parse_date(end_date)
        )

    # --- Pagination: 6 per page ---
    paginator = Paginator(codes_qs.order_by('-created_at'), 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # --- Generate QR images for current page ---
    codes = []
    for code in page_obj:
        qr = qrcode.QRCode(
            version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8, border=2
        )
        qr.add_data(code.code)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()

        codes.append({
            "product_name": code.product_name,
            "code": code.code,
            "created_at": code.created_at,
            "used": code.used,
            "image_base64": b64
        })

    return render(request, 'accounts/dashboard.html', {
        'codes': codes,
        'codes_count': codes_qs.count(),
        'page_obj': page_obj,
        'start_date': start_date,
        'end_date': end_date
    })


@login_required
def download_selected_codes(request):
    # Get date range from GET
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    codes_qs = ProductCode.objects.filter(user=request.user)

    if start_date and end_date:
        codes_qs = codes_qs.filter(
            created_at__date__gte=parse_date(start_date),
            created_at__date__lte=parse_date(end_date)
        )

    # Generate ZIP
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for code in codes_qs:
            qr = qrcode.QRCode(box_size=8, border=2)
            qr.add_data(code.code)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buf = BytesIO()
            img.save(buf, format="PNG")
            zip_file.writestr(f"{code.product_name}_{code.code}.png", buf.getvalue())

    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="selected_codes.zip"'
    return response
