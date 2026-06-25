import re
from email import message_from_file
from urllib.parse import urlparse

# Define a baseline dictionary of common psychological triggers & phishing keywords
RISK_KEYWORDS = [
    "urgent", "action required", "suspended", "wire transfer", "unauthorized",
    "password reset", "verify your account", "invoice", "gift card", "ceo"
]

def analyze_email(eml_file_path):
    print(f"🔍 Analyzing Artifact: {eml_file_path}\n" + "="*50)
    
    with open(eml_file_path, "r", encoding="utf-8", errors="ignore") as f:
        msg = message_from_file(f)
        
    # 1. Inspect Sender Info
    sender = msg.get("From", "Unknown Sender")
    subject = msg.get("Subject", "No Subject")
    print(f"👤 [Sender]: {sender}")
    print(f"📌 [Subject]: {subject}\n")
    
    # Extract the plain text body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body = part.get_payload(decode=True).decode(errors='ignore')
                break
    else:
        body = msg.get_payload(decode=True).decode(errors='ignore')

    # 2. Key Requirement: Identify Suspicious Keywords & Triggers
    found_keywords = [kw for kw in RISK_KEYWORDS if kw in body.lower() or kw in subject.lower()]
    print(f"🚩 [Red Flags - Risk Keywords Found]:")
    if found_keywords:
        for kw in found_keywords:
            print(f"   • Trigger detected: '{kw}'")
    else:
        print("   • No basic risk keywords triggered.")
        
    # 3. Key Requirement: Extract and Dissect Links
    # Regular expression to extract URLs
    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', body)
    
    print(f"\n🔗 [Extracted Links for Domain Inspection]:")
    if urls:
        unique_urls = list(set(urls))
        for url in unique_urls:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path.split('/')[0]
            
            print(f"   • Full URL: {url}")
            print(f"     └─ True Root Domain: {domain}")
            
            # Subdomain Trap Warning
            if domain.count('.') > 2:
                print("      ⚠️  WARNING: High number of subdomains. Verify from right-to-left!")
    else:
        print("   • No hyperlinked URLs found in plaintext body.")
        
    print("="*50 + "\n🔒 Triage Complete. Review domains carefully against corporate lookalikes.")
    

analyze_email("suspicious_packet.eml")