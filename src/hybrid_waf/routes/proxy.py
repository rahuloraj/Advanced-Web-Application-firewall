from flask import Blueprint, request, jsonify
from src.hybrid_waf.utils.signature_checker import check_signature
import logging

# Create a dedicated logger for WAF detections
waf_logger = logging.getLogger('waf_detections')
waf_logger.setLevel(logging.INFO)

# Create file handler
fh = logging.FileHandler('logs/detections.log')
fh.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)

# Add the handler to the logger
waf_logger.addHandler(fh)

proxy_bp = Blueprint('proxy', __name__)

@proxy_bp.route('/check_request', methods=['POST'])
def check_request():
    data = request.get_json()
    
    user_input = data.get("user_request", "")
    uri = data.get("uri", user_input)
    get_data = data.get("get_data", "")
    post_data = data.get("post_data", "")
    
    # --- Step 1: Signature-Based Detection ---
    signature_result = check_signature(user_input)
    
    if signature_result == "valid":
        waf_logger.info(f"{user_input} - valid")
        return jsonify({
            "status": "valid",
            "message": "All Clear! Your request passed our security checks with flying colors.✨"
        })

    if signature_result == "malicious":
        waf_logger.info(f"{user_input} - malicious(signature)")
        return jsonify({
            "status": "malicious",
            "message": "Critical Alert! Malicious pattern detected in your request.<br>Access Denied!🔒"
        })
    
    # --- Step 2: ML-Based Anomaly Detection (Only for obfuscated requests) ---
    if signature_result == "obfuscated":
        from src.hybrid_waf.utils.preprocessor import extract_features
        from src.hybrid_waf.utils.ml_checker import check_ml_prediction
        
        features = extract_features(uri, get_data, post_data)
        prediction = check_ml_prediction(features)
        
        final_status = "malicious" if prediction == 1 else "valid"
        
        waf_logger.info(f"{user_input} - malicious(ML)" if prediction == 1 else f"{user_input} - valid")
            
        return jsonify({
            "status": "obfuscated",
            "ml_verdict": (
                "🚨 Threat Confirmed! AI Defense System Blocked Suspicious Activity.🔒" 
                if final_status == "malicious" 
                else "✅ Advanced AI Scan Complete: Request Verified Safe ✨"
            ),
            "message": "Suspicious Pattern Detected - Engaging Advanced AI Analysis...",
            "features": features
        })