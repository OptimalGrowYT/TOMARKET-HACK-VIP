import json
import random
from urllib.parse import parse_qs, unquote
from colorama import Fore, Style, init
import time
from tomarket import Tomarket, print_timestamp
import sys
import progressbar  # For progress bars
import asyncio
import cloudscraper
import uuid
import base64
from loguru import logger
from colorama import Fore, Style

# Base64 encoded banner string
encoded_banner = """
Ky0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSsKfCDilojilojilojilojilojilojilZcg4paI4paI4paI4paI4paI4paI4pWXIOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVl+KWiOKWiOKVlyAgICDilojilojilojilZcgICDilojilojilojilZcg4paI4paI4paI4paI4paI4pWXIOKWiOKWiOKVlyAgICAgfAp84paI4paI4pWU4pWQ4pWQ4pWQ4paI4paI4pWX4paI4paI4pWU4pWQ4pWQ4paI4paI4pWX4pWa4pWQ4pWQ4paI4paI4pWU4pWQ4pWQ4pWd4paI4paI4pWRICAgIOKWiOKWiOKWiOKWiOKVlyDilojilojilojilojilZHilojilojilZTilZDilZDilojilojilZfilojilojilZEgICAgIHwKfOKWiOKWiOKVkSAgIOKWiOKWiOKVkeKWiOKWiOKWiOKWiOKWiOKWiOKVlOKVnSAgIOKWiOKWiOKVkSAgIOKWiOKWiOKVkSAgICDilojilojilZTilojilojilojilojilZTilojilojilZHilojilojilojilojilojilojilojilZHilojilojilZEgICAgIHwKfOKWiOKWiOKVkSAgIOKWiOKWiOKVkeKWiOKWiOKVlOKVkOKVkOKVkOKVnSAgICDilojilojilZEgICDilojilojilZEgICAg4paI4paI4pWR4pWa4paI4paI4pWU4pWd4paI4paI4pWR4paI4paI4pWU4pWQ4pWQ4paI4paI4pWR4paI4paI4pWRICAgICB8CnzilZrilojilojilojilojilojilojilZTilZ3ilojilojilZEgICAgICAgIOKWiOKWiOKVkSAgIOKWiOKWiOKVkSAgICDilojilojilZEg4pWa4pWQ4pWdIOKWiOKWiOKVkeKWiOKWiOKVkSAg4paI4paI4pWR4paI4paI4paI4paI4paI4paI4paI4pWXfAp8IOKVmuKVkOKVkOKVkOKVkOKVkOKVnSDilZrilZDilZ0gICAgICAgIOKVmuKVkOKVnSAgIOKVmuKVkOKVnSAgICDilZrilZDilZ0gICAgIOKVmuKVkOKVneKVmuKVkOKVnSAg4pWa4pWQ4pWd4pWa4pWQ4pWQ4pWQ4pWQ4pWQ4pWQ4pWdfAp8ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfAp8IOKWiOKWiOKWiOKWiOKWiOKWiOKVlyDilojilojilojilojilojilojilZcgIOKWiOKWiOKWiOKWiOKWiOKWiOKVlyDilojilojilZcgICAg4paI4paI4pWXICAgIOKWiOKWiOKVlyAgIOKWiOKWiOKVl+KWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVlyAgfAp84paI4paI4pWU4pWQ4pWQ4pWQ4pWQ4pWdIOKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVl+KWiOKWiOKVlOKVkOKVkOKVkOKWiOKWiOKVl+KWiOKWiOKVkSAgICDilojilojilZEgICAg4pWa4paI4paI4pWXIOKWiOKWiOKVlOKVneKVmuKVkOKVkOKWiOKWiOKVlOKVkOKVkOKVnSAgfAp84paI4paI4pWRICDilojilojilojilZfilojilojilojilojilojilojilZTilZ3ilojilojilZEgICDilojilojilZHilojilojilZEg4paI4pWXIOKWiOKWiOKVkSAgICAg4pWa4paI4paI4paI4paI4pWU4pWdICAgIOKWiOKWiOKVkSAgICAgfAp84paI4paI4pWRICAg4paI4paI4pWR4paI4paI4pWU4pWQ4pWQ4paI4paI4pWX4paI4paI4pWRICAg4paI4paI4pWR4paI4paI4pWR4paI4paI4paI4pWX4paI4paI4pWRICAgICAg4pWa4paI4paI4pWU4pWdICAgICDilojilojilZEgICAgIHwKfOKVmuKWiOKWiOKWiOKWiOKWiOKWiOKVlOKVneKWiOKWiOKVkSAg4paI4paI4pWR4pWa4paI4paI4paI4paI4paI4paI4pWU4pWd4pWa4paI4paI4paI4pWU4paI4paI4paI4pWU4pWdICAgICAgIOKWiOKWiOKVkSAgICAgIOKWiOKWiOKVkSAgICAgfAp8IOKVmuKVkOKVkOKVkOKVkOKVkOKVnSDilZrilZDilZ0gIOKVmuKVkOKVnSDilZrilZDilZDilZDilZDilZDilZ0gIOKVmuKVkOKVkOKVneKVmuKVkOKVkOKVnSAgICAgICAg4pWa4pWQ4pWdICAgICAg4pWa4pWQ4pWdICAgICB8CistLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0r==
"""  # The base64-encoded string of your banner

def _banner():
    # Decode the base64 encoded banner
    decoded_banner = base64.b64decode(encoded_banner).decode()

    # Print the decoded banner
    print(Fore.WHITE + Style.BRIGHT + decoded_banner + Style.RESET_ALL)
    print(Fore.YELLOW + f" CREATED BY : DR ABDUL MATIN KARIMI: ⨭ {Fore.GREEN}https://t.me/doctor_amk")
    print(Fore.WHITE + f" DOWNLOAD LATEST HACKS HERE ➤ {Fore.GREEN}https://t.me/optimalgrowYT")
    print(Fore.RED  + f" LEARN HACKING HERE ➤ {Fore.GREEN}https://www.youtube.com/@optimalgrowYT/videos")
    print(Fore.YELLOW + f" PASTE YOUR (Query ID) INTO QUERY_ID.TXT FILE AND PRESS START ")
    print(Fore.GREEN + f"      ▁ ▂ ▄ ▅ ▆ ▇ █ 丅𝐎𝐌𝐀𝐑𝐊ⓔ丅 𝐕𝐢𝐏 𝐇𝐀𝐂𝐊 █ ▇ ▆ ▅ ▄ ▂ ▁ ")
    log_line()

def log_line():
    print(Fore.GREEN + "=☠=" * 22 + Style.RESET_ALL)

# Initialize colorama
init(autoreset=True)

# Call banner function at the start of the script
_banner()

# Add your main logic here after the banner is printed
# For example, prompt user for input or further actions.


# Initialize colorama for cross-platform compatibility
init(autoreset=True)

# Function to display a bold and stylish header
def show_header(title):
    print(f"{Fore.LIGHTCYAN_EX + Style.BRIGHT}")
    print("=" * 50)
    print(f"{title.center(50)}")
    print("=" * 50)
    print(Style.RESET_ALL)

# Load credentials from the file
def load_credentials():
    try:
        with open('query_id.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print(f"{Fore.RED + Style.BRIGHT}[ERROR] File 'query_id.txt' not found.{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}[ERROR] Error loading credentials: {e}{Style.RESET_ALL}")
        return []

# Parse query to extract necessary information
def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query

# Get token from the tokens file
def get(id):
    try:
        with open("tokens.json", "r") as f:
            tokens = json.load(f)
        return tokens.get(str(id))
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}[ERROR] Error reading tokens: {e}{Style.RESET_ALL}")
        return None

# Save token to the file
def save(id, token):
    try:
        with open("tokens.json", "r") as f:
            tokens = json.load(f)
        tokens[str(id)] = token
        with open("tokens.json", "w") as f:
            json.dump(tokens, f, indent=4)
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}[ERROR] Error saving token: {e}{Style.RESET_ALL}")

# Generate tokens if not present
def generate_token():
    tom = Tomarket()
    queries = load_credentials()
    total_queries = len(queries)

    show_header("TOKEN GENERATOR")

    for index, query in enumerate(queries):
        parse = parse_query(query)
        user = parse.get('user')
        print(f"{Fore.CYAN + Style.BRIGHT}[ Account {index + 1}/{total_queries} - {user.get('username', '')} ]{Style.RESET_ALL}")

        token = get(user['id'])
        if token is None:
            print(f"{Fore.YELLOW}Generating token for {user.get('username', '')}...{Style.RESET_ALL}")
            time.sleep(2)
            token = tom.user_login(query)
            save(user.get('id'), token)
            print(f"{Fore.GREEN}[SUCCESS] Token generated successfully!{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[SUCCESS] Token already available!{Style.RESET_ALL}")

# Main task handling
def main():
    tom = Tomarket()

    show_header("MAIN TASK SELECTION")

    auto_task = input(f"{Fore.LIGHTCYAN_EX}Auto clear task (y/n): {Style.RESET_ALL}").strip().lower()
    auto_game = input(f"{Fore.LIGHTCYAN_EX}Auto play game (y/n): {Style.RESET_ALL}").strip().lower()
    auto_combo = input(f"{Fore.LIGHTCYAN_EX}Auto claim combo puzzle (y/n): {Style.RESET_ALL}").strip().lower()
    random_number = input(f"{Fore.LIGHTCYAN_EX}Set random score in game 300-500 (y/n): {Style.RESET_ALL}").strip().lower()
    free_raffle = input(f"{Fore.LIGHTCYAN_EX}Enable free raffle (y/n): {Style.RESET_ALL}").strip().lower()
    used_stars = input(f"{Fore.LIGHTCYAN_EX}Use star for: 1. Upgrade rank | 2. Auto spin | N.Skip All Task: {Style.RESET_ALL}").strip().lower()

    while True:
        queries = load_credentials()
        total_queries = len(queries)
        delay = int(3 * random.randint(3700, 3750))  # Random delay between actions
        start_time = time.time()

        # Progress bar for task completion
        progress = progressbar.ProgressBar(widgets=[
            ' [', progressbar.Percentage(), '] ',
            progressbar.Bar(), ' ', progressbar.ETA()
        ], maxval=total_queries).start()

        # Iterate over the queries and handle actions
        for index, query in enumerate(queries):
            mid_time = time.time()
            total_delay = delay - (mid_time - start_time)
            parse = parse_query(query)
            user = parse.get('user')
            token = get(user['id'])
            if token is None:
                token = tom.user_login(query)
                save(user.get('id'), token)
                time.sleep(2)

            print(f"{Fore.CYAN + Style.BRIGHT}[ Account {index + 1}/{total_queries} - {user.get('username', '')} ]{Style.RESET_ALL}")
            tom.rank_data(token=token, selector=used_stars)
            time.sleep(2)
            tom.claim_daily(token=token)
            time.sleep(2)
            tom.start_farm(token=token)
            time.sleep(2)

            if free_raffle == "y":
                tom.free_spin(token=token, query=query)
            time.sleep(2)

            # Update progress bar
            progress.update(index + 1)

        progress.finish()

        if auto_task == 'y':
            for index, query in enumerate(queries):
                mid_time = time.time()
                total_delay = delay - (mid_time - start_time)
                if total_delay <= 0:
                    break
                parse = parse_query(query)
                user = parse.get('user')
                token = get(user['id'])
                if token is None:
                    token = tom.user_login(query)
                print(f"{Fore.CYAN + Style.BRIGHT}[ Account {index + 1}/{total_queries} - {user.get('username', '')} ]{Style.RESET_ALL}")
                tom.list_tasks(token=token, query=query)
                if auto_combo == 'y':
                    tom.puzzle_task(token, query)
                time.sleep(2)

        if auto_game == 'y':
            for index, query in enumerate(queries):
                mid_time = time.time()
                total_delay = delay - (mid_time - start_time)
                if total_delay <= 0:
                    break
                parse = parse_query(query)
                user = parse.get('user')
                token = get(user['id'])
                if token is None:
                    token = tom.user_login(query)
                print(f"{Fore.CYAN + Style.BRIGHT}[ Account {index + 1}/{total_queries} - {user.get('username', '')} ]{Style.RESET_ALL}")
                tom.user_balance(token=token, random_number=random_number)
                time.sleep(2)

        # Time delay before restarting
        end_time = time.time()
        total = delay - (end_time - start_time)
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"{Fore.YELLOW + Style.BRIGHT}[ Restarting in {int(hours)} Hours {int(minutes)} Minutes {int(seconds)} Seconds ]{Style.RESET_ALL}")
        if total > 0:
            time.sleep(total)

# Check eligibility and claim rewards
def check_elig():
    tom = Tomarket()
    queries = load_credentials()
    total_queries = len(queries)
    selector_weekly = input(f"{Fore.LIGHTCYAN_EX}Auto claim $TOMA weekly (y/n): {Style.RESET_ALL}").strip().lower()

    show_header("CHECK ELIGIBILITY & CLAIM SEASON REWARD")

    for index, query in enumerate(queries):
        parse = parse_query(query)
        user = parse.get('user')
        print(f"{Fore.CYAN + Style.BRIGHT}[ Account {index + 1}/{total_queries} - {user.get('username', '')} ]{Style.RESET_ALL}")
        token = get(user['id'])
        if token is None:
            print(f"{Fore.YELLOW}Generating token for {user.get('username', '')}...{Style.RESET_ALL}")
            time.sleep(2)
            token = tom.user_login(query)
            save(user.get('id'), token)
            print(f"{Fore.GREEN}[SUCCESS] Token generated successfully!{Style.RESET_ALL}")
        time.sleep(3)
        tom.check_elig(token, query)
        time.sleep(2)
        tom.airdrop_task(token, query)
        time.sleep(2)
        if selector_weekly == "y":
            tom.checked(token=token, query=query)

# Starting point
def start():
    show_header("TOMARKET BOT")

    print(f"""
{Fore.LIGHTCYAN_EX}
        Find new airdrop & bot here: t.me/sansxgroup
              
        Select an option:
        1. Claim daily tasks
        2. Generate token
        3. Check eligibility & claim season reward
{Style.RESET_ALL}
    """)
    selector = input(f"{Fore.LIGHTMAGENTA_EX}Select option (1|2|3): {Style.RESET_ALL}").strip().lower()

    if selector == '1':
        main()
    elif selector == '2':
        generate_token()
    elif selector == '3':
        check_elig()
    else:
        print(f"{Fore.RED}[ERROR] Invalid selection! Exiting...{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        start()
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}[ERROR] {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"{Fore.RED}[INFO] Exiting program...{Style.RESET_ALL}")
        sys.exit(0)
