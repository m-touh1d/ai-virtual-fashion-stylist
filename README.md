# GRWMVS – Get Ready With Me Virtual Stylist

> **An AI-powered Virtual Fashion Stylist that allows users to virtually try on trending clothing items using computer vision and AI.**

---

## Overview

GRWMVS (Get Ready With Me Virtual Stylist) is an AI-powered fashion styling application developed using Django and Python. The project enables users to upload a full-body image, automatically detects different body parts using computer vision, and allows them to virtually try on clothing items with realistic AI-generated overlays.

Instead of imagining how an outfit might look, users can preview clothing directly on their uploaded image before making styling decisions. The project combines body landmark detection, image processing, and AI-powered virtual try-on technology to deliver an interactive styling experience.

---

## Problem Statement

Choosing the right outfit while shopping online can be difficult because users cannot accurately visualize how clothing will look on them.

GRWMVS addresses this challenge by providing an intelligent virtual try-on system that allows users to preview outfits on their own body before making fashion decisions.

---

## Features

* User Registration & Login System
* Upload Full Body Image
* Automatic Body Part Detection
* Face, Neck, Body, Legs and Feet Identification
* Interactive Body Part Selection
* Trending Clothing Recommendations
* AI-Based Virtual Try-On
* Image Processing with Realistic Clothing Overlay
* Responsive and Interactive User Interface
* Secure User Authentication
* Product Management using Django Admin

---

## How It Works

1. User logs into the application.
2. Uploads a full-body photograph.
3. MediaPipe detects major body landmarks.
4. The webpage highlights different body regions.
5. User clicks a body part (Face, Neck, Body, Legs or Feet).
6. Trending fashion products for that category are displayed.
7. User selects a clothing item.
8. LightX AI generates a realistic virtual try-on.
9. The final styled image is displayed to the user.

---

## Technology Stack

| Category                | Technologies            |
| ----------------------- | ----------------------- |
| Backend                 | Python 3.14, Django 6.0 |
| Frontend                | HTML5, CSS3, JavaScript |
| Computer Vision         | MediaPipe               |
| Image Processing        | OpenCV, Pillow          |
| AI Virtual Try-On       | LightX API              |
| Image Hosting           | ImgBB API               |
| Database                | SQLite (Django ORM)     |
| Version Control         | Git, GitHub             |
| Development Environment | Visual Studio Code      |

---

## Project Architecture

```text
User Login
      │
      ▼
Upload Full Body Image
      │
      ▼
MediaPipe Body Detection
      │
      ▼
Detect Body Parts
      │
      ▼
User Selects Body Part
      │
      ▼
Display Trending Fashion Items
      │
      ▼
LightX AI Virtual Try-On
      │
      ▼
Generate Styled Image
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/m-touh1d/ai-virtual-fashion-stylist.git
```

### Navigate to the Project

```bash
cd ai-virtual-fashion-stylist
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Database Migrations

```bash
python manage.py migrate
```

### Start the Development Server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000
```

---

## Future Enhancements

* AI-generated outfit recommendations based on fashion trends
* Personalized wardrobe management
* Skin tone and color matching
* Seasonal outfit suggestions
* Gender-specific styling
* E-commerce platform integration
* One-click purchase links
* Mobile application
* Multiple outfit comparison
* AI-powered fashion assistant chatbot

---

## Project Status

**Current Status:** Active Development

This project is currently under continuous development with additional AI features, improved virtual try-on quality, and enhanced user experience planned for future releases.

---

## Author

**Mohammed Touheed**

Bachelor of Engineering (Computer Science)

GitHub: https://github.com/m-touh1d

---

## License

This project is developed for educational and learning purposes.
