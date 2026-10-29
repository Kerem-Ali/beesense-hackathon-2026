import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
from .scoring import score_location
from .llama_client import generate_verdict, transcribe_voice
from .pdf_generator import generate_pdf
from .whatsapp import send_text, send_document, upload_media

load_dotenv()
app = FastAPI(title="BeeSense Hackathon - WhatsApp Agent")

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "beesense_verify_2026")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.get("/webhook")
async def verify_webhook(request: Request):
    """WhatsApp Cloud API verification"""
    params = request.query_params
    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return PlainTextResponse(params.get("hub.challenge"))
    return PlainTextResponse("Verification failed", status_code=403)

@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()
    print(f"Incoming: {data}")
    
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' not in entry:
            return {"status": "no message"}
        
        message = entry['messages'][0]
        from_number = message['from']
        msg_type = message['type']
        
        # 1. Location pin - MAIN FLOW
        if msg_type == "location":
            lat = message['location']['latitude']
            lon = message['location']['longitude']
            
            # Immediate ACK - avoid timeout
            send_text(from_number, f"📍 Pin aldım: {lat:.4f}, {lon:.4f}\n🛰️ BeeSense analiz ediyor... 60sn içinde rapor gelecek.")
            
            # Background processing (in production use Modal/BackgroundTasks)
            # For hackathon MVP we process sync
            result = score_location(lat, lon)  # SAM 3.1 + 5 engines
            
            # Llama Spark verdict
            verdict = generate_verdict(result, lat, lon)
            
            # Generate PDF
            pdf_path = generate_pdf(result, verdict, lat, lon)
            
            # Upload and send back
            media_id = upload_media(pdf_path)
            caption = f"""🐝 BeeSense Verdict
📍 {lat:.4f}, {lon:.4f}

{verdict['verdict_tr']}

Skor: {result['ecological_score']}/100
Bloom: {result['bloom_window']}
Kapasite: Max {result['capacity']} kovan
Risk: {result['risk']}
Rekabet: {result['competition']} kovan 2km içinde

5 alternatif lokasyon PDF içinde."""
            
            send_document(from_number, media_id, caption)
            
        # 2. Text - Llama Spark extracts location intent
        elif msg_type == "text":
            text = message['text']['body']
            if any(k in text.lower() for k in ["merhaba", "selam", "rapor", "pin"]):
                send_text(from_number, "Merhaba! 🐝 Konum pin'i at, sana forage + bloom + kapasite + risk skorlu raporu WhatsApp'tan atayım. Örn: Muğla Köyceğiz için pin bırak.")
            else:
                # Use Llama to extract location from text
                send_text(from_number, f"Anladım: '{text}'. Lütfen haritadan pin at ki net skor hesaplayayım. Yazıyla konum tahmini yakında!")
        
        # 3. Voice - Llama Voice Transcribe
        elif msg_type == "audio":
            # Download audio, transcribe
            send_text(from_number, "🎙️ Ses notunu aldım, transkribe ediyorum...")
            # transcription = transcribe_voice(message['audio']['id'])
            # Then process as text
            
    except Exception as e:
        print(f"Error: {e}")
        # Don't crash webhook
        pass
    
    return {"status": "ok"}

@app.get("/")
async def health():
    return {"status": "BeeSense hackathon API running", "track": "Indie", "theme": "Build for Your World"}
