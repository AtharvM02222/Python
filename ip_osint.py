#!/usr/bin/env python3
"""
IP Address OSINT Tool
"""

import requests
import sys
import json

def analyze_ip(ip):
    """Analyze IP address"""
    print(f"\n{'='*60}")
    print(f"IP Address Analysis: {ip}")
    print(f"{'='*60}\n")
    
    try:
        # Use ip-api.com (free, no key needed)
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        
        if data['status'] == 'success':
            print(f"IP:           {data.get('query', 'N/A')}")
            print(f"Country:      {data.get('country', 'N/A')}")
            print(f"Region:       {data.get('regionName', 'N/A')}")
            print(f"City:         {data.get('city', 'N/A')}")
            print(f"ZIP:          {data.get('zip', 'N/A')}")
            print(f"Latitude:     {data.get('lat', 'N/A')}")
            print(f"Longitude:    {data.get('lon', 'N/A')}")
            print(f"Timezone:     {data.get('timezone', 'N/A')}")
            print(f"ISP:          {data.get('isp', 'N/A')}")
            print(f"Organization: {data.get('org', 'N/A')}")
            print(f"AS:           {data.get('as', 'N/A')}")
            
            # Google Maps link
            lat = data.get('lat')
            lon = data.get('lon')
            if lat and lon:
                print(f"\nGoogle Maps:  https://www.google.com/maps?q={lat},{lon}")
        else:
            print(f"Error: {data.get('message', 'Unknown error')}")
        
        # Additional check with ipinfo.io
        print(f"\n{'='*60}")
        print("Additional Info (ipinfo.io)")
        print(f"{'='*60}\n")
        
        response2 = requests.get(f"https://ipinfo.io/{ip}/json")
        data2 = response2.json()
        
        print(f"Hostname:     {data2.get('hostname', 'N/A')}")
        print(f"Company:      {data2.get('org', 'N/A')}")
        print(f"Postal:       {data2.get('postal', 'N/A')}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python ip_osint.py <ip_address>")
        print("Example: python ip_osint.py 8.8.8.8\n")
        sys.exit(1)
    
    analyze_ip(sys.argv[1])
