from PIL import Image
import os
from django.conf import settings

ZONE_SCALE = {
    'face':  {'w': 0.60, 'h': 0.45},
    'neck':  {'w': 0.55, 'h': 0.70},
    'chest': {'w': 1.00, 'h': 1.00},
    'legs':  {'w': 1.00, 'h': 1.00},
    'feet':  {'w': 0.90, 'h': 0.90},
}


def crop_transparent_padding(img):
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img


def get_overlay_path(item_name):
    from .models import Product
    try:
        product = Product.objects.get(name__iexact=item_name)
        if product.overlay_png:
            path = os.path.join(settings.MEDIA_ROOT, str(product.overlay_png))
            if os.path.exists(path):
                return path
        if product.image:
            path = os.path.join(settings.MEDIA_ROOT, str(product.image))
            if os.path.exists(path):
                return path
    except Exception as e:
        print(f"Error finding overlay: {e}")
    return None


def apply_overlay(photo_path, item_name, zone, zones):
    overlay_path = get_overlay_path(item_name)
    if not overlay_path:
        print(f"No overlay found for: {item_name}")
        return None
    try:
        base    = Image.open(photo_path).convert('RGBA')
        overlay = Image.open(overlay_path).convert('RGBA')
    except Exception as e:
        print(f"Image open error: {e}")
        return None

    overlay = crop_transparent_padding(overlay)
    bw, bh  = base.size
    z       = zones[zone]
    left    = int((z['left']   / 100) * bw)
    top     = int((z['top']    / 100) * bh)
    width   = int((z['width']  / 100) * bw)
    height  = int((z['height'] / 100) * bh)
    scale   = ZONE_SCALE.get(zone, {'w': 0.9, 'h': 0.9})
    ow      = int(width  * scale['w'])
    oh      = int(height * scale['h'])

    orig_w, orig_h = overlay.size
    if orig_w > 0 and orig_h > 0:
        ratio = min(ow / orig_w, oh / orig_h)
        ow    = int(orig_w * ratio)
        oh    = int(orig_h * ratio)

    overlay_resized = overlay.resize((ow, oh), Image.LANCZOS)

    if zone == 'feet':
        paste_x = left + (width - ow) // 2
        paste_y = top  + height - oh
    elif zone in ('chest', 'legs'):
        paste_x = left + (width - ow) // 2
        paste_y = top
    else:
        paste_x = left + (width  - ow) // 2
        paste_y = top  + (height - oh) // 2

    paste_x = max(0, min(paste_x, bw - ow))
    paste_y = max(0, min(paste_y, bh - oh))
    base.paste(overlay_resized, (paste_x, paste_y), overlay_resized)

    result_dir  = os.path.join(settings.MEDIA_ROOT, 'results')
    os.makedirs(result_dir, exist_ok=True)
    result_name = f'result_{zone}_{item_name.lower().replace(" ","_")}.png'
    result_path = os.path.join(result_dir, result_name)
    base.convert('RGB').save(result_path)
    return '/media/results/' + result_name