import requests
import os

class SafeBrowsingChecker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    
    def check_url(self, url):
        """
        Check if a URL is malicious using Google Safe Browsing API
        Returns: (is_safe: bool, threat_types: list)
        """
        payload = {
            "client": {
                "clientId": "discord-security-bot",
                "clientVersion": "1.0.0"
            },
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION"
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [
                    {"url": url}
                ]
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # If matches found, URL is malicious
                if "matches" in result:
                    threat_types = [match["threatType"] for match in result["matches"]]
                    return False, threat_types  # Not safe
                else:
                    return True, []  # Safe
            else:
                print(f"API Error: {response.status_code}")
                return None, []  # Error state
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None, []  # Error state

def extract_urls(text):
    """
    Extract URLs from message text
    Simple implementation - can be improved with regex
    """
    import re
    url_pattern = re.compile(
        r'\b(?:https?://)?'                                # optional scheme
        r'(?:localhost|'                                   # or localhost
        r'(?:\d{1,3}\.){3}\d{1,3}|'                        # or IPv4
        r'(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})'               # or domain
        r'(?::\d+)?'                                       # optional port
        r'(?:/[^\s\'"<>]*)?',                              # optional path/query/fragment
        flags=re.IGNORECASE
    )

    urls = []
    for m in url_pattern.finditer(text):
        u = m.group(0)
        # strip common trailing punctuation that often follows URLs in text
        u = u.rstrip('.,:;!?)"\']')
        urls.append(u)
    return urls