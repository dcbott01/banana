import requests
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Base URL for requests
base_url = 'https://interface.carv.io/banana'

# Headers for the requests
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Origin': 'https://banana.carv.io',
    'Referer': 'https://banana.carv.io/',
    'Sec-CH-UA': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'Sec-CH-UA-Mobile': '?0',
    'Sec-CH-UA-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-App-ID': 'carv',
}

def print_welcome_message():
    print(r"""
 
  _  _   _    ____  _   ___    _   
 | \| | /_\  |_  / /_\ | _ \  /_\  
 | .` |/ _ \  / / / _ \|   / / _ \ 
 |_|\_/_/ \_\/___/_/ \_\_|_\/_/ \_\
                                   

    """)
    print(Fore.GREEN + Style.BRIGHT + "BANANA BOT")
    print(Fore.CYAN + Style.BRIGHT + "Jajanin dong orang baik :)")
    print(Fore.YELLOW + Style.BRIGHT + "0x5bc0d1f74f371bee6dc18d52ff912b79703dbb54")
    print(Fore.RED + Style.BRIGHT + "Update Link: https://github.com/dcbott01/banana")
    print(Fore.BLUE + Style.BRIGHT + "Tukang Rename MATI AJA")

def login(tg_info):
    login_payload = {
        "tgInfo": tg_info,
        "InviteCode": ""
    }

    login_url = f'{base_url}/login'
    login_response = requests.post(login_url, headers=headers, json=login_payload)
    time.sleep(1)  # Sleep for 1 second

    login_response_data = login_response.json()
    if 'data' in login_response_data and 'token' in login_response_data['data']:
        return login_response_data['data']['token']
    else:
        print('Token not found in the response.')
        return None

def achieve_quest(quest_id):
    achieve_url = f'{base_url}/achieve_quest'
    achieve_payload = {"quest_id": quest_id}
    response = requests.post(achieve_url, headers=headers, json=achieve_payload)
    return response

def claim_quest(quest_id):
    claim_url = f'{base_url}/claim_quest'
    claim_payload = {"quest_id": quest_id}
    response = requests.post(claim_url, headers=headers, json=claim_payload)
    return response

def do_click(click_count):
    click_url = f'{base_url}/do_click'
    click_payload = {"clickCount": click_count}
    response = requests.post(click_url, headers=headers, json=click_payload)
    return response

def get_lottery_info():
    lottery_info_url = f'{base_url}/get_lottery_info'
    response = requests.get(lottery_info_url, headers=headers)
    return response

def claim_lottery():
    claim_lottery_url = f'{base_url}/claim_lottery'
    claim_payload = {"claimLotteryType": 1}
    response = requests.post(claim_lottery_url, headers=headers, json=claim_payload)
    return response

def do_lottery():
    do_lottery_url = f'{base_url}/do_lottery'
    response = requests.post(do_lottery_url, headers=headers, json={})
    return response

def calculate_remaining_time(lottery_data):
    last_countdown_start_time = lottery_data.get('last_countdown_start_time', 0)
    countdown_interval = lottery_data.get('countdown_interval', 0)  # in minutes
    countdown_end = lottery_data.get('countdown_end', False)

    if not countdown_end:
        current_time = int(time.time() * 1000)  # Current time in milliseconds
        elapsed_time_minutes = (current_time - last_countdown_start_time) / 60000  # Convert elapsed time to minutes
        remaining_time_minutes = max(countdown_interval - elapsed_time_minutes, 0)  # Remaining time in minutes
        return remaining_time_minutes
    return 0

def ask_user_choice(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ['yes', 'no']:
            return choice == 'yes'
        print("Invalid input. Please enter 'yes' or 'no'.")

def process_account(tg_info, perform_lottery, perform_quests):
    token = login(tg_info)
    if token:
        headers['Authorization'] = token
        headers.update({
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        })
        
        # Fetch user info
        user_info_url = f'{base_url}/get_user_info'
        user_info_response = requests.get(user_info_url, headers=headers)
        print(f"{Fore.GREEN}====== Berhasil Mendapatkan Data ======")
        time.sleep(1)  # Sleep for 1 second
        user_info_data = user_info_response.json()
        
        user_info = user_info_data.get('data', {})
        username = user_info.get('username', 'N/A')
        peel = user_info.get('peel', 'N/A')
        usdt = user_info.get('usdt', 'N/A')
        banana_name = user_info.get('equip_banana', {}).get('name', 'N/A')
        today_click_count = user_info.get('today_click_count', 0)
        max_click_count = user_info.get('max_click_count', 0)
        
        print(f"{Fore.CYAN}[Username] : {Fore.MAGENTA}{username}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[Peels] : {Fore.MAGENTA}{peel}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[USDT] : {Fore.MAGENTA}{usdt}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[Banana Name] : {Fore.MAGENTA}{banana_name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[Today Click Count] : {Fore.MAGENTA}{today_click_count}{Style.RESET_ALL}")

        remaining_time_minutes = float('inf')  # Initialize with an arbitrary large value

        # Fetch lottery info if the user chose to perform lottery or to check claim
        if perform_lottery or True:  # Always check lottery info
            lottery_info_response = get_lottery_info()
            time.sleep(1)  # Sleep for 1 second
            lottery_info_data = lottery_info_response.json()
            
            # Calculate remaining time for claiming
            remaining_time_minutes = calculate_remaining_time(lottery_info_data.get('data', {}))

            # Convert remaining time to hours, minutes, seconds
            remaining_hours = int(remaining_time_minutes // 60)
            remaining_minutes = int(remaining_time_minutes % 60)
            remaining_seconds = int((remaining_time_minutes * 60) % 60)

            print(f"{Fore.YELLOW}Sisa Waktu untuk claim Banana: "
                  f"{remaining_hours} jam {remaining_minutes} menit {remaining_seconds} detik")

            # Check for remaining lottery count and perform lottery if needed
            remain_lottery_count = lottery_info_data.get('data', {}).get('remain_lottery_count', 0)
            print(f"{Fore.YELLOW}[Gacha Harvest] : {remain_lottery_count}")
            if remain_lottery_count > 0 and perform_lottery:
                print(f"{Fore.YELLOW}Melakukan Lottery...")
                do_lottery_response = do_lottery()

                # Parse and print lottery result
                if do_lottery_response.status_code == 200:
                    lottery_result = do_lottery_response.json().get('data', {})
                    banana_name = lottery_result.get('name', 'N/A')
                    sell_exchange_peel = lottery_result.get('sell_exchange_peel', 'N/A')
                    sell_exchange_usdt = lottery_result.get('sell_exchange_usdt', 'N/A')

                    print(f"{Fore.GREEN}====== Berhasil Mendapatkan Banana {banana_name} ======")
                    print(f"{Fore.YELLOW}Banana Name : {banana_name}")
                    print(f"{Fore.YELLOW}Peel Limit : {lottery_result.get('daily_peel_limit', 'N/A')}")
                    print(f"{Fore.YELLOW}Harga : {sell_exchange_peel} Peel, {sell_exchange_usdt} Usdt")
                    print(f"{Fore.GREEN}======")
                    
                time.sleep(1)  # Sleep for 1 second

            # Claim lottery if countdown is finished
            if remaining_time_minutes <= 0:
                print(f"{Fore.YELLOW}Claiming Lottery Reward...")
                claim_lottery_response = claim_lottery()

        # Perform quests if user chose to
        if perform_quests:
            print(f"{Fore.GREEN}====== Berhasil Mendapatkan List Quest ======")

            # Check for clicks if below max clicks
            if today_click_count < max_click_count:
                click_count = max_click_count - today_click_count
                if click_count > 0:
                    print(f"{Fore.YELLOW}Performing {click_count} clicks...")
                    do_click(click_count)
                    time.sleep(1)  # Sleep for 1 second
                else:
                    print(f"{Fore.YELLOW}Click tidak diperlukan atau sudah mencapai batas maksimum.")
            
            # Fetch quest list
            quest_list_url = f'{base_url}/get_quest_list'
            quest_list_response = requests.get(quest_list_url, headers=headers)
            time.sleep(1)  # Sleep for 1 second
            quest_list_data = quest_list_response.json()
            
            # Extract and print quest names and claim statuses
            quest_list = quest_list_data.get('data', {}).get('quest_list', [])
            for index, quest in enumerate(quest_list, start=1):
                quest_name = quest.get('quest_name', 'N/A')
                is_achieved = quest.get('is_achieved', False)
                is_claimed = quest.get('is_claimed', False)
                quest_id = quest.get('quest_id')
                
                # Convert boolean to Yes/No
                achieved_status = "Yes" if is_achieved else "No"
                claimed_status = "Yes" if is_claimed else "No"
                
                # Color coding for quest details
                quest_name_color = Fore.CYAN
                achieved_color = Fore.GREEN if is_achieved else Fore.RED
                claimed_color = Fore.GREEN if is_claimed else Fore.RED
                
                print(f"{Fore.BLUE}[Quest {index}] : {quest_name_color}{quest_name} {Fore.BLUE}, "
                      f"[Is Achieved] : {achieved_color}{achieved_status} {Fore.BLUE}, "
                      f"[Is Claimed] : {claimed_color}{claimed_status}{Style.RESET_ALL}")
                
                # Skip the achievement process for 'bind' quests
                if 'bind' in quest_name.lower():
                    if not is_achieved:
                        print(f"{Fore.YELLOW}Skipping Quest, Please do by Yourself")
                        time.sleep(1)  # Sleep for 1 second
                        continue
                
                # Achieve quests if not achieved
                if not is_achieved:
                    # Automatically achieve the quest without prompting
                    achieve_response = achieve_quest(quest_id)
                    time.sleep(1)  # Sleep for 1 second

# Claim quests if achieved and not claimed
                if is_achieved and not is_claimed:
                    # Automatically claim the quest without prompting
                    claim_response = claim_quest(quest_id)
                    time.sleep(1)  # Sleep for 1 second


        print(f"{Fore.GREEN}====== Memproses Akun Berikutnya.... ======")
    
    else:
        print(f"{Fore.RED}Unable to fetch user info and quest list due to missing token.")

def main():
    # Print the welcome message
    print_welcome_message()

    # Read tg_info from file
    with open('query.txt', 'r') as file:
        tg_infos = file.readlines()

    # Collect user choices once at the start
    perform_lottery = ask_user_choice("Do you want to do gacha Harvest? (yes/no): ")
    perform_quests = ask_user_choice("Do you want to do quests? (yes/no): ")

    while True:
        min_remaining_time = float('inf')

        # Process all accounts and find the one with the minimum remaining claim time
        for index, tg_info in enumerate(tg_infos, start=1):
            tg_info = tg_info.strip()
            if tg_info:
                print(f"{Fore.CYAN}====== Memproses Akun {index} ======")
                token = login(tg_info)
                if token:
                    headers['Authorization'] = token
                    headers.update({
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache'
                    })
                    
                    # Fetch lottery info
                    lottery_info_response = get_lottery_info()
                    time.sleep(1)  # Sleep for 1 second
                    lottery_info_data = lottery_info_response.json()
                    
                    # Calculate remaining time for claiming
                    remaining_time_minutes = calculate_remaining_time(lottery_info_data.get('data', {}))
                    if remaining_time_minutes < min_remaining_time:
                        min_remaining_time = remaining_time_minutes

                    process_account(tg_info, perform_lottery, perform_quests)
                    time.sleep(5)  # Sleep for 5 seconds between accounts

        if min_remaining_time < float('inf'):
            # Convert remaining time to hours, minutes, seconds
            remaining_hours = int(min_remaining_time // 60)
            remaining_minutes = int(min_remaining_time % 60)
            remaining_seconds = int((min_remaining_time * 60) % 60)

            print(f"{Fore.GREEN}Menunggu {remaining_hours} jam {remaining_minutes} menit {remaining_seconds} detik sebelum memproses ulang...")
            time.sleep(min_remaining_time * 60)  # Sleep for the minimum remaining time before re-evaluating
        else:
            print(f"{Fore.RED}Tidak ada akun yang memenuhi kriteria claim dalam waktu dekat.")
            print(f"{Fore.GREEN}Menunggu waktu sebelum memproses ulang...")
            time.sleep(10 * 60)  # Sleep for 10 minutes before re-evaluating

if __name__ == '__main__':
    main()
