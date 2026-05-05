# PSS Junk Hauling – AI Booking Assistant
Built with Python Django + Claude AI

## Setup Instructions

### Step 1 — Open terminal/command prompt and go into the folder
```
cd pss_junk
```

### Step 2 — Install requirements
```
pip install -r requirements.txt
```

### Step 3 — Add your Claude API key
Open `pss_junk/settings.py` and find:
```
ANTHROPIC_API_KEY = 'your-api-key-here'
```
Replace with your key from https://console.anthropic.com

Also update your phone number:
```
BUSINESS_PHONE = "(your phone number)"
```

### Step 4 — Set up the database
```
python manage.py migrate
```

### Step 5 — Run the server
```
python manage.py runserver
```

### Step 6 — Open in browser
- Customer booking page: http://127.0.0.1:8000
- Your appointments dashboard: http://127.0.0.1:8000/appointments/

## What it does
- AI assistant chats with customers and collects their booking info
- Saves every appointment to a database
- You can view all appointments at /appointments/
- AI knows your service area (Cleveland + suburbs), pricing, and hours

## To customize
- Change service areas in settings.py under SERVICE_AREAS
- Change pricing or services in booking/views.py under SYSTEM_PROMPT
- Change business hours in settings.py under BUSINESS_HOURS
