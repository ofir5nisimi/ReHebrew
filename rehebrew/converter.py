"""
English to Hebrew text converter

Maps English keyboard characters to their Hebrew equivalents
for converting text typed with wrong keyboard layout.
"""

from typing import Tuple

# English to Hebrew keyboard mapping
# Maps each English key to its Hebrew equivalent position
EN_TO_HE_MAP = {
    # Top row (lowercase)
    'q': '/', 'w': "'", 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט',
    'u': 'ו', 'i': 'ן', 'o': 'ם', 'p': 'פ',
    
    # Home row (lowercase)
    'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י',
    'j': 'ח', 'k': 'ל', 'l': 'ך', ';': 'ף', "'": ',',
    
    # Bottom row (lowercase)
    'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ', 'n': 'מ',
    'm': 'צ', ',': 'ת', '.': 'ץ', '/': '.',
    
    # Top row (uppercase)
    'Q': '/', 'W': "'", 'E': 'ק', 'R': 'ר', 'T': 'א', 'Y': 'ט',
    'U': 'ו', 'I': 'ן', 'O': 'ם', 'P': 'פ',
    
    # Home row (uppercase)
    'A': 'ש', 'S': 'ד', 'D': 'ג', 'F': 'כ', 'G': 'ע', 'H': 'י',
    'J': 'ח', 'K': 'ל', 'L': 'ך', ':': ':', '"': ',',
    
    # Bottom row (uppercase)
    'Z': 'ז', 'X': 'ס', 'C': 'ב', 'V': 'ה', 'B': 'נ', 'N': 'מ',
    'M': 'צ', '<': 'ת', '>': 'ץ',
    
    # Special characters
    '`': ';', '~': '~', '[': ']', ']': '[', '\\': '\\',
    '{': '}', '}': '{', '|': '|',
}


def convert_to_hebrew(text: str) -> Tuple[str, int]:
    """
    Convert English-layout gibberish text to Hebrew.
    
    Args:
        text: The English text to convert
        
    Returns:
        Tuple of (converted_text, number_of_characters_converted)
    """
    result = []
    converted_count = 0
    
    for char in text:
        if char in EN_TO_HE_MAP:
            result.append(EN_TO_HE_MAP[char])
            converted_count += 1
        else:
            # Keep non-mappable characters as-is (spaces, numbers, etc.)
            result.append(char)
    
    return ''.join(result), converted_count


def convert_to_english(text: str) -> Tuple[str, int]:
    """
    Convert Hebrew text back to English-layout.
    (Reverse conversion - for future use)
    
    Args:
        text: The Hebrew text to convert
        
    Returns:
        Tuple of (converted_text, number_of_characters_converted)
    """
    # Create reverse mapping
    he_to_en_map = {v: k for k, v in EN_TO_HE_MAP.items() if k.islower() or not k.isalpha()}
    
    result = []
    converted_count = 0
    
    for char in text:
        if char in he_to_en_map:
            result.append(he_to_en_map[char])
            converted_count += 1
        else:
            result.append(char)
    
    return ''.join(result), converted_count
