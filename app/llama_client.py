import os
from dotenv import load_dotenv
load_dotenv()
def generate_verdict(scoring_result, lat, lon):
    return {
        "verdict_tr": f"{scoring_result['flora']} teyit edildi. {scoring_result['bloom_window']} açılıyor, max {scoring_result['capacity']} kovan.",
        "verdict_en": "confirmed",
        "decision": "MOVE",
        "reasoning": "mock"
    }
def transcribe_voice(audio_id):
    return "Transcribed"