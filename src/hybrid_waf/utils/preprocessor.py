import math

def compute_length(text: str) -> int:
    return len(text)

def shannon_entropy(text: str) -> float:
    if not text:
        return 0.0
    frequency = {}
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1
    entropy = 0.0
    for freq in frequency.values():
        p = freq / len(text)
        entropy -= p * math.log2(p)
    return entropy

def numeric_text_ratio(text: str) -> float:
    if not text:
        return 0.0
    numeric_count = sum(c.isdigit() for c in text)
    alpha_count = sum(c.isalpha() for c in text)
    if alpha_count == 0:
        return float(numeric_count)
    return numeric_count / alpha_count

def special_char_count(text: str) -> int:
    # Define special characters to count
    special_chars = ["'", '"', "{", "}", "[", "]", "--", ";", "/", "\\", "=", "<", ">"]
    count = 0
    for sp in special_chars:
        count += text.count(sp)
    return count

def extract_features(uri: str, get_data: str, post_data: str) -> list:
    """
    Extracts eight features from the provided URI, GET, and POST data.
    Returns a list of features in the following order:
      [URI_Length, GET_Length, POST_Length, URI_Entropy, GET_Entropy, POST_Entropy,
       Numeric_Text_Ratio, Special_Char_Count]
    """
    features = {}
    features["URI_Length"] = compute_length(uri)
    features["GET_Length"] = compute_length(get_data)
    features["POST_Length"] = compute_length(post_data)
    features["URI_Entropy"] = shannon_entropy(uri)
    features["GET_Entropy"] = shannon_entropy(get_data)
    features["POST_Entropy"] = shannon_entropy(post_data)
    combined = uri + get_data + post_data
    features["Numeric_Text_Ratio"] = numeric_text_ratio(combined)
    features["Special_Char_Count"] = special_char_count(combined)
    
    # Return the features as a fixed-order list
    return [
        features["URI_Length"],
        features["GET_Length"],
        features["POST_Length"],
        features["URI_Entropy"],
        features["GET_Entropy"],
        features["POST_Entropy"],
        features["Numeric_Text_Ratio"],
        features["Special_Char_Count"]
    ]
