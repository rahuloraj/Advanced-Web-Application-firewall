import re

# Define known malicious patterns (expanded with additional signatures)
MALICIOUS_PATTERNS = [
    r"(?:\bunion\b|\bselect\b|\binsert\b|\bdelete\b|\bdrop\b|\bupdate\b).*?\bfrom\b",  # SQL Injection
    r"(\bscript\b|<script>)",  # XSS Attack
    r"(\balert\b|\bconsole\.log\b)",  # JavaScript-based attacks
    r"(?:--)|(/\*.*?\*/)|(#.*?\n)",  # Comment-based SQL Injection
    # Additional SQL Injection Signatures
    r"(?i)union\s+select", r"(?i)drop\s+table", r"(?i)or\s+1=1", r"--", 
    r"' or '1'='1", r"1' or '1'='1", r"1' or 1=1--", r"(?i)admin'--", r"#",
    r"/\*.*\*/", r"' and '1'='1", r"' and sleep\(", r"(?i)or\s+sleep\(",
    r"'; drop table users;--", r"'; exec xp_cmdshell\(", r"(?i)or\s+1=1--", 
    r"(?i)waitfor\s+delay", r"(?i)select\s+\*", r"';shutdown --", 
    r"' union all select", r"' and benchmark\(", r"' having 1=1--", 
    r"' and ascii\(", r"' group by columnnames having 1=1--", 
    r"' and extractvalue\(", r"(?i)or\s+'a'='a", r"(?i)1 or 1=1", 
    r"(?i)order by \d+", r"convert\(int,", r"(?i)select username", 
    r"(?i)select password", r"'; waitfor delay '0:0:10'--", 
    r"' OR '1'='1'--", r"(?i)select\s+@@version", r"(?i)select\s+@@datadir", 
    r"(?i)select\s+load_file", r"(?i)select\s+user\(\)", 
    r"(?i)select\s+database\(\)", r"\" OR \"1\"=\"1", r"\' OR \'1\'=\'1",
    # Additional XSS Signatures
    r"(?i)<script>", r"(?i)<img src=", r"(?i)onerror=", r"(?i)alert\(", 
    r"(?i)document\.cookie", r"javascript:", r"(?i)<iframe>", r"(?i)<svg>", 
    r"(?i)onmouseover=", r"(?i)onload=", r"(?i)eval\(", r"settimeout\(", 
    r"setinterval\(", r"(?i)innerhtml=", r"(?i)srcdoc=", 
    r"(?i)<link rel=stylesheet href=", r"fetch\(", r"xhr\.open\(", 
    r"window\.location=", r"self\.location=", r"(?i)prompt\(", 
    r"constructor\.constructor\(", r"String\.fromCharCode\(", r"&#x", 
    r"&lt;script&gt;", r"(?i)<body onload=", r"onfocus=", r"onblur=", 
    r"onclick=", r"onkeydown=", r"onkeyup=", r"src=javascript:", 
    r"data:text/html;base64", r"(?i)<embed>", r"(?i)confirm\(",
    # Additional HTML Injection Signatures
    r"(?i)<div>", r"(?i)<span>", r"(?i)<input", r"(?i)<form", 
    r"(?i)<body", r"(?i)<html", r"(?i)<a href=", r"(?i)<p>", 
    r"(?i)<button>", r"</", r"(?i)<table>", r"(?i)<meta>", r"(?i)<object>", 
    r"(?i)<style>", r"(?i)<textarea>", r"(?i)<fieldset>", 
    r"(?i)<label>", r"(?i)<iframe src=", r"(?i)value=", 
    r"(?i)name=", r"(?i)action=", r"(?i)placeholder=", 
    r"(?i)<marquee>", r"(?i)<select>", r"(?i)<option>", r"(?i)<audio>", 
    r"(?i)<video>", r"(?i)<source>", r"(?i)<track>",
    # Additional CSRF Signatures
    r"fetch\(", r"xhr\.open\(", r"xmlhttprequest", r"(?i)<form action=", 
    r"cross-site", r"token=", r"access_token=", r"xsrf-token", 
    r"csrf-token", r"application/x-www-form-urlencoded", 
    r"submitform\(", r"credentials=", r"(?i)<input type=hidden", 
    r"Authorization: Bearer", r"(?i)<form method=",
    # Additional SSRF Signatures
    r"file://", r"gopher://", r"ftp://", r"http://127\.0\.0\.1", 
    r"http://localhost", r"169\.254\.", r"internal", 
    r"metadata\.google\.internal", r"aws", r"azure", 
    r"kubernetes\.default\.svc", r"169\.254\.169\.254", r"127\.0\.0\.53", 
    r"metadata\.", r"0x7f000001", r"0:0:0:0:0:ffff:7f00:1", 
    r"169\.254\.169\.254/latest/meta-data/", r"file:/etc/passwd", 
    r"file:/c:/windows/system32/", r"http://0x7f000001", 
    r"localhost:8080", r"127\.0\.0\.1:3306", r"http://10\.", 
    r"http://192\.168\."
]

# Define obfuscation patterns (suspicious but not explicit attacks)
OBFUSCATION_PATTERNS = [
    r"(%[0-9A-Fa-f]{2})+",  # URL encoding
    r"(\\x[0-9A-Fa-f]{2})+",  # Hex encoding
    r"(\bchar\b|\bconcat\b|\bsubstr\b)",  # SQL obfuscation functions
    r"(\bbase64_decode\b|\bbase64_encode\b)",  # Base64 encoding
    r"(\\u[0-9A-Fa-f]{4})+",  # Unicode escape sequences
    r"(\bfromCharCode\b)",  # JavaScript obfuscation
    r"(\bROT13\b)",  # ROT13 encoding
    r"(\bdecodeURIComponent\b|\bencodeURIComponent\b)",  # URI encoding
    r"(\bhexToInt\b|\bcharCodeAt\b)",  # Character conversion tricks
    r"(\\bXOR\\b|\bXOR\b)",  # XOR encoding
    r"(\bmd5\b|\bsha1\b|\bsha256\b)",  # Hash-based obfuscation
    r"(\bblind_sql\b|\btime_delay\b)",  # Blind SQL injection techniques
    r"(\bcase when\b|\bcase\b|\bthen\b)",  # SQL CASE obfuscation
    r"(?:--)|(/\*.*?\*/)|(#.*?\n)",  # Comment-based SQL obfuscation
]

def check_signature(user_input: str):
    """
    Checks if the user request matches malicious or obfuscation patterns.
    Returns:
        - "malicious" if it's an attack
        - "obfuscated" if it looks suspicious
        - "valid" if nothing is detected
    """
    user_input = " ".join(user_input.split())  # Normalize input
    
    for pattern in MALICIOUS_PATTERNS:
        if re.search(pattern, user_input, re.IGNORECASE):
            return "malicious"  # Directly detected attack
    
    for pattern in OBFUSCATION_PATTERNS:
        if re.search(pattern, user_input, re.IGNORECASE):
            return "obfuscated"  # Suspicious but needs further analysis

    return "valid"  # No issues detected
