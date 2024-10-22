import bcrypt
import hashlib
import os
import json
import uuid
import re
import sys
import shutil
import threading
import time
import random
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import textwrap
from textwrap import wrap
from datetime import datetime
import base64
from colorama import Fore, Style, Back, init
init(autoreset=True)

width = os.get_terminal_size().columns

TRANSACTIONS_FILE = 'transactions.json'
SHOP_FILE = 'shop.json'
USERS_FILE = 'users.json'
MESSAGES_FILE = 'messages.json'
GROUPS_FILE = 'groups.json'
FUSERS_FILE = 'fusers.json'
GMESSAGES_FILE = 'gmessages.json'
THEME_FILE = 'theme.json'
POSTS_FILE = 'posts.json'
SAVED_MESSAGES_FILE = 'saved_messages.json'
FILES_FILE = 'files.json'
REFER_FILE = 'refer.json'
ITEMS_FILE = 'items.json'
USHOP_FILE = 'ushop.json'

FILES_TO_REFRESH = {
    'transactions': 'transactions.json',
    'shop': 'shop.json',
    'users': 'users.json',
    'messages': 'messages.json',
    'groups': 'groups.json',
    'fusers': 'fusers.json',
    'gmessages': 'gmessages.json',
    'theme': 'theme.json',
    'posts': 'posts.json',
    'saved_messages': 'saved_messages.json',
    'files': 'files.json',
    'refer': 'refer.json',
    'items': 'items.json',
    'ushop': 'ushop.json'
}

data_store = {}

def load_json(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f, indent=4)
        return {}
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                data = {}
                with open(file, 'w') as f:
                    json.dump(data, f, indent=4)
            return data
    except json.JSONDecodeError:
        with open(file, 'w') as f:
            json.dump({}, f, indent=4)
        return {}
        
# Define global variables for each data type
users = {}
transactions = {}
shop = {}
messages = {}
groups = {}
fusers = {}
gmessages = {}
theme = {}
posts = {}
saved_messages = {}
files = {}
refer = {}
items = {}
ushop = {}

def load_data():
    """Loads all necessary data from JSON files into global variables."""
    global users, transactions, shop, messages, groups, fusers, gmessages, theme
    global posts, saved_messages, files, refer, items, ushop

    users = load_json(USERS_FILE)  # Load user data
    
    transactions = load_json(TRANSACTIONS_FILE)  # Load transactions

    shop = load_json(SHOP_FILE)  # Load shop data
    
    messages = load_json(MESSAGES_FILE)  # Load messages
    
    groups = load_json(GROUPS_FILE)  # Load groups

    fusers = load_json(FUSERS_FILE)  # Load friend users

    gmessages = load_json(GMESSAGES_FILE)  # Load group messages

    theme = load_json(THEME_FILE)  # Load theme
    posts = load_json(POSTS_FILE)  # Load posts
    saved_messages = load_json(SAVED_MESSAGES_FILE)  # Load saved messages

    files = load_json(FILES_FILE)  # Load files

    refer = load_json(REFER_FILE)  # Load referrals

    items = load_json(ITEMS_FILE)  # Load items
    ushop = load_json(USHOP_FILE)  # Load user shop
    
def auto_load_data():
    """Continuously load data every 0.1 seconds."""
    while True:
        load_data()
        time.sleep(0.1)

# Start the auto-load data thread
loading_thread = threading.Thread(target=auto_load_data, daemon=True)
loading_thread.start()    

def save_json(file, data):
    try:
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(Fore.RED + f"Failed to save data to {file}: {e}")
        
# Function to refresh a single file every 0.1 seconds
def auto_refresh(file_path, storage_key):
    while True:
        data = load_json(file_path)
        data_store[storage_key] = data  # Update the global data store for this file
        time.sleep(0.1)  # Sleep for 0.1 seconds before refreshing again


# Function to start all auto-refresh processes in separate threads
def start_auto_refresh():
    for key, file_path in FILES_TO_REFRESH.items():
        # Start a thread for each file, refreshing every 0.1 seconds
        threading.Thread(target=auto_refresh, args=(file_path, key), daemon=True).start()
        
def get_terminal_width():
    """Get the width of the terminal."""
    try:
        return shutil.get_terminal_size((80, 20)).columns
    except Exception as e:
        print(f"Error detecting terminal size: {e}")
        return 80         
        
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def centered_loading_animation(message, delay, symbols=['🕛', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚'],iterations=10):
    terminal_width = width
    
    for _ in range(iterations):  # Run for a fixed number of iterations
        for symbol in symbols:
            # Create the full loading string
            display_message = f'{message} {symbol}'
            # Center the message
            centered_message = display_message.center(terminal_width)
            
            sys.stdout.write(f'\r{centered_message}')  # Overwrite the line
            sys.stdout.flush()  # Ensure the output is displayed immediately
            time.sleep(0.1)  # Use the passed delay for animation timing
    
    # Clear the line on exit
    sys.stdout.write('\r' + ' ' * terminal_width + '\r')
    sys.stdout.flush() 
    
def centered_loading_animation_az(message, delay, symbols=['⏳', '⌛'],iterations=10):
    terminal_width = width
    
    for _ in range(iterations):  # Run for a fixed number of iterations
        for symbol in symbols:
            # Create the full loading string
            display_message = f'{message} {symbol}'
            # Center the message
            centered_message = display_message.center(terminal_width)
            
            sys.stdout.write(f'\r{centered_message}')  # Overwrite the line
            sys.stdout.flush()  # Ensure the output is displayed immediately
            time.sleep(0.5)  # Use the passed delay for animation timing
    
    # Clear the line on exit
    sys.stdout.write('\r' + ' ' * terminal_width + '\r')
    sys.stdout.flush()        
    
def masked_input(prompt):
    """Custom input function that displays a mask character instead of user input."""
    print(prompt, end='', flush=True)
    pin = ''
    while True:
        char = getch()
        if char in ('\r', '\n'):  # Enter key
            print()  # Move to the next line
            break
        elif char == '\x7f':  # Backspace key
            if pin:
                pin = pin[:-1]  # Remove last character
                # Move cursor back and overwrite with spaces, then return
                sys.stdout.write('\b \b')  
        else:
            pin += char
            sys.stdout.write('🙈')  # Print the mask character
        sys.stdout.flush()
    return pin

def getch():
    """Get a single character from standard input without echoing."""
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch    
    
def validate_email(email):
    # Define the regex pattern for a valid email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Check if the input matches the email pattern
    if re.match(email_regex, email):
        return True
    else:
        return False
    

# Hash an email using SHA-256 (for user identification)
def hash_email(emails):
    return hashlib.sha256(emails.encode('utf-8')).hexdigest()

# Hash a password or PIN using bcrypt
def hash_password_pin(plain_text):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_text.encode('utf-8'), salt)

# Verify a password or PIN against the stored hash
def verify_password_pin(plain_text, hashed_value):
    return bcrypt.checkpw(plain_text.encode('utf-8'), hashed_value)

# Center the text in the terminal
def center_texts(text):
    terminal_width = get_terminal_width()
    return text.center(terminal_width)
    
def center_text(text):
    """Center the given text based on the terminal width."""
    width = os.get_terminal_size().columns
    centered = text.center(width)
    return centered    
    
def center_emoji(emoji):
    """Center the given emoji based on the terminal width."""
    width = os.get_terminal_size().columns
    centered = emoji.center(width)
    return centered        

# Loading animation
def loading_az():
    animation = ['⌛ loading ..... ', '⏳ loading ..... '] * 10
    for frame in animation:
        time.sleep(0.3)
        sys.stdout.write("\r" + frame)
        sys.stdout.flush()
        
def register_user(name, email, password, pin):
    users = data_store.get('users', {})
    
    # Check if the user is already registered
    if hash_email(email) in users:
        print(Fore.RED + "You already have an account.")
        time.sleep(2)
        return start()

    emojis = ["🧛", "👹", "🤡", "👽", "🤖", "🤑", "😎", "🤓", "🥸", "🤕", "🤠", "👻", "🎃", "😈", "😇", "🤩", "❤️", "😺", "😹", "😿", "😸", "💝", "💓", "💘", "💗", "🫂", "❣️", "💌", "💞", "💀", "👀", "👁️", "🗣️", "🧟", "🧌", "🎄", "🥷", "👼", "💂", "🫅", "🤵", "👰", "🚀", "👷", "👮", "🕵️", "✈️", " 🔬", "⚕️", "🧑", "🏭", "🚒", "🧑🌾", "🏫", "🎓", "🧑‍💼", "⚖️", "🧑‍💻", "🎤", "🎨", "🍳", "👳", "🧕", "👲", "🌻", "🏵️", "🌸", "🥀", "🌹", "💐", "🌍", "🌎", "🐯", "🐼", "🐨", "🐻", "🐶", "🐨", "🐹", "🐭", "🐣", "🐥", "🦭", "🦢", "🦀", "🐋", "🐟", "🐞", "🍑", "🎁", "🎊", "🪩", "💰", "🧸"]  

    hashed_email = hash_email(email)
    hashed_password = hash_password_pin(password)
    hashed_pin = hash_password_pin(pin)  # Fixed missing argument
    user_emoji = random.choice(emojis)
    balance = '0.00'
    username = name.replace(" ", "_") + str(uuid.uuid4())[:5]
    refer = str(uuid.uuid4())
    
    # Store the user's data
    users[hashed_email] = {
        'name': name,
        'username': username,
        'password': hashed_password.decode('utf-8'),  # No need to decode, store as bytes
        'pin': hashed_pin.decode('utf-8'),  # No need to decode, store as bytes
        'country': "",
        'bio': "",
        'sex': "",
        'age': "",
        'balance': balance,
        'user_emoji': user_emoji,
        'refer': refer
    }
    
    save_json(USERS_FILE, users)
    return username

# Log in a user
def login_user(email, password):
    users = data_store.get('users', {})
    if email == admin["email"] and password == admin["password"]:
        loading_az()
        admin_dashboard(users, email)
        return "admin"
    
    hashed_email = hash_email(email)
    
    # Check if the user exists
    if hashed_email not in users:
        print(Fore.RED +"\n"+" Email not found.")
        time.sleep(2)
        return loginn
    
    stored_password = users[hashed_email]['password']
    
    # Verify the password
    if verify_password_pin(password, stored_password.encode('utf-8')):
        print("")
        centered_loading_animation(Fore.BLUE+"Logging in ... ", 0.1)
        time.sleep(0.5)
        face(users, email)
        return email
    else:
        print(Fore.RED +center_text("\n🚨 Invalid credentials 🙊"))
        time.sleep(2)
        return loginn()
        
def like(users, email, post):
    """Allow a user to like or unlike a post and display formatted like count."""
    hashed_email = hash_email(email)
    user_data = users.get(hashed_email)

    # Check if the user has liked this post before
    if user_data['username'] in post['likes']:
        # User already liked the post, so unlike it
        post['likes'].remove(user_data['username'])
        post['count'] -= 1  # Decrease like count
        save_post(post)  # Update the posts file
    else:
        # User has not liked the post, so like it
        post['likes'].append(user_data['username'])
        post['count'] += 1  # Increase like count
        save_post(post)  # Update the posts file

    time.sleep(0.3)  # Show the message for 0.3 seconds
    return post
    
def format_like_count(count):
    """Format the like count to display with 'k' for thousand, 'M' for million, and 'B' for billion."""
    if count >= 1_000_000_000:
        return f"{count / 1_000_000_000:.1f}B"  # Format billions as 'B'
    elif count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"  # Format millions as 'M'
    elif count >= 1_000:
        return f"{count / 1_000:.2f}k"  # Format thousands as 'k'
    else:
        return str(count)  # Display count as-is if less than 1000    

def display_post(post):
    """Display the current post details including the updated like count."""
    print(Style.DIM + center_text(f"{post['name']} • {post['username']}"))
    print(Style.DIM + "-" * width)
    print("")
    print(Style.DIM + Fore.BLUE + post['content'])
    print("")
    
    # Format timestamp and like count
    formatted_time = format_time_ago(post['timestamp'])
    like_count = post['count']
    formatted_like_count = format_like_count(like_count)  # Format the like count
    print("\n" + Style.DIM + f" {formatted_time}" + Style.RESET_ALL + Style.DIM + f" ♥️ {formatted_like_count}".rjust(width - 13))
    print(Style.DIM + "-" * width)
    
def save_post(post):
    """Update the posts file with the new like count."""
    posts = data_store.get('posts', {})
    for user_posts in posts.values():
        for p in user_posts:
            if p['id'] == post['id']:
                p['count'] = post['count']
                p['likes'] = post['likes']
                break
    save_json(POSTS_FILE, posts) 
    
def format_time_ago(timestamp):
    """Format the time difference from now to the given timestamp."""
    now = datetime.now()
    post_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    time_diff = now - post_time

    if time_diff.days > 0:
        return f"{time_diff.days} days ago"
    elif time_diff.seconds // 3600 > 0:
        return f"{time_diff.seconds // 3600} hrs ago"
    elif time_diff.seconds // 60 > 0:
        return f"{time_diff.seconds // 60} mins ago"
    else:
        return f"{time_diff.seconds} secs ago"

def face(users, email):
    posts= data_store.get('posts', {})
    all_posts = []
    
    for user, data in users.items():
        user_posts = data_store['posts'].get(data['username'], [])
        all_posts.extend(user_posts)

    sorted_posts = sorted(all_posts, key=lambda x: x['timestamp'], reverse=True)
    
    hashed_email = hash_email(email)
    user_data = users.get(hashed_email)
    current_post_index = 0
    
    while True:  # Main loop to stay within the 'face' function
        clear_screen()
        print(Back.WHITE)
        print(Fore.BLUE + "\n" + "  Maskbook" + Style.RESET_ALL + "  " + "M. MENU   ".rjust(width - len("  Maskbook") - 2))
        print(" ")
        print(Style.DIM + "—" * width)
        print("\n" + f"  {user_data['user_emoji']} " + Style.RESET_ALL + "   ( " + Fore.GREEN + "What's on your mind?" + Style.RESET_ALL + " )" + "    📷")
        print(Fore.YELLOW + Style.DIM + "\n     [1] Create Post  [2] View More" + Style.RESET_ALL)
        print(" ")
        print(Style.DIM + "—" * width)
        print("")
        print(Style.BRIGHT + center_text("📸 Posts"))
        print("\n")

        if sorted_posts:
            # Show the current post
            post = sorted_posts[current_post_index]
            print(Style.DIM + center_text(f"{post['name']} • {post['username']}"))
            print(Style.DIM + "-" * width)
            print("")
            print(Style.DIM + Fore.BLUE + post['content'])
            print("")
            formatted_time = format_time_ago(post['timestamp'])
            like_count = post['count']
            formatted_like_count = format_like_count(like_count)  # Format the like count
            print("\n" + Style.DIM + f" {formatted_time}" + Style.RESET_ALL + Style.DIM + f" ♥️ {formatted_like_count}".rjust(width - 13))
            print(Style.DIM + "-" * width)
            
            # Handle user input and update the post index
            new_index = handle_input(current_post_index, sorted_posts, users, email)
            
            # If handle_input returns None, exit 'face' and move to the next function
            if new_index is None:
                break
            else:
                current_post_index = new_index
        else:
            print(Fore.RED + center_text("No posts available"))
            print("")
            handle_input(current_post_index, sorted_posts, users, email)
        
def handle_input(current_post_index, posts, users, email):
    """Handle user input to navigate posts."""
    hashed_email= hash_email(email)
    user_data = users.get(hashed_email)
    max_index = len(posts) - 1  # Max index for posts

    while True:  # Loop until a valid input is entered
        user_input = input(Style.DIM + "\nWhat's on your mind: " + Style.RESET_ALL)

        if user_input == 'm':  # Go to dashboard
            user_dashboard(email)
            return current_post_index  # Exit 'face' function with the current index
        
        elif user_input == 'n':  # Next post
            if current_post_index < max_index:
                return current_post_index + 1  # Go to the next post
            else:
                print(Fore.RED + center_text("\nNo more posts available"))
                time.sleep(0.9)
                return current_post_index  # Stay on the same post

        elif user_input == 'p':  # Previous post
            if current_post_index > 0:
                return current_post_index - 1  # Go to the previous post
            else:
                print(Fore.RED + center_text("\nPrevious posts end here"))
                time.sleep(0.9)
                return current_post_index  # Stay on the same post

        elif user_input == 'l':  # Like/unlike the current post
            if 0 <= current_post_index <= max_index:
                post = posts[current_post_index]
                post = like(users, email, post)  # Call the like function
                display_post(post)  # Re-display the post immediately after like/unlike
                return current_post_index  # Stay on the current post after liking
            else:
                print(Fore.RED + center_text("\nNo post to like"))
                time.sleep(0.9)
                return current_post_index  # Stay on the same post
        
        else:  # Invalid input
            print(Fore.RED + center_text("\nInvalid input"))
            time.sleep(0.9)
            return current_post_index  # Stay on the same post  
            
def get_verified(user_data, email):
    clear_screen()
    while True:
        verify = '✅'
        users = data_store.get('users', {})
        hashed_email = hash_email(email)
        user_data = users.get(hashed_email)

        # Check if user is already verified
        if verify not in user_data['name']:
            print("")
            print(Style.DIM + " ⬅️ b" + Style.RESET_ALL + Fore.BLUE + " Get Verified".rjust(width - 8))
            print("")
            print("")
            print(Style.DIM + center_text("Premium"))
            print("")
            print(Style.DIM + center_text("Yearly / $129"))
            print(center_text(" Enhanced Experience"))
            print("")
            print(Style.DIM + "  Ai Assistant *")
            print(Style.DIM + "  Unlimited Downloads *")
            print(Style.DIM + "  Get paid to post *")
            print(Style.DIM + "  Checkmark *")
            print(Style.DIM + "  Maskbook Pro *")
            print("_" * width)
            print(center_text("\n SUBSCRIBE"))
            get = input(Style.DIM + "\nWhat's on your mind: ")

            # Check for multiple valid inputs for subscribing
            if get.lower() in ['subscribe', 'sub', 'se']:
                user_balance = float(user_data['balance'])
                if user_balance < 129:
                    print(Fore.YELLOW + "You don't have enough balance to subscribe.")
                    time.sleep(0.9)
                    return get_verified(users, email)
                else:
                    print("")
                    centered_loading_animation_az(Fore.BLUE + "Subscribing...", 0.2)
                    print(Fore.RED + "SUBSCRIBED")
                    
                    # Update user data
                    user_data['name'] += " " + verify  # Append the checkmark to the user's name
                    user_data['balance'] = float(user_data.get('balance', 0)) - 129  # Deduct subscription fee
                    save_json(USERS_FILE, users)  # Save updated user data
                    
                    # Update all posts with the new verified name
                    update_user_posts(users, user_data['name'])  # Update posts

                    time.sleep(0.9)
                    return menu(users, email)
            elif get == 'b':
                return menu(users, email)
            else:
                print(Fore.RED + "Invalid input")
                time.sleep(0.9)
                return get_verified(users, email)
        else:
            print("")
            print(" ⬅️ b")
            print("")
            print("")
            print(Fore.RED + "  You are a Verified user" + Style.RESET_ALL + f" {user_data['name']}")
            print("")
            print("")
            gg = input(Style.DIM + " 👍 return to your dashboard " + Style.RESET_ALL)
            if gg == 'b':
                return menu(users, email)

def update_user_posts(user_data, verified_name):
    """Update all posts to reflect the verified user's name."""
    posts = data_store.get('posts', {})# Load posts from the JSON file
    for user, data in users.items():
        user_posts = posts.get(data['username'], [])
        for post in user_posts:
            if post['name'] == verified_name.strip(" " + '✅'):  # Update if the post is from the verified user
                post['name'] = verified_name  # Update to the verified name
    save_json(POSTS_FILE, posts)  # Save the updated posts back to the JSON file
                
def referral(user_data, email):
    clear_screen()
    users = data_store.get('users', {}) # Load user data
    refer = data_store.get('refer', {})  # Load referral data
    hashed_email = hash_email(email) # Hash the input email to access user data
    user_data = users.get(hashed_email) # Retrieve user data based on hashed email

    print("")
    print(" ⬅️ b")
    print("")
    print("")
    print(Fore.BLUE + center_text("Invite Friends"))
    print("")
    print(Style.DIM + " Invite a friend and get $34")
    print("")
    print("")
    print(Fore.BLUE + " Referral Id")
    print(Style.DIM + "_" * width)
    print(Fore.BLUE + "\n Redeem code")
    print(Style.DIM + "_" * width)

    kj = input(Style.DIM + "\n what's on your mind  " + Style.RESET_ALL)

    if not kj:
        print(Fore.RED + "Your input is empty")
        time.sleep(0.9)
        return referral(users, email)

    if kj.lower() == 'b':
        return user_dashboard(email)

    elif kj.lower() == 'rc':  # Redeem code option
        print("")
        code = input(Style.DIM + "\n enter the code to Redeem  " + Style.RESET_ALL).strip()  # Strip whitespace

        # Check if the code is the user's own referral code
        if code == user_data['refer']:
            print(Fore.RED + "You can't redeem your own code")
            time.sleep(0.9)
            return referral(users, email)

        # Check if the user has already redeemed the code
        if 'redeemers' in refer.get(code, {}):
            if user_data['username'] in refer[code]['redeemers']:
                print(Fore.RED + "You have already redeemed this code.")
                time.sleep(0.9)
                return referral(users, email)

        # Find the user who owns the referral code
        code_owner_data = None
        for user_hash, user_info in users.items():
            if user_info['refer'] == code:
                code_owner_data = user_info
                break

        # If the code owner is found
        if code_owner_data:
            print("")
            centered_loading_animation_az(Fore.BLUE + "Redeeming...", 0.1)
            print("")
            print(Fore.GREEN + "Redeemed Successfully")
            time.sleep(0.9)

            # Split the $34 between the code owner and the redeemer
            amount_to_each = 34 / 2

            # Update the balances
            user_data['balance'] = str(float(user_data['balance']) + amount_to_each)  # Redeemer's balance
            code_owner_data['balance'] = str(float(code_owner_data['balance']) + amount_to_each)  # Owner's balance

            # Save the updated user data back into the users.json
            users[hashed_email] = user_data
            users[code_owner_data['username']] = code_owner_data  # Assuming username is unique
            save_json(USERS_FILE, users)

            print(Fore.GREEN + f"${amount_to_each:.2f} added to your balance.")
            print(Fore.GREEN + f"${amount_to_each:.2f} added to the owner's balance.")

            # Update the referral file with the redeemer's details
            if code not in refer:
                refer[code] = {'code_owner': code_owner_data['username'], 'redeemers': []}

            refer[code]['redeemers'].append(user_data['username'])  # Add the redeemer's username

            # Save the updated referral data
            save_json(REFER_FILE, refer)

            return referral(users, email)

        # If the code isn't found
        else:
            print(Fore.RED + center_text("Code not found"))
            time.sleep(0.9)
            return referral(users, email)

    elif kj.lower() == 'ri':  # Display referral code
        print(Fore.YELLOW + "This is your referral code " + Style.RESET_ALL + f"{user_data['refer']}")
        bg = input(Style.DIM + "return to dashboard  " + Style.RESET_ALL)
        if bg == 'b':
            return referral(users, email)
        else:
            print(Fore.RED + "Invalid input")
            time.sleep(0.9)
            return referral(users, email)

    else:
        print(Fore.RED + "Invalid input")
        time.sleep(0.9)
        return referral(users, email)
        
def format_balance(balance):
    """Format the balance to display with 'k' for thousand, 'M' for million, and 'B' for billion."""
    balance = float(balance)
    if balance >= 1_000_000_000:
        return f"${balance / 1_000_000_000:.2f}B"  # Format billions with 2 decimal places
    elif balance >= 1_000_000:
        return f"${balance / 1_000_000:.2f}M"  # Format millions with 2 decimal places
    elif balance >= 1_000:
        return f"${balance / 1_000:.2f}k"  # Format thousands with 2 decimal places
    else:
        return f"${balance:.2f}"  # Display balance as-is with 2 decimal places    
                
def user_dashboard(email):
    while True:
        load_data()
        # Load required JSON files once at the start of the loop
        groups = data_store.get('groups', {})
        fusers = data_store.get('fusers', {})
        gmessages = data_store.get('gmessages', {})
        messages = data_store.get('messages', {})
        shop = data_store.get('shop', {})
        transactions = data_store.get('transactions', {})

        hashed_email = hash_email(email)
        user_data = users.get(hashed_email)
        
        if not user_data:
            print(Fore.RED + "User not found!")
            time.sleep(2)
            return main_menu()  # Handle error gracefully by returning to the main menu
        
        clear_screen()
        formatted_balance = format_balance(user_data['balance'])
        
        # Set the terminal width for consistent formatting
        print("")
        print(Style.DIM+" ⬅️ b"+Style.RESET_ALL+Style.BRIGHT + Fore.BLUE + "  MENU".rjust(width-7))
        print(" ")
        print("")
        print(Style.DIM+center_text("Balance"))
        print("")
        print(Fore.GREEN + center_text(formatted_balance))
        print("")
        print(Style.DIM+ "_" * width)
        
        # User interaction options
        print(Fore.YELLOW + "\n"+"  👥 Invite Friends")
        print(Style.DIM+ "_" * width)
        print(Fore.CYAN + "  \n  🛍️ Shopping   |    🧑‍🔧 Menu")
        print(Style.DIM + "_" * width)
        print(Fore.CYAN + "  \n  📩 Messages   |    👥 Friends")
        print(Style.DIM + "_" * width)
        print(Fore.CYAN + "  \n 🔍 Search     |    📊 WSR-Fund")
        print(Style.DIM + "_" * width)
        print(Fore.CYAN + "  \n 🫂 Groups     |    ⚙️ Settings")
        print(Style.DIM + "_" * width)
        print(Fore.CYAN + "  \n 🛑 Logout ")
        print(Style.DIM + "_" * width)
        
        # Take user input for dashboard options
        choice = input(Style.DIM + "\nPick What's on your mind: " + Style.RESET_ALL)
        
        if choice in ['Sg', 'sg', 'SG', 'sG']:
            shop_glo(users, email)
            time.sleep(2.9)
        elif choice in ['Mu', 'MU', 'mu', 'mU']:
            menu(users, email)  # Pass 'users' and 'email' to the menu function
        elif choice.lower()== 'if':
            referral(users, email)
        elif choice == 'b':
            return face(users, email)
        elif choice in ['Ms', 'MS', 'ms', 'mS']:
            my_friends(user_data, email)  # Ensure my_messages function exists
        elif choice in ['Fs', 'fs', 'FS', 'fS']:
            my_friends(user_data, email)  # Proper handling for friends
        elif choice in ['Sh', 'SH', 'sh', 'sH']:
            search(users, groups, email)  # Ensure search is correctly defined
        elif choice in ['Wd', 'wd', 'WD', 'wD', 'wf', 'WF', 'wF', 'Wf']:
            wsr_fund(users, email)  # Ensure wsr_fund is properly defined
        elif choice in ['Gs', 'GS', 'gs', 'gS']:
            crowds(users, email)  # Ensure the group function exists and works with 'users'
        elif choice in ['Ss', 'ss', 'SS', 'sS']:
            settings(users, email)  # Pass user-specific data to the settings function
        elif choice in ['Lt', 'lt', 'LT', 'lT']:
            print(Fore.RED + "Logging out...")
            time.sleep(2)
            return main_menu()  # Return to the main menu after logging out
        else:
            print(Fore.RED + "Invalid input!")
            time.sleep(3) 
            
def shop_glo(users, email):
    clear_screen()
    users = data_store.get('users', {})
    hashed_email = hash_email(email)
    user_data = users.get(hashed_email)

    # Load all items from shop
    all_items = []
    shop_data = data_store.get('shop', {})  # Load the shop data once

    for user, items in shop_data.items():
        for item_key, item_data in items.items():  # Ensure we access each item correctly
            all_items.append(item_data)

    items = sorted(all_items, key=lambda x: x['timestamp'], reverse=True)  # Sort items by time, most recent first
    current_item_index = 0

    def display_item(item=None):
        if item:
            name = item.get('name', 'Unknown Name')  # Use a default value if 'name' is missing
            username = item.get('username', 'Unknown Seller')  # Use a default value if 'username' is missing
            print(Style.DIM + center_text(f"{name} • {username}"))
            print(Style.DIM + "-" * width)
            print("")
            print(Style.DIM + center_text(f"{item.get('product_name', 'Unknown Product')}"))
            print("")
            print(Style.DIM + Fore.BLUE + item.get('content', 'No description available'))
            print("")
            print(Style.DIM + center_text("$" + str(item.get('amount', '0'))))
            print("")
            formatted_time = format_time_ago(item['timestamp'])
            print(Style.DIM + f"Posted {formatted_time}")
        else:
            print(Fore.RED + center_text("No items available"))
            print(Style.DIM + "-" * width)

    while True:
        clear_screen()

        print("")
        print(Style.DIM + " ⬅️ b" + Style.RESET_ALL + Style.DIM + Fore.BLUE + "My Shop".rjust(width - 7))
        print("")
        print("")
        print(Fore.BLUE + center_text("Market Place"))
        print("")
        print("")
        print(Style.DIM + center_text("🛒 Items"))
        print("")
        print("")

        if items:
            display_item(items[current_item_index])
        else:
            display_item()  # Display "No items available" if the item list is empty

        # Prompt for user input
        user_input = input(Style.DIM + "\nWhat's on your mind: " + Style.RESET_ALL)

        if user_input == 'b':
            return user_dashboard(email)  # Return to menu
        elif user_input.lower() == 'ms':
            my_shop(users, email)  # Just a placeholder for my shop
            time.sleep(1)  # Pause for a moment before prompting the user
        elif user_input == 'n':  # Show the next item
            if current_item_index + 1 < len(items):
                current_item_index += 1
            else:
                print(Fore.RED + "No more items.")
                time.sleep(0.9)
        elif user_input == 'p':  # Show the previous item
            if current_item_index > 0:
                current_item_index -= 1
            else:
                print(Fore.RED + "No previous items.")
                time.sleep(0.9)
        elif user_input.lower() == 'buy':  # Buy the current item
            if items:
                item = items[current_item_index]
                balance = float(user_data.get('balance', 0))
                item_price = float(item.get('amount', 0))

                # Adjust the purchase cost
                cost_to_seller = 2
                cost_to_buyer = item_price + 3  # 3$ deduction for the buyer

                # Check if the user has enough balance
                if balance >= cost_to_buyer:
                    # Deduct the price from the buyer's balance
                    new_balance = balance - cost_to_buyer
                    user_data['balance'] = new_balance

                    # Find the seller and add the amount to their balance
                    seller_username = item['username']
                    seller_data = next((data for data in users.values() if data['username'] == seller_username), None)
                    if seller_data:
                        seller_data['balance'] = float(seller_data.get('balance', 0)) + cost_to_seller

                        # Update the users data
                        users[hashed_email] = user_data  # Update buyer's data
                        # Here you need to fetch seller's email, assuming it's stored with the user
                        seller_hashed_email = next((hash for hash, data in users.items() if data['username'] == seller_username), None)
                        if seller_hashed_email:
                            users[seller_hashed_email] = seller_data  # Update seller's data
                            save_json(USERS_FILE, users)  # Save the updated users data

                            # Save the purchased item to ITEMS_FILE
                            purchased_item = {
                                'buyer': user_data['name'],
                                'name': item['name'],
                                'username': item['username'],
                                'product_name': item['product_name'],
                                'content': item['content'],
                                'amount': item['amount'],
                                'timestamp': item['timestamp'],
                                'id': item['id']
                            }

                            # Load the items file
                            items_data = load_json(ITEMS_FILE)

                            # Ensure items_data is a dictionary
                            if not isinstance(items_data, dict):
                                items_data = {}

                            # Add the purchased item using its ID as the key
                            items_data[purchased_item['id']] = purchased_item

                            # Save the updated items data back to ITEMS_FILE
                            save_json(ITEMS_FILE, items_data)

                            # Remove the purchased item from the list
                            items.pop(current_item_index)

                            # Save the updated items back to the SHOP_FILE
                            shop_data[seller_hashed_email] = {k: v for k, v in shop_data[seller_hashed_email].items() if v != item}
                            save_json(SHOP_FILE, shop_data)

                            # Print purchase successful message
                            print(Fore.GREEN + "Purchase successful! Your new balance is $" + str(new_balance))
                        else:
                            print(Fore.RED + "Seller email not found.")
                    else:
                        print(Fore.RED + "Seller data not found. Please try again.")
                else:
                    print(Fore.RED + "You don't have enough balance to purchase this item.")
                
                time.sleep(0.9)
            else:
                print(Fore.RED + "No items available to buy.")
                time.sleep(0.9)
        else:
            print(Fore.RED + "Invalid input")
            time.sleep(0.9)
            
def my_shop(users, email):
    clear_screen()
    users = data_store.get('users', {})
    hashed_email = hash_email(email)
    user_data = users.get(hashed_email)
    
    # Load the entire shop data instead of just fetching 'username'
    shop_user = data_store.get('shop', {}) # Assuming this returns a dictionary of users

    print("\n ⬅️ b\n\n")
    print(Fore.BLUE + center_text("Maskbook Merchant") + "\n\n")
    
    # Check if the user is not a merchant
    if user_data['username'] not in shop_user:
        print(Fore.RED + center_text("You are not a Merchant yet") + "\n")
        print(Fore.BLUE + Style.DIM + center_text("1. Become Merchant"))
        print(Style.DIM + "_" * width)  # Assuming width is 40
        
        while True:
            uk = input(Style.DIM + "\nWhat on your mind   " + Style.RESET_ALL)

            if uk == 'b':
                return shop_glo(users, email)
            elif uk == '1':
                print("")
                centered_loading_animation_az(Fore.YELLOW + "Creating Merchant Dashboard ....", 0.2)
                
                # Add user as a merchant in shop_user
                shop_user[user_data['username']] = {  # Ensure this is set correctly
                    'name': user_data['name'],
                    'username': user_data['username'],
                    'pin': user_data['pin']
                }
                # Use the variable instead of string
                save_json(USHOP_FILE, shop_user)  # Corrected from 'USHOP_FILE'
                merchant_dashboard(users, email)
                break
            else:
                print(Fore.RED + "Invalid input")
                time.sleep(0.9)
    else:
        merchant_dashboard(users, email)
        
def merchant_dashboard(users, email):
    clear_screen()
    shop_data = data_store.get('shop', {})
    items = shop_data.get(hash_email(email), {})
    
    # Load the files data if 'files' is meant to be loaded from another source
    files = data_store.get('files', {})  # Ensure FILES_DATA_FILE points to the correct file

    print("\n ⬅️ b\n\n")
    print(Fore.BLUE + center_text("Maskbook Merchant") + "\n")

    # Retrieve user data
    user_data = users.get(hash_email(email))  # Fetch user data here
    if not user_data:
        print(Fore.RED + "User data not found!")
        return  # Exit if user data is not found

    print(Style.DIM + center_text(f"{user_data['name']}\n\n"))
    print(Fore.BLUE + "  My Items   |  Create Items")
    print(Style.DIM + "_" * width)
    
        # Prompt for user input
    hj = input(Style.DIM + "\n  What on your mind  " + Style.RESET_ALL)

    if hj == 'b':
        return my_shop(users, email)
    # Handle other options (like creating items) as per your previous logic...
    elif hj.lower() == 'mi':
        clear_screen()
        print("")
        print(" ⬅️ b")
        print("")
        print(Fore.BLUE+center_text("My items"))
    # Display all items for the current user
        if items:
            for item_key, item_data in items.items():
                # Check if the item belongs to the specific user's username
                if item_data['username'] == user_data['username']:
                    print(Style.DIM + f"\nProduct: {item_data['product_name']}")
                    print(Style.DIM + f"Description: {item_data['content']}")
                    print(Style.DIM + f"ID: {item_data['id']}")
                    print(Style.DIM + f"Price: {item_data['amount']}")
                    print(Style.DIM + "-" * width)
        else:
            print(Fore.RED + center_text("No Items") + "\n")
        jm = input(Style.DIM+"\n What on your mind  ")
        if jm == 'b':
            return merchant_dashboard(users, email)    

    elif hj.lower() == 'ci':
        product_name = input(Style.DIM + "\nWhat is your product name  ")
        if not product_name:
            print(Fore.RED + "Name cannot be empty")
            time.sleep(0.9)
            return merchant_dashboard(users, email)

        amount = input(Style.DIM + "\nhow much do you want to sell this product  ")
        if not amount or not amount.isdigit():  # Ensure amount is a number
            print(Fore.RED + "Amount must be a valid number and cannot be empty")
            time.sleep(0.9)
            return merchant_dashboard(users, email)

        content = input(Style.DIM + "\nTell us more about your product  ")
        if not content:
            print(Fore.RED + "Description cannot be empty")
            time.sleep(0.9)
            return merchant_dashboard(users, email)

        product_id = input(Style.DIM + "\n input the file_id of your product ").strip()  # Clean the input
        # Check if product_id exists in files
        if not any(file_info['file_id'] == product_id for user_files in files.values() for file_info in user_files):
            print(Fore.RED + "Please input a correct file_id so others can access your product when purchased")
            time.sleep(0.9)
            return merchant_dashboard(users, email)

        print("")
        centered_loading_animation_az(Fore.MAGENTA + "Listing your product", 0.2)
        print(Fore.BLUE + center_text("Listed Successfully"))

        # Save the new item data using the user_data correctly
        new_items[user_data['name']] = {
            'product_name': product_name,
            'amount': amount,
            'content': content,
            'id': product_id,
            'username': user_data['username'],
            'name': user_data['name'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if hashed_email in shop_data:
             user_items = shop_data[hashed_email]
        else:
            user_items = {}
        user_items[new_item['id']]= new_item    
        shop_data[hash_email(email)] = user_items  # Ensure the new item is added to the correct user
        save_json(SHOP_FILE, new_items)  # Corrected to save back to the correct shop_data

        return merchant_dashboard(users, email)  # Return to dashboard

    else:
        print(Fore.RED + "Invalid input")
        time.sleep(0.9)
        return merchant_dashboard(users, email)  # Return to dashboard if invalid input
    
def settings(users, email):
    hashed_email = hash_email(email)
    user_data = users.get(hashed_email)
    
    if not user_data:
        print(Fore.RED + "User not found.")
        return
    
    clear_screen()
    print("")
    print(Style.DIM + " ⬅️ b")
    print("")
    print("")
    print(Style.DIM+ center_text("Account Settings"))
    print("")
    print(Style.DIM+Fore.GREEN +center_text( f"{user_data['name']}"))
    print("")
    print(Style.DIM+ "_" * width)
    print(Style.DIM+Fore.CYAN + "\n  👤 Change Name  |   🔐 Change Pass")
    print(Style.DIM + "_" * width)
    print(Style.DIM+Fore.CYAN + "\n  Change Email   |    Help")
    print(Style.DIM + "_" * width)
    print(Style.DIM+Fore.CYAN + "\n  Add country   |  Add Sex")
    print(Style.DIM + "_" * width)
    print(Style.DIM+Fore.CYAN + "\n  Add bio   |    Add Age")
    print(Style.DIM + "_" * width)
    st = input(Style.DIM + "\n  input an Option: "+Style.RESET_ALL)

    if st == 'b':
        return user_dashboard(email)  # user_data should be passed

    elif st.lower() == 'cn':
        change_name(users, email)
    
    elif st.lower() == 'cp':
        change_password(users, email)
    
    elif st.lower() == 'ce':
        change_email(users, email)
    
    elif st.lower() == 'hp':
        show_help(users, email)
    
    elif st.lower() == 'cy':
        country = input(Fore.BLUE + "\nWhat is your country: " + Style.RESET_ALL)
        pin = input(Fore.BLUE + "What is your pin: ")

        if not verify_password_pin(pin, user_data['pin'].encode('utf-8')):
            print(Fore.RED + "Incorrect pin.")
            time.sleep(1)
            return settings(users, email)
        else:
            user_data['country'] = country
            save_json(USERS_FILE, users)
            print(Fore.GREEN + f"Country updated to {country}")
            time.sleep(0.9)
            return settings(users, email)

    elif st.lower() == 'sx' :
        sex = input(Fore.BLUE + "\nWhat is your marital status:  " + Style.RESET_ALL)
        pin = input(Fore.BLUE + "Your pin:  " + Style.RESET_ALL)

        if not verify_password_pin(pin, user_data['pin'].encode('utf-8')):
            print(Fore.RED + "\n🚨 This does not match your pin.")
            time.sleep(0.9)
            return settings(users, email)
        else:
            user_data['sex'] = sex
            save_json(USERS_FILE, users)
            print(Fore.GREEN + f"\nYour marital status is updated to {sex}")
            time.sleep(0.8)
            return settings(users, email)

    elif st.lower() == 'bo':
        bio = input(Fore.BLUE + "\nWhat is your bio write-up: " + Style.RESET_ALL)
        pin = input(Fore.BLUE + "Your pin: " + Style.RESET_ALL)

        if not verify_password_pin(pin, user_data['pin'].encode('utf-8')):
            print(Fore.RED + "\n🚨 This does not match your existing pin.")
            time.sleep(0.9)
            return settings(users, email)
        else:
            user_data['bio'] = bio
            save_json(USERS_FILE, users)
            print(Fore.GREEN + f"\nYour bio is updated.")
            time.sleep(0.8)
            return settings(users, email)

    elif st.lower() == 'ae':
        age(users, email)

    else:
        print(Fore.RED + "Invalid input")
        return settings(users, email)


def change_name(users, email):
    hashed_email = hash_email(email)
    user_data = users.get(hashed_email)
    
    new_name = input(Fore.BLUE + "\nWhat is your new name: " + Style.RESET_ALL)
    current_password = input(Fore.BLUE + "What is your current password: ")
    
    if not verify_password_pin(current_password, user_data['password'].encode('utf-8')):
        print(Fore.RED + "Incorrect password")
        time.sleep(0.9)
        return settings(users, email)
    else:
        user_data['name'] = new_name
        save_json(USERS_FILE, users)
        print(Fore.GREEN + f"\nYour name is updated to {new_name}")
        time.sleep(0.8)
        return settings(users, email)


def age(users, email):
    hashed_email = hash_email(email)
    user_data = users.get(hashed_email)

    age = input(Fore.BLUE + "\nWhat is your age: " + Style.RESET_ALL)
    pin = input(Fore.BLUE + "\nYour pin: " + Style.RESET_ALL)

    if not verify_password_pin(pin, user_data['pin'].encode('utf-8')):
        print(Fore.RED + "\n🚨 This does not match your pin.")
        time.sleep(0.9)
        return settings(users, email)
    else:
        user_data['age'] = age
        save_json(USERS_FILE, users)
        print(Fore.GREEN + f"\nYour age is updated to {age}.")
        time.sleep(0.8)
        return settings(users, email)
        
def change_password(users, email):
    hashed_email = hash_email(email)
    user_data = users.get(hashed_email)

    if not user_data:
        print(Fore.RED + "User not found.")
        return settings(users, email)

    pin = input(Fore.BLUE + "\nWhat is your pin 🙈: " + Style.RESET_ALL)

    # Verify the pin with the stored hashed pin
    if not verify_password_pin(pin, user_data['pin'].encode('utf-8')):
        print(Fore.RED + "Incorrect pin")
        time.sleep(0.9)
        return settings(users, email)
    else:
        new_password = input(Fore.BLUE + "\nYour new password: " + Style.RESET_ALL)

        # Hash the new password
        hashed_new_password = hash_password_pin(new_password)

        # Check if new password is the same as the old password
        if verify_password_pin(new_password, user_data['password'].encode('utf-8')):
            print(Fore.RED + "Your new password is the same as the old password")
            time.sleep(1)
            return settings(users, email)
        else:
            # Update only the password field for this user
            user_data['password'] = hashed_new_password.decode('utf-8')

            # Save only the updated users dictionary, which includes the changed password for this user
            save_json(USERS_FILE, users)
            print(Fore.GREEN + "\nYour password has been updated.")
            time.sleep(1.9)
            return settings(users, email)
            
def change_email(users, email):
    hashed_email = hash_email(email)
    user_data = users.get(hashed_email)

    if not user_data:
        print(Fore.RED + "User not found.")
        return settings(users, email)

    new_email = input(Fore.BLUE + "\nWhat is your new email: " + Style.RESET_ALL)
    hashed_new_email = hash_email(new_email)

    if hashed_new_email in users:
        print(Fore.RED + "\nThis email already exists with an account.")
        time.sleep(0.9)
        return settings(users, email)

    # Check the current password for verification
    current_password = input(Fore.BLUE + "What is your current password: " + Style.RESET_ALL)
    
    if not verify_password_pin(current_password, user_data['password'].encode('utf-8')):
        print(Fore.RED + "Incorrect password.")
        time.sleep(0.9)
        return settings(users, email)
    else:
        # Remove the old hashed email and assign it to the new one
        users[hashed_new_email] = users.pop(hashed_email)
        
        # Save the changes
        save_json(USERS_FILE, users)

        print(Fore.GREEN + f"\nYour email has been updated to {new_email}.")
        time.sleep(0.8)

        return settings(users, new_email)  # Continue with the new email in session
        
def attention():
    clear_screen()
    print("")
    print(Fore.RED+center_text("🚨 ATTENTION 🚨"))
    print(Style.DIM+center_text("How to use"))
    print("")
    print(Fore.RED+"To call a function with 1 name:"+Style.RESET_ALL+"Use the first and last letters of a function name"+Style.RESET_ALL+Fore.RED+"Example. "+Style.RESET_ALL+"Groups, you call it this way gs Implement it this way to other function with 1 name")
    print("")
    print(Fore.RED+"To call a function with 2 name:"+Style.RESET_ALL+"Use the first and first letters of the function name"+Style.RESET_ALL+Fore.RED+"Example. "+Style.RESET_ALL+"My Profile, you call it this way mp Implement it this way to other function with 2 names")
    print("")
    bm = input(Style.DIM+"\n Input c to continue:  "+Style.RESET_ALL)
    if bm.lower() == 'c':
        start()
    else:
        print(Fore.RED+"Invalid Input")
        time.sleep(0.9)
        return attention()
    
    
            
def menu(users, email):
    clear_screen()
    print("")
    print(Style.DIM + "⬅️ b" + Style.RESET_ALL + Fore.BLUE + "MENU".rjust(width - 7))
    print("")
    print("")
    print(Style.DIM + "_" * width)
    print(Fore.GREEN + "\n  📠 Pay   |    🏧 Deposit")
    print(Style.DIM + "_" * width)
    print(Fore.GREEN + "\n  My Profile   |   Transactions")
    print(Style.DIM + "_" * width)
    print(Fore.BLUE + "\n  Get Verified")
    print(Style.DIM + "_" * width)
    choice = input(Style.DIM + "\nSelect an option: " + Style.RESET_ALL).strip()

    if choice.lower() == 'py':
        pay_user(users, email)
    elif choice.lower() == 'dt':
        deposit(users, email)
    elif choice.lower() == 'mp':
        my_profile(users, email)
    elif choice.lower() == 'gv':
        get_verified(users, email)
    elif choice.lower() == 'ts':
        print(Fore.RED+"\nWorking on Maskbook transactions chain")
        time.sleep(0.9)
        return menu(users, email)
    elif choice == 'b':
        return user_dashboard(email)  # Return to the user dashboard
    else:
        print(Fore.RED + "Invalid option. Please try again.")
        time.sleep(1.5)
        return menu(users, email)


def pay_user(users, email):
    clear_screen()

    print("")
    print(Style.DIM+" ⬅️ b")
    print("")
    print("")
    print(Fore.BLUE + center_text("Pay a User"))
    print("")
    print("")

    hashed_email = hash_email(email)  # Use hashed email for lookup
    user_data = users.get(hashed_email)
    
    if not user_data:
        print(Fore.RED + "User not found.")
        return menu(users, email)
    
    recipient_email = input(Style.DIM + "\n  Enter the recipient's email: " + Style.RESET_ALL)
    hashed_recipient_email = hash_email(recipient_email)  # Hash recipient email for lookup
    if recipient_email == 'b':
        return menu(users, email)
    
    # Check if recipient exists
    if hashed_recipient_email not in users:
        print(Fore.RED + "Recipient email is not registered.")
        time.sleep(1)
        return pay_user(users, email)
    
    # Prevent paying yourself
    if hashed_recipient_email == hashed_email:
        print(Fore.RED + "You cannot pay yourself.")
        time.sleep(0.9)
        return pay_user(users, email)

    # PIN Validation
    pin = masked_input(Fore.BLUE + "\nWhat is your pin: ")
    if not verify_password_pin(pin, users[hashed_email]['pin'].encode('utf-8')):
        print(Fore.RED + "\nIncorrect pin.")
        time.sleep(1)
        return pay_user(users, email)

    clear_screen()

    # Display recipient's information
    print( "" )
    print(Style.DIM+" ⬅️ b")
    print("")
    print("")
    print(Fore.BLUE + center_text("Recipient"))
    print( "")
    print("")
    print("\n" + center_text(f"{users[hashed_recipient_email]['user_emoji']}"))
    print(Fore.BLUE + "\n" + center_text(f"{users[hashed_recipient_email]['name']}"))
    print("")
    print(Style.DIM+ "_" * width)

    try:
        user_input = input(Fore.MAGENTA + "\nHow much do you want to pay this user: " + Style.RESET_ALL)
    
        if user_input == 'b':
            return pay_user(users, email)

    # Convert input to a float if it's not 'b'
        amount = float(user_input)
    
        if amount == 0:
            print(Fore.RED + "Invalid amount")
            time.sleep(0.9)
            return pay_user(users, email)

    except ValueError:
        print(Fore.RED + "\nInvalid input. Please enter a valid number.")
        time.sleep(0.9)
        return pay_user(users, email)

    # Validate if the sender has enough balance
    sender_balance = float(user_data['balance'])
    recipient_balance = float(users[hashed_recipient_email]['balance'])

    if amount > sender_balance:
        print(Fore.YELLOW + "\nYou don't have enough balance to pay this user.")
        time.sleep(1.5)
        return pay_user(users, email)
    else:
        # Deduct from sender and add to recipient
        new_sender_balance = sender_balance - amount
        users[hashed_email]['balance'] = f"{new_sender_balance:.2f}"

        new_recipient_balance = recipient_balance + amount
        users[hashed_recipient_email]['balance'] = f"{new_recipient_balance:.2f}"

        # Save updated balances
        save_json(USERS_FILE, users)
        
        print(Fore.GREEN + f"\nSuccessfully paid {amount:.2f} to {users[hashed_recipient_email]['name']}.")
        print(Fore.GREEN + f"\nYour new balance is {users[hashed_email]['balance']}.")

        # Log the transaction
        status = 'Successful ✅'
        transaction_id = f'anx-62026gsj5289bst28ojs6wn7jw{str(uuid.uuid4())[:5]}'
        
        try:
            transaction = load_json(TRANSACTIONS_FILE)
        except FileNotFoundError:
            transaction = {}

        transaction[transaction_id] = {
            'sender_email': hashed_email,
            'recipient_email': hashed_recipient_email,
            'amount': amount,
            'status': status,
            'transaction_id': transaction_id
        }
        
        # Save the transaction
        save_json(TRANSACTIONS_FILE, transaction)
    
    input(Fore.CYAN + "\nPress Enter to return to the menu..." + Style.RESET_ALL)
    return menu(users, email)


def deposit(users, email):
    clear_screen()
    print("")
    print(Style.DIM+"⬅️ b")
    print("")
    print("")
    print(Style.DIM + center_text("Deposit to your account"))
    print("")
    print("")
    print(Style.DIM+"_"*width)
    print(Fore.MAGENTA + "\n  BTC   |   ETH")
    print(Style.DIM + "_" * width)

    vb = input(Fore.BLUE + "\nPick an option: " + Style.RESET_ALL)
    if vb.lower() == 'btc':
        btc_deposit(users, email)  # Implement BTC deposit functionality
    elif vb == 'b':
        return menu(users, email)
    elif vb.lower == 'eth':
        print(Fore.RED+"Coming soon...")
        time.sleep(0.9)
        return deposit(users, email)
    else:
        print(Fore.RED + "Invalid input.")
        time.sleep(0.9)
        return deposit(users, email)       
        
def my_profile(users, email):
    hashed_email = hash_email(email)  # Hash the email before accessing the user data
    while True:
        users = data_store.get('users', {})
        user_data = users.get(hashed_email)

        if user_data is None:
            print(Fore.RED + "User not found.")
            time.sleep(1.5)
            return menu(users, email)

        clear_screen()
        print("")
        print(Style.DIM+" ⬅️ b"+Style.RESET_ALL+Style.DIM+" 📸 p".rjust(width-8))
        print("")
        print(Fore.BLUE + center_text("My Profile"))
        print("")
        print("\n" + center_text(f"{user_data['user_emoji']}"))
        print(Fore.BLUE + "\n" + center_text(f"{user_data['name']}"))

        if user_data['bio']:
            print(Fore.YELLOW + "\n" + center_text(f"{user_data['bio']}"))
        else:
            print(Fore.RED+"\n"+center_text("Add bio"))

        if user_data['country']:
            print(Fore.BLUE + "\n" + center_text(f"{user_data['country']}"))
        else:
            print(Fore.RED+"\n"+center_text("Add country"))
            
        if user_data['sex']:
            print(Fore.YELLOW + "\n" + center_text(f"{user_data['sex']}"))
        else:
            print(Fore.RED+"\n"+center_text("Add marital status"))
            
        if user_data.get('age'):
            print(Fore.MAGENTA+"\n"+center_text(f"{user_data['age']} Years old"))
        else:
            print(Fore.RED+"\n"+center_text("Add Age"))

        posts = data_store.get('posts', {})
        user_posts = posts.get(user_data['username'], [])  # Get list of posts for the user (empty if none)

        print(Fore.CYAN + "_" * width)
        print("")
        print(Style.DIM + center_text("📸 Posts"))
        print("")

        if user_posts:
            # Sort posts by timestamp (newest first)
            user_posts_sorted = sorted(user_posts, key=lambda p: p['timestamp'], reverse=True)
            
            for post in user_posts_sorted:
                time_diff = format_time_difference(post['timestamp'])
                like_count = post['count']
                formatted_like_count = format_like_count(like_count)  #
                print(Style.DIM + center_text(f"{user_data['name']} • {user_data['username']}"))
                print(Style.DIM + "-" * width)
                print("")
                print(Fore.BLUE + f"{post['content']}")
                print("")
                print(Fore.RED + Style.DIM + f"({time_diff})" + Style.RESET_ALL + f" ♥️ {formatted_like_count}".rjust(width-8))
                print(Style.DIM + "-" * width)
                print("")
        else:
            print(center_text(Fore.RED+" No Posts"))

        choice = input(Style.DIM + "\n  What on your mind: " + Style.RESET_ALL)
        if choice == 'b':
            return menu(users, email)  # Go back to the menu
        elif choice == 'p':
            clear_screen()
            post = input(Style.DIM+"What do you want to post?  "+Style.RESET_ALL)
            if not post:
                print("Post cannot be empty.")
                time.sleep(0.7)
                continue  # Stay in the profile loop
            ids = str(uuid.uuid4())
            new_post = {
                'id': ids,
                'name': user_data['name'],
                'username': user_data['username'],
                'content': post,
                'count': 0,  # Initial like count
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'likes': []
            }
            
            # Add the new post to the existing list of posts for this user
            user_posts.append(new_post)
            posts[user_data['username']] = user_posts  # Save the updated post list for the user
            save_json(POSTS_FILE, posts)  # Save updated posts to the file
            
            print(Fore.GREEN + "Post added successfully!")
            time.sleep(1.5)
            continue  # Refresh profile and show the new post immediately
        else:
            print(Fore.RED + "Invalid input")
            time.sleep(0.9)
            
def btc_deposit(users, email):
    hashed_email = hash_email(email)  # Hash the email before accessing the user data
    clear_screen()
    print("")
    print(" ⬅️ b")
    print("")
    print("\n")
    print(Back.YELLOW + Style.BRIGHT + Fore.BLUE + center_text("BTC Deposit"))
    print("")
    print("\n")
    print(Style.DIM + "\n" + center_text("bc1qjhwua5ln0nmfj2htf27vvlpreyehxr3jt693nc"))
    print(Fore.CYAN + "_" * width)
    print(Fore.BLUE + "\nMake a Deposit of the amount you need to the BTC address ")

    txn_id = input(Fore.GREEN + "\nInput your payment transaction id or (0) back: " + Style.RESET_ALL)
    if txn_id == 'b':
        return deposit(users, email)

    # Ensure the user's email exists in the data
    user_data = users.get(hashed_email)
    if user_data is None:
        print(Fore.RED + "several network issue with btc reload and try again later")
        return deposit(users, email)

    status = 'Pending ⏳'
    deposit_id = str(uuid.uuid4())

    print(Fore.CYAN + "_" * width)
    print(Fore.YELLOW + "\n" + center_text(f"   {user_data['name']}"))
    print(Fore.BLUE + f"\n   Deposit: " + Style.RESET_ALL + Fore.RED + f"{status}")
    print(Fore.YELLOW + "   Deposit id: " + Style.RESET_ALL + f"{deposit_id}")

    try:
        transaction = data_store['transactions']  # Load existing transactions
    except FileNotFoundError:
        transaction = {}  # If file not found, initialize an empty dictionary

    transaction[hashed_email] = {
        'txn_id': txn_id,
        'deposit_id': deposit_id,  # Store hashed email in the transaction file
        'status': status
    }
    save_json(TRANSACTIONS_FILE, transaction)
    
    gh = input(Fore.RED + "Input b to return: ")
    if gh == 'b':
        centered_loading_animation_az(Fore.BLUE+"\n Returning...")  # Assuming this is a loading function
        return deposit(users, email)
    else:
        print(Fore.RED + "Invalid input")
        return btc_deposit(users, email)  # Prompt again for input         

# Load necessary data only once at the start of the application
groups = data_store.get('groups', {})
users = data_store.get('users', {})
fusers = data_store.get('fusers', {})

def search(users, groups, email):
    hashed_email = hash_email(email)
    user_data = users.get(hashed_email)  # Get user data using hashed email

    while True:
        groups = data_store.get('groups', {})
        users = data_store.get('users', {})
        fusers = data_store.get('fusers', {})
        clear_screen()  # Clear the screen
        print("")
        print(Style.DIM + " ⬅️ b" +Style.RESET_ALL+Style.DIM+"🔍 SEARCH".rjust(width-9))
        print("")
        print("")
        print(Fore.BLUE + center_text("Discover more"))
        print("")
        print("")
        print("\n")
        print(Fore.BLUE + "  🫂 Groups   |    👥 Friends")
        print(Style.DIM+"_"*width)
        print(Fore.BLUE+"\n  ️📥 Download Files ")
        print(Style.DIM+"_"*width)
        print("")
        cb = input(Style.DIM + "\nWhat do you want to discover? " + Style.RESET_ALL)

        if cb == 'b':
            return user_dashboard(email)  # Return to user dashboard with email
        elif cb.lower() == 'gs':
            find_groups(user_data, groups, email)  # Pass user_data and email
        elif cb.lower() == 'fs':
            find_friends(users, friends, email)  # Pass email for finding friends
        elif cb.lower() == 'df':
            my_instance.download_file(users, email)
        else:
            print(Fore.RED + "Invalid Input")
            time.sleep(1)  # Delay for better user experience
            return search(users, groups, email)
            
def find_groups(user_data, groups, email):  # Accept email as parameter
    while True:
        clear_screen()
        print( "")
        print(Style.DIM+" ⬅️ b")
        print("")
        print(Fore.BLUE + center_text("Discover Groups"))
        print("")
        print("")
    
        fg = input(Style.DIM + "\nEnter the name of the group to discover: " + Style.RESET_ALL).strip()
    
        if fg == 'b':
            return search(users, groups, email)  # Go back to search with email

        group_found = False
    
        # Loop through groups to find a match
        for group_name in groups.keys():
            if fg.lower() == group_name.lower():  # Case-insensitive match
                group_found = True
                print(Fore.CYAN + f"Group found: {group_name}")
            
                # Prompt the user to join the group
                jg = input(Fore.BLUE + "\nDo you want to join this group? (Y/N): ").strip().lower()
                if jg == 'y':
                    save_group(user_data, group_name, groups, email)  # Pass email to save_group
                    return  # Exit after joining
                elif jg == 'n':
                    print(Fore.RED + "Canceling...")
                    time.sleep(0.9)
                    return find_groups(user_data, groups, email)  # Allow the user to search again
                else:
                    print(Fore.RED + "Invalid input.")
                    time.sleep(0.9)
                    return find_groups(user_data, groups, email)  # Re-prompt after invalid input
    
        # If no group was found
        if not group_found:
            print(Fore.RED + f"No group found with the name '{fg}'.")
            time.sleep(1.5)
            return find_groups(user_data, groups, email)  # Return to search again

def save_group(user_data, group_name, groups, email):  # Pass email to save_group
    # Check if the user is already a member of the group
    if user_data['username'] in groups[group_name]['members']:
        print(Fore.RED + "You are already a member of this group.")
        time.sleep(0.7)
        return find_groups(user_data, groups, email)  # Return to find_groups with email

    # Add the user to the group members list
    groups[group_name]['members'].append(user_data['username'])
    
    # Save the updated groups to the file
    save_json(GROUPS_FILE, groups)

    print(Fore.GREEN + "Joined the group successfully.")
    time.sleep(0.7)
    return find_groups(user_data, groups, email)  # Return to find_groups with email
    
# Load necessary data once at the start
users = data_store.get('users', {})
friends = data_store.get('fusers', {})

def find_friends(users, friends, email):
    users = data_store.get('users', {})
    hashed_email = hash_email(email)  # Hash the email
    user_data = users.get(hashed_email)  # Get the current user data

    while True:
        users = data_store.get('users', {})
        friends = data_store.get('fusers', {})
        clear_screen()  # Clear the screen
        print("")
        print(" ⬅️ b")
        print("")
        print(Fore.BLUE + center_text("Find a Friend"))
        print("")
        print("")

        username_input = input(Style.DIM + f"\nWhat is your friend's username: {Style.RESET_ALL}").strip()

        if username_input.lower() == 'b':
            return search(users, friends, email)  # Return to the search function

        # Search for the friend in the users data
        friend = next((data for _, data in users.items() if data['username'] == username_input), None)

        if friend:
            if friend['username'] == user_data['username']:
                print(Fore.CYAN + "You are trying to search for yourself 🫤")
                time.sleep(1)
                continue
            else:
                # If a friend is found, display their details
                clear_screen()
                print(Fore.CYAN + "")
                print(" ⬅️ b")
                print("")
                print("")
                print(f"\n{center_text(friend['user_emoji'])}")
                print(Fore.BLUE + center_text(f"{friend['name']}"))
                print(Fore.YELLOW + f"\n{center_text(friend['bio'] if friend['bio'] else 'No bio')}")
                print(Fore.BLUE + f"\n{center_text(friend['country'] if friend['country'] else 'No country')}")
                print(Fore.YELLOW + f"\n{center_text(friend['sex'] if friend['sex'] else 'No marital status')}")
                print(Style.DIM + "_" * width)
                
                # Load posts from the file and filter posts for the friend
                posts = data_store['posts']
                print("")
                print(Style.DIM + center_text("📸 Posts"))
                print("")

                # Filter posts for the friend
                user_posts = [
                    post for username, user_posts_list in posts.items()
                    if username == friend['username']
                    for post in user_posts_list
                ]
                
                if user_posts:
                    # Sort posts by timestamp in descending order
                    user_posts_sorted = sorted(user_posts, key=lambda p: p['timestamp'], reverse=True)
                    for post in user_posts_sorted:
                        time_diff = format_time_difference(post['timestamp'])
                        print(Style.DIM + center_text(f"{friend['name']} • {friend['username']}"))
                        print(Style.DIM + "-" * width)
                        print("")
                        print(Fore.BLUE + f"{post['content']}")
                        print("")
                        print(Fore.RED + Style.DIM + f"({time_diff})" + Style.RESET_ALL + f" ♥️ {post['count']}".rjust(width - 8))
                        print(Style.DIM + "-" * width)
                        print("")
                else:
                    print(center_text("No Posts"))
                    print("")
                    print(Style.DIM + "_" * width)
                
                # Prompt to add the friend
                cm = input(Style.DIM+f"\nAdd friend (y/n): {Style.RESET_ALL}").strip().lower()

                if cm == 'y':
                    save_friend(user_data, friend, email)  # Save the friend relationship
                    print(Fore.GREEN + "Friend added successfully!")
                    time.sleep(0.9)
                    return search(users, friends, email)  # Return to search after adding the friend
                elif cm == 'n':
                    print("Cancelling...")
                    time.sleep(0.9)
                    continue
                elif cm == 'b':
                    return find_friends(users, friends, email)
                else:
                    print(Fore.RED + "Invalid input")
                    time.sleep(0.9)
                    continue

        # If the friend is not found
        print(Fore.YELLOW + "\nNo user found 🚫")
        time.sleep(0.9)
        
def save_friend(user_data, friend, email):
    # Check if the user is already friends with the specified friend
    if user_data['username'] in friends and friend['username'] in friends[user_data['username']]:
        print("\nYou are both already friends.")
        time.sleep(1.4)
        return search(users, groups, email)  # Return to search after displaying the message

    # Add user to the friends list if not already present
    if user_data['username'] not in friends:
        friends[user_data ['username']] = []

    # Add the friend's username to the user's friends list
    friends[user_data['username']].append(friend['username'])

    # Ensure mutual friendship: Add the user to the friend's list
    if friend['username'] not in friends:
        friends[friend['username']] = []
    
    if user_data['username'] not in friends[friend['username']]:
        friends[friend['username']].append(user_data['username'])

    # Save the updated friends list back to the file
    save_json(FUSERS_FILE, friends)
    print(Fore.GREEN + "\nFriend request sent!")
    time.sleep(1.6)

    return find_friends(users, friends, email)  # Return to search or any appropriate function
class MyClass:
    def __init__(self):
        self.Maskbook_folder = "/storage/emulated/0/Maskbook"  # Initialize folder path

    def download_file(self, users, email):
        hashed_email = hash_email(email)
        clear_screen()
        self.check_or_create_maskbook_folder()  # Ensure the folder exists
        files = data_store.get('files', {})# Load the files dictionary

        print("")
        print(" ⬅️ b")
        print("")
        print(Style.DIM + center_text("Downloads"))
        print("")
        print("")

        file_id = input(Style.DIM + "What is the file ID you want to download? " + Style.RESET_ALL).strip()
        if file_id == 'b':
            return search(users, groups, email)

        # Search for the file across all users
        file_to_download = None
        for user_files in files.values():  # Iterate through all user files
            for file_info in user_files:
                if file_info['file_id'] == file_id:  # Check if file_id matches
                    file_to_download = file_info
                    break  # Exit the inner loop if found
            if file_to_download:
                break  # Exit the outer loop if found

        if file_to_download is None:
            print("Invalid file ID. No such file found.")
            time.sleep(0.9)
            return  # Exit the function if not found

        file_path = file_to_download['file_path']  # Get the file path

        if os.path.isfile(file_path):
            print(f"Downloading file: {file_path}...")
            original_filename = os.path.basename(file_path)
            destination_path = os.path.join(self.Maskbook_folder, f"Maskbook_{original_filename}")

            try:
                shutil.copy(file_path, destination_path)
                print(f"File downloaded successfully to {destination_path}!")
                gj = input(Style.DIM + "File downloaded, return home? (press 'b') " + Style.RESET_ALL)
                if gj == 'b':
                    return search(users, groups, email)  # Ensure email is passed here
            except (FileNotFoundError, PermissionError) as e:
                print(f"Error during download: {e}")
        else:
            print(f"File not found at {file_path}.")
            time.sleep(0.9)
            return my_instance.download_file(users, email)

    def check_or_create_maskbook_folder(self):
        if not os.path.exists(self.Maskbook_folder):
            os.makedirs(self.Maskbook_folder)
            message = f"{Fore.BLUE}'Maskbook' folder created at: {self.Maskbook_folder}"
        
            print(message)  # Display the message
            time.sleep(0.8)  # Wait for 0.8 seconds
        
            # Clear the message from the console
            print("\r" + " " * len(message) + "\r", end='')  # Clear the line

# Create an instance of MyClass
my_instance = MyClass()

# Example usage:
# my_instance.download_file(users, email)  # Ensure to call this with the correct parameters    
            
def display_existing_messages(user_messages):
    """Display existing saved messages and files if any."""
    if not user_messages:
        print(Fore.CYAN + "You have no saved messages or files.")
    else:
        print(Fore.CYAN + "\nYour saved messages and files:")
        for idx, entry in enumerate(user_messages, 1):
            if isinstance(entry, str):
                # Display messages
                print(Fore.GREEN + f"{idx}. Message: {entry}")
            elif isinstance(entry, dict) and 'file_path' in entry and 'file_id' in entry:
                # Display file information
                print(Fore.GREEN + f"{idx}. File: {entry['file_path']} (ID: {entry['file_id']})")
            else:
                print(Fore.RED + f"{idx}. Unknown entry type.")
    print("")

def save_message_chat(user_data, email):
    """Save user's messages and files, display them immediately, and persist them to a file."""
    hashed_email = hash_email(email)
    print("")
    print(Style.DIM + " ⬅️ b")
    print("")
    print(Fore.BLUE + center_text("SAVE MESSAGES"))
    print("")
    print("")

    # Load saved messages and files
    saved_data = data_store.get('saved_messages', {})
    saved_files = data_store.get('files', {})

    # Get the user's saved messages and files
    username = user_data['username']
    user_messages = saved_data.get(username, [])
    user_files = saved_files.get(username, [])

    # Combine messages and files for display
    combined_entries = user_messages + user_files  # Assuming user_files is a list of dicts

    # Display existing messages and files
    display_existing_messages(combined_entries)

    while True:
        # Prompt user to enter a message or a file path to save
        message = input("Enter a message or a file path to save (or 'b' to return): ").strip()
        if message == 'b':  # User can type 'b' to return
            return my_friends(user_data, email)
        
        # Check if input is a file path and handle file saving
        if os.path.isfile(message):
            file_path = message
            file_id = str(uuid.uuid4())  # Generate a unique ID for the file

            # Save file information
            files = data_store.get('files', {})
            file_entry = {
                'file_path': file_path,
                'file_id': file_id,
                'username': username
            }
            user_files.append(file_entry)  # Append file entry to user's files
            files[username] = user_files  # Update files for the user
            save_json(FILES_FILE, files)
            print(f"{Fore.GREEN}File saved: {file_path} (ID: {file_id})")
        else:
            # Save the message to the user's message list
            user_messages.append(message)
            # Save the updated messages to file
            saved_data[username] = user_messages
            save_json(SAVED_MESSAGES_FILE, saved_data)

            # Display the saved message immediately
            clear_screen()
            return save_message_chat(user_data)
            
def my_friends(user_data, email):
    while True:
        clear_screen()
        friends_list = data_store.get('fusers', {}).get(user_data['username'], [])  # Load the friends list for the user

        print("")
        print(Style.DIM+" ⬅️ b")
        print("")
        print(Style.DIM + Fore.BLUE +center_text("FRIENDS"))
        print("")
        print("")
        print("\n")
        print(Fore.CYAN + "s. 💾 Save Message")
        print(Style.DIM + "_" * width)
        print("")
        if not friends_list:  # If the user has no friends
            print(Style.DIM+Fore.RED + center_text("\nYou have no friends."))
        for idx, friend in enumerate(friends_list, 1):
            print(Fore.GREEN + f"\n{idx}. {friend}")

        print(Style.DIM + "_" * width)

        # Prompt user to select a friend or save a message
        cf = input(Style.DIM+"\nOpen a chat or press 'b' to return: ")

        if cf == 'b':
            return user_dashboard(email)
            # Ensure the function stops after navigating to the dashboard

        elif cf.lower() == 's':  # Option to save a message
            clear_screen()
            save_message_chat(user_data)

        # Validate the user input and open the chat
        elif cf.isdigit() and 1 <= int(cf) <= len(friends_list):
            selected_index = int(cf)
            selected_friend = friends_list[selected_index - 1]
            print(Style.DIM+center_text(f"\nOpening chat with {selected_friend}..."))
            time.sleep(1.5)
            return chat(users, user_data, selected_friend, email)  # Call the chat function with the selected friend
        else:
            print("\nInvalid input. Returning to the friends list...")
            time.sleep(1.5)
            return my_friends(user_data, email)
            # Stay in the current function without returning
                
def format_message_box(message, width=30, align='left'):
    """Format a message into a box with specified width and alignment."""
    lines = textwrap.wrap(message, width=width)
    if align == 'right':
        lines = [line.rjust(width) for line in lines]
    elif align == 'left':
        lines = [line.ljust(width) for line in lines]

    box = '\n'.join(f"║ {line} ║" for line in lines)
    top_bottom_border = '╔' + '═' * (width + 2) + '╗'
    
    return top_bottom_border + '\n' + box + '\n' + '╚' + '═' * (width + 2) + '╝'

def format_time_difference(timestamp):
    """Format time difference from timestamp to now, showing only the largest relevant time unit."""
    try:
        message_time = datetime.fromisoformat(timestamp)
        now = datetime.now()
        delta = now - message_time

        seconds = delta.total_seconds()
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24

        if days > 0:
            return f"{int(days)}d"
        elif hours > 0:
            return f"{int(hours)}hr"
        elif minutes > 0:
            return f"{int(minutes)}ms"
        else:
            return "0ms"

    except ValueError:
        return "Invalid time"

def display_chat_history(messages, chat_key, selected_friend, user_data):
    """Display the chat history with proper message alignment."""
    clear_screen()
    print( "" )
    print(" ⬅️ b")
    print("")
    print("")
    print(Fore.BLUE + center_text(f"{selected_friend}"))
    print("")
    
    terminal_width = get_terminal_width()
    message_width = terminal_width - 4  # Leave some padding for borders

    if chat_key in messages:
        print("")
        print(Style.DIM+ "\n"+"Chat History".rjust(-8))
        print("")
        for message in messages[chat_key]:
            if message['sender'] == user_data['username']:
                # Sender's message (right-aligned with blue background)
                formatted_message = format_message_box(message['message'], width=message_width, align='right')
                print(Fore.BLUE + Back.WHITE + formatted_message + Style.RESET_ALL)
            else:
                # Receiver's message (left-aligned with white background)
                formatted_message = format_message_box(message['message'], width=message_width, align='left')
                print(Fore.WHITE + Back.BLUE + formatted_message + Style.RESET_ALL)
            
            # Print timestamp in a smaller font style
            time_diff = format_time_difference(message['timestamp'])
            print(Fore.RED + Style.DIM + f"({time_diff})" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nNo messages yet.")
    
    print(Style.DIM + "_" * width)
    time.sleep(0.9)

def delete_messages(messages, chat_key, text):
    """Delete messages containing the specified text."""
    if chat_key in messages:
        original_length = len(messages[chat_key])
        messages[chat_key] = [msg for msg in messages[chat_key] if text not in msg['message']]
        return original_length - len(messages[chat_key])
    return 0

def delete_all_user_messages(messages, chat_key, user_data):
    """Delete all messages sent by the specified user."""
    if chat_key in messages:
        original_length = len(messages[chat_key])
        messages[chat_key] = [msg for msg in messages[chat_key] if msg['sender'] != user_data['username']]
        return original_length - len(messages[chat_key])
    return 0

def chat(users, user_data, selected_friend, email):
    hashed_email = hash_email(email)
    clear_screen()
    
    # Try to load the messages from the file, handle if file is empty or missing
    messages = data_store.get('messages', {})
    
    # Generate a unique chat key using both usernames (sorted alphabetically)
    chat_key = f"{min(user_data['username'], selected_friend)}-{max(user_data['username'], selected_friend)}"
    
    # Display initial chat history
    display_chat_history(messages, chat_key, selected_friend, user_data)

    # Input loop to keep the chat active
    while True:
        user_input = input(Style.DIM+Fore.BLUE + " \nType a message: "+Style.RESET_ALL)
        
        if user_input.lower() == 'b':
            return my_friends(user_data, email)
        
        if user_input.startswith('delete/'):
            command = user_input[7:]
            if command == 'all':
                # Delete all messages sent by the user
                deleted_count = delete_all_user_messages(messages, chat_key, user_data['username'])
                print(Fore.RED + f"Deleted {deleted_count} messages sent by you.")
            else:
                # Delete messages containing the specified text
                deleted_count = delete_messages(messages, chat_key, command)
                print(Fore.RED + f"Deleted {deleted_count} messages containing '{command}'.")
            
            # Save the updated messages to messages.json
            with open("messages.json", "w") as file:
                json.dump(messages, file, indent=4)
            
            # Redisplay chat history
            display_chat_history(messages, chat_key, selected_friend, user_data)
            continue

        # Create a new message entry
        new_message = {
            "sender": user_data['username'],
            "message": user_input,
            "timestamp": datetime.now().isoformat()  # Store timestamp in ISO format
        }

        # Add the message to the conversation history
        if chat_key not in messages:
            messages[chat_key] = []
        
        messages[chat_key].append(new_message)
        
        # Save the updated messages to messages.json
        with open("messages.json", "w") as file:
            json.dump(messages, file, indent=4)

        # Immediately display the sent message in chat history
        display_chat_history(messages, chat_key, selected_friend, user_data)
        
        print(Fore.RED + Style.DIM + "(just now)" + Style.RESET_ALL)  # Display "just now" in a smaller font style
        time.sleep(0.5)  # Simulate message being sent

    return my_friends(user_data, email)
    
def crowds(users, email):
    hashed_email = hash_email(email)
    user_data = users.get(hashed_email)
    clear_screen()
    print("")
    print(Style.DIM+" ⬅️ b")
    print(Fore.BLUE+center_text("Groups"))
    print("")
    print("")
    print(Fore.BLUE + "\n  ➕ Create  Group  |   🫂 My Group")
    print(Style.DIM + "_" * width)
    mo = input(Style.DIM + "\nInput an option: "+Style.RESET_ALL)
    
    if mo.lower() =='cg' :
        create_group(users, email)
    elif mo.lower() == 'mg':
        my_groups(users, email)
    elif mo == 'b':
        return user_dashboard(email)
                
def my_groups(users, email):
    hashed_email = hash_email(email)
    user_data = users.get(hashed_email)
    clear_screen()
    
    groups_data = data_store.get('groups', {})
    user_groups = []  # List to store groups the user has joined or created
    
    # Iterate through all groups and check if the user is either a member or the creator
    for group_name, group_info in groups_data.items():
        if user_data['username'] in group_info.get('members', []):
            user_groups.append(group_name)

    if not user_groups:
        print("")
        print(" ⬅️ b")
        print("")
        print("\n")
        print(Fore.BLUE+center_text("YOUR GROUPS"))
        print("")
        print("\n")
        print(Fore.CYAN + "\nYou are not a member of any groups.")
        print("")
        print("")
        aj = input(Style.DIM+"Whats on your mind   "+Style.RESET_ALL)
        if aj == 'b':
            return crowds(users, email)  # Correct return call
    
    # Display the list of groups
    print(Style.DIM + "_" * width)
    for idx, group in enumerate(user_groups, 1):
        print(Fore.GREEN + f"\n{idx}. {group}")
    print("")
    print(Style.DIM + "_" * width)
    
    # Prompt user to select a group
    cf = input("\nOpen a chat with a specific group (number): ")
    
    if cf == 'b':  # Option to go back
        return crowds(users, email)
    
    # Validate the user input and open the chat
    if cf.isdigit() and 1 <= int(cf) <= len(user_groups):
        selected_index = int(cf)
        selected_group = user_groups[selected_index - 1]
        print(f"\nOpening group chat for {selected_group}...")
        time.sleep(1.5)
        return group_chat(users, selected_group, email)  # Correct group_chat call
    else:
        print("\nInvalid input. Returning to the group list...")
        time.sleep(1.5)
        return my_groups(users, email)  # Correct recursive call
    
def get_terminal_width():
    """Get the width of the terminal."""
    try:
        return shutil.get_terminal_size((80, 20)).columns
    except Exception as e:
        print(f"Error detecting terminal size: {e}")
        return 80  # Default width if detection fails

def format_group_message_box(message, width=30, align='left'):
    """Format a message into a box without the sender's username inside."""
    # Wrap the content based on the provided width
    lines = textwrap.wrap(message, width=width)
    
    # Adjust alignment for each line (left or right)
    if align == 'right':
        lines = [line.rjust(width) for line in lines]
    elif align == 'left':
        lines = [line.ljust(width) for line in lines]

    # Create the message box with borders
    box = '\n'.join(f"║ {line} ║" for line in lines)
    top_bottom_border = '╔' + '═' * (width + 2) + '╗'
    
    return top_bottom_border + '\n' + box + '\n' + '╚' + '═' * (width + 2) + '╝'

def format_time_difference(timestamp):
    """Format time difference from timestamp to now."""
    try:
        message_time = datetime.fromisoformat(timestamp)
        now = datetime.now()
        delta = now - message_time

        seconds = delta.total_seconds()
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24

        if days > 0:
            return f"{int(days)}d"
        elif hours > 0:
            return f"{int(hours)}hr"
        elif minutes > 0:
            return f"{int(minutes)}m"
        else:
            return "0s"
    except ValueError:
        return "Invalid time"

def display_group_chat(messages, chat_key, selected_group, user_data):
    """Display the chat history with sender usernames outside their messages."""
    clear_screen()
    print("")
    print(Style.DIM+" ⬅️ b")
    print("")
    print(Fore.BLUE + center_text(f"{selected_group}"))
    print( "")
    print("")
    terminal_width = get_terminal_width()
    message_width = terminal_width - 4  # Leave some padding for borders

    if chat_key in messages:
        print(Style.DIM + "\n"+"Chat History".rjust(width-8))
        print( "\n")
        for message in messages[chat_key]:
            sender_username = message['sender']  # Get the actual sender's username

            if sender_username == user_data['username']:
                # Right-aligned message box without username inside
                formatted_message = format_group_message_box(message['message'], width=message_width, align='right')
                print(Fore.GREEN + Style.DIM + f"{sender_username}".rjust(message_width) + Style.RESET_ALL)
                print(Fore.BLUE + Back.WHITE + formatted_message + Style.RESET_ALL)
            else:
                # Left-aligned message box without username inside
                formatted_message = format_group_message_box(message['message'], width=message_width, align='left')
                print(Fore.GREEN + Style.DIM + f"{sender_username}".ljust(message_width) + Style.RESET_ALL)
                print(Fore.WHITE + Back.BLUE + formatted_message + Style.RESET_ALL)
            
            # Display the time difference below the message
            time_diff = format_time_difference(message['timestamp'])
            print(Fore.RED + Style.DIM + f"({time_diff})" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nNo messages yet.")
    print(Style.DIM + "_" * width)

def group_chat(user_data, selected_group, email):
    hashed_email = hash_email(email)
    user_data = users.get(hashed_email)
    clear_screen()
    
    # Load messages from the file
    messages = data_store.get('gmessages', {})

    # Generate a unique chat key based on the group name
    chat_key = f"group_{selected_group}"
    
    # Display chat history for the group
    display_group_chat(messages, chat_key, selected_group, user_data)

    while True:
        user_input = input(Fore.CYAN + "\nType a message: "+Style.RESET_ALL)
        
        if user_input.lower() == 'refresh':
            display_group_chat(messages, chat_key, selected_group, user_data)
        elif user_input.lower() == 'b':
            return my_groups(users, email)  # Correct arguments passed to my_groups
        
        elif user_input.startswith('delete/'):
            command = user_input[7:]
            if command == 'all':
                # Delete all messages sent by the user
                deleted_count = delete_all_user_messages(messages, chat_key, user_data['username'])
                print(Fore.RED + f"Deleted {deleted_count} messages sent by you.")
            else:
                # Delete messages containing the specified text
                deleted_count = delete_messages(messages, chat_key, command)
                print(Fore.RED + f"Deleted {deleted_count} messages containing '{command}'.")
            
            # Save the updated messages to gmessages.json
            with open("gmessages.json", "w") as file:
                json.dump(messages, file, indent=4)
            
            # Redisplay chat history
            display_group_chat(messages, chat_key, selected_group, user_data)
            continue
        
        # Add new message to the group chat
        new_message = {
            "sender": user_data['username'],
            "message": user_input,
            "timestamp": datetime.now().isoformat()  # Store timestamp in ISO format
        }
        
        if chat_key not in messages:
            messages[chat_key] = []
        
        messages[chat_key].append(new_message)
        
        # Save the updated messages to gmessages.json
        with open("gmessages.json", "w") as file:
            json.dump(messages, file, indent=4)
        
        display_group_chat(messages, chat_key, selected_group, user_data)
        
        print(Fore.RED + Style.DIM + "(just now)" + Style.RESET_ALL)  # Display "just now" in a smaller font style
        time.sleep(0.5)
     
    return my_groups(users, group_name, email)  
        
def create_group(users, email):
    hashed_email = hash_email(email)
    clear_screen()
    print("")
    print(" ⬅️ b")
    print("")
    print("")
    print(Fore.BLUE + "Create a Group".center(40))
    print("")
    print("")
    
    groups = data_store.get('groups', {})
    users = data_store.get('users', {})
    user_data = users.get(hashed_email)
    
    while True:
        group_name = input(Fore.BLUE + "Enter the name of your group "+Style.RESET_ALL).strip()
        
        # Check if the group name is valid (non-empty)
        if group_name == 'b':
            return crowds(users, email)
        if not group_name:
            print(Fore.RED + "Group name cannot be empty.")
            return create_group(users, email)
        
        # Check if the group already exists
        if group_name not in groups:
            # Add the new group to the groups file with the creator's username
            groups[group_name] = {
                'members': [user_data['username']]  # Assuming 'username' is the user's identifier
            }
            
            save_json(GROUPS_FILE, groups)
            print(Fore.GREEN + "Group created successfully.")
            time.sleep(0.8)
            return crowds(users, email)
        else:
            # Group already exists
            print(Fore.RED + f"Group already exists with this name: {group_name}")
            fg = input(Fore.BLUE + "Input 0 to create a new group, or 00 to return: ")
            
            if fg == '0':
                return create_group(users, email)  # Prompt the user again for a new group name
            elif fg == '00':
                return crowds(users, email)
            else:
                print(Fore.RED + "Invalid input. Please try again.")
                
def wsr_fund(users, email):
    hashed_email = hash_email(email)
    users = data_store.get('users', {})
    user_data = users.get(hashed_email)
    while True:
        clear_screen()
        print("")
        print(Style.DIM+" ⬅️ b")
        print("")
        print("")
        print(Fore.BLUE + center_text("WHISPER FUNDRAISER"))
        print("")
        print("")
        print(Style.DIM + center_text(f"Welcome {user_data['name']}"))
        print("")
        print("")
        print(Fore.BLUE + "\n1. 🚆 Support WHISPER  |  2. 💲 Monetize")
        print(Style.DIM + "_"*width)

        choice = input(Style.DIM+"\nPick a choice....: "+Style.RESET_ALL)
        
        if choice == '1':
            support(users, email)  # Ensure this function is defined elsewhere
            break
        elif choice == '2':
            monetize(users, email)  # Ensure this function is defined elsewhere
            break
        elif choice == 'b':
            return user_dashboard(email)
        else:
            print(Fore.RED + "Invalid input, please try again.")
            time.sleep(2)
            
def support(users, email):
    clear_screen()
    btc="bc1qjhwua5ln0nmfj2htf27vvlpreyehxr3jt693nc"
    print("")
    print(" ⬅️ b")
    print("")
    print(Fore.BLUE+center_text("Support Maskbook"))
    print("")
    print("")
    print(Fore.CYAN+"\n1. Support With BTC")
    print(Style.DIM+"_"*width)
    print(Fore.BLUE+"Deposit to email"+Style.RESET_ALL+Style.DIM+"maskbook.official@gmail.com")
    choiice=input(Style.DIM+"\n pick an option: "+Style.RESET_ALL)
    if choiice == 'b':
        return wsr_fund(users, email)
    elif choiice == '1':
        print(Fore.GREEN+ f"Make a support to the address:"+Style.DIM+ f"{btc}")
        ret=input("what on your mind... ")
        if ret == 'b':
            return wsr_fund(users, email)
        else:
            print(Fore.RED+"Invalid input")
            return wsr_fund(users, email)
    else:
        print(Fore.RED+"invalid input")
        time.sleep(1.5)
        return support(users, email) 
        
def monetize(users, email):
    hashed_email = hash_email(email)
    users = data_store.get('users', {})
    user_data = users.get(hashed_email)
    clear_screen()
    print("")
    print(" ⬅️ b")
    print("")
    print("\n")
    print(Back.CYAN+ Style.BRIGHT+Fore.BLUE + f"Welcome to Maskbook Monetizing")
    print("")
    print(Style.DIM+center_text(f"{user_data['name']}"))
    print("")
    print("")
    print(Fore.RED + "\nComing soon...")
    fo = input(Style.DIM + "what on your mind ")
    if fo == 'b':
        return wsr_fund(users, email)
    else:
        print(Fore.RED+"invalid input")
        return monetize(users, email)
        
admin = {
    "email": "alexndubuisiaugustine.chat@gmail.com",
    "password": "Alex12345#"
} 
width = os.get_terminal_size().columns  
def admin_dashboard(users, email):
    """Display the admin dashboard."""
    while True:
        clear_screen()
        print(Fore.GREEN+"="*width)
        print(Back.RED+Fore.GREEN+center_text("Admin Dashboard"))
        print(Fore.GREEN+"="*width)
        print(Fore.BLUE+"\n1. Add Bal   |   2. Deduct Bal")
        print(Fore.RED+"_"*width)
        print(Fore.BLUE+"\n3. Create Page  |   4. Create Group")
        print(Fore.RED+"_"*width)
        print(Fore.BLUE+"\n5. Pst to Pg  |   6. Pst to Gp")
        print(Fore.RED+"_"*width)
        print(Fore.BLUE+"\n7. Add stuff to Shop   |   8.  View Users")
        print(Fore.RED+"_"*width)
        print(Fore.BLUE+"\n0. Logout   |   add like  ")
        print(Fore.RED+"_"*width)
        choice = input(Fore.GREEN+"\nChoose an option my Admin: "+Style.RESET_ALL)
        if choice == '0':
            time.sleep(0.9)
            return
        elif choice == '1':
            add_user_balance(users, email)
        elif choice == '2':
            deduct_user_balance(users, email)
        elif choice == '3':
            create_page()
        elif choice == '4':
            create_group(groups, email)
        elif choice == '5':
            post_to_page()
        elif choice.lower() == 'al':
            add_like_count()
        elif choice == '6':
            post_to_group()
        elif choice == '7':
            add_product_to_store()
        elif choice == '8':
            view_users()
        else:
            print(Fore.RED + "Boss your input is wrong")

def add_user_balance(users, email):
    hashed_email = hash_email(email)
    clear_screen()
    """Add balance to a user account."""
    print(Fore.RED + "=" * width)
    print(Back.CYAN + Style.BRIGHT + Fore.RED + center_text("Add User Balance"))
    print(Fore.RED + "=" * width)
    
    users = data_store.get('users', {})
    user_data = users.get(hashed_email)
    
    user_email = input(Fore.GREEN + "\nEnter the user email Boss or 0 back: " + Style.RESET_ALL)
    hashed_user_email = hash_email(user_email)
    if user_email =='0':
        return admin_dashboard(users, email)
    
    if hashed_user_email in users:
        try:
            amount = float(input(Fore.YELLOW + "\nEnter the amount to add Boss: " + Style.RESET_ALL))
            print(Fore.GREEN + "Adding ......")
            time.sleep(0.9)
            # Convert the string balance to float, add the amount, then convert back to string
            current_balance = float(users[hashed_user_email]['balance'])
            updated_balance = current_balance + amount
            users[hashed_user_email]['balance'] = f"{updated_balance:.2f}"  # Store the balance as a string formatted to 2 decimal places
            save_json(USERS_FILE, users)
            print(Fore.GREEN + f"Added {amount} to {users[hashed_user_email]['name']}'s balance. New balance: {users[hashed_user_email]['balance']}")
        except ValueError:
            print(Fore.RED + "Invalid amount entered. Please enter a valid number.")
    else:
        print(Fore.RED + "User not found Boss.")
    
    time.sleep(0.9)
    return add_user_balance(users, email)

def deduct_user_balance(users, email):
    hashed_email = hash_email(email)
    clear_screen()
    """Deduct balance from a user account."""
    print(Fore.YELLOW + "=" * width)
    print(Back.RED + Style.BRIGHT + Fore.YELLOW + center_text("Deduct User Balance"))
    print(Fore.YELLOW + "=" * width)
    
    users = data_store.get('users', {})
    user_data = users.get(hashed_email)
    user_email = input(Fore.GREEN + "Enter the user's email: " + Style.RESET_ALL)
    hashed_user_email = hash_email(user_email)
    
    if hashed_user_email in users:
        try:
            current_balance = float(users[hashed_user_email].get('balance', "0.00"))  # Convert balance to float
            if current_balance == 0.00:
                print(Fore.RED + f"{users[hashed_user_email]['name']} has no balance to deduct boss.")
            else:
                amount = float(input(Fore.YELLOW + "Enter the amount to deduct boss: " + Style.RESET_ALL))
                if current_balance >= amount:
                    updated_balance = current_balance - amount
                    users[hashed_user_email]['balance'] = f"{updated_balance:.2f}"  # Update and store balance as a string
                    save_json(USERS_FILE, users)
                    print(Fore.GREEN + f"Deducted {amount} from {users[hashed_user_email]['name']}'s balance. New balance: {users[hashed_user_email]['balance']}")
                else:
                    print(Fore.RED + "Insufficient balance.")
        except ValueError:
            print(Fore.RED + "Invalid amount entered. Please enter a valid number.")
    else:
        print(Fore.RED + "User not found.")
        time.sleep(0.9)
        r
    
    input(Fore.CYAN + "Press Enter to return to Admin Dashboard..." + Style.RESET_ALL)

def create_page():
    clear_screen()
    """Create a new page."""
    print_banner("Create Page", Fore.CYAN)
    pages = data_store['pages']
    page_name = input("Enter the name of the page: ")
    if page_name not in pages:
        pages[page_name] = {'posts': []}
        save_json(PAGES_FILE, pages)
        print(Fore.GREEN + "Page created successfully.")
    else:
        print(Fore.RED + "Page already exists.")
    input("Press Enter to return to Admin Dashboard...")

def post_to_page():
    clear_screen()
    """Post a message to a page."""
    print_banner("Post to Page", Fore.CYAN)
    pages = data_store['pages']
    page_name = input("Enter the name of the page: ")
    if page_name in pages:
        post = input("Enter your post: ")
        pages[page_name]['posts'].append(post)
        save_json(PAGES_FILE, pages)
        print(Fore.GREEN + "Post added successfully.")
    else:
        print(Fore.RED + "Page not found.")
    input("Press Enter to return to Admin Dashboard...")

def post_to_group():
    clear_screen()
    """Post a message to a group."""
    print_banner("Post to Group", Fore.CYAN)
    groups =  data_store.get('groups', {})
    group_name = input("Enter the name of the group: ")
    if group_name in groups:
        message = input("Enter your message: ")
        groups[group_name]['messages'].append(message)
        save_json(GROUPS_FILE, groups)
        print(Fore.GREEN + "Message posted successfully.")
    else:
        print(Fore.RED + "Group not found.")
    input("Press Enter to return to Admin Dashboard...")

def add_product_to_store():
    clear_screen()
    """Add a product to the store."""
    print_banner("Add Product to Store", Fore.CYAN)
    spy_store = data_store['shops']
    product_name = input("Enter the name of the product: ")
    if product_name not in spy_store:
        price = float(input("Enter the price of the product: "))
        spy_store[product_name] = {'price': price}
        save_json(SPY_STORE_FILE, spy_store)
        print(Fore.GREEN + "Product added successfully.")
    else:
        print(Fore.RED + "Product already exists.")
    input("Press Enter to return to Admin Dashboard...")
        

users = data_store.get('users', {})

def view_users():
    # Load the users data from the file
    users_data = data_store.get('users', {})
    
    # Count the number of users
    user_count = len(users_data)
    
    if user_count > 0:
        # Display the number of users
        print(f"Boss, you got {user_count} user{'s' if user_count != 1 else ''}")
        time.sleep(0.9)
        return
    else:
        print("Boss, you got no user yet")
        time.sleep(0.9)
        return         
        
def start():
    clear_screen()
    print(Fore.BLUE+Style.BRIGHT+"\n"+center_text("Maskbook"))
    print("\n")
    print(Style.DIM+"—"*width)
    print(Style.DIM+"By proceeding, you agree to Terms which includes letting Maskbook to keep your data encrypted.")
    print(Style.DIM+"—"*width)
    print("\n"+Style.RESET_ALL+" "+"[1]. "+Back.BLUE+" Login "+Style.RESET_ALL+Style.DIM+" | "+Style.RESET_ALL+"[2]. "+Back.WHITE+Fore.BLUE+ " Create new account "+Style.RESET_ALL)
    print("_"*width)
    print("\n"+center_text("[3]. "+Style.DIM+"Forgot password?"))
    print(Style.DIM+"_"*width)
    print("\n")
    starts = input("\n"+Style.DIM+" What's on your mind?   "+Style.RESET_ALL)
    if starts == '1':
        loginn()
    if not starts:
        print(Fore.RED+" It cannot be empty")
        time.sleep(0.9)
        return start()
            
    elif starts == '2':
        create()
        
def loginn():
    centered_loading_animation_az(Fore.BLUE+"Welcome ... ", 0.9)
    clear_screen()
    print(Style.DIM+"  ⬅️"+" .[b]")
    print("\n")
    print("\n")
    print(Fore.BLUE+Style.BRIGHT+center_text("Maskbook"))
    print("\n")
    print("\n")
    email = input(Style.DIM+"  email address:   ")
    if email == 'b':
        return start()
        
    if not validate_email(email):
        print(Fore.RED+"\n"+" Invalid email")
        time.sleep(1)
        return loginn()
        
    if not email:
        print(Fore.RED+"\n"+" Email cannot be empty")
        time.sleep(1)
        return loginn()
        
    password = masked_input("\n"+Style.DIM+"  Password:   ")
    if password == 'b':
        return loginn()
    if not password:
        print(Fore.RED+"\n"+" Password cannot be empty")
        time.sleep(1)
        return loginn()
    login_user(email, password)
    
def create():
    clear_screen()
    print(Style.DIM+"  ⬅️"+" .[b]")
    print("\n")
    print("Join Maskbook")
    print("\n")
    print(center_emoji("♥️  📸 😎"))
    print(center_emoji("🫂 👥 👤"))
    print(Style.DIM+center_text("Create an account to connect with friends, family and communities of people who share your interests."))
    print(Style.DIM+"—"*width)
    print("\n"+center_text("[5]. "+Back.BLUE+Fore.WHITE+" Get Started "+Style.RESET_ALL))
    print("\n"+center_text("     "+"[6]. "+Back.WHITE+Fore.BLACK+" I already have an account "+Style.RESET_ALL))
    print("\n")
    check = input(Style.DIM+"\n  What's on your mind  ")
    if check == 'b':
        return start()
    elif check == '5':
        names()
    elif check == '6':
        return loginn()
        
def names():
    clear_screen()
    print(Style.DIM+"  ⬅️"+" .[b]")
    print("\n")
    print(Style.BRIGHT+Fore.WHITE+"  What's your name?")
    print(" ")
    print(Style.DIM+"  Enter the name you use in real life.")
    print("\n")
    name = input(Style.DIM+"   Your fullname:  ")
    if name == 'b':
        return create()
    if not name:
        print(Fore.RED+"\n"+"Name cannot be empty")
        time.sleep(1)
        return names()
    emails(name)
    return name
    
def emails(name):    
    clear_screen()
    print(Style.DIM+"  ⬅️"+" .[b]")
    print("\n")
    print(Style.BRIGHT+Fore.WHITE+"  What's your email address?")
    print(" ")
    print(Style.DIM+"  Enter the email address on which you can be contacted. No one will see this on your profile")
    print("\n")
    email = input(Style.DIM+"   What's your email:  ")
    if email == 'b':
        return names()
    if not email:
        print(Fore.RED+"\n"+" email cannot be empty")
        time.sleep(1)
        return emails(name)
    if not validate_email(email):
        print(Fore.RED+"\n"+" Invalid email")
        time.sleep(1)
        return emails(name)
    passwords(name, email)
    return email
    
def passwords(name, email):
    clear_screen()
    print(Style.DIM+"  ⬅️"+" .[b]")
    print("\n")
    print(Style.BRIGHT+Fore.WHITE+"  Create a strong password")
    print(" ")
    print(Style.DIM+"  Create a very strong password to avoid been hack. No one will see this on your profile")
    print("\n")
    password = input(Style.DIM+"   Create a password:  ")
    if password == 'b':
        return emails(name)
    if not password:
        print(Fore.RED+"\n"+" password cannot be empty")
        time.sleep(1)
        return passwords(name, email)
    pins(name, email, password) 
    return password
        
def pins(name, email, password):
    clear_screen()
    print(Style.DIM+"  ⬅️"+" .[b]")
    print("\n")
    print(Style.BRIGHT+Fore.WHITE+"  Create a strong pin")
    print(" ")
    print(Style.DIM+"  Create a very strong pin to avoid been hack. No one will see this on your profile")
    print("\n")
    pin = input(Style.DIM+"   Create a pin:  ")
    if pin == 'b':
        return passwords(name, email)
    if not pin:
        print(Fore.RED+"pin cannot be empty")
        time.sleep(1)
        return pins(name, email, password)
        
    username = register_user(name, email, password, pin)
    if username:
        print("\n")
        print("\n")
        print(Style.BRIGHT+center_emoji("🥳🎉"))
        print(Style.DIM+Fore.GREEN + center_text(f"\n Created successfully"))
        time.sleep(0.9)
        return loginn()
        

def main_menu():
    start_auto_refresh()
    load_data()
    while True:
        attention()
            
if __name__ == "__main__":
    main_menu()     