from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
load_dotenv()
import os
import numpy as np

IBM_API_KEY = os.environ['IBM_API_KEY']

authenticator = IAMAuthenticator(IBM_API_KEY)
tone_analyzer = ToneAnalyzerV3(
    version='2020-02-25',
    authenticator=authenticator
)

tone_analyzer.set_service_url('https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/421d8d20-ab81-4291-a7ba-0e37f6cbf9de')

import time

def get(raw):
    try:
        resp = tone_analyzer.tone(
            {'text': raw},
            content_type='application/json',
            sentences=True
        )
        if resp.status_code == 200:
            return resp.result
        else:
            return {'error': resp.status_code}
    except Exception as e:
        return {'error': e}

def extract_score(raw_tone, tone_id):
    if not raw_tone.get('document_tone'):
        return np.nan

    tones = raw_tone.get('document_tone').get('tones')
    matching_tones = [t for t in tones if t['tone_id'] == tone_id]

    if not matching_tones:
        return np.nan

    return matching_tones[0]['score']
