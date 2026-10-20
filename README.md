# Portable Soil Testing Kit

## Overview
Portable Soil Testing Kit is a web-based project designed to present soil-related information through a simple interface. It combines a Django web application with a sensor-oriented workflow for soil and temperature measurements.

## Features
- Web interface for soil analysis.
- Soil and temperature sensor-oriented workflow.
- Dedicated home and contact pages.
- Django-based application.

## Tech Stack
- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Hardware:** Arduino and sensors for the intended measurement workflow

## Project Structure
- `soil_django/` — Django application and configuration
- `api/` — API and deployment-related files
- `save_model.py` — Model-related utility script

## Run Locally
```bash
git clone https://github.com/Divya-Dharshini-31/SOIL_TESTING_KIT.git
cd SOIL_TESTING_KIT/soil_django
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

**Note:** Live sensor readings depend on the corresponding hardware and data integration being configured.
