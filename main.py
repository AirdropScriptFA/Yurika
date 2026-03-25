import requests
import random
import string
import time
import json
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

def show_info():
    print(f"{Fore.CYAN}{Style.BRIGHT}="*60)
    print(f"{Fore.WHITE}{Style.BRIGHT}Project Info: {Fore.MAGENTA}Yurika AI(r)DROP Waitlist")
    print(f"{Fore.WHITE}{Style.BRIGHT}Powered by:   {Fore.YELLOW}ForestArmy")
    print(f"{Fore.WHITE}{Style.BRIGHT}Telegram:     {Fore.GREEN}t.me/ForestArmy")
    print(f"{Fore.CYAN}{Style.BRIGHT}="*60 + "\n")

def generate_random_email():
    # random email
    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(8, 12)))
    domains = ["@gmail.com", "@outlook.com", "@yahoo.com", "@icloud.com"]
    return f"{prefix}{random.choice(domains)}"

def load_proxies():
    try:
        with open("proxies.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

# --- SETUP ---
show_info()
target_ref = input(f"{Fore.WHITE}Enter Referral Code: ").strip()
use_proxy = input(f"{Fore.WHITE}Use proxies? (yes/no): ").strip().lower()

proxy_list = load_proxies() if use_proxy == "yes" else []
url = "https://www.airdrop.works/api/waitlist"
branches = ["educator", "builder", "creator", "scout", "diplomat"]
total_success = 0

print(f"\n{Fore.GREEN}🚀 [STARTING] Chaos Mode Active (No Batching)...")

try:
    while True:
        branch = random.choice(branches)
        email = generate_random_email()
        
        payload = {
            "email": email,
            "primaryBranch": branch,
            "referralCode": target_ref
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/{random.randint(110, 124)}.0.0.0",
            "Origin": "https://www.airdrop.works",
            "Referer": f"https://www.airdrop.works/?ref={target_ref}"
        }

        # Proxy Logic
        current_proxy = None
        if use_proxy == "yes" and proxy_list:
            p = random.choice(proxy_list)
            current_proxy = {"http": f"http://{p}", "https": f"http://{p}"}

        print(f"{Fore.BLUE}📦 [SENDING]: {Fore.WHITE}{email} {Fore.BLUE}via {Fore.YELLOW}{branch.upper()}")
        
        try:
            response = requests.post(url, json=payload, headers=headers, proxies=current_proxy, timeout=12)
            
            if response.status_code == 200:
                total_success += 1
                data = response.json()
                print(f"{Fore.GREEN}✅ [SUCCESS] Rank: {data.get('rank')} | Total: {total_success}")
                # Near-instant sending with slight jitter to prevent local socket errors
                time.sleep(random.uniform(0.1, 1.0))

            elif response.status_code == 429:
                print(f"{Fore.RED}🛑 [RATE LIMIT] Too many requests. Waiting 30 seconds...")
                time.sleep(30)
                
            else:
                print(f"{Fore.RED}❌ [FAILED] Status: {response.status_code}")
                print(Fore.LIGHTRED_EX + response.text)
                time.sleep(5)

        except Exception as e:
            print(f"{Fore.RED}⚠️ [ERROR]: {e}")
            time.sleep(10)

except KeyboardInterrupt:
    print(f"\n\n{Fore.YELLOW}🛑 Session ended by ForestArmy user.")
    print(f"{Fore.CYAN}Final Stats: {total_success} successful referrals.")
