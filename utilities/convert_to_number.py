def convert_to_number(text):
    """
    Converts shorthand numbers like 33.6K, 1.2M, 5B to full integers.
    """
    multipliers = {'K': 1_000, 'M': 1_000_000, 'B': 1_000_000_000}
    text = text.upper().replace(',', '').strip()
    
    if text[-1] in multipliers:
        return int(float(text[:-1]) * multipliers[text[-1]])
    try:
        return int(text)
    except ValueError:
        return None
