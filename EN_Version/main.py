import asyncio
import os
import time
import random
import base64
import shutil
import ctypes

try:
    import pyglet
    pyglet.options['shadow_window'] = False
    player = pyglet.media.Player()
    AUDIO_OK = True
except ImportError:
    AUDIO_OK = False

from aiogram import Bot
from aiogram.types import FSInputFile, ChatPermissions, BotCommand
from aiogram.enums import ChatAction
import config

bot = Bot(token=config.BOT_TOKEN)

# ==========================================
# COLOR ENGINE
# ==========================================
os.system('') 

THEMES = {
    "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
    "blue": "\033[94m", "purple": "\033[95m", "cyan": "\033[96m", "white": "\033[97m"
}
CURRENT_THEME = "cyan"

def colorize(text, theme=None):
    global CURRENT_THEME
    t = theme if theme else CURRENT_THEME
    if t == "rainbow":
        colors = ["\033[91m", "\033[93m", "\033[92m", "\033[96m", "\033[94m", "\033[95m"]
        rainbow_text = ""
        for i, char in enumerate(text):
            if char in ['\n', '\t']: rainbow_text += char
            else: rainbow_text += colors[i % len(colors)] + char
        return rainbow_text + "\033[0m"
    if t in THEMES: return f"{THEMES[t]}{text}\033[0m"
    return text

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ==========================================
# WINDOW SIZE
# ==========================================
def ask_window_size():
    clear_screen()
    print("╔══════════════════════════════════════════════════╗")
    print("║             CHOOSE PANEL WINDOW SIZE             ║")
    print("╠══════════════════════════════════════════════════╣")
    print("║  1. 25% (Small)                                  ║")
    print("║  2. 50% (Medium)                                 ║")
    print("║  3. 65% (Normal)                                 ║")
    print("║  4. 85% (Large)                                  ║")
    print("║  5. 100% (Full Screen)                           ║")
    print("╚══════════════════════════════════════════════════╝")
    
    while True:
        choice = input("\nYour choice (1-5): ")
        
        try:
            user32 = ctypes.windll.user32
            sw = user32.GetSystemMetrics(0)
            sh = user32.GetSystemMetrics(1)
            max_cols = int(sw / 10) 
            max_lines = int(sh / 22) 
            if max_cols > 200: max_cols = 200
        except:
            max_cols, max_lines = 150, 45

        try:
            if choice == "1": os.system('mode con: cols=80 lines=25'); break
            elif choice == "2": os.system('mode con: cols=100 lines=30'); break
            elif choice == "3": os.system(f'mode con: cols={int(max_cols*0.65)} lines={int(max_lines*0.65)}'); break
            elif choice == "4": os.system(f'mode con: cols={int(max_cols*0.85)} lines={int(max_lines*0.85)}'); break
            elif choice == "5": os.system(f'mode con: cols={max_cols} lines={max_lines}'); break
            else: print("Wrong choice, bro. Press 1-5.")
        except Exception as e:
            print(f"Failed to resize: {e}")
            break

# ==========================================
# SMART PANEL (COLOR FIXED)
# ==========================================
def draw_panel(title, options):
    cols = shutil.get_terminal_size().columns
    width = max(60, cols - 4) 
    
    # Removed hardcoded "cyan" -> now uses CURRENT_THEME
    print(colorize("╔" + "═" * width + "╗"))
    
    title_str = f"  {title}  "
    left_pad = (width - len(title_str)) // 2
    right_pad = width - len(title_str) - left_pad
    print(colorize("║" + " " * left_pad + title_str + " " * right_pad + "║"))
    print(colorize("╠" + "═" * width + "╣"))
    
    col_width = (width - 1) // 2
    right_width = width - 1 - col_width
    
    for i in range(0, len(options), 2):
        left_opt = options[i]
        right_opt = options[i+1] if i+1 < len(options) else ""
        
        left_str = f" {left_opt}"[:col_width].ljust(col_width)
        right_str = f" {right_opt}"[:right_width].ljust(right_width)
        
        print(colorize(f"║{left_str}│{right_str}║"))
            
    print(colorize("╚" + "═" * width + "╝"))

def get_file_type(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png', '.webp']: return 'photo'
    elif ext in ['.mp4', '.mov', '.avi', '.mkv']: return 'video'
    elif ext in ['.gif']: return 'animation'
    elif ext in ['.mp3', '.ogg', '.wav', '.m4a']: return 'audio'
    elif ext in ['.webm', '.tgs']: return 'sticker'
    else: return 'document'

async def smart_send_file(chat_id, path, caption=""):
    file_type = get_file_type(path)
    file = FSInputFile(path)
    if file_type == 'photo': await bot.send_photo(chat_id=chat_id, photo=file, caption=caption)
    elif file_type == 'video': await bot.send_video(chat_id=chat_id, video=file, caption=caption)
    elif file_type == 'animation': await bot.send_animation(chat_id=chat_id, animation=file, caption=caption)
    elif file_type == 'audio': await bot.send_audio(chat_id=chat_id, audio=file, caption=caption)
    elif file_type == 'sticker': await bot.send_sticker(chat_id=chat_id, sticker=file)
    else: await bot.send_document(chat_id=chat_id, document=file, caption=caption)

def pause():
    print(colorize("\n[BRO, DONE!] Press Enter to continue...", "yellow"))
    return asyncio.to_thread(input)

# ==========================================
# SECTION 1: TEXT
# ==========================================
async def menu_text():
    while True:
        clear_screen()
        draw_panel("1. TEXT", [
            "1. Regular text", "2. HTML (bold)", "3. 'Typing...' effect",
            "4. Reverse text", "5. CAPS (SCREAM)", "6. Meme text",
            "7. Base64 Encryption", "8. SECRET TEXT", "0. Back to menu"
        ])
        choice = await asyncio.to_thread(input, colorize("\nWhat do you choose, bro? -> ", "green"))
        if choice == "0": break
        elif choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            text = await asyncio.to_thread(input, colorize("Enter text, bro:\n> ", "green"))
            if choice == "4": text = text[::-1]
            elif choice == "5": text = text.upper()
            elif choice == "6": text = ''.join(c.upper() if i%2==0 else c.lower() for i,c in enumerate(text))
            elif choice == "7": text = base64.b64encode(text.encode()).decode()
            elif choice == "8": text = f"<tg-spoiler>{text}</tg-spoiler>"
            try:
                mode = "HTML" if choice in ["2", "8"] else None
                if choice == "3":
                    await bot.send_chat_action(config.CHAT_ID, ChatAction.TYPING)
                    await asyncio.sleep(1.5)
                await bot.send_message(chat_id=config.CHAT_ID, text=text, parse_mode=mode)
                print(colorize("[BRO, SENT!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()

# ==========================================
# SECTION 2: MEDIA
# ==========================================
async def menu_media():
    while True:
        clear_screen()
        draw_panel("2. MEDIA", [
            "1. Send file", "2. Location", "3. Contact", 
            "4. Sticker", "5. Video Note", "0. Back to menu"
        ])
        choice = await asyncio.to_thread(input, colorize("\nWhat do you choose, bro? -> ", "green"))
        if choice == "0": break
        elif choice == "1":
            path = (await asyncio.to_thread(input, colorize("Path to file:\n> ", "green"))).strip('"\' ')
            if not os.path.exists(path): print(colorize("[ERROR] No file.", "red")); await pause(); continue
            caption = await asyncio.to_thread(input, colorize("Caption:\n> ", "green"))
            try: await smart_send_file(config.CHAT_ID, path, caption); print(colorize("[BRO, SENT!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            try:
                lat = await asyncio.to_thread(input, colorize("Latitude:\n> ", "green"))
                lon = await asyncio.to_thread(input, colorize("Longitude:\n> ", "green"))
                await bot.send_location(config.CHAT_ID, float(lat), float(lon)); print(colorize("[BRO, LOCATION!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "3":
            phone = await asyncio.to_thread(input, colorize("Phone:\n> ", "green"))
            name = await asyncio.to_thread(input, colorize("Name:\n> ", "green"))
            try: await bot.send_contact(config.CHAT_ID, phone, name); print(colorize("[BRO, CONTACT!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "4":
            path = (await asyncio.to_thread(input, colorize("Path to sticker:\n> ", "green"))).strip('"\' ')
            try: await bot.send_sticker(config.CHAT_ID, FSInputFile(path)); print(colorize("[BRO, STICKER!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "5":
            path = (await asyncio.to_thread(input, colorize("Path to video (.mp4):\n> ", "green"))).strip('"\' ')
            try: await bot.send_video_note(config.CHAT_ID, FSInputFile(path)); print(colorize("[BRO, VIDEO NOTE!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()

# ==========================================
# SECTION 3: SPAM ZONE (CTRL+C FIXED)
# ==========================================
async def menu_spam():
    while True:
        clear_screen()
        draw_panel("3. SPAM ZONE", [
            "1. Text", "2. File", "3. SMART SPAM",
            "4. STONES", "5. INFINITE", "0. Back to menu"
        ])
        choice = await asyncio.to_thread(input, colorize("\nWhat do you choose, bro? -> ", "green"))
        if choice == "0": break
        elif choice in ["1", "2", "3", "4", "5"]:
            if choice == "1": text = await asyncio.to_thread(input, colorize("Text:\n> ", "green")); path=None
            elif choice == "2": path = (await asyncio.to_thread(input, colorize("Path to file:\n> ", "green"))).strip('"\' '); text=None
            elif choice == "4": text = "STONE " * 50; path=None
            elif choice == "5": text = await asyncio.to_thread(input, colorize("Text:\n> ", "green")); path=None
            else: text = await asyncio.to_thread(input, colorize("Text:\n> ", "green")); path=None

            if path and not os.path.exists(path): print(colorize("[ERROR] No file.", "red")); await pause(); continue
            try:
                count = 999999 if choice == "5" else int(await asyncio.to_thread(input, colorize("How many times? ", "green")))
                delay = "random" if choice in ["3", "4", "5"] else float(await asyncio.to_thread(input, colorize(f"Delay: ", "green")) or config.DEFAULT_SPAM_DELAY)
            except ValueError: 
                print(colorize("[ERROR] Need a number!", "red"))
                await pause()
                continue

            print(colorize("\nLet's spam...", "yellow"))
            for i in range(count):
                try:
                    if path: await smart_send_file(config.CHAT_ID, path)
                    else: await bot.send_message(config.CHAT_ID, text)
                    print(colorize(f"[{i+1}/{count if count < 999999 else 'INF'}] ok", "green"))
                    await asyncio.sleep(random.uniform(1.5, 3.5) if delay == "random" else delay)
                except asyncio.CancelledError:
                    print(colorize("\n[BRO] Spam interrupted!", "yellow"))
                    return
                except Exception as e: 
                    print(colorize(f"[BAN] {e}", "red"))
                    break
            await pause()

# ==========================================
# SECTION 4: TRICKS
# ==========================================
async def menu_features():
    while True:
        clear_screen()
        draw_panel("4. TRICKS", [
            "1. Poll", "2. Pin", "3. Dice",
            "4. Darts", "5. Basketball", "6. Roulette",
            "7. Football", "8. Random (1-100)", "0. Back to menu"
        ])
        choice = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if choice == "0": break
        elif choice == "1":
            q = await asyncio.to_thread(input, "Question: "); o1 = await asyncio.to_thread(input, "Opt 1: "); o2 = await asyncio.to_thread(input, "Opt 2: ")
            try: await bot.send_poll(config.CHAT_ID, q, [o1, o2]); print(colorize("[POLL!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            try:
                msg = await bot.send_message(config.CHAT_ID, "Pinned!")
                await bot.pin_chat_message(config.CHAT_ID, msg.message_id); print(colorize("[PINNED!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice in ["3", "4", "5", "6", "7"]:
            emoji = {"3":"🎲", "4":"🎯", "5":"🏀", "6":"🎰", "7":"⚽"}[choice] 
            try: await bot.send_dice(config.CHAT_ID, emoji=emoji); print(colorize("[GAME!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "8":
            try: await bot.send_message(config.CHAT_ID, f"Number: {random.randint(1, 100)}"); print(colorize("[NUMBER!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()

# ==========================================
# SECTION 5: ADMIN PANEL
# ==========================================
async def menu_admin():
    while True:
        clear_screen()
        draw_panel("5. ADMIN PANEL", [
            "1. Mute all", "2. Unmute all", "3. Change title",
            "4. Change description", "5. Ban by ID", "6. Ban by @user",
            "7. Kick by ID", "8. Kick by @user", "9. Delete message",
            "0. Back to menu"
        ])
        choice = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if choice == "0": break
        elif choice == "1":
            try: await bot.set_chat_permissions(config.CHAT_ID, ChatPermissions(can_send_messages=False)); print(colorize("[MUTED!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            try: await bot.set_chat_permissions(config.CHAT_ID, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)); print(colorize("[UNMUTED!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "3":
            t = await asyncio.to_thread(input, "New title: ")
            try: await bot.set_chat_title(config.CHAT_ID, t); print(colorize("[OK]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "4":
            d = await asyncio.to_thread(input, "New description: ")
            try: await bot.set_chat_description(config.CHAT_ID, d); print(colorize("[OK]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice in ["5", "6", "7", "8"]:
            if choice in ["5", "7"]:
                try: target = int(await asyncio.to_thread(input, "ID: "))
                except ValueError: print(colorize("[ERROR] Need numbers", "red")); await pause(); continue
            else: target = (await asyncio.to_thread(input, "@user: ")).strip()
            try:
                if choice in ["5", "6"]: await bot.ban_chat_member(config.CHAT_ID, target); print(colorize("[BANNED!]", "green"))
                else:
                    await bot.ban_chat_member(config.CHAT_ID, target); await bot.unban_chat_member(config.CHAT_ID, target); print(colorize("[KICKED!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "9":
            try: msg_id = int(await asyncio.to_thread(input, "Message ID: ")); await bot.delete_message(config.CHAT_ID, msg_id); print(colorize("[DELETED!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()

# ==========================================
# SECTION 6-10
# ==========================================
async def menu_bot_settings():
    while True:
        clear_screen(); draw_panel("6. BOT SETTINGS", ["1. Set commands", "2. Bot description", "0. Back"])
        choice = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if choice == "0": break
        elif choice == "1":
            try: await bot.set_my_commands([BotCommand(command="start", description="Start")]); print(colorize("[OK!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            d = await asyncio.to_thread(input, "Description: ")
            try: await bot.set_my_description(d); print(colorize("[OK]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()

async def menu_settings():
    while True:
        clear_screen(); draw_panel("7. INFO", ["1. Profile", "2. Ping", "3. Chat info", "4. Members", "0. Back"])
        choice = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if choice == "0": break
        elif choice == "1":
            me = await bot.get_me(); print(colorize(f"\nName: {me.first_name}\nUser: @{me.username}", "white")); await pause()
        elif choice == "2":
            start = time.time(); await bot.get_me(); print(colorize(f"\nPing: {round((time.time() - start) * 1000, 2)} ms", "white")); await pause()
        elif choice == "3":
            try:
                chat = await bot.get_chat(config.CHAT_ID); print(colorize(f"\nTitle: {chat.title}", "white"))
            except Exception as e: print(colorize(f"\n[ERROR] {e}", "red"))
            await pause()
        elif choice == "4":
            try: print(colorize(f"\nMembers: {await bot.get_chat_member_count(config.CHAT_ID)}", "white"))
            except Exception as e: print(colorize(f"\n[ERROR] {e}", "red"))
            await pause()

async def menu_help():
    while True:
        clear_screen(); draw_panel("8. GUIDE", ["1. Text", "2. Media", "3. Spam", "4. Tricks", "5. Admin", "6. Settings", "7. Info", "8. Music", "0. Back"])
        choice = await asyncio.to_thread(input, colorize("\nWhich section? ", "green"))
        if choice == "0": break
        print(colorize("\nEXPLANATION FOR THIS SECTION...", "yellow")); await pause()

async def menu_music():
    global player
    if not AUDIO_OK: print(colorize("\n[ERROR] Pyglet is not installed!", "red")); await pause(); return
    while True:
        clear_screen(); draw_panel("9. MUSIC", ["1. Play", "2. Pause/Resume", "3. Stop", "4. Vol UP (+10%)", "5. Vol DOWN (-10%)", "0. Back"])
        print(colorize("[STATUS] " + ("Playing..." if player.playing else "Silence"), "green"))
        choice = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if choice == "0": break
        elif choice == "1":
            path = (await asyncio.to_thread(input, "Path to mp3: ")).strip('"\' ')
            try: 
                player = pyglet.media.Player()
                source = await asyncio.to_thread(pyglet.media.load, path, streaming=True)
                player.queue(source); player.play(); print(colorize("[PLAYING!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            if player.playing: player.pause(); print(colorize("[PAUSED]", "green"))
            else: player.play(); print(colorize("[RESUMED]", "green"))
            await pause()
        elif choice == "3": player.pause(); player.seek(0); print(colorize("[STOPPED]", "green")); await pause()
        elif choice == "4": player.volume = min(1.0, player.volume + 0.1); print(colorize(f"[VOLUME: {int(player.volume*100)}%]", "green")); await pause()
        elif choice == "5": player.volume = max(0.0, player.volume - 0.1); print(colorize(f"[VOLUME: {int(player.volume*100)}%]", "green")); await pause()

async def menu_theme():
    global CURRENT_THEME
    while True:
        clear_screen(); draw_panel("10. THEME", ["1. Red", "2. Green", "3. Blue", "4. Yellow", "5. Purple", "6. Cyan", "7. RAINBOW", "0. Back"])
        choice = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if choice == "0": break
        elif choice == "1": CURRENT_THEME = "red"
        elif choice == "2": CURRENT_THEME = "green"
        elif choice == "3": CURRENT_THEME = "blue"
        elif choice == "4": CURRENT_THEME = "yellow"
        elif choice == "5": CURRENT_THEME = "purple"
        elif choice == "6": CURRENT_THEME = "cyan"
        elif choice == "7": CURRENT_THEME = "rainbow"
        else: continue
        print(colorize("\n[THEME CHANGED!]", "green")); await pause()

# ==========================================
# MAIN MENU (CTRL+C FIXED)
# ==========================================
async def main():
    ask_window_size()
    clear_screen()
    print(colorize("Starting...", "yellow")); await bot.delete_webhook()
    try:
        me = await bot.get_me(); print(colorize(f"[BOT @{me.username} IS ONLINE!]", "green")); await asyncio.sleep(1)
    except Exception as e: print(colorize(f"[ERROR] {e}", "red")); return

    while True:
        try:
            clear_screen()
            draw_panel("BRO-PANEL BOT V14", [
                "1. TEXT", "6. BOT SETTINGS",
                "2. MEDIA", "7. INFO & PING",
                "3. SPAM ZONE", "8. GUIDE (HELP)",
                "4. TRICKS", "9. MUSIC",
                "5. ADMIN PANEL", "10. THEME",
                "0. EXIT", ""
            ])
            
            choice = await asyncio.to_thread(input, colorize("\nChoose section (0-10): ", "green"))

            if choice == "0": 
                print(colorize("Exiting...", "yellow"))
                if AUDIO_OK: player.pause() 
                break
            elif choice == "1": await menu_text()
            elif choice == "2": await menu_media()
            elif choice == "3": await menu_spam()
            elif choice == "4": await menu_features()
            elif choice == "5": await menu_admin()
            elif choice == "6": await menu_bot_settings()
            elif choice == "7": await menu_settings()
            elif choice == "8": await menu_help()
            elif choice == "9": await menu_music()
            elif choice == "10": await menu_theme()

        except (KeyboardInterrupt, asyncio.CancelledError):
            print(colorize("\n\n[BRO] You pressed Ctrl+C. Exiting the bot...", "red"))
            if AUDIO_OK: player.pause()
            break

    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
