"""
Run this ONCE to generate placeholder overlay PNGs.
python core/generate_overlays.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.join('media', 'overlays')
os.makedirs(OUTPUT_DIR, exist_ok=True)

overlays = {
    # Eyewear
    'aviator_sunglasses':  ('#1a1a1a', 'oval',      'AVIATOR'),
    'wayfarer_frames':     ('#2d2d2d', 'rect',       'WAYFARER'),
    'sport_goggles':       ('#003399', 'oval',       'SPORT'),
    'round_metal_frames':  ('#c0a060', 'oval',       'ROUND'),
    'cat_eye_sunglasses':  ('#8B0000', 'cat',        'CAT-EYE'),
    'oversized_frames':    ('#000000', 'rect',       'OVERSIZED'),
    'tinted_lenses':       ('#6B8E23', 'oval',       'TINTED'),
    'butterfly_frames':    ('#9B59B6', 'cat',        'BUTTERFLY'),

    # Chains
    'gold_cuban_chain':    ('#FFD700', 'chain',      'CUBAN'),
    'silver_dog_tag':      ('#C0C0C0', 'chain',      'DOG TAG'),
    'rope_chain':          ('#DAA520', 'chain',      'ROPE'),
    'pearl_necklace':      ('#F5F5F5', 'chain',      'PEARL'),

    # Tops
    'oversized_tee':       ('#4A4A8A', 'shirt',      'OVERSIZED TEE'),
    'linen_shirt':         ('#D2B48C', 'shirt',      'LINEN'),
    'bomber_jacket':       ('#2F4F4F', 'jacket',     'BOMBER'),
    'polo_shirt':          ('#8B0000', 'shirt',      'POLO'),
    'crop_top':            ('#FF69B4', 'shirt',      'CROP TOP'),
    'off_shoulder_blouse': ('#DDA0DD', 'shirt',      'OFF SHOULDER'),
    'denim_jacket':        ('#1560BD', 'jacket',     'DENIM'),
    'floral_kurti':        ('#FF6B6B', 'shirt',      'KURTI'),

    # Pants
    'slim_fit_jeans':      ('#1a3a6b', 'pants',      'SLIM JEANS'),
    'cargo_shorts':        ('#556B2F', 'shorts',     'CARGO'),
    'chino_pants':         ('#C19A6B', 'pants',      'CHINO'),
    'athletic_joggers':    ('#2d2d2d', 'pants',      'JOGGERS'),
    'high_waist_jeans':    ('#2244AA', 'pants',      'HIGH WAIST'),
    'mini_skirt':          ('#FF1493', 'shorts',     'MINI SKIRT'),
    'wide_leg_pants':      ('#708090', 'pants',      'WIDE LEG'),

    # Shoes
    'air_force_sneakers':  ('#FFFFFF', 'shoe',       'AIR FORCE'),
    'leather_loafers':     ('#4a2c00', 'shoe',       'LOAFERS'),
    'high_top_boots':      ('#1a1a1a', 'boot',       'HIGH TOP'),
    'sport_slippers':      ('#FF8C00', 'slipper',    'SLIPPERS'),
    'block_heels':         ('#8B0000', 'heel',       'BLOCK HEEL'),
    'platform_sneakers':   ('#000000', 'shoe',       'PLATFORM'),
    'ballet_flats':        ('#FFB6C1', 'slipper',    'BALLET'),
}

def make_overlay(name, color, shape, label):
    W, H = 400, 300
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    r, g, b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
    c = (r, g, b, 220)
    outline = (max(0,r-40), max(0,g-40), max(0,b-40), 255)

    if shape == 'oval':
        draw.ellipse([60,80,170,160], fill=c, outline=outline, width=3)
        draw.ellipse([230,80,340,160], fill=c, outline=outline, width=3)
        draw.rectangle([165,105,235,135], fill=c)
    elif shape == 'rect':
        draw.rounded_rectangle([50,80,180,165], radius=12, fill=c, outline=outline, width=3)
        draw.rounded_rectangle([220,80,350,165], radius=12, fill=c, outline=outline, width=3)
        draw.rectangle([175,108,225,138], fill=c)
    elif shape == 'cat':
        draw.polygon([(60,140),(160,80),(190,130),(60,140)], fill=c, outline=outline)
        draw.polygon([(240,140),(340,80),(310,130),(240,140)], fill=c, outline=outline)
        draw.rectangle([185,115,245,135], fill=c)
    elif shape == 'chain':
        for i in range(8):
            x = 40 + i*42
            draw.ellipse([x,120,x+34,155], fill=c, outline=outline, width=2)
    elif shape in ('shirt','jacket'):
        draw.polygon([(80,20),(200,20),(220,80),(60,80)], fill=c, outline=outline, width=2)
        draw.polygon([(200,20),(320,20),(340,80),(220,80)], fill=c, outline=outline, width=2)
        draw.rectangle([60,80,340,280], fill=c, outline=outline, width=2)
        if shape == 'jacket':
            draw.line([(200,80),(200,280)], fill=outline, width=3)
    elif shape == 'pants':
        draw.rectangle([80,20,190,280], fill=c, outline=outline, width=2)
        draw.rectangle([210,20,320,280], fill=c, outline=outline, width=2)
        draw.rectangle([80,20,320,80], fill=c, outline=outline, width=2)
    elif shape == 'shorts':
        draw.rectangle([80,20,190,160], fill=c, outline=outline, width=2)
        draw.rectangle([210,20,320,160], fill=c, outline=outline, width=2)
        draw.rectangle([80,20,320,80], fill=c, outline=outline, width=2)
    elif shape in ('shoe','boot','slipper','heel'):
        draw.ellipse([40,120,320,240], fill=c, outline=outline, width=2)
        draw.rectangle([40,120,220,180], fill=c, outline=outline, width=2)
        if shape in ('boot','heel'):
            draw.rectangle([220,60,300,180], fill=c, outline=outline, width=2)

    # Label
    draw.text((W//2, H-20), label, fill=(255,255,255,200), anchor='mm')
    path = os.path.join(OUTPUT_DIR, name + '.png')
    img.save(path)
    print(f'Created: {path}')

for name, (color, shape, label) in overlays.items():
    make_overlay(name, color, shape, label)

print('\nAll overlays generated in media/overlays/')