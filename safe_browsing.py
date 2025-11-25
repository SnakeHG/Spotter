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
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    return urls