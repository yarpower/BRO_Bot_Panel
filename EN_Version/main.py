import asyncio
import os
import time
import random
import base64
import shutil
import ctypes
import platform
import string
import re
import urllib.parse
from datetime import datetime

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
START_TIME = time.time()

# ==========================================
# COLOR ENGINE & UI
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
            sw, sh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            max_cols, max_lines = int(sw / 10), int(sh / 22) 
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

def draw_panel(title, options):
    cols = shutil.get_terminal_size().columns
    width = max(60, cols - 4) 
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
# DATA FOR GENERATOR
# ==========================================
LAST_NAMES = ["Ivanov", "Smirnov", "Kuznetsov", "Popov", "Vasiliev", "Petrov", "Sokolov", "Mikhailov"]
FIRST_NAMES_M = ["Alexander", "Dmitry", "Maxim", "Sergey", "Andrey", "Alexey", "Artem", "Ilya"]
FIRST_NAMES_F = ["Anastasia", "Maria", "Daria", "Anna", "Elizabeth", "Polina", "Victoria", "Ekaterina"]
CITIES = ["Moscow", "St. Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan"]
DOMAINS = ["mail.ru", "yandex.ru", "gmail.com", "bk.ru", "list.ru"]
BANKS = [("Sberbank", "044525225"), ("VTB", "044525187"), ("Alfa-Bank", "044525593"), ("Tinkoff", "044525974")]
CAR_BRANDS = ["Toyota", "BMW", "Audi", "Ford", "Lada", "Kia", "Hyundai", "Mercedes-Benz"]
COMPANIES = ["LLC StroyInvest", "LLC TekhnoProm", "LLC AlfaGroup", "LLC VectorSoft"]

def transliterate(name):
    mapping = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
    return "".join(mapping.get(c, c) for c in name.lower())

def gen_inn():
    inn = [random.randint(0, 9) for _ in range(10)]
    c11 = sum(inn[i] * [7, 2, 4, 10, 3, 5, 9, 4, 6, 8][i] for i in range(10)) % 11 % 10
    inn.append(c11)
    c12 = sum(inn[i] * [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8][i] for i in range(11)) % 11 % 10
    inn.append(c12)
    return "".join(map(str, inn))

def gen_snils():
    snils = [random.randint(0, 9) for _ in range(9)]
    cs = sum(snils[i] * (9 - i) for i in range(9))
    if cs > 101: cs %= 101
    if cs in (100, 101): cs = 0
    s = "".join(map(str, snils))
    return f"{s[:3]}-{s[3:6]}-{s[6:9]} {cs:02d}"

def gen_card():
    prefix = "4"
    digits = [int(c) for c in prefix] + [random.randint(0, 9) for _ in range(14)]
    s = sum(d * (2 if i%2==0 else 1) - 9 if d * (2 if i%2==0 else 1) > 9 else d * (2 if i%2==0 else 1) for i, d in enumerate(reversed(digits)))
    check = (10 - (s % 10)) % 10
    digits.append(check)
    return " ".join(["".join(map(str, digits))[i:i+4] for i in range(0, 16, 4)])

# ==========================================
# SECTIONS 1-5
# ==========================================
async def menu_text():
    while True:
        clear_screen(); draw_panel("1. TEXT", ["1. Regular", "2. HTML", "3. Typing", "4. Reverse", "5. CAPS", "6. Meme", "7. Base64", "8. Spoiler", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c == "0": break
        elif c in ["1","2","3","4","5","6","7","8"]:
            t = await asyncio.to_thread(input, "Text: ")
            if c=="4": t=t[::-1]
            elif c=="5": t=t.upper()
            elif c=="7": t=base64.b64encode(t.encode()).decode()
            elif c=="8": t=f"<tg-spoiler>{t}</tg-spoiler>"
            try:
                mode="HTML" if c in ["2","8"] else None
                if c=="3": await bot.send_chat_action(config.CHAT_ID, ChatAction.TYPING); await asyncio.sleep(1)
                await bot.send_message(config.CHAT_ID, t, parse_mode=mode); print(colorize("[SENT]", "green"))
            except Exception as e: print(colorize(f"[ERR] {e}", "red"))
            await pause()

async def menu_media():
    while True:
        clear_screen(); draw_panel("2. MEDIA", ["1. File", "2. Geo", "3. Contact", "4. Sticker", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c == "0": break
        elif c == "1":
            p = (await asyncio.to_thread(input, "File path: ")).strip('"\' ')
            try: await smart_send_file(config.CHAT_ID, p); print(colorize("[SENT]", "green"))
            except Exception as e: print(colorize(f"[ERR] {e}", "red"))
            await pause()
        elif c=="2":
            try:
                lat_str=await asyncio.to_thread(input,"Lat: "); lon_str=await asyncio.to_thread(input,"Lon: "); await bot.send_location(config.CHAT_ID, float(lat_str), float(lon_str)); print(colorize("[SENT]","green"))
            except ValueError: print(colorize("[ERROR] Need numbers","red"))
            except Exception as e: print(colorize(f"[ERR] {e}","red"))
            await pause()

async def menu_spam():
    while True:
        clear_screen(); draw_panel("3. SPAM", ["1. Text", "2. Smart", "3. Infinite", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c == "0": break
        elif c in ["1","2","3"]:
            t = await asyncio.to_thread(input, "Text: ")
            try:
                cnt = 999999 if c=="3" else int(await asyncio.to_thread(input, "How many? "))
                d = "random" if c=="2" else 1.0
                for i in range(cnt):
                    await bot.send_message(config.CHAT_ID, t)
                    print(colorize(f"[{i+1}] ok", "green"))
                    await asyncio.sleep(random.uniform(1.5,3.5) if d=="random" else d)
            except asyncio.CancelledError: return
            except Exception as e: print(colorize(f"[BAN] {e}", "red"))
            await pause()

async def menu_features():
    while True:
        clear_screen(); draw_panel("4. TRICKS", ["1. Poll", "2. Pin", "3. Dice", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c=="0": break
        elif c=="1": await bot.send_poll(config.CHAT_ID, "Q?", ["A", "B"]); await pause()
        elif c=="2": await bot.send_message(config.CHAT_ID, "Pinned!"); await pause()
        elif c=="3": await bot.send_dice(config.CHAT_ID, emoji="🎲"); await pause()

async def menu_admin():
    while True:
        clear_screen(); draw_panel("5. ADMIN", ["1. Mute", "2. Unmute", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c=="0": break
        elif c=="1": await bot.set_chat_permissions(config.CHAT_ID, ChatPermissions(can_send_messages=False)); await pause()
        elif c=="2": await bot.set_chat_permissions(config.CHAT_ID, ChatPermissions(can_send_messages=True, can_send_media_messages=True)); await pause()

# ==========================================
# SECTIONS 6-10
# ==========================================
async def menu_bot_settings():
    while True:
        clear_screen(); draw_panel("6. SETTINGS", ["1. Commands", "2. Description", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c=="0": break
        elif c=="1": await bot.set_my_commands([BotCommand(command="start", description="Start")]); await pause()
        elif c=="2": d=await asyncio.to_thread(input,"Desc: "); await bot.set_my_description(d); await pause()

async def menu_settings():
    while True:
        clear_screen(); draw_panel("7. INFO", ["1. Profile", "2. Ping", "3. Chat", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c=="0": break
        elif c=="1": me=await bot.get_me(); print(f"Name: {me.first_name}\nUser: @{me.username}"); await pause()
        elif c=="2": st=time.time(); await bot.get_me(); print(f"Ping: {round((time.time()-st)*1000, 2)} ms"); await pause()
        elif c=="3": ch=await bot.get_chat(config.CHAT_ID); print(f"Title: {ch.title}\nID: {ch.id}"); await pause()

async def menu_help():
    while True:
        clear_screen(); draw_panel("8. GUIDE", ["1. Text", "2. Spam", "3. OSINT", "4. Fakes", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c=="0": break
        clear_screen()
        if c=="1": print("TEXT: Encryption, effects, spoilers."); await pause()
        elif c=="2": print("SPAM: Smart and Infinite."); await pause()
        elif c=="3": print("OSINT: Links for manual search."); await pause()
        elif c=="4": print("FAKES: Data generation."); await pause()

async def menu_music():
    global player
    if not AUDIO_OK: print("Pyglet not installed!"); await pause(); return
    while True:
        clear_screen(); draw_panel("9. MUSIC", ["1. Play", "2. Pause", "3. Stop", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c=="0": break
        elif c=="1":
            p = await asyncio.to_thread(input, "MP3 path: ")
            try: player = pyglet.media.Player(); s = await asyncio.to_thread(pyglet.media.load, p, streaming=True); player.queue(s); player.play(); print("[PLAYING]")
            except Exception as e: print(e)
            await pause()
        elif c=="2": player.pause(); await pause()
        elif c=="3": player.pause(); player.seek(0); await pause()

async def menu_theme():
    global CURRENT_THEME
    while True:
        clear_screen(); draw_panel("10. THEME", ["1. Red", "2. Green", "3. Blue", "4. RAINBOW", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c=="0": break
        elif c=="1": CURRENT_THEME="red"
        elif c=="2": CURRENT_THEME="green"
        elif c=="3": CURRENT_THEME="blue"
        elif c=="4": CURRENT_THEME="rainbow"
        print(colorize("[THEME CHANGED]", "green")); await pause()

# ==========================================
# SECTIONS 11-15
# ==========================================
async def menu_utils():
    while True:
        clear_screen(); draw_panel("11. UTILS", ["1. Base64", "2. Password", "3. Calc", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c=="0": break
        elif c=="1": 
            txt=await asyncio.to_thread(input,"Base64: ")
            try: print(base64.b64decode(txt).decode())
            except: print(colorize("[ERROR] Invalid code", "red"))
            await pause()
        elif c=="2": 
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            print(colorize("".join(random.choice(chars) for _ in range(16)), "green")); await pause()
        elif c=="3": 
            ex=await asyncio.to_thread(input,"Expr: ")
            try: print(colorize(f"Result: {eval(ex, {'__builtins__': None})}", "green"))
            except: print(colorize("[ERROR] Invalid expr", "red"))
            await pause()

async def send_delayed(chat_id, text, delay):
    await asyncio.sleep(delay)
    try: await bot.send_message(chat_id, f"⏰ [DELAYED]:\n{text}")
    except: pass

async def menu_timer():
    while True:
        clear_screen(); draw_panel("12. TIMER", ["1. Create", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c=="0": break
        elif c=="1":
            t=await asyncio.to_thread(input,"Text: "); 
            try:
                d=int(await asyncio.to_thread(input,"Sec: "))
                asyncio.create_task(send_delayed(config.CHAT_ID, t, d)); print(colorize("[SET]", "green"))
            except: print(colorize("[ERROR] Need numbers", "red"))
            await pause()

async def menu_special():
    while True:
        clear_screen(); draw_panel("13. SPECIAL", ["1. Coin", "2. RPS", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c=="0": break
        elif c=="1": await bot.send_message(config.CHAT_ID, f"Coin: {random.choice(['Heads', 'Tails'])}"); await pause()
        elif c=="2": await bot.send_message(config.CHAT_ID, f"RPS: {random.choice(['Rock', 'Paper', 'Scissors'])}"); await pause()

async def menu_userinfo():
    while True:
        clear_screen(); draw_panel("14. USER", ["1. Find", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c=="0": break
        elif c=="1":
            t=await asyncio.to_thread(input,"ID or @: ")
            try: 
                if t.startswith('@'): u = await bot.get_chat(t)
                else: u = await bot.get_chat(int(t))
                print(f"Name: {u.first_name}\nID: {u.id}")
            except Exception as e: print(colorize(f"Error: {e}", "red"))
            await pause()

async def menu_system():
    while True:
        clear_screen(); draw_panel("15. SYSTEM", ["1. Uptime", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c=="0": break
        elif c=="1": up=int(time.time()-START_TIME); print(f"Uptime: {up//3600}h\nOS: {platform.system()}"); await pause()

# ==========================================
# SECTION 16: FAKE GENERATOR
# ==========================================
async def menu_fake_gen():
    while True:
        clear_screen(); draw_panel("16. FAKE GEN", ["1. Person", "2. Card", "3. Auto", "4. Company", "5. Crypto", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c == "0": break
        try:
            if c == "1":
                g = random.choice(["M", "F"])
                f = random.choice(FIRST_NAMES_M if g=="M" else FIRST_NAMES_F)
                l = random.choice(LAST_NAMES) + ("a" if g=="F" else "")
                txt = f"👤 <b>IDENTITY</b>\nName: {f} {l}\nCity: {random.choice(CITIES)}\nINN: <code>{gen_inn()}</code>\nSNILS: <code>{gen_snils()}</code>"
            elif c == "2":
                b = random.choice(BANKS)
                txt = f"💳 <b>CARD</b>\nBank: {b[0]}\nNum: <code>{gen_card()}</code>\nCVV: <code>{random.randint(100,999)}</code>"
            elif c == "3":
                txt = f"🚗 <b>AUTO</b>\nBrand: {random.choice(CAR_BRANDS)}\nVIN: <code>{''.join(random.choice('ABCDEFGHJKLMNPRSTUVWXYZ0123456789') for _ in range(17))}</code>"
            elif c == "4":
                txt = f"🏢 <b>COMPANY</b>\nName: {random.choice(COMPANIES)}\nOGRN: <code>{random.randint(1000000000000, 9999999999999)}</code>"
            elif c == "5":
                txt = f"🪙 <b>CRYPTO</b>\nBTC: <code>bc1q{''.join(random.choice('acdefghjklmnpqrstuvwxyz023456789') for _ in range(38))}</code>"
            else: continue
            
            await bot.send_message(config.CHAT_ID, txt, parse_mode="HTML")
            print(colorize("[SENT TO CHAT]", "green"))
        except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
        await pause()

# ==========================================
# SECTION 17: OSINT
# ==========================================
async def menu_osint():
    while True:
        clear_screen(); draw_panel("17. OSINT", ["1. Phone", "2. Email", "3. Nick", "4. Name", "0. Back"])
        c = await asyncio.to_thread(input, colorize("\nChoice: ", "green"))
        if c == "0": break
        
        target = await asyncio.to_thread(input, colorize("Enter target: ", "green"))
        if not target: continue
        
        try:
            if c == "1":
                t = re.sub(r'[^\d+]', '', target)
                txt = f"📱 <b>OSINT: {t}</b>\n\n🔍 <b>Links:</b>\n• <a href='https://www.google.com/search?q={t}'>Google</a>\n• <a href='https://vk.com/search?c[section]=people&c[q]={t}'>VK</a>"
            elif c == "2":
                user = target.split('@')[0]
                txt = f"📧 <b>OSINT: {target}</b>\n\n🔍 <b>Links:</b>\n• <a href='https://vk.com/{user}'>VK</a>\n• <a href='https://github.com/{user}'>GitHub</a>"
            elif c == "3":
                txt = f"🕵️ <b>OSINT: {target}</b>\n\n🔍 <b>Links:</b>\n• <a href='https://vk.com/{target}'>VK</a>\n• <a href='https://t.me/{target}'>Telegram</a>"
            elif c == "4":
                q = urllib.parse.quote(target)
                txt = f"👤 <b>OSINT: {target}</b>\n\n🔍 <b>Links:</b>\n• <a href='https://www.google.com/search?q={q}'>Google</a>\n• <a href='https://yandex.ru/search/?text={q}'>Yandex</a>"
            else: continue
            
            await bot.send_message(config.CHAT_ID, txt, parse_mode="HTML", disable_web_page_preview=True)
            print(colorize("[REPORT SENT]", "green"))
        except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
        await pause()

# ==========================================
# MAIN MENU (ALL 17 SECTIONS)
# ==========================================
async def main():
    ask_window_size()
    clear_screen(); print(colorize("Starting...", "yellow")); await bot.delete_webhook()
    try:
        me = await bot.get_me(); print(colorize(f"[BOT @{me.username} IS ONLINE!]", "green")); await asyncio.sleep(1)
    except Exception as e: print(colorize(f"[ERROR] {e}", "red")); return

    while True:
        try:
            clear_screen()
            draw_panel("BRO-PANEL BOT V17.1", [
                "1. TEXT", "10. THEME",
                "2. MEDIA", "11. UTILITIES",
                "3. SPAM ZONE", "12. TIMER",
                "4. TRICKS", "13. SPECIAL OPS",
                "5. ADMIN PANEL", "14. USER INFO",
                "6. BOT SETTINGS", "15. SYSTEM",
                "7. INFO & PING", "16. FAKE GENERATOR",
                "8. GUIDE", "17. OSINT CHECK",
                "9. MUSIC", "0. EXIT"
            ])
            
            choice = await asyncio.to_thread(input, colorize("\nChoose section (0-17): ", "green"))

            if choice == "0": print(colorize("Exiting...", "yellow")); break
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
            elif choice == "11": await menu_utils()
            elif choice == "12": await menu_timer()
            elif choice == "13": await menu_special()
            elif choice == "14": await menu_userinfo()
            elif choice == "15": await menu_system()
            elif choice == "16": await menu_fake_gen()
            elif choice == "17": await menu_osint()

        except (KeyboardInterrupt, asyncio.CancelledError):
            print(colorize("\n\n[BRO] Exiting...", "red"))
            if AUDIO_OK: player.pause()
            break
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
