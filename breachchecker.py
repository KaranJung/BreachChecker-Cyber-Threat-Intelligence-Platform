#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ║
║  ▓                                                                        ▓  ║
║  ▓                 CYBER THREAT INTELLIGENCE PLATFORM                     ▓  ║
║  ▓      Created by Hydra_x001 -- For security research purposes only !!   ▓  ║
║   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
import os
import hashlib
import json
import requests
import time
from tabulate import tabulate
from colorama import init, Fore, Style, Back

def check_python_environment():

    print("🐍 Verifying Python environment...")
    
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print(f"❌ Python {python_version.major}.{python_version.minor} detected")
        print("⚠️  Python 3.6+ required. Please upgrade Python.")
        sys.exit(1)
    else:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}: COMPATIBLE")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ pip: AVAILABLE")
    except subprocess.CalledProcessError:
        print("❌ pip: NOT FOUND")
        print("⚠️  Installing pip...")
        try:
            # Try to install pip using ensurepip
            subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
            print("✅ pip: INSTALLED")
        except subprocess.CalledProcessError:
            print("❌ Failed to install pip automatically")
            print("Please install pip manually: https://pip.pypa.io/en/stable/installation/")
            sys.exit(1)
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ pip: UPDATED TO LATEST")
    except subprocess.CalledProcessError:
        print("⚠️  pip upgrade failed, continuing with current version")

def check_and_install_requirements():
    
    required_packages = {
        'requests': 'requests>=2.28.0',
        'tabulate': 'tabulate>=0.9.0', 
        'colorama': 'colorama>=0.4.6'
    }
    
    missing_packages = []
    
    print("🔍 Checking Python packages...")
    
    for package, version_spec in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package}: FOUND")
        except ImportError:
            print(f"❌ {package}: MISSING")
            missing_packages.append(version_spec)
    
    if missing_packages:
        print(f"\n🚀 Installing {len(missing_packages)} missing packages...")
        for package in missing_packages:
            try:
                print(f"📦 Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package}: INSTALLED")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                print("Please install manually: pip install -r requirements.txt")
                sys.exit(1)
        print("🎉 All dependencies installed successfully!")
    else:
        print("✅ All dependencies satisfied!")
    
    print("─" * 50)

def verify_system_requirements():
    
    print("🔧 SYSTEM REQUIREMENTS VERIFICATION")
    print("=" * 50)
    
    check_python_environment()
    
    check_and_install_requirements()
    
    print("🎯 System ready for breach hunting!")
    print("=" * 50)

verify_system_requirements()

init(autoreset=True)

class C:
    H = Fore.MAGENTA + Style.BRIGHT  # Headers
    I = Fore.CYAN + Style.BRIGHT     # Info
    S = Fore.GREEN + Style.BRIGHT    # Success
    W = Fore.YELLOW + Style.BRIGHT   # Warning
    E = Fore.RED + Style.BRIGHT      # Error
    N = Style.RESET_ALL              # Normal
    B = Fore.BLUE + Style.BRIGHT     # Blue accent
    G = Fore.WHITE + Back.BLACK + Style.BRIGHT  # Highlighted
    D = Fore.BLACK + Style.BRIGHT    # Dim
    P = Fore.MAGENTA                 # Purple

def clear_screen():
    
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    
    clear_screen()
    banner_lines = __doc__.strip().split('\n')
    for line in banner_lines:
        print(f"{C.G}{line}{C.N}")
        time.sleep(0.02)
    
    print(f"\n{C.B}{'═' * 78}{C.N}")
    print(f"{C.I}🌐 System Status: {C.S}ONLINE{C.N} | {C.I}🔍 Breach Database: {C.S}CONNECTED{C.N}")
    print(f"{C.I}⚡ API Endpoints: {C.S}ACTIVE{C.N} | {C.I}🛡️  Security Level: {C.W}MAXIMUM{C.N}")
    print(f"{C.B}{'═' * 78}{C.N}")

BASE = "https://api.xposedornot.com/v1"
PASS_API = "https://passwords.xposedornot.com/v1"

def spin(msg, t=1.5):
    
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    dots = "⣾⣽⣻⢿⡿⣟⣯⣷"
    end = time.time() + t
    i = 0
    while time.time() < end:
        for c in chars:
            progress = int((i % 20) / 2)
            bar = f"{'█' * progress}{'░' * (10 - progress)}"
            sys.stdout.write(f"\r{C.I}{c} {msg} {C.B}[{bar}]{C.N}")
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1
    print(f"\r{C.S}✓ {msg} {C.G}[{'█' * 10}] COMPLETE{C.N}")

def print_section_header(title):
    
    print(f"\n{C.B}╔{'═' * (len(title) + 4)}╗{C.N}")
    print(f"{C.B}║ {C.H}{title}{C.B} ║{C.N}")
    print(f"{C.B}╚{'═' * (len(title) + 4)}╝{C.N}")

def handle(r):
    
    if r.status_code == 200:
        print(f"{C.S}✓ Response: {C.G}200 OK{C.N}")
        return r.json()
    elif r.status_code == 404:
        print(f"{C.W}⚠ Status: {C.W}404 NOT FOUND{C.N}")
    elif r.status_code == 429:
        print(f"{C.E}⚠ Status: {C.E}429 RATE LIMITED{C.N}")
    else:
        print(f"{C.E}✖ Status: {C.E}HTTP {r.status_code}{C.N}")
    return None

def check_email():
    
    print_section_header("🔍 EMAIL BREACH SCANNER")
    e = input(f"{C.I}┌─ Target Email{C.N}\n{C.I}└─► {C.N}").strip()
    
    print(f"\n{C.I}🎯 Initiating scan for: {C.G}{e}{C.N}")
    spin("Scanning breach databases", 2.0)
    
    try:
        data = handle(requests.get(f"{BASE}/check-email/{e}", timeout=10))
        if not data: return
        
        breaches = data.get("breaches", [])
        if breaches:
            b = breaches[0] if isinstance(breaches[0], list) else breaches
            print(f"\n{C.E}💀 SECURITY ALERT: EMAIL COMPROMISED{C.N}")
            print(f"{C.E}{'▓' * 50}{C.N}")
            
            table = []
            for i, x in enumerate(b):
                status = f"{C.E}BREACHED{C.N}"
                table.append([f"{C.W}{i+1}{C.N}", f"{C.E}{x}{C.N}", status])
            
            print(tabulate(table, headers=[f"{C.H}#", f"{C.H}Breach Name", f"{C.H}Status"], 
                          tablefmt="fancy_grid", stralign="left"))
            print(f"\n{C.W}⚠ RECOMMENDATION: Change passwords immediately!{C.N}")
        else:
            print(f"\n{C.S}✅ SECURITY STATUS: CLEAN{C.N}")
            print(f"{C.S}{'▓' * 30}{C.N}")
            print(f"{C.S}No breaches detected for this email address.{C.N}")
    except Exception as ex:
        print(f"{C.E}❌ ERROR: {ex}{C.N}")

def breach_analytics():
    
    print_section_header("📊 BREACH ANALYTICS ENGINE")
    e = input(f"{C.I}┌─ Target Email{C.N}\n{C.I}└─► {C.N}").strip()
    
    print(f"\n{C.I}🔬 Deep scanning: {C.G}{e}{C.N}")
    spin("Analyzing breach patterns", 2.5)
    
    try:
        data = handle(requests.get(f"{BASE}/breach-analytics?email={e}", timeout=10))
        if not data: return
        
        m = data.get("BreachMetrics", {})
        
        r = m.get("risk", [{}])[0]
        rl, rs = r.get("risk_label","Unknown"), r.get("risk_score",0)
        
        print(f"\n{C.B}╔═══════════════════════════════════════╗{C.N}")
        print(f"{C.B}║           RISK ASSESSMENT             ║{C.N}")
        print(f"{C.B}╚═══════════════════════════════════════╝{C.N}")
        
        if rl == "Low":
            color, icon = C.S, "🟢"
        elif rl == "Medium":
            color, icon = C.W, "🟡"
        else:
            color, icon = C.E, "🔴"
            
        print(f"{icon} Risk Level: {color}{rl} ({rs}/100){C.N}")
        
        ind = m.get("industry",[[]])[0]
        if ind:
            print(f"\n{C.B}╔═══════════════════════════════════════╗{C.N}")
            print(f"{C.B}║         INDUSTRY BREAKDOWN            ║{C.N}")
            print(f"{C.B}╚═══════════════════════════════════════╝{C.N}")
            
            tbl = []
            for x, c in ind:
                if c > 0:
                    bar = "█" * min(int(c/5), 20)
                    tbl.append([f"{C.I}{x.upper()}{C.N}", f"{C.W}{c}{C.N}", f"{C.G}{bar}{C.N}"])
            
            if tbl:
                print(tabulate(tbl, headers=[f"{C.H}Industry", f"{C.H}Count", f"{C.H}Visual"], 
                              tablefmt="fancy_grid"))
        
        ps = m.get("passwords_strength",[{}])[0]
        print(f"\n{C.B}╔═══════════════════════════════════════╗{C.N}")
        print(f"{C.B}║       PASSWORD SECURITY PROFILE      ║{C.N}")
        print(f"{C.B}╚═══════════════════════════════════════╝{C.N}")
        
        pst = [
            [f"{C.E}Plain Text{C.N}", f"{C.E}{ps.get('PlainText',0)}{C.N}", "🔓"],
            [f"{C.W}Easy Crack{C.N}", f"{C.W}{ps.get('EasyToCrack',0)}{C.N}", "⚠️"],
            [f"{C.S}Strong Hash{C.N}", f"{C.S}{ps.get('StrongHash',0)}{C.N}", "🔒"],
            [f"{C.I}Unknown{C.N}", f"{C.I}{ps.get('Unknown',0)}{C.N}", "❓"]
        ]
        print(tabulate(pst, headers=[f"{C.H}Type", f"{C.H}Count", f"{C.H}Risk"], 
                      tablefmt="fancy_grid"))
        
    except Exception as ex:
        print(f"{C.E}❌ ERROR: {ex}{C.N}")

def check_password():
    
    print_section_header("🔐 PASSWORD EXPOSURE SCANNER")
    p = input(f"{C.I}┌─ Target Password{C.N}\n{C.I}└─► {C.N}").strip()
    
    print(f"\n{C.I}🔒 Generating secure hash...{C.N}")
    spin("Computing SHA3-512 hash", 1.5)
    
    h = hashlib.sha3_512(p.encode()).hexdigest()[:10]
    print(f"{C.I}🔍 Hash prefix: {C.G}{h}{C.N}")
    
    spin("Querying breach databases", 2.0)
    
    try:
        data = handle(requests.get(f"{PASS_API}/pass/anon/{h}", timeout=10))
        if not data:
            print(f"\n{C.S}✅ PASSWORD STATUS: SECURE{C.N}")
            print(f"{C.S}{'▓' * 40}{C.N}")
            print(f"{C.S}Password not found in known breaches.{C.N}")
            return
        
        s = data.get("SearchPassAnon",{})
        cnt = int(s.get("count",0))
        
        print(f"\n{C.E}💥 PASSWORD COMPROMISED{C.N}")
        print(f"{C.E}{'▓' * 50}{C.N}")
        print(f"{C.E}Exposed {cnt} times in data breaches{C.N}")
        
        chars = s.get("char","").split(";")
        if chars:
            print(f"\n{C.B}╔═══════════════════════════════════════╗{C.N}")
            print(f"{C.B}║        PASSWORD COMPOSITION          ║{C.N}")
            print(f"{C.B}╚═══════════════════════════════════════╝{C.N}")
            
            tbl = []
            for x in chars:
                if ":" in x:
                    k, v = x.split(":")
                    name_map = {
                        "D": ("🔢 Digits", C.I),
                        "A": ("🔤 Letters", C.B), 
                        "S": ("🔣 Special", C.W),
                        "L": ("📏 Length", C.G)
                    }
                    name, color = name_map.get(k, (k, C.N))
                    tbl.append([f"{color}{name}{C.N}", f"{C.W}{v}{C.N}"])
            
            if tbl:
                print(tabulate(tbl, headers=[f"{C.H}Component", f"{C.H}Count"], 
                              tablefmt="fancy_grid"))
        
        print(f"\n{C.E}⚠ CRITICAL: Change this password immediately!{C.N}")
        
    except Exception as ex:
        print(f"{C.E}❌ ERROR: {ex}{C.N}")

def list_domain_breaches():
    """Enhanced domain breach lister with proper API implementation"""
    print_section_header("🌐 DOMAIN BREACH LISTER")
    print(f"{C.I}🔍 Fetching comprehensive domain breach database...{C.N}")
    spin("Querying domain breach registry", 2.0)
    
    try:
        headers = {
            'Content-Length': '0',
            'User-Agent': 'XposedOrNot-CLI/1.0'
        }
        
        response = requests.post(f"{BASE}/domain-breaches", headers=headers, timeout=15)
        data = handle(response)
        
        if not data: 
            print(f"{C.E}❌ Failed to retrieve domain breach data{C.N}")
            return
        
        breaches = []
        if "metrics" in data and "Breaches_Details" in data["metrics"]:
            breaches = data["metrics"]["Breaches_Details"]
        elif "domain_breaches" in data:
            breaches = data["domain_breaches"]
        elif isinstance(data, list):
            breaches = data
        
        if breaches:
            print(f"\n{C.E}🚨 DOMAIN BREACH DATABASE{C.N}")
            print(f"{C.E}{'▓' * 60}{C.N}")
            print(f"{C.I}📊 Total breaches found: {C.W}{len(breaches)}{C.N}")
            
            table_data = []
            for i, breach in enumerate(breaches[:25], 1):  # Limit to first 25 for readability
                breach_name = breach.get("breach", breach.get("name", "Unknown"))
                domain = breach.get("domain", breach.get("Domain", "N/A"))
                records = breach.get("xposed_records", breach.get("records", breach.get("exposed_records", "N/A")))
                
                # Format large numbers
                if isinstance(records, (int, str)) and str(records).isdigit():
                    records = f"{int(records):,}"
                
                table_data.append([
                    f"{C.W}{i}{C.N}",
                    f"{C.E}{breach_name}{C.N}",
                    f"{C.I}{domain}{C.N}",
                    f"{C.W}{records}{C.N}"
                ])
            
            print(f"\n{tabulate(table_data, headers=[f'{C.H}#', f'{C.H}Breach Name', f'{C.H}Domain', f'{C.H}Records Exposed'], tablefmt='fancy_grid', stralign='left')}")
            
            if len(breaches) > 25:
                print(f"\n{C.I}📝 Showing first 25 of {len(breaches)} total breaches{C.N}")
                
            print(f"\n{C.W}⚠ SECURITY INSIGHT: These domains have experienced data breaches{C.N}")
            
        else:
            print(f"\n{C.S}✅ DOMAIN STATUS: CLEAN{C.N}")
            print(f"{C.S}{'▓' * 40}{C.N}")
            print(f"{C.S}No domain breaches found in current database.{C.N}")
            
    except requests.exceptions.Timeout:
        print(f"{C.E}❌ REQUEST TIMEOUT: Server took too long to respond{C.N}")
    except requests.exceptions.ConnectionError:
        print(f"{C.E}❌ CONNECTION ERROR: Unable to reach API server{C.N}")
    except Exception as ex:
        print(f"{C.E}❌ SYSTEM ERROR: {str(ex)}{C.N}")

def list_breaches():
    """Interactive breach database browser"""
    print_section_header("📋 BROWSE ALL BREACHES")
    dom = input(f"{C.I}┌─ Domain (or leave empty){C.N}\n{C.I}└─► {C.N}").strip()
    url = f"{BASE}/breaches?domain={dom}" if dom else f"{BASE}/breaches"
    print(f"{C.I}Loading breaches{C.N}")
    spin("Loading")
    data = handle(requests.get(url, timeout=10))
    if not data: return
    br = data.get("exposedBreaches") or data.get("Exposed Breaches") or []
    if br:
        tbl = []
        for b in br[:20]:
            rid = b.get("breachID") or b.get("Breach ID")
            dom = b.get("domain") or b.get("Domain")
            dt = b.get("breachedDate") or b.get("Breached Date","")
            tbl.append([rid,dom,dt.split("T")[0]])
        print(f"\n{C.S}First {len(tbl)} breaches:{C.N}")
        print(tabulate(tbl,headers=["ID","Domain","Date"],tablefmt="fancy_grid"))
    else:
        print(f"\n{C.S}✅ No breaches.{C.N}")

def main():
    
    print_banner()
    
    actions = {
        "1": ("🔍 Check Email Breaches", check_email),
        "2": ("📊 Breach Analytics", breach_analytics), 
        "3": ("🔐 Check Password Exposure", check_password),
        "4": ("🌐 List Domain Breaches", list_domain_breaches),
        "5": ("📋 Browse All Breaches", list_breaches),
        "0": ("🚪 Exit Console", sys.exit)
    }
    
    while True:
        print(f"\n{C.B}╔═══════════════════════════════════════════════════════════════╗{C.N}")
        print(f"{C.B}║                    🎯 Select the Options 🎯                   ║{C.N}")
        print(f"{C.B}╚═══════════════════════════════════════════════════════════════╝{C.N}")
        
        for k, (n, _) in actions.items():
            if k == "0":
                print(f"{C.E}{k}. {n}{C.N}")
            else:
                print(f"{C.S}{k}. {C.I}{n}{C.N}")
        
        print(f"\n{C.B}{'─' * 63}{C.N}")
        choice = input(f"{C.H}┌─ Select Option{C.N}\n{C.H}└─► {C.N}").strip()
        
        act = actions.get(choice)
        if act:
            print(f"\n{C.I}🚀 Launching: {act[0]}{C.N}")
            time.sleep(0.5)
            act[1]()
            input(f"\n{C.W}Press ENTER to continue...{C.N}")
        else:
            print(f"{C.E}❌ Invalid option. Try again.{C.N}")
            time.sleep(1)

if __name__ == "__main__":
    main()
