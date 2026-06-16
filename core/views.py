from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import os
import json
from decimal import Decimal
from django.conf import settings
from .ai_engine import detect_body_zones
from .overlay_engine import apply_overlay


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def home(request):
    from .models import Product
    # Trending products for homepage
    trending = {}
    for zone in ['face', 'neck', 'chest', 'legs', 'feet']:
        trending[zone] = list(
            Product.objects.filter(
                category=zone, is_active=True
            ).order_by('-trend_score')[:3].values(
                'id', 'name', 'brand', 'price', 'trend_label', 'image'
            )
        )
    # Fix image URLs
    for zone in trending:
        for p in trending[zone]:
            p['image'] = '/media/' + str(p['image']) if p['image'] else ''
            p['price'] = float(p['price'])

    return render(request, 'home.html', {
        'trending': json.dumps(trending, cls=DecimalEncoder),
    })


def register_view(request):
    if request.method == 'POST':
        name     = request.POST.get('name')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('home')
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        login(request, user)
        messages.success(request, f'Welcome, {name}!')
        return redirect('home')
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
        else:
            messages.error(request, 'Invalid email or password.')
        return redirect('home')
    return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('home')


def get_products_for_gender(gender):
    from .models import Product
    products_by_zone = {}
    for zone in ['face', 'neck', 'chest', 'legs', 'feet']:
        qs = Product.objects.filter(
            category=zone, is_active=True
        ).filter(
            Q(gender=gender) | Q(gender='unisex')
        ).order_by('-trend_score')[:4]
        products_by_zone[zone] = [
            {
                'id':          p.id,
                'name':        p.name,
                'brand':       p.brand,
                'price':       float(p.price),
                'trend_label': p.trend_label,
                'image':       '/media/' + str(p.image)       if p.image       else '',
                'overlay_png': '/media/' + str(p.overlay_png) if p.overlay_png else '',
            }
            for p in qs
        ]
    return products_by_zone


def upload_view(request):
    if request.method == 'POST':
        photo  = request.FILES.get('photo')
        gender = request.POST.get('gender')
        if photo:
            media_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(media_path, exist_ok=True)
            file_path = os.path.join(media_path, photo.name)
            with open(file_path, 'wb+') as f:
                for chunk in photo.chunks():
                    f.write(chunk)
            try:
                zones       = detect_body_zones(file_path)
                ai_detected = True
            except Exception as e:
                print(f"AI detection failed: {e}")
                zones       = None
                ai_detected = False

            products_by_zone = get_products_for_gender(gender)
            photo_url = '/media/uploads/' + photo.name
            return render(request, 'stylist.html', {
                'photo_url':        photo_url,
                'gender':           gender,
                'zones':            zones,
                'ai_detected':      ai_detected,
                'products_by_zone': json.dumps(products_by_zone, cls=DecimalEncoder),
            })
        else:
            messages.error(request, 'Please upload a photo.')
    return redirect('home')


def try_on_view(request):
    if request.method == 'POST':
        photo_path = request.POST.get('photo_path')
        item_name  = request.POST.get('item_name')
        zone       = request.POST.get('zone')
        gender     = request.POST.get('gender')
        zones_json = request.POST.get('zones')

        try:
            zones = json.loads(zones_json)
        except Exception:
            from .ai_engine import get_default_zones
            zones = get_default_zones()

        full_photo_path = os.path.join(
            settings.MEDIA_ROOT,
            photo_path.replace('/media/', '').replace('/', os.sep)
        )

        from .models import Product
        from .fashn_engine import virtual_tryon, download_and_save_result

        result_url = None
        try:
            product      = Product.objects.get(name__iexact=item_name)
            garment_path = None
            if product.overlay_png:
                garment_path = os.path.join(settings.MEDIA_ROOT, str(product.overlay_png))
            elif product.image:
                garment_path = os.path.join(settings.MEDIA_ROOT, str(product.image))

            if garment_path and os.path.exists(garment_path):
                print(f"🚀 Calling LightX AI for: {item_name}")
                ai_result_url = virtual_tryon(full_photo_path, garment_path)
                if ai_result_url:
                    result_url = download_and_save_result(ai_result_url, item_name, zone)
                else:
                    result_url = apply_overlay(full_photo_path, item_name, zone, zones)
            else:
                result_url = apply_overlay(full_photo_path, item_name, zone, zones)
        except Exception as e:
            print(f"Try-on error: {e}")
            result_url = apply_overlay(full_photo_path, item_name, zone, zones)

        products_by_zone = get_products_for_gender(gender)
        return render(request, 'stylist.html', {
            'photo_url':        photo_path,
            'result_url':       result_url,
            'gender':           gender,
            'zones':            zones,
            'ai_detected':      True,
            'tried_item':       item_name,
            'products_by_zone': json.dumps(products_by_zone, cls=DecimalEncoder),
        })

    return redirect('home')


@login_required
def save_outfit_view(request):
    if request.method == 'POST':
        from .models import SavedOutfit
        SavedOutfit.objects.create(
            user       = request.user,
            name       = request.POST.get('outfit_name', 'My Outfit'),
            gender     = request.POST.get('gender', ''),
            photo_url  = request.POST.get('photo_url', ''),
            result_url = request.POST.get('result_url', ''),
            face_item  = request.POST.get('face_item', ''),
            neck_item  = request.POST.get('neck_item', ''),
            chest_item = request.POST.get('chest_item', ''),
            legs_item  = request.POST.get('legs_item', ''),
            feet_item  = request.POST.get('feet_item', ''),
        )
        messages.success(request, '✅ Outfit saved!')
        return redirect('profile')
    return redirect('home')


@login_required
def profile_view(request):
    from .models import SavedOutfit
    outfits = SavedOutfit.objects.filter(user=request.user)
    return render(request, 'profile.html', {'outfits': outfits})


def trending_view(request):
    from .models import Product
    gender   = request.GET.get('gender', 'male')
    occasion = request.GET.get('occasion', 'all')

    qs = Product.objects.filter(is_active=True).filter(
        Q(gender=gender) | Q(gender='unisex')
    )
    if occasion != 'all':
        qs = qs.filter(Q(occasion=occasion) | Q(occasion='all'))

    products = list(qs.order_by('-trend_score').values(
        'id', 'name', 'brand', 'price', 'trend_label',
        'image', 'category', 'occasion'
    ))
    for p in products:
        p['image'] = '/media/' + str(p['image']) if p['image'] else ''
        p['price'] = float(p['price'])

    return render(request, 'trending.html', {
        'products': json.dumps(products, cls=DecimalEncoder),
        'gender':   gender,
        'occasion': occasion,
    })