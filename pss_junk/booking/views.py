import json
import uuid
import re
import urllib.request
import urllib.error
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import ChatSession, Appointment

SYSTEM_PROMPT = """You are a friendly booking assistant for PSS Junk Hauling, a junk removal company based in Cleveland, Ohio.

YOUR JOB:
- Greet customers warmly
- Help them book a junk removal appointment
- Collect all required info step by step (don't ask for everything at once)
- Be conversational, friendly, and professional

SERVICE AREA:
We serve Cleveland and surrounding areas including: Cleveland Heights, Parma, Lakewood, Euclid, Strongsville, Mentor, Westlake, North Olmsted, Brook Park, and Garfield Heights.

If a customer is outside these areas, politely let them know we don't currently serve their location.

SERVICES WE OFFER:
- Full junk removal (furniture, appliances, electronics, general clutter)
- Garage/basement/attic cleanouts
- Furniture removal (couches, mattresses, dressers, etc.)
- Appliance removal (fridges, washers, dryers, etc.)
- Estate cleanouts
- Commercial junk removal
- Yard waste and debris removal
- Hot tub / shed removal

PRICING (give estimates, final price confirmed on-site):
- Small load (1/4 truck): $100-$175
- Medium load (1/2 truck): $175-$275
- Large load (3/4 truck): $275-$375
- Full truck load: $375-$500+
- Single item (couch, mattress, etc.): $75-$125
- Appliances: $85-$150 each

BUSINESS HOURS:
Monday-Saturday, 7am-7pm
We do NOT work Sundays.

BOOKING FLOW - collect these one at a time naturally:
1. Customer's full name
2. Phone number (so we can confirm)
3. Full address (including city)
4. What needs to be removed (type and rough amount)
5. Preferred date (remind them Mon-Sat only)
6. Preferred time window (morning 7am-12pm, afternoon 12pm-4pm, evening 4pm-7pm)
7. Any special notes (stairs, tight spaces, parking, etc.)

Once you have ALL of the above, summarize the booking details clearly and tell them:
"Great! I've logged your appointment request. Our team will call you to confirm."

IMPORTANT RULES:
- Never make up prices or policies not listed above
- If asked something you don't know, say "I'll have our team follow up with you on that"
- Always be warm, helpful, and reassuring
- Keep messages SHORT and conversational
- If customer seems unsure about what they have, help them estimate

When you have successfully collected all booking info, end your message with this exact tag on a new line:
BOOKING_COMPLETE:{name}|{phone}|{address}|{city}|{job_type}|{date}|{time}|{notes}
"""


def call_gemini(messages, system_prompt):
    api_key = settings.GEMINI_API_KEY
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    # Build conversation history for Gemini
    gemini_messages = []

    # Add system prompt as first user message
    gemini_messages.append({
        "role": "user",
        "parts": [{"text": f"INSTRUCTIONS FOR YOU:\n{system_prompt}\n\nUnderstood? Please confirm briefly."}]
    })
    gemini_messages.append({
        "role": "model",
        "parts": [{"text": "Understood! I'm ready to help customers book junk removal appointments for PSS Junk Hauling in Cleveland."}]
    })

    # Add conversation history
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        gemini_messages.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    payload = json.dumps({
        "contents": gemini_messages,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1000,
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data["candidates"][0]["content"]["parts"][0]["text"]


def index(request):
    return render(request, 'booking/index.html', {
        'business_name': settings.BUSINESS_NAME,
        'business_phone': settings.BUSINESS_PHONE,
        'business_hours': settings.BUSINESS_HOURS,
    })


def admin_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'booking/admin_view.html', {
        'appointments': appointments,
        'business_name': settings.BUSINESS_NAME,
    })


@csrf_exempt
def chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    data = json.loads(request.body)
    user_message = data.get('message', '').strip()
    session_key = data.get('session_key', '')

    if not session_key:
        session_key = str(uuid.uuid4())

    session, _ = ChatSession.objects.get_or_create(
        session_key=session_key,
        defaults={'messages': []}
    )

    messages = session.messages or []
    messages.append({"role": "user", "content": user_message})

    try:
        ai_reply = call_gemini(messages, SYSTEM_PROMPT)

        booking_saved = False
        clean_reply = ai_reply

        if 'BOOKING_COMPLETE:' in ai_reply:
            try:
                tag_line = [l for l in ai_reply.split('\n') if 'BOOKING_COMPLETE:' in l][0]
                booking_data = tag_line.replace('BOOKING_COMPLETE:', '').strip()
                parts = booking_data.split('|')
                if len(parts) >= 7:
                    appt = Appointment.objects.create(
                        customer_name=parts[0].strip(),
                        phone=parts[1].strip(),
                        address=parts[2].strip(),
                        city=parts[3].strip(),
                        job_type=parts[4].strip(),
                        preferred_date=parts[5].strip(),
                        preferred_time=parts[6].strip(),
                        notes=parts[7].strip() if len(parts) > 7 else '',
                    )
                    session.appointment = appt
                    booking_saved = True
                clean_reply = re.sub(r'\nBOOKING_COMPLETE:.*', '', ai_reply).strip()
            except Exception:
                pass

        messages.append({"role": "assistant", "content": ai_reply})
        session.messages = messages
        session.save()

        return JsonResponse({
            'reply': clean_reply,
            'session_key': session_key,
            'booking_saved': booking_saved,
        })

    except Exception as e:
        return JsonResponse({
            'reply': f'Sorry, something went wrong. Please call us at {settings.BUSINESS_PHONE}',
            'session_key': session_key
        }, status=200)
