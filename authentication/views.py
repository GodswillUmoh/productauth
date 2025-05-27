from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import ProductCode
import qrcode
import os
from django.conf import settings
import uuid, qrcode, os, io, zipfile
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
import io
import zipfile
from io import BytesIO
from django.shortcuts import get_object_or_404
from django.contrib import messages
from datetime import datetime


# the codes

def generate_code(request):
    if request.method == "POST":
        num_codes = int(request.POST.get("num_codes", 1))
        product_name = request.POST.get("product_name", "")
        manufacturer = request.POST.get("manufacturer", "")
        nafdac_no = request.POST.get("nafdac_no", "")
        date_produced = request.POST.get("date_produced", "")
        date_expired = request.POST.get("date_expired", "")
        location_manufactured = request.POST.get("location_manufactured", "")
        ingredients = request.POST.get("ingredients", "")
        image = request.FILES.get("image")

        generated_codes = []

        for _ in range(num_codes):
            code = str(uuid.uuid4())

            # ✅ Generate QR code from UUID
            qr = qrcode.make(code)
            filename = f"{code}.png"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            qr.save(filepath)

            # ✅ Save product details to DB
            product_code = ProductCode.objects.create(
                code=code,
                product_name=product_name,
                manufacturer=manufacturer,
                nafdac_no=nafdac_no,
                date_produced=date_produced,
                date_expired=date_expired,
                location_manufactured=location_manufactured,
                ingredients=ingredients,
                image=image  # optional image
            )
            product_code.qr_code_image.name = filename
            product_code.save()

            generated_codes.append(product_code)

        request.session['recent_codes'] = [str(c.id) for c in generated_codes]
        return redirect('authentication:generate_code')

    # 🧠 Show last 6 recent codes
    recent_ids = request.session.get('recent_codes', [])[-6:]
    codes = ProductCode.objects.filter(id__in=recent_ids)

    return render(request, "authentication/generate.html", {"codes": codes})



def download_pdf(request):
    # Get the last generated codes (you can filter by session or timestamp as needed)
    codes = ProductCode.objects.order_by('-created_at')[:5]  # last 5 generated codes

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="qr_codes.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 100

    for code in codes:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, f"Product: {code.product_name}")
        p.setFont("Helvetica", 10)
        p.drawString(50, y - 20, f"Code: {code.code}")

        img_path = os.path.join(settings.MEDIA_ROOT, code.qr_code_image.name)
        p.drawImage(img_path, 50, y - 140, width=100, height=100)

        y -= 180
        if y < 150:
            p.showPage()
            y = height - 100

    p.save()
    return response


def download_all_codes(request):
    # Get last 5 codes (you can customize this)
    codes = ProductCode.objects.order_by('-created_at')[:5]

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zip_file:
        for code in codes:
            qr_path = os.path.join(settings.MEDIA_ROOT, code.qr_code_image.name)
            if os.path.exists(qr_path):
                with open(qr_path, "rb") as f:
                    zip_file.writestr(os.path.basename(qr_path), f.read())

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=qr_codes.zip'
    return response



# additional codes

def download_all_codes_pdf(request):
    recent_ids = request.session.get('recent_codes', [])
    codes = ProductCode.objects.filter(id__in=recent_ids)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    y = 800

    for code in codes:
        if code.qr_code_image:
            p.drawString(100, y, f"{code.product_name or 'Product'} - {code.code}")
            p.drawImage(code.qr_code_image.path, 100, y - 100, width=100, height=100)
            y -= 150
            if y < 150:
                p.showPage()
                y = 800

    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="product_codes.pdf")



def download_all_codes_zip(request):
    recent_ids = request.session.get('recent_codes', [])
    codes = ProductCode.objects.filter(id__in=recent_ids)

    # Create in-memory zip
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="qr_codes.zip"'

    zip_buffer = zipfile.ZipFile(response, 'w')

    for code in codes:
        if code.qr_code_image and os.path.exists(code.qr_code_image.path):
            zip_buffer.write(code.qr_code_image.path, arcname=os.path.basename(code.qr_code_image.path))

    zip_buffer.close()
    return response



def verify_code(request, code):
    product = get_object_or_404(ProductCode, code=code)

    if request.method == 'POST':
        if not product.used:
            consumed = request.POST.get('consumed') == 'yes'
            if consumed:
                product.used = True
                product.save()
                messages.success(request, 'Product marked as used.')
            else:
                messages.info(request, 'Product marked as unused.')
        else:
            messages.error(request, 'This product has already been used.')
        return redirect('authentication:verify_code', code=code)

    context = {
        'product': product,
        'image': product.image.url if product.image else None,
        'nafdac_no': product.nafdac_no,
        'date_produced': product.date_produced,
        'date_expired': product.date_expired,
        'manufacturer': product.manufacturer,
        'location_manufactured': product.location_manufactured,
        'ingredients': product.ingredients,
    }

    return render(request, 'authentication/verify.html', context)



def scan_qr_page(request):
    return render(request, 'authentication/scan.html')


#added
# views.py
def home(request):
    return render(request, 'base.html', {'now': datetime.now()})


