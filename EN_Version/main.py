import asyncio
import os
import time
import random
import base64

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
# COLOR ENGINE (ANSI codes)
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
        print(colorize("=== 1. BRO, HERE IS TEXT ===", "cyan"))
        print("1. Regular text\n2. HTML (bold)\n3. 'Typing...' effect\n4. Reverse text\n5. CAPS (SCREAM)")
        print("6. Meme text\n7. Base64 Encryption\n8. SECRET TEXT (Spoiler)\n0. Back")
        
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
        print(colorize("=== 2. BRO, HERE IS MEDIA ===", "cyan"))
        print("1. File\n2. Location\n3. Contact\n4. Sticker\n5. Video Note\n0. Back")
        
        choice = await asyncio.to_thread(input, colorize("\nWhat do you choose, bro? -> ", "green"))
        if choice == "0": break
        
        elif choice == "1":
            path = (await asyncio.to_thread(input, colorize("Path to file:\n> ", "green"))).strip('"\' ')
            if not os.path.exists(path): print(colorize("[ERROR] No file.", "red")); await pause(); continue
            caption = await asyncio.to_thread(input, colorize("Caption (Enter - skip):\n> ", "green"))
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
# SECTION 3: SPAM ZONE
# ==========================================
async def menu_spam():
    while True:
        clear_screen()
        print(colorize("=== 3. BRO, HERE IS SPAM ===", "cyan"))
        print("1. Text\n2. File\n3. SMART SPAM (random)\n4. STONES 🗿\n5. INFINITE\n0. Back")
        
        choice = await asyncio.to_thread(input, colorize("\nWhat do you choose, bro? -> ", "green"))
        if choice == "0": break
        elif choice in ["1", "2", "3", "4", "5"]:
            if choice == "1": text = await asyncio.to_thread(input, colorize("Text:\n> ", "green")); path=None
            elif choice == "2": path = (await asyncio.to_thread(input, colorize("Path to file:\n> ", "green"))).strip('"\' '); text=None
            elif choice == "4": text = "🗿" * 50; path=None
            elif choice == "5": text = await asyncio.to_thread(input, colorize("Text:\n> ", "green")); path=None
            else: text = await asyncio.to_thread(input, colorize("Text:\n> ", "green")); path=None

            if path and not os.path.exists(path): print(colorize("[ERROR] No file.", "red")); await pause(); continue
            try:
                count = 999999 if choice == "5" else int(await asyncio.to_thread(input, colorize("How many times? ", "green")))
                delay = "random" if choice in ["3", "4", "5"] else float(await asyncio.to_thread(input, colorize(f"Delay (Enter for {config.DEFAULT_SPAM_DELAY}): ", "green")) or config.DEFAULT_SPAM_DELAY)
            except ValueError: 
                print(colorize("[ERROR] Need a number!", "red"))
                await pause()
                continue

            print(colorize("\nLet's spam...", "yellow"))
            for i in range(count):
                try:
                    if path: await smart_send_file(config.CHAT_ID, path)
                    else: await bot.send_message(config.CHAT_ID, text)
                    print(colorize(f"[{i+1}/{count if count < 999999 else '∞'}] ok", "green"))
                    await asyncio.sleep(random.uniform(1.5, 3.5) if delay == "random" else delay)
                except Exception as e: print(colorize(f"[TG BAN] {e}", "red")); break
            await pause()

# ==========================================
# SECTION 4: TRICKS
# ==========================================
async def menu_features():
    while True:
        clear_screen()
        print(colorize("=== 4. TRICKS ===", "cyan"))
        print("1. Poll\n2. Pin\n3. Dice\n4. Darts\n5. Basketball\n6. Roulette\n7. Football\n8. Random (1-100)\n0. Back")
        choice = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if choice == "0": break
        elif choice == "1":
            q = await asyncio.to_thread(input, "Question: "); o1 = await asyncio.to_thread(input, "Opt 1: "); o2 = await asyncio.to_thread(input, "Opt 2: ")
            try: await bot.send_poll(config.CHAT_ID, q, [o1, o2]); print(colorize("[POLL CREATED!]", "green"))
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
            try: await bot.send_dice(config.CHAT_ID, emoji=emoji); print(colorize("[GAME STARTED!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "8":
            try: await bot.send_message(config.CHAT_ID, f"Number: {random.randint(1, 100)}"); print(colorize("[NUMBER SENT!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()

# ==========================================
# SECTION 5: ADMIN PANEL
# ==========================================
async def menu_admin():
    while True:
        clear_screen()
        print(colorize("=== 5. ADMIN PANEL ===", "cyan"))
        print("1. Mute all\n2. Unmute all\n3. Change title\n4. Change description")
        print("5. Ban by ID\n6. Ban by @user\n7. Kick by ID\n8. Kick by @user\n9. Delete message\n0. Back")
        choice = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if choice == "0": break
        elif choice == "1":
            try: await bot.set_chat_permissions(config.CHAT_ID, ChatPermissions(can_send_messages=False)); print(colorize("[MUTED ALL!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            try: await bot.set_chat_permissions(config.CHAT_ID, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)); print(colorize("[UNMUTED ALL!]", "green"))
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
# SECTION 6-8: SETTINGS, INFO, GUIDE
# ==========================================
async def menu_bot_settings():
    while True:
        clear_screen(); print(colorize("=== 6. BOT SETTINGS ===", "cyan"))
        print("1. Set commands\n2. Bot description\n0. Back")
        choice = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if choice == "0": break
        elif choice == "1":
            try:
                await bot.set_my_commands([BotCommand(command="start", description="Start"), BotCommand(command="help", description="Help")])
                print(colorize("[COMMANDS SET!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            d = await asyncio.to_thread(input, "Description: ")
            try: await bot.set_my_description(d); print(colorize("[OK]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()

async def menu_settings():
    while True:
        clear_screen(); print(colorize("=== 7. INFO ===", "cyan"))
        print("1. Profile\n2. Ping\n3. Chat info\n4. Member count\n0. Back")
        choice = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if choice == "0": break
        elif choice == "1":
            me = await bot.get_me(); print(colorize(f"\nName: {me.first_name}\nUser: @{me.username}\nID: {me.id}", "white")); await pause()
        elif choice == "2":
            start = time.time(); await bot.get_me(); print(colorize(f"\nPing: {round((time.time() - start) * 1000, 2)} ms", "white")); await pause()
        elif choice == "3":
            try:
                chat = await bot.get_chat(config.CHAT_ID)
                print(colorize(f"\nTitle: {chat.title}\nID: {chat.id}\nType: {chat.type}", "white"))
            except Exception as e: print(colorize(f"\n[ERROR] {e}", "red"))
            await pause()
        elif choice == "4":
            try: print(colorize(f"\nMembers: {await bot.get_chat_member_count(config.CHAT_ID)}", "white"))
            except Exception as e: print(colorize(f"\n[ERROR] {e}", "red"))
            await pause()

async def menu_help():
    while True:
        clear_screen(); print(colorize("=== 8. GUIDE ===", "cyan"))
        print("1. Text\n2. Media\n3. Spam\n4. Tricks\n5. Admin\n6. Settings\n7. Info\n8. Music\n0. Back")
        choice = await asyncio.to_thread(input, colorize("\nWhich section to explain? ", "green"))
        clear_screen()
        if choice == "1": print(colorize("EXPLANATION FOR TEXT (HTML, Base64, etc.)", "yellow")); await pause()
        elif choice == "2": print(colorize("EXPLANATION FOR MEDIA (Notes, Geo)", "yellow")); await pause()
        elif choice == "3": print(colorize("EXPLANATION FOR SPAM (Smart, Infinite)", "yellow")); await pause()
        elif choice == "4": print(colorize("EXPLANATION FOR GAMES AND POLLS", "yellow")); await pause()
        elif choice == "5": print(colorize("EXPLANATION FOR BANS AND MUTES", "yellow")); await pause()
        elif choice == "6": print(colorize("EXPLANATION FOR BOT COMMANDS", "yellow")); await pause()
        elif choice == "7": print(colorize("EXPLANATION FOR PING AND STATS", "yellow")); await pause()
        elif choice == "8": print(colorize("EXPLANATION FOR MUSIC (Pyglet)", "yellow")); await pause()
        elif choice == "0": break

# ==========================================
# SECTION 9: MUSIC
# ==========================================
async def menu_music():
    global player
    if not AUDIO_OK: print(colorize("\n[ERROR] Pyglet is not installed!", "red")); await pause(); return

    while True:
        clear_screen(); print(colorize("=== 9. MUSIC ===", "cyan"))
        print(colorize("[STATUS] " + ("Playing..." if player.playing else "Silence/Paused"), "green"))
        print("1. Play\n2. Pause/Resume\n3. Stop\n4. Volume UP (+10%)\n5. Volume DOWN (-10%)\n0. Back")
        
        choice = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if choice == "0": break
        elif choice == "1":
            path = (await asyncio.to_thread(input, "Path to mp3:\n> ")).strip('"\' ')
            if not os.path.exists(path): print(colorize("[ERROR] No file", "red")); await pause(); continue
            try:
                player = pyglet.media.Player(); source = await asyncio.to_thread(pyglet.media.load, path); player.queue(source); player.play()
                print(colorize("[MUSIC STARTED!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            if player.playing: player.pause(); print(colorize("[PAUSED]", "green"))
            else: player.play(); print(colorize("[RESUMED]", "green"))
            await pause()
        elif choice == "3":
            player.pause(); player.seek(0); print(colorize("[STOPPED]", "green")); await pause()
        elif choice == "4":
            player.volume = min(1.0, player.volume + 0.1); print(colorize(f"[VOLUME: {int(player.volume*100)}%]", "green")); await pause()
        elif choice == "5":
            player.volume = max(0.0, player.volume - 0.1); print(colorize(f"[VOLUME: {int(player.volume*100)}%]", "green")); await pause()

# ==========================================
# SECTION 10: THEME
# ==========================================
async def menu_theme():
    global CURRENT_THEME
    while True:
        clear_screen()
        print(colorize("=== 10. THEME SETTINGS ===", "cyan"))
        print("1. 🔴 Red\n2. 🟢 Green\n3. 🔵 Blue\n4. 🟡 Yellow")
        print("5. 🟣 Purple\n6. 🔷 Cyan\n7. 🌈 RAINBOW\n0. Back")
        
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
# MAIN MENU
# ==========================================
async def main():
    clear_screen()
    print(colorize("Starting...", "yellow")); await bot.delete_webhook()
    try:
        me = await bot.get_me(); print(colorize(f"[BOT @{me.username} IS ONLINE!]", "green")); await asyncio.sleep(1)
    except Exception as e: print(colorize(f"[ERROR] {e}", "red")); return

    while True:
        clear_screen()
        print(colorize("╔════════════════════════════════════════════════╗", "cyan"))
        print(colorize("║          🤖 BRO-PANEL BOT V11 🤖             ║", "cyan"))
        print(colorize("╠════════════════════════════════════════════════╣", "cyan"))
        print(colorize("║ 1. 📝 TEXT           │ 6. ⚙️ BOT SETTINGS     ║", "cyan"))
        print(colorize("║ 2. 📁 MEDIA          │ 7. ℹ️ INFO & PING       ║", "cyan"))
        print(colorize("║ 3. 💣 SPAM ZONE      │ 8. 📖 GUIDE (HELP)     ║", "cyan"))
        print(colorize("║ 4. 🎲 TRICKS         │ 9. 🎵 MUSIC            ║", "cyan"))
        print(colorize("║ 5. 👑 ADMIN PANEL    │ 10. 🎨 THEME SETTINGS  ║", "cyan"))
        print(colorize("╠════════════════════════════════════════════════╣", "cyan"))
        print(colorize("║ 0. 🚪 EXIT                                     ║", "cyan"))
        print(colorize("╚════════════════════════════════════════════════╝", "cyan"))
        
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

    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
