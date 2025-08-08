import os
import sys
import time
from colorama import Fore, Style, init
import pyfiglet

# Initialize colorama for colored output
init(autoreset=True)

def print_banner():
    splitterz_ascii = r"""
   _____       ___ __  __
  / ___/____  / (_) /_/ /____  ________
  \__ \/ __ \/ / / __/ __/ _ \/ __/__  /
 ___/ / /_/ / / / /_/ /_/  __/ /   /  /_
/____/ .___/_/_/\__/\__/\___/_/   /__ _/
    /_/  Coded By - Frenzyyy                                  
"""

    print(Fore.MAGENTA + splitterz_ascii + Style.RESET_ALL)

def progress_bar(total, prefix='', suffix='', length=40, fill='█', speed=0.03):
    for i in range(total + 1):
        percent = 100 * (i / float(total))
        filled_length = int(length * i // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        # Color the bar progress green, rest gray
        bar_colored = Fore.GREEN + fill * filled_length + Fore.WHITE + '-' * (length - filled_length)
        print(f'\r{Fore.YELLOW}{prefix} {Style.RESET_ALL}|{bar_colored}{Fore.YELLOW}| {percent:.1f}% {Fore.GREEN}{suffix}{Style.RESET_ALL}', end='\r')
        time.sleep(speed)
    print()

def main():
    print_banner()

    file_path = input(Fore.LIGHTYELLOW_EX + "[?] Enter path to your email list file: " + Style.RESET_ALL).strip()

    if not os.path.isfile(file_path):
        print(Fore.RED + "[!] File not found. Exiting." + Style.RESET_ALL)
        sys.exit()

    with open(file_path, "r", encoding="utf-8") as f:
        emails = [line.strip() for line in f if line.strip()]

    if not emails:
        print(Fore.RED + "[!] No emails found in the file. Exiting." + Style.RESET_ALL)
        sys.exit()

    domains = sorted(set(email.split("@")[-1] for email in emails if "@" in email))

    if not domains:
        print(Fore.RED + "[!] No valid domains found in the emails. Exiting." + Style.RESET_ALL)
        sys.exit()

    print(Fore.MAGENTA + "\n[+] Domains found:" + Style.RESET_ALL)
    for i, domain in enumerate(domains, start=1):
        print(Fore.CYAN + f"   {i}. @{domain}" + Style.RESET_ALL)

    try:
        choice = int(input(Fore.LIGHTYELLOW_EX + "\n[?] Choose domain number to filter: " + Style.RESET_ALL))
        chosen_domain = "@" + domains[choice - 1]
    except (ValueError, IndexError):
        print(Fore.RED + "[!] Invalid choice. Exiting." + Style.RESET_ALL)
        sys.exit()

    print(Fore.LIGHTBLUE_EX + "\n[~] Filtering emails..." + Style.RESET_ALL)
    progress_bar(40, prefix='Progress', suffix='Complete')

    filtered_emails = [email for email in emails if email.lower().endswith(chosen_domain.lower())]

    os.makedirs("result", exist_ok=True)
    output_file = f"result/filtered_{chosen_domain.replace('@','')}.txt"

    print(Fore.LIGHTBLUE_EX + "[~] Saving filtered results..." + Style.RESET_ALL)
    progress_bar(40, prefix='Progress', suffix='Complete')

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(filtered_emails))

    print(Fore.GREEN + f"\n[✓] {len(filtered_emails)} emails found for domain {chosen_domain}" + Style.RESET_ALL)
    print(Fore.BLUE + f"[+] Filtered emails saved to: {output_file}\n" + Style.RESET_ALL)

    for email in filtered_emails:
        print(Fore.GREEN + email + Style.RESET_ALL)

if __name__ == "__main__":
    main()
