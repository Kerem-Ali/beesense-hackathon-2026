import os
import requests
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GRAPH_URL = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}"

def send_text(to_number: str, text: str):
    """Send text message via WhatsApp Cloud API"""
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print(f"[MOCK WhatsApp to {to_number}]: {text}")
        return
    
    url = f"{GRAPH_URL}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text}
    }
    try:
        r = requests.post(url, headers=headers, json=payload)
        print(f"WhatsApp text sent: {r.status_code} {r.text[:200]}")
    except Exception as e:
        print(f"WhatsApp error: {e}")

def upload_media(file_path: str) -> str:
    """Upload PDF to WhatsApp and return media_id"""
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print(f"[MOCK upload {file_path}]")
        return "mock_media_id_123"
    
    url = f"{GRAPH_URL}/media"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'application/pdf')}
            data = {'messaging_product': 'whatsapp', 'type': 'document'}
            r = requests.post(url, headers=headers, files=files, data=data)
            result = r.json()
            print(f"Media upload: {result}")
            return result.get("id", "mock_id")
    except Exception as e:
        print(f"Upload error: {e}")
        return "mock_id"

def send_document(to_number: str, media_id: str, caption: str):
    """Send document via WhatsApp"""
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print(f"[MOCK document to {to_number} caption: {caption[:100]}]")
        return
    
    url = f"{GRAPH_URL}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "document",
        "document": {
            "id": media_id,
            "caption": caption,
            "filename": "BeeSense_Report.pdf"
        }
    }
    try:
        r = requests.post(url, headers=headers, json=payload)
        print(f"Document sent: {r.status_code} {r.text[:300]}")
    except Exception as e:
        print(f"Doc send error: {e}")
