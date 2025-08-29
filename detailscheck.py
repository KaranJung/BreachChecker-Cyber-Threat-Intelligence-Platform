import requests
import json
import re
import os
from datetime import datetime
import argparse
import sys
from typing import Dict, List, Any, Optional
import time
import dns.resolver
import whois
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import socket

class AdvancedOSINTTool:
    def __init__(self):
        self.hudson_rock_url = "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email"
        self.hibp_url = "https://haveibeenpwned.com/api/v3/breachedaccount/"
        self.dehashed_url = "https://api.dehashed.com/search"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        
    def check_email_format(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def hudson_rock_search(self, email: str) -> Dict[str, Any]:
        """Search Hudson Rock for compromised credentials"""
        try:
            response = self.session.get(f"{self.hudson_rock_url}?email={email}", timeout=30)
            if response.status_code == 200:
                return response.json()
            return {"error": f"API returned status code {response.status_code}"}
        except Exception as e:
            return {"error": f"Hudson Rock search failed: {str(e)}"}
    
    def haveibeenpwned_search(self, email: str, hibp_api_key: str = None) -> Dict[str, Any]:
        """Check Have I Been Pwned for breaches"""
        headers = {'User-Agent': self.user_agent}
        if hibp_api_key:
            headers['hibp-api-key'] = hibp_api_key
            
        try:
            response = self.session.get(f"{self.hibp_url}{email}", headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"breaches": []}
            else:
                return {"error": f"HIBP API returned status code {response.status_code}"}
        except Exception as e:
            return {"error": f"HIBP search failed: {str(e)}"}
    
    def dehashed_search(self, email: str, dehashed_api_key: str = None) -> Dict[str, Any]:
        """Search Dehashed for compromised data (requires API key)"""
        if not dehashed_api_key:
            return {"error": "Dehashed API key required"}
            
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Basic {dehashed_api_key}'
        }
        
        try:
            response = self.session.get(
                f"{self.dehashed_url}?query=email:{email}",
                headers=headers,
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Dehashed API returned status code {response.status_code}"}
        except Exception as e:
            return {"error": f"Dehashed search failed: {str(e)}"}
    
    def social_media_search(self, email: str) -> Dict[str, Any]:
        """Check for social media profiles associated with email"""
        # This is a placeholder - in a real implementation, you would use various APIs
        # or techniques to find social media profiles
        return {"message": "Social media search would be implemented with specialized APIs"}
    
    def domain_whois_lookup(self, domain: str) -> Dict[str, Any]:
        """Perform WHOIS lookup on domain"""
        try:
            domain_info = whois.whois(domain)
            return {
                "registrar": domain_info.registrar,
                "creation_date": str(domain_info.creation_date),
                "expiration_date": str(domain_info.expiration_date),
                "name_servers": list(domain_info.name_servers) if domain_info.name_servers else [],
                "emails": domain_info.emails if hasattr(domain_info, 'emails') else []
            }
        except Exception as e:
            return {"error": f"WHOIS lookup failed: {str(e)}"}
    
    def dns_lookup(self, domain: str) -> Dict[str, Any]:
        """Perform DNS lookup on domain"""
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
        results = {}
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                results[record_type] = [str(r) for r in answers]
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
                results[record_type] = []
            except Exception as e:
                results[record_type] = f"Error: {str(e)}"
                
        return results
    
    def google_search(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """Perform Google search (placeholder)"""
        # In a real implementation, you would use Google's API or scrape results
        return {"message": "Google search would be implemented with proper API access"}
    
    def analyze_results(self, email: str, hudson_data: Dict, hibp_data: Dict, 
                       dehashed_data: Dict, whois_data: Dict, dns_data: Dict) -> str:
        """Analyze and compile all results into a comprehensive report"""
        report = [
            "=" * 80,
            f"COMPREHENSIVE OSINT REPORT",
            "=" * 80,
            f"Target: {email}",
            f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 80,
            ""
        ]
        
        # Hudson Rock Data
        report.extend([
            "HUDSON ROCK DATA:",
            "-" * 40
        ])
        
        if 'error' in hudson_data:
            report.append(f"Error: {hudson_data['error']}")
        elif 'stealers' in hudson_data and hudson_data['stealers']:
            report.append(f"Status: COMPROMISED")
            report.append(f"Total Breaches: {len(hudson_data['stealers'])}")
            report.append(f"Corporate Services: {hudson_data.get('total_corporate_services', 0)}")
            report.append(f"User Services: {hudson_data.get('total_user_services', 0)}")
            
            for i, breach in enumerate(hudson_data['stealers'], 1):
                report.extend([
                    f"\nBreach #{i}:",
                    f"  Date: {breach.get('date_compromised', 'Unknown')}",
                    f"  IP: {breach.get('ip', 'Unknown')}",
                    f"  Computer: {breach.get('computer_name', 'Unknown')}",
                    f"  OS: {breach.get('operating_system', 'Unknown')}",
                    f"  Top Logins: {', '.join(breach.get('top_logins', []))}",
                    f"  Top Passwords: {', '.join(breach.get('top_passwords', []))}"
                ])
        else:
            report.append("Status: No compromises found in Hudson Rock database")
        
        # HIBP Data
        report.extend([
            "\nHAVE I BEEN PWNED DATA:",
            "-" * 40
        ])
        
        if 'error' in hibp_data:
            report.append(f"Error: {hibp_data['error']}")
        elif 'breaches' in hibp_data:
            if hibp_data['breaches']:
                report.append(f"Status: Found in {len(hibp_data['breaches'])} breaches")
                for breach in hibp_data['breaches']:
                    report.append(f"  - {breach.get('Name', 'Unknown')} ({breach.get('BreachDate', 'Unknown date')})")
            else:
                report.append("Status: No breaches found in HIBP database")
        else:
            report.append("Status: HIBP data not available")
        
        # Dehashed Data
        report.extend([
            "\nDEHASHED DATA:",
            "-" * 40
        ])
        
        if 'error' in dehashed_data:
            report.append(f"Note: {dehashed_data['error']}")
        elif 'entries' in dehashed_data and dehashed_data['entries']:
            report.append(f"Status: Found {dehashed_data.get('total', 0)} entries")
            for entry in dehashed_data['entries'][:5]:  # Show first 5 entries
                report.append(f"  - {entry.get('email', 'N/A')} | {entry.get('password', 'N/A')} | {entry.get('source', 'Unknown source')}")
        else:
            report.append("Status: No data found in Dehashed database")
        
        # Domain analysis if email has a domain
        domain = email.split('@')[-1] if '@' in email else None
        if domain:
            report.extend([
                "\nDOMAIN ANALYSIS:",
                "-" * 40,
                f"Domain: {domain}"
            ])
            
            # WHOIS Data
            if 'error' in whois_data:
                report.append(f"WHOIS Error: {whois_data['error']}")
            else:
                report.extend([
                    f"Registrar: {whois_data.get('registrar', 'Unknown')}",
                    f"Creation Date: {whois_data.get('creation_date', 'Unknown')}",
                    f"Expiration Date: {whois_data.get('expiration_date', 'Unknown')}"
                ])
            
            # DNS Data
            report.append("\nDNS Records:")
            for record_type, records in dns_data.items():
                if records:
                    report.append(f"  {record_type}: {', '.join(records)}")
        
        # Recommendations
        report.extend([
            "\nSECURITY RECOMMENDATIONS:",
            "-" * 40,
            "1. Immediately change all passwords for compromised accounts",
            "2. Enable two-factor authentication on all critical accounts",
            "3. Scan all devices for malware and info-stealers",
            "4. Monitor financial accounts for suspicious activity",
            "5. Use a password manager to generate strong, unique passwords",
            "6. Consider identity theft protection services",
            "7. Check for additional exposure at: https://haveibeenpwned.com/",
            ""
        ])
        
        return "\n".join(report)
    
    def save_report(self, email: str, report: str):
        """Save report to file with email-based naming"""
        # Create reports directory if it doesn't exist
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        # Clean email for filename
        clean_email = email.replace('@', '_at_').replace('.', '_dot_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/{clean_email}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            return filename
        except Exception as e:
            print(f"Error saving report: {e}")
            return None

def main():
    print(r"""
   ___   _____  ___   _   _ ________   __
  / _ \ /  ___|/ _ \ | \ | |_   _\ \ / /
 / /_\ \\ `--./ /_\ \|  \| | | |  \ V / 
 |  _  | `--. \  _  || . ` | | |   \ /  
 | | | |/\__/ / | | || |\  | | |   | |  
 \_| |_/\____/\_| |_/\_| \_/ \_/   \_/  
                                                                                                            
    """)
    print("Advanced OSINT Tool - For Red Team Operations")
    print("=" * 55)
    
    # Get target email
    email = input("Target Email: ").strip()
    
    if not email:
        print("Error: No email provided")
        return
    
    # Initialize tool
    tool = AdvancedOSINTTool()
    
    # Validate email format
    if not tool.check_email_format(email):
        print("Error: Invalid email format")
        return
    
    print("\n[+] Searching OSINT sources...")
    
    # Search various sources
    hudson_data = tool.hudson_rock_search(email)
    hibp_data = tool.haveibeenpwned_search(email)  # Note: HIBP requires API key for full access
    dehashed_data = tool.dehashed_search(email)  # Note: Dehashed requires API key
    
    # Domain analysis
    domain = email.split('@')[-1]
    whois_data = tool.domain_whois_lookup(domain)
    dns_data = tool.dns_lookup(domain)
    
    # Generate report
    report = tool.analyze_results(email, hudson_data, hibp_data, dehashed_data, whois_data, dns_data)
    
    # Display report
    print("\n" + "=" * 80)
    print("SEARCH RESULTS:")
    print("=" * 80)
    print(report)
    
    # Save report
    filename = tool.save_report(email, report)
    if filename:
        print(f"\n[+] Report saved to: {filename}")
    else:
        print("\n[-] Failed to save report")

if __name__ == "__main__":
    main()