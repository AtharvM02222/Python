#!/usr/bin/env python3
"""
Phone Number OSINT Tool
Requires: pip3 install phonenumbers
"""

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except ImportError:
    print("Installing phonenumbers...")
    import subprocess
    subprocess.run(['pip3', 'install', 'phonenumbers'])
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone

import sys

def analyze_phone(number):
    """Analyze phone number"""
    print(f"\n{'='*60}")
    print(f"Phone Number Analysis: {number}")
    print(f"{'='*60}\n")
    
    try:
        # Parse number
        parsed = phonenumbers.parse(number, None)
        
        # Get info
        print(f"Valid:        {phonenumbers.is_valid_number(parsed)}")
        print(f"Possible:     {phonenumbers.is_possible_number(parsed)}")
        print(f"Country:      {geocoder.description_for_number(parsed, 'en')}")
        print(f"Carrier:      {carrier.name_for_number(parsed, 'en')}")
        print(f"Timezone:     {timezone.time_zones_for_number(parsed)}")
        print(f"Number Type:  {phonenumbers.number_type(parsed)}")
        print(f"E164 Format:  {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)}")
        print(f"International: {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        print(f"National:     {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to include country code (e.g., +1234567890)")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python phone_osint.py <phone_number>")
        print("Example: python phone_osint.py +919876543210\n")
        sys.exit(1)
    
    analyze_phone(sys.argv[1])
