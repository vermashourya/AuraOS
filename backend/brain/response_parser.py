import re

TYPE_MAP = {
    '[WEATHER]': 'weather',
    '[CODE]':    'code',
    '[DATA]':    'data',
    '[TEXT]':    'text',
}

def detect_response_type(response):
    text = response.text.strip()
    for tag in TYPE_MAP:
        if text.startswith(tag):
            return TYPE_MAP[tag]
    return 'text'

def format_response(response, response_type):
    text = response.text.strip()
    # strip the tag from the start
    for tag in TYPE_MAP:
        if text.startswith(tag):
            text = text[len(tag):].strip()
            break
    if response_type == 'weather':
        return f'🌤 WEATHER REPORT\n\n{text}'
    return text

def parse_aura_response(raw_response):
    response_type = detect_response_type(raw_response)
    formatted = format_response(raw_response, response_type)
    return formatted
