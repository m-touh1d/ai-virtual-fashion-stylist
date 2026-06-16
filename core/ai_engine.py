import cv2
import numpy as np
import os

def detect_body_zones(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return get_default_zones()

    h, w = image.shape[:2]

    try:
        import mediapipe as mp
        BaseOptions           = mp.tasks.BaseOptions
        PoseLandmarker        = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        VisionRunningMode     = mp.tasks.vision.RunningMode

        model_path = os.path.join(os.path.dirname(__file__), 'pose_landmarker.task')
        if not os.path.exists(model_path):
            download_model(model_path)

        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.IMAGE,
        )

        with PoseLandmarker.create_from_options(options) as landmarker:
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            )
            result = landmarker.detect(mp_image)

        if not result.pose_landmarks or len(result.pose_landmarks) == 0:
            return get_default_zones()

        lm = result.pose_landmarks[0]

        # Landmark indices
        NOSE           = 0
        LEFT_EAR       = 7
        RIGHT_EAR      = 8
        LEFT_SHOULDER  = 11
        RIGHT_SHOULDER = 12
        LEFT_HIP       = 23
        RIGHT_HIP      = 24
        LEFT_KNEE      = 25
        RIGHT_KNEE     = 26
        LEFT_ANKLE     = 27
        RIGHT_ANKLE    = 28
        LEFT_HEEL      = 29
        RIGHT_HEEL     = 30
        LEFT_FOOT      = 31
        RIGHT_FOOT     = 32

        def y(i): return lm[i].y * 100
        def x(i): return lm[i].x * 100

        nose_y      = y(NOSE)
        l_ear_x     = x(LEFT_EAR);  r_ear_x = x(RIGHT_EAR)
        sho_y       = (y(LEFT_SHOULDER)  + y(RIGHT_SHOULDER)) / 2
        sho_lx      = x(LEFT_SHOULDER);  sho_rx = x(RIGHT_SHOULDER)
        hip_y       = (y(LEFT_HIP)       + y(RIGHT_HIP))       / 2
        knee_y      = (y(LEFT_KNEE)      + y(RIGHT_KNEE))      / 2
        ankle_y     = (y(LEFT_ANKLE)     + y(RIGHT_ANKLE))     / 2

        # Try to get foot tip
        try:
            foot_y = (y(LEFT_FOOT) + y(RIGHT_FOOT)) / 2
        except Exception:
            foot_y = ankle_y + 5

        body_left  = min(sho_lx, sho_rx) - 5
        body_width = abs(sho_lx - sho_rx) + 10

        # Face zone — from top of head to chin (chin ~ shoulder level)
        head_top   = max(0, nose_y - (sho_y - nose_y) * 0.9)
        face_cx    = (l_ear_x + r_ear_x) / 2
        face_w     = abs(l_ear_x - r_ear_x) + 6
        face_left  = max(0, face_cx - face_w / 2)

        zones = {
            'face': {
                'top':    round(head_top, 2),
                'left':   round(face_left, 2),
                'width':  round(min(face_w, 35), 2),
                'height': round(sho_y - head_top + 2, 2),
            },
            'neck': {
                'top':    round(sho_y - (sho_y - nose_y) * 0.28, 2),
                'left':   round(face_cx - 5, 2),
                'width':  10,
                'height': round((sho_y - nose_y) * 0.32, 2),
            },
            'chest': {
                'top':    round(sho_y, 2),
                'left':   round(max(0, body_left), 2),
                'width':  round(min(body_width, 80), 2),
                'height': round(hip_y - sho_y, 2),
            },
            'legs': {
                'top':    round(hip_y, 2),
                'left':   round(max(0, body_left), 2),
                'width':  round(min(body_width, 80), 2),
                'height': round(knee_y - hip_y, 2),
            },
            'feet': {
                'top':    round(knee_y, 2),
                'left':   round(max(0, body_left - 3), 2),
                'width':  round(min(body_width + 6, 85), 2),
                'height': round(foot_y - knee_y + 3, 2),
            },
        }
        print("✅ MediaPipe zones:", zones)
        return zones

    except Exception as e:
        print(f"MediaPipe error: {e}")
        return get_default_zones()


def download_model(model_path):
    import urllib.request
    url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task"
    print("Downloading MediaPipe model (~5MB)...")
    urllib.request.urlretrieve(url, model_path)
    print("Model ready!")


def get_default_zones():
    """
    Pixel-perfect zones tuned for standard full-body photo
    (person standing straight, white background, head to toe)
    """
    return {
        'face':  { 'top': 2,  'left': 34, 'width': 32, 'height': 16 },
        'neck':  { 'top': 18, 'left': 40, 'width': 20, 'height': 5  },
        'chest': { 'top': 22, 'left': 24, 'width': 52, 'height': 30 },
        'legs':  { 'top': 52, 'left': 26, 'width': 48, 'height': 32 },
        'feet':  { 'top': 84, 'left': 28, 'width': 44, 'height': 13 },
    }