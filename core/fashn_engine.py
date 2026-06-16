import requests
import time
import os
from django.conf import settings

LIGHTX_API_KEY = "5508dad5a8b04675a5545a4880047d73_d5110a74cb474352b0e91c44e5d89e00_andoraitools"
IMGBB_API_KEY  = "16e37e634aa417872e285ac5f31a688b"


def virtual_tryon(person_image_path, garment_image_path):
    person_url  = upload_image_to_imgbb(person_image_path)
    garment_url = upload_image_to_imgbb(garment_image_path)

    if not person_url or not garment_url:
        print("❌ Image upload failed")
        return None

    print(f"✅ Person URL: {person_url}")
    print(f"✅ Garment URL: {garment_url}")

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': LIGHTX_API_KEY,
    }

    payload = {
        "imageUrl":      person_url,
        "styleImageUrl": garment_url,
    }

    response = requests.post(
        'https://api.lightxeditor.com/external/api/v2/aivirtualtryon',
        headers=headers,
        json=payload,
        timeout=30,
    )

    print(f"LightX response: {response.status_code} {response.text}")

    if response.status_code != 200:
        print(f"❌ LightX API error: {response.text}")
        return None

    data     = response.json()
    order_id = data.get('body', {}).get('orderId')

    if not order_id:
        print(f"❌ No orderId in response: {data}")
        return None

    print(f"✅ Order ID: {order_id}")
    return poll_result(order_id, headers)


def poll_result(order_id, headers, max_attempts=20):
    for attempt in range(max_attempts):
        time.sleep(3)
        response = requests.post(
            'https://api.lightxeditor.com/external/api/v1/order-status',
            headers=headers,
            json={"orderId": order_id},
            timeout=15,
        )

        if response.status_code != 200:
            print(f"Poll error: {response.text}")
            continue

        data   = response.json()
        status = data.get('body', {}).get('status')
        print(f"Attempt {attempt+1}: status = {status}")

        if status == 'active':
            output_url = data.get('body', {}).get('output')
            print(f"✅ Result URL: {output_url}")
            return output_url

        if status == 'failed':
            print("❌ Try-on failed")
            return None

    print("❌ Timeout waiting for result")
    return None


def upload_image_to_imgbb(image_path):
    try:
        with open(image_path, 'rb') as f:
            response = requests.post(
                'https://api.imgbb.com/1/upload',
                params={'key': IMGBB_API_KEY},
                files={'image': f},
                timeout=30,
            )
        data = response.json()
        if data.get('success'):
            return data['data']['url']
        print(f"ImgBB error: {data}")
        return None
    except Exception as e:
        print(f"Upload error: {e}")
        return None


def download_and_save_result(result_url, item_name, zone):
    try:
        response = requests.get(result_url, timeout=30)
        if response.status_code == 200:
            result_dir  = os.path.join(settings.MEDIA_ROOT, 'results')
            os.makedirs(result_dir, exist_ok=True)
            result_name = f'ai_result_{zone}_{item_name.lower().replace(" ","_")}.png'
            result_path = os.path.join(result_dir, result_name)
            with open(result_path, 'wb') as f:
                f.write(response.content)
            return '/media/results/' + result_name
    except Exception as e:
        print(f"Download error: {e}")
    return None