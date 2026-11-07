import asyncio
import os
import time
import random
import base64

# Trying to import pyglet for music
try:
    import pyglet
    pyglet.options['shadow_window'] = False # Prevent extra window from opening
    player = pyglet.media.Player()
    AUDIO_OK = True
except ImportError:
    print("[WARNING] Pyglet is not installed. Run: pip install pyglet")
    AUDIO_OK = False

from aiogram import Bot
from aiogram.types import FSInputFile, ChatPermissions, BotCommand
from aiogram.enums import ChatAction
import config

bot = Bot(token=config.BOT_TOKEN)

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
    return asyncio.to_thread(input, "\n[BRO, DONE!] Press Enter to continue...")

# ==========================================
# SECTION 1: TEXT
# ==========================================
async def menu_text():
    while True:
        clear_screen()
        print("=== 1. BRO, HERE IS THE TEXT ===")
        print("1. Send regular text")
        print("2. Send beautiful text (HTML: <b>bold</b>)")
        print("3. 'Bot is typing...' effect")
        print("4. Reverse text")
        print("5. CAPS (SCREAMING)")
        print("6. Meme text (AlTeRnAtInG)")
        print("7. Base64 Encryption (secret)")
        print("8. SECRET TEXT (Spoiler, hidden under black)")
        print("0. Back to main")
        
        choice = await asyncio.to_thread(input, "\nWhat do you choose, bro? ")
        if choice == "0": break
        elif choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            text = await asyncio.to_thread(input, "Enter text, bro:\n> ")
            
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
                print("[BRO, SENT!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()

# ==========================================
# SECTION 2: MEDIA
# ==========================================
async def menu_media():
    while True:
        clear_screen()
        print("=== 2. BRO, HERE IS MEDIA ===")
        print("1. Send file (auto-detect)")
        print("2. Send location (point on map)")
        print("3. Send fake contact")
        print("4. Send sticker")
        print("5. Send video note (round video)")
        print("0. Back to main")
        
        choice = await asyncio.to_thread(input, "\nWhat do you choose, bro? ")
        if choice == "0": break
        
        elif choice == "1":
            path_input = await asyncio.to_thread(input, "Path to file (drag here):\n> ")
            path = path_input.strip('"\' ')
            if not os.path.exists(path): print("[ERROR] No such file, bro."); await pause(); continue
            caption = await asyncio.to_thread(input, "Caption (Enter - skip):\n> ")
            try: await smart_send_file(config.CHAT_ID, path, caption); print("[BRO, SENT!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()

        elif choice == "2":
            lat = await asyncio.to_thread(input, "Latitude (55.7558):\n> ")
            lon = await asyncio.to_thread(input, "Longitude (37.6173):\n> ")
            try: await bot.send_location(config.CHAT_ID, latitude=float(lat), longitude=float(lon)); print("[BRO, LOCATION SENT!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()

        elif choice == "3":
            phone = await asyncio.to_thread(input, "Phone (+7999...):\n> ")
            name = await asyncio.to_thread(input, "Name:\n> ")
            try: await bot.send_contact(config.CHAT_ID, phone_number=phone, first_name=name); print("[BRO, CONTACT SENT!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()

        elif choice == "4":
            path_input = await asyncio.to_thread(input, "Path to sticker (.webp):\n> ")
            path = path_input.strip('"\' ')
            try: await bot.send_sticker(config.CHAT_ID, sticker=FSInputFile(path)); print("[BRO, STICKER SENT!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()

        elif choice == "5":
            path_input = await asyncio.to_thread(input, "Path to video for note (.mp4):\n> ")
            path = path_input.strip('"\' ')
            try: await bot.send_video_note(config.CHAT_ID, video_note=FSInputFile(path)); print("[BRO, VIDEO NOTE SENT!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()

# ==========================================
# SECTION 3: SPAM ZONE
# ==========================================
async def menu_spam():
    while True:
        clear_screen()
        print("=== 3. BRO, HERE IS SPAM (CAREFUL!) ===")
        print("1. Text spam (controlled)")
        print("2. Spam file/image")
        print("3. SMART SPAM (TG doesn't ban as fast)")
        print("4. STONE SPAM (🗿) - hardcore")
        print("5. INFINITE SPAM (Stop: Ctrl+C in console)")
        print("0. Back to main")
        
        choice = await asyncio.to_thread(input, "\nWhat do you choose, bro? ")
        if choice == "0": break
        
        elif choice in ["1", "2", "3", "4", "5"]:
            if choice == "1": text = await asyncio.to_thread(input, "Text for spam:\n> "); path=None
            elif choice == "2": 
                path_input = await asyncio.to_thread(input, "Path to file:\n> ")
                path = path_input.strip('"\' '); 
                text=None
            elif choice == "4": text = "🗿" * 50; path=None
            elif choice == "5": text = await asyncio.to_thread(input, "Text for INFINITE spam:\n> "); path=None
            else: text = await asyncio.to_thread(input, "Text for smart spam:\n> "); path=None

            if path and not os.path.exists(path): print("[ERROR] No file, bro."); await pause(); continue
            
            try:
                if choice == "5":
                    count = 999999
                    delay = "random"
                    print("\n[WARNING] Infinite spam enabled! To stop, press Ctrl+C in this window.")
                else:
                    count = int(await asyncio.to_thread(input, "How many times? "))
                    if choice in ["3", "4"]: delay = "random"
                    else:
                        delay_input = await asyncio.to_thread(input, f"Delay (Enter for {config.DEFAULT_SPAM_DELAY} sec): ")
                        delay = float(delay_input) if delay_input.strip() else config.DEFAULT_SPAM_DELAY
            except ValueError: continue

            print(f"\nLet's spam...")
            for i in range(count):
                try:
                    if path: await smart_send_file(config.CHAT_ID, path)
                    else: await bot.send_message(config.CHAT_ID, text)
                    print(f"[{i+1}/{count if count < 999999 else '∞'}] sent, bro!")
                    
                    if delay == "random": await asyncio.sleep(random.uniform(1.5, 3.5))
                    else: await asyncio.sleep(delay)
                except Exception as e: 
                    print(f"[TG BAN] {e}"); 
                    break
            await pause()

# ==========================================
# SECTION 4: TRICKS
# ==========================================
async def menu_features():
    while True:
        clear_screen()
        print("=== 4. BRO, HERE ARE TRICKS ===")
        print("1. Create poll")
        print("2. Pin message")
        print("3. Roll DICE")
        print("4. Throw DARTS")
        print("5. Play BASKETBALL")
        print("6. Spin ROULETTE (casino)")
        print("7. Kick FOOTBALL")
        print("8. Random number (1-100)")
        print("0. Back to main")
        
        choice = await asyncio.to_thread(input, "\nWhat do you choose, bro? ")
        if choice == "0": break
        
        elif choice == "1":
            q = await asyncio.to_thread(input, "Poll question:\n> ")
            o1 = await asyncio.to_thread(input, "Option 1:\n> ")
            o2 = await asyncio.to_thread(input, "Option 2:\n> ")
            try: await bot.send_poll(chat_id=config.CHAT_ID, question=q, options=[o1, o2]); print("[BRO, POLL CREATED!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()
        elif choice == "2":
            msg = await bot.send_message(config.CHAT_ID, "Pinned, bro!")
            await bot.pin_chat_message(chat_id=config.CHAT_ID, message_id=msg.message_id); print("[BRO, PINNED!]"); await pause()
        elif choice in ["3", "4", "5", "6", "7"]:
            emoji = "🎲"
            if choice == "4": emoji = "🎯"
            elif choice == "5": emoji = "🏀"
            elif choice == "6": emoji = "🎰"
            elif choice == "7": emoji = "⚽"
            try: await bot.send_dice(chat_id=config.CHAT_ID, emoji=emoji); print("[BRO, GAME STARTED!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()
        elif choice == "8":
            num = random.randint(1, 100)
            try: await bot.send_message(config.CHAT_ID, f"Bro, rolled number: {num}"); print("[BRO, NUMBER SENT!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()

# ==========================================
# SECTION 5: ADMIN PANEL
# ==========================================
async def menu_admin():
    while True:
        clear_screen()
        print("=== 5. BRO, HERE IS ADMIN PANEL ===")
        print("1. Mute EVERYONE (like silence)")
        print("2. Unmute EVERYONE (let them write)")
        print("3. Change group TITLE")
        print("4. Change group DESCRIPTION")
        print("5. BAN by ID (numbers)")
        print("6. BAN by @username (nick)")
        print("7. KICK by ID (numbers)")
        print("8. KICK by @username (nick)")
        print("9. DELETE message (by message ID)")
        print("0. Back to main")
        
        choice = await asyncio.to_thread(input, "\nWhat do you choose, bro? ")
        if choice == "0": break
        
        elif choice == "1":
            try: await bot.set_chat_permissions(chat_id=config.CHAT_ID, permissions=ChatPermissions(can_send_messages=False)); print("[BRO, EVERYONE MUTED!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()
        elif choice == "2":
            try: await bot.set_chat_permissions(chat_id=config.CHAT_ID, permissions=ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)); print("[BRO, EVERYONE UNMUTED!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()
        elif choice == "3":
            t = await asyncio.to_thread(input, "New group title:\n> ")
            try: await bot.set_chat_title(chat_id=config.CHAT_ID, title=t); print("[BRO, RENAMED!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()
        elif choice == "4":
            d = await asyncio.to_thread(input, "New group description:\n> ")
            try: await bot.set_chat_description(chat_id=config.CHAT_ID, description=d); print("[BRO, DESCRIPTION CHANGED!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()
            
        elif choice in ["5", "6", "7", "8"]:
            if choice in ["5", "7"]:
                target = await asyncio.to_thread(input, "Enter user numeric ID:\n> ")
                try: user_id = int(target)
                except ValueError: print("[ERROR] This is not an ID, bro. Need numbers."); await pause(); continue
            else:
                target_input = await asyncio.to_thread(input, "Enter @username (starting with @):\n> ")
                target = target_input.strip()
                user_id = target

            try:
                if choice in ["5", "6"]: # BAN
                    await bot.ban_chat_member(chat_id=config.CHAT_ID, user_id=user_id)
                    print(f"[BRO, USER {target} IS BANNED!]")
                else: # KICK
                    await bot.ban_chat_member(chat_id=config.CHAT_ID, user_id=user_id)
                    await bot.unban_chat_member(chat_id=config.CHAT_ID, user_id=user_id)
                    print(f"[BRO, USER {target} IS KICKED!]")
            except Exception as e:
                print(f"[ERROR] Failed. Maybe no user or bot is not admin. ({e})")
            await pause()
            
        elif choice == "9":
            msg_id = await asyncio.to_thread(input, "Enter message ID:\n> ")
            try: await bot.delete_message(chat_id=config.CHAT_ID, message_id=int(msg_id)); print("[BRO, MESSAGE DELETED!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()

# ==========================================
# SECTION 6: BOT SETTINGS
# ==========================================
async def menu_bot_settings():
    while True:
        clear_screen()
        print("=== 6. BRO, BOT SETTINGS ===")
        print("1. Set bot commands (Menu / )")
        print("2. Change bot description")
        print("0. Back to main")
        
        choice = await asyncio.to_thread(input, "\nWhat do you choose, bro? ")
        if choice == "0": break
        elif choice == "1":
            print("\n[INFO] Setting commands: /start, /help, /spam")
            try:
                commands = [
                    BotCommand(command="start", description="Start the bot"),
                    BotCommand(command="help", description="Help"),
                    BotCommand(command="spam", description="Start spamming")
                ]
                await bot.set_my_commands(commands)
                print("[BRO, COMMANDS SET!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()
        elif choice == "2":
            d = await asyncio.to_thread(input, "New bot description:\n> ")
            try: await bot.set_my_description(description=d); print("[BRO, BOT DESCRIPTION CHANGED!]")
            except Exception as e: print(f"[ERROR] {e}")
            await pause()

# ==========================================
# SECTION 7: INFO
# ==========================================
async def menu_settings():
    while True:
        clear_screen()
        print("=== 7. BRO, HERE IS INFO ===")
        print("1. Bot profile")
        print("2. Ping to TG servers")
        print("3. Chat info")
        print("4. How many people in chat?")
        print("0. Back to main")
        
        choice = await asyncio.to_thread(input, "\nWhat do you choose, bro? ")
        if choice == "0": break
        elif choice == "1":
            me = await bot.get_me(); print(f"\nName: {me.first_name}\nUsername: @{me.username}\nID: {me.id}"); await pause()
        elif choice == "2":
            start = time.time(); await bot.get_me(); print(f"\nPing: {round((time.time() - start) * 1000, 2)} ms. All good."); await pause()
        elif choice == "3":
            try:
                chat = await bot.get_chat(config.CHAT_ID)
                print(f"\nTitle: {chat.title}\nID: {chat.id}\nType: {chat.type}")
            except Exception as e: print(f"\n[ERROR] {e}")
            await pause()
        elif choice == "4":
            try: print(f"\nPeople in chat: {await bot.get_chat_member_count(config.CHAT_ID)}")
            except Exception as e: print(f"\n[ERROR] {e}")
            await pause()

# ==========================================
# SECTION 8: GUIDE (HELP)
# ==========================================
async def menu_help():
    while True:
        clear_screen()
        print("=== 8. BRO, HERE IS THE GUIDE (WHAT IT ALL MEANS) ===")
        print("1. About TEXT section")
        print("2. About MEDIA section")
        print("3. About SPAM section")
        print("4. About TRICKS section")
        print("5. About ADMIN section")
        print("6. About BOT SETTINGS section")
        print("7. About INFO section")
        print("8. About MUSIC section")
        print("0. Back to main")
        
        choice = await asyncio.to_thread(input, "\nWhich section to explain, bro? ")
        
        clear_screen()
        if choice == "1":
            print("--- GUIDE: TEXT ---")
            print("Here you just send text to the chat.")
            print("• HTML: Makes text bold (<b>), italic (<i>), etc.")
            print("• 'Typing' effect: Bot shows 'typing...' for 1.5 sec, then sends text.")
            print("• Reverse: Writes text backwards (Hello -> olleH).")
            print("• Base64: Encrypts text into unreadable letters (for secrets).")
            print("• Secret text: Text is hidden under a black spoiler until clicked.")
            await pause()
        elif choice == "2":
            print("--- GUIDE: MEDIA ---")
            print("Here you send files. Bot AUTOMATICALLY detects what you sent.")
            print("• Video note: Sends video as a round message.")
            print("• Location: Sends a point on the map by coordinates.")
            print("• Contact: Sends a fake phone number with a name.")
            await pause()
        elif choice == "3":
            print("--- GUIDE: SPAM ZONE ---")
            print("Here the bot spams.")
            print("• Regular: Sends with the delay you specify.")
            print("• SMART SPAM: Bot sets a random delay from 1.5 to 3.5 sec. Telegram likes this more.")
            print("• INFINITE: Bot will spam until you press Ctrl+C in the window.")
            print("• STONE SPAM: Sends 50 🗿 emojis in one message.")
            await pause()
        elif choice == "4":
            print("--- GUIDE: TRICKS ---")
            print("Here are the entertainments.")
            print("• Poll: Creates a voting poll in chat.")
            print("• Games (Dice, Darts, Roulette): Sends animated TG emojis.")
            print("• Pin: Bot writes a message and pins it to the top.")
            await pause()
        elif choice == "5":
            print("--- GUIDE: ADMIN ---")
            print("IMPORTANT: Bot must be an admin in the group!")
            print("• Mute: Forbids everyone to write.")
            print("• Ban: Kicks a person out forever.")
            print("• Kick: Kicks out, but person can return.")
            print("• ID: It's numbers. User: It's @nickname.")
            print("• Delete: Deletes a message by its internal ID.")
            await pause()
        elif choice == "6":
            print("--- GUIDE: BOT SETTINGS ---")
            print("• Commands: Adds a blue 'Menu' button to the chat.")
            print("• Description: Changes the text people see when they first start the bot.")
            await pause()
        elif choice == "7":
            print("--- GUIDE: INFO ---")
            print("Just shows data: bot name, ping, number of people in the group.")
            await pause()
        elif choice == "8":
            print("--- GUIDE: MUSIC ---")
            print("This section plays music DIRECTLY ON YOUR COMPUTER (via pyglet).")
            print("• Play: Specify the path to the mp3 file.")
            print("• Pause/Resume: Pauses the track or resumes it.")
            print("• Volume: Change from 0.0 to 1.0 (e.g., 0.5 is 50%).")
            await pause()
        elif choice == "0":
            break
        else:
            print("No such option, bro.")
            await asyncio.sleep(1)

# ==========================================
# SECTION 9: MUSIC (LOCAL PLAYER)
# ==========================================
async def menu_music():
    global player 
    
    if not AUDIO_OK:
        print("\n[ERROR] Pyglet is not installed. Run: pip install pyglet")
        await pause()
        return

    while True:
        clear_screen()
        print("=== 9. BRO, HERE IS MUSIC (PLAYER) ===")
        
        if player.playing:
            print("[STATUS] Music is playing right now...")
        else:
            print("[STATUS] Silence or pause.")

        print("1. Play track (file path)")
        print("2. Pause / Resume")
        print("3. Stop music")
        print("4. Volume UP (+10%)")
        print("5. Volume DOWN (-10%)")
        print("0. Back to main")
        
        choice = await asyncio.to_thread(input, "\nWhat do you choose, bro? ")
        if choice == "0": break
        
        elif choice == "1":
            path_input = await asyncio.to_thread(input, "Path to mp3 file:\n> ")
            path = path_input.strip('"\' ')
            if not os.path.exists(path):
                print("[ERROR] No such file, bro."); await pause(); continue
            
            try:
                print("[...] Loading track...")
                player = pyglet.media.Player()
                source = await asyncio.to_thread(pyglet.media.load, path)
                player.queue(source)
                player.play()
                print("[BRO, MUSIC STARTED!]")
            except Exception as e:
                print(f"[ERROR] {e}")
            await pause()

        elif choice == "2":
            if player.playing:
                player.pause()
                print("[BRO, PAUSED!]")
            else:
                player.play()
                print("[BRO, RESUMED!]")
            await pause()

        elif choice == "3":
            player.pause()
            player.seek(0) 
            print("[BRO, MUSIC STOPPED!]")
            await pause()

        elif choice == "4":
            vol = player.volume
            new_vol = min(1.0, vol + 0.1)
            player.volume = new_vol
            print(f"[BRO, VOLUME: {int(new_vol*100)}%]")
            await pause()

        elif choice == "5":
            vol = player.volume
            new_vol = max(0.0, vol - 0.1)
            player.volume = new_vol
            print(f"[BRO, VOLUME: {int(new_vol*100)}%]")
            await pause()

# ==========================================
# MAIN MENU
# ==========================================
async def main():
    clear_screen()
    print("Starting... Connecting...")
    await bot.delete_webhook()
    
    try:
        me = await bot.get_me()
        print(f"[BRO, BOT @{me.username} IS ONLINE!]")
        await asyncio.sleep(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    while True:
        clear_screen()
        print("=" * 50)
        print("       BRO, YOU ARE IN THE CONTROL PANEL")
        print("=" * 50)
        print("1. TEXT (regular, meme, secret)")
        print("2. MEDIA (files, stickers, video notes)")
        print("3. SPAM ZONE (text, files, infinite)")
        print("4. TRICKS (polls, dice, roulette)")
        print("5. ADMIN PANEL (mute, ban by ID/@user)")
        print("6. BOT SETTINGS (commands)")
        print("7. INFO AND PING")
        print("8. GUIDE (What does it all mean?)")
        print("9. MUSIC (Player right in console)")
        print("0. EXIT")
        print("=" * 50)
        
        choice = await asyncio.to_thread(input, "Choose section (0-9): ")

        if choice == "0":
            print("Exiting... See ya, bro!")
            if AUDIO_OK:
                player.pause() 
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

    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())