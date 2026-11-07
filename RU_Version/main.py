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
import uuid
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
# ЦВЕТА И ИНТЕРФЕЙС
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
    print("║             ВЫБЕРИ РАЗМЕР ОКНА ПАНЕЛИ            ║")
    print("╠══════════════════════════════════════════════════╣")
    print("║  1. 25% (Маленькое)                              ║")
    print("║  2. 50% (Среднее)                                ║")
    print("║  3. 65% (Нормальное)                             ║")
    print("║  4. 85% (Большое)                                ║")
    print("║  5. 100% (На весь экран)                         ║")
    print("╚══════════════════════════════════════════════════╝")
    
    while True:
        choice = input("\nТвой выбор (1-5): ")
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
            else: print("Неверный выбор, бро. Нажми 1-5.")
        except Exception as e:
            print(f"Не удалось изменить размер: {e}")
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
    print(colorize("\n[БРО, ГОТОВО!] Жми Enter, чтобы продолжить...", "yellow"))
    return asyncio.to_thread(input)

# ==========================================
# БАЗЫ ДЛЯ ГЕНЕРАТОРА
# ==========================================
LAST_NAMES = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев", "Петров", "Соколов", "Михайлов"]
FIRST_NAMES_M = ["Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей", "Артём", "Илья"]
FIRST_NAMES_F = ["Анастасия", "Мария", "Дарья", "Анна", "Елизавета", "Полина", "Виктория", "Екатерина"]
CITIES = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань", "Нижний Новгород"]
DOMAINS = ["mail.ru", "yandex.ru", "gmail.com", "bk.ru", "list.ru"]
BANKS = [("Сбербанк", "044525225"), ("ВТБ", "044525187"), ("Альфа-Банк", "044525593"), ("Тинькофф", "044525974")]
CAR_BRANDS = ["Toyota", "BMW", "Audi", "Ford", "Lada", "Kia", "Hyundai", "Mercedes-Benz"]
COMPANIES = ["ООО СтройИнвест", "ООО ТехноПром", "ООО АльфаГрупп", "ООО ВекторСофт", "ООО ГлобалМедиа"]

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
# РАЗДЕЛ 1-8 (СТАРЫЕ)
# ==========================================
async def menu_text():
    while True:
        clear_screen(); draw_panel("1. ТЕКСТ", ["1. Обычный", "2. HTML", "3. 'Печатает'", "4. Перевертыш", "5. КАПС", "6. Мемный", "7. Base64", "8. Спойлер", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c == "0": break
        elif c in ["1","2","3","4","5","6","7","8"]:
            t = await asyncio.to_thread(input, "Текст: ")
            if c=="4": t=t[::-1]
            elif c=="5": t=t.upper()
            elif c=="6": t=''.join(ch.upper() if i%2==0 else ch.lower() for i,ch in enumerate(t))
            elif c=="7": t=base64.b64encode(t.encode()).decode()
            elif c=="8": t=f"<tg-spoiler>{t}</tg-spoiler>"
            try:
                mode="HTML" if c in ["2","8"] else None
                if c=="3": await bot.send_chat_action(config.CHAT_ID, ChatAction.TYPING); await asyncio.sleep(1.5)
                await bot.send_message(config.CHAT_ID, t, parse_mode=mode); print(colorize("[ОТПРАВЛЕНО]", "green"))
            except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red"))
            await pause()

async def menu_media():
    while True:
        clear_screen(); draw_panel("2. МЕДИА", ["1. Файл", "2. Гео", "3. Контакт", "4. Стикер", "5. Кружок", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c == "0": break
        elif c == "1":
            p = (await asyncio.to_thread(input, "Путь к файлу: ")).strip('"\' ')
            cap = await asyncio.to_thread(input, "Подпись: ")
            try: await smart_send_file(config.CHAT_ID, p, cap); print(colorize("[ОТПРАВЛЕНО]", "green"))
            except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red"))
            await pause()
        elif c=="2":
            try: lat_str=await asyncio.to_thread(input,"Широта: "); lon_str=await asyncio.to_thread(input,"Долгота: "); await bot.send_location(config.CHAT_ID, float(lat_str), float(lon_str)); print(colorize("[ОТПРАВЛЕНО]","green"))
            except ValueError: print(colorize("[ОШИБКА] Введи числа!","red"))
            except Exception as e: print(colorize(f"[ОШИБКА] {e}","red"))
            await pause()

async def menu_spam():
    while True:
        clear_screen(); draw_panel("3. СПАМ-ЗОНА", ["1. Текст", "2. Умный", "3. Бесконечный", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c == "0": break
        elif c in ["1","2","3"]:
            t = await asyncio.to_thread(input, "Текст: ")
            try:
                cnt = 999999 if c=="3" else int(await asyncio.to_thread(input, "Сколько раз? "))
                d = "random" if c=="2" else 1.0
                for i in range(cnt):
                    await bot.send_message(config.CHAT_ID, t)
                    print(colorize(f"[{i+1}] ок", "green"))
                    await asyncio.sleep(random.uniform(1.5,3.5) if d=="random" else d)
            except asyncio.CancelledError: return
            except Exception as e: print(colorize(f"[БАН] {e}", "red"))
            await pause()

async def menu_features():
    while True:
        clear_screen(); draw_panel("4. ФИШКИ", ["1. Опрос", "2. Закреп", "3. Кубик", "4. Рандом (1-100)", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c=="0": break
        elif c=="1":
            q=await asyncio.to_thread(input,"Вопрос: "); o1=await asyncio.to_thread(input,"Вар1: "); o2=await asyncio.to_thread(input,"Вар2: ")
            await bot.send_poll(config.CHAT_ID, q, [o1,o2]); await pause()
        elif c=="2":
            m = await bot.send_message(config.CHAT_ID, "Закреплено!"); await bot.pin_chat_message(config.CHAT_ID, m.message_id); await pause()
        elif c=="3": await bot.send_dice(config.CHAT_ID, emoji="🎲"); await pause()
        elif c=="4": await bot.send_message(config.CHAT_ID, f"Число: {random.randint(1,100)}"); await pause()

async def menu_admin():
    while True:
        clear_screen(); draw_panel("5. АДМИНКА", ["1. Мут всем", "2. Размут", "3. Сменить название", "4. Бан по ID", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c=="0": break
        elif c=="1": await bot.set_chat_permissions(config.CHAT_ID, ChatPermissions(can_send_messages=False)); await pause()
        elif c=="2": await bot.set_chat_permissions(config.CHAT_ID, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)); await pause()
        elif c=="3":
            t=await asyncio.to_thread(input,"Новое название: "); await bot.set_chat_title(config.CHAT_ID, t); await pause()
        elif c=="4":
            tid=await asyncio.to_thread(input,"ID: ")
            try: await bot.ban_chat_member(config.CHAT_ID, int(tid)); print("[ЗАБАНЕН]")
            except Exception as e: print(e)
            await pause()

async def menu_bot_settings():
    while True:
        clear_screen(); draw_panel("6. НАСТРОЙКИ", ["1. Команды", "2. Описание", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c=="0": break
        elif c=="1": await bot.set_my_commands([BotCommand(command="start", description="Start")]); await pause()
        elif c=="2": d=await asyncio.to_thread(input,"Описание: "); await bot.set_my_description(d); await pause()

async def menu_settings():
    while True:
        clear_screen(); draw_panel("7. ИНФО", ["1. Профиль", "2. Пинг", "3. Инфо чата", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c=="0": break
        elif c=="1": me=await bot.get_me(); print(f"Имя: {me.first_name}\nЮзер: @{me.username}"); await pause()
        elif c=="2": st=time.time(); await bot.get_me(); print(f"Пинг: {round((time.time()-st)*1000, 2)} мс"); await pause()
        elif c=="3": ch=await bot.get_chat(config.CHAT_ID); print(f"Название: {ch.title}\nID: {ch.id}"); await pause()

async def menu_help():
    while True:
        clear_screen(); draw_panel("8. ГАЙД", ["1. Текст", "2. Спам", "3. OSINT", "4. Фейки", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c=="0": break
        clear_screen()
        if c=="1": print("ТЕКСТ: Шифрование, эффекты, спойлеры."); await pause()
        elif c=="2": print("СПАМ: Умный и Бесконечный."); await pause()
        elif c=="3": print("OSINT: Ссылки для ручного поиска."); await pause()
        elif c=="4": print("ФЕЙКИ: Генерация данных (только для тестов!)."); await pause()

# ==========================================
# РАЗДЕЛ 9: МУЗЫКА (РАСШИРЕННЫЙ)
# ==========================================
async def menu_music():
    global player
    if not AUDIO_OK: print(colorize("\n[ОШИБКА] Pyglet не установлен!", "red")); await pause(); return
    while True:
        clear_screen()
        draw_panel("9. МУЗЫКА (ПЛЕЕР)", [
            "1. Включить трек", "2. Пауза / Продолжить", 
            "3. Стоп", "4. Громче (+10%)", 
            "5. Тише (-10%)", "6. Статус", 
            "0. Назад"
        ])
        
        # Показываем статус внизу панели
        try:
            is_playing = player.playing
            vol = int(player.volume * 100)
            print(colorize(f"[СТАТУС] Играет: {'Да' if is_playing else 'Нет'} | Громкость: {vol}%", "green"))
        except: pass
        
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c=="0": break
        elif c=="1":
            p = await asyncio.to_thread(input, "Путь к mp3: ")
            try: 
                player = pyglet.media.Player()
                s = await asyncio.to_thread(pyglet.media.load, p, streaming=True)
                player.queue(s)
                player.play()
                print(colorize("[ИГРАЕТ]", "green"))
            except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red"))
            await pause()
        elif c=="2":
            if player.playing: player.pause(); print(colorize("[ПАУЗА]", "green"))
            else: player.play(); print(colorize("[ПРОДОЛЖАЕМ]", "green"))
            await pause()
        elif c=="3": 
            player.pause(); player.seek(0); print(colorize("[СТОП]", "green")); await pause()
        elif c=="4": 
            player.volume = min(1.0, player.volume + 0.1); print(colorize(f"[ГРОМКОСТЬ: {int(player.volume*100)}%]", "green")); await pause()
        elif c=="5": 
            player.volume = max(0.0, player.volume - 0.1); print(colorize(f"[ГРОМКОСТЬ: {int(player.volume*100)}%]", "green")); await pause()
        elif c=="6":
            print(colorize(f"Играет: {player.playing}\nГромкость: {int(player.volume*100)}%", "yellow")); await pause()

# ==========================================
# РАЗДЕЛ 10-15
# ==========================================
async def menu_theme():
    global CURRENT_THEME
    while True:
        clear_screen(); draw_panel("10. СМЕНА ТЕМЫ", ["1. Красный", "2. Зеленый", "3. Синий", "4. РАДУГА", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c=="0": break
        elif c=="1": CURRENT_THEME="red"
        elif c=="2": CURRENT_THEME="green"
        elif c=="3": CURRENT_THEME="blue"
        elif c=="4": CURRENT_THEME="rainbow"
        print(colorize("[ТЕМА ИЗМЕНЕНА]", "green")); await pause()

async def menu_utils():
    while True:
        clear_screen(); draw_panel("11. УТИЛИТЫ", ["1. Base64 Декодер", "2. Пароль", "3. Калькулятор", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c=="0": break
        elif c=="1":
            txt=await asyncio.to_thread(input,"Base64: ")
            try: print(base64.b64decode(txt).decode())
            except: print(colorize("[ОШИБКА] Неверный код", "red"))
            await pause()
        elif c=="2":
            try: l=int(await asyncio.to_thread(input,"Длина (16): "))
            except: l=16
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            print(colorize("".join(random.choice(chars) for _ in range(l)), "green")); await pause()
        elif c=="3":
            ex=await asyncio.to_thread(input,"Пример (2+2): ")
            try: print(colorize(f"Ответ: {eval(ex, {'__builtins__': None})}", "green"))
            except: print(colorize("[ОШИБКА] Кривой пример", "red"))
            await pause()

async def send_delayed(chat_id, text, delay):
    await asyncio.sleep(delay)
    try: await bot.send_message(chat_id, f"⏰ [ОТЛОЖКА]:\n{text}")
    except: pass

async def menu_timer():
    while True:
        clear_screen(); draw_panel("12. ТАЙМЕР", ["1. Создать", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c=="0": break
        elif c=="1":
            t=await asyncio.to_thread(input,"Текст: ")
            try:
                d=int(await asyncio.to_thread(input,"Секунд: "))
                asyncio.create_task(send_delayed(config.CHAT_ID, t, d)); print(colorize("[ЗАПУЩЕН]", "green"))
            except: print(colorize("[ОШИБКА] Нужны цифры", "red"))
            await pause()

async def menu_special():
    while True:
        clear_screen(); draw_panel("13. СПЕЦ-ОПЕРАЦИИ", ["1. Монетка", "2. КНБ", "3. Спам эмодзи", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c=="0": break
        elif c=="1": await bot.send_message(config.CHAT_ID, f"Монетка: {random.choice(['Орёл', 'Решка'])}"); await pause()
        elif c=="2": await bot.send_message(config.CHAT_ID, f"КНБ: {random.choice(['Камень', 'Ножницы', 'Бумага'])}"); await pause()
        elif c=="3":
            e=await asyncio.to_thread(input,"Эмодзи: ")
            try:
                cnt=int(await asyncio.to_thread(input,"Раз: "))
                for _ in range(cnt): await bot.send_message(config.CHAT_ID, e*50); await asyncio.sleep(1)
            except: pass
            await pause()

async def menu_userinfo():
    while True:
        clear_screen(); draw_panel("14. ЮЗЕР", ["1. Найти", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c=="0": break
        elif c=="1":
            t=await asyncio.to_thread(input,"ID или @юзер: ")
            try:
                if t.startswith('@'): u = await bot.get_chat(t)
                else: u = await bot.get_chat(int(t))
                print(f"Имя: {u.first_name}\nЮзер: @{u.username}\nID: {u.id}")
            except Exception as e: print(colorize(f"Ошибка: {e}", "red"))
            await pause()

async def menu_system():
    while True:
        clear_screen(); draw_panel("15. СИСТЕМА", ["1. Показать Uptime", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c=="0": break
        elif c=="1":
            up = int(time.time() - START_TIME)
            print(f"Аптайм: {up//3600}ч {(up%3600)//60}м {up%60}с\nОС: {platform.system()}\nPython: {platform.python_version()}")
            await pause()

# ==========================================
# РАЗДЕЛ 16: ГЕНЕРАТОР ФЕЙКОВ (РАСШИРЕННЫЙ)
# ==========================================
async def menu_fake_gen():
    while True:
        clear_screen()
        draw_panel("16. ФЕЙК-ГЕНЕРАТОР", [
            "1. Личность РФ", "2. Банк. Карта", 
            "3. Автомобиль", "4. Компания", 
            "5. Крипта", "6. Паспорт", 
            "7. Вод. Права", "8. Мед. Карта", 
            "9. Диплом", "10. Тех. Данные",
            "0. Назад"
        ])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c == "0": break
        try:
            if c == "1":
                g = random.choice(["M", "F"])
                f = random.choice(FIRST_NAMES_M if g=="M" else FIRST_NAMES_F)
                l = random.choice(LAST_NAMES) + ("а" if g=="F" else "")
                txt = f"👤 <b>ЛИЧНОСТЬ</b>\nФИО: {l} {f}\nГород: {random.choice(CITIES)}\nИНН: <code>{gen_inn()}</code>\nСНИЛС: <code>{gen_snils()}</code>\nТел: +7 (9{random.randint(10,99)}) {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}\nEmail: {transliterate(f)}.{transliterate(l[:-1])}{random.randint(10,99)}@{random.choice(DOMAINS)}"
            elif c == "2":
                b = random.choice(BANKS)
                txt = f"💳 <b>КАРТА</b>\nБанк: {b[0]}\nНомер: <code>{gen_card()}</code>\nСрок: {random.randint(1,12):02d}/{random.randint(27,32)}\nCVV: <code>{random.randint(100,999)}</code>"
            elif c == "3":
                txt = f"🚗 <b>АВТО</b>\nМарка: {random.choice(CAR_BRANDS)}\nГод: {random.randint(2000,2024)}\nVIN: <code>{''.join(random.choice('ABCDEFGHJKLMNPRSTUVWXYZ0123456789') for _ in range(17))}</code>\nНомер: {random.choice('АВЕКМНОРСТУХ')}{random.randint(100,999)}{random.choice('АВЕКМНОРСТУХ')}{random.choice('АВЕКМНОРСТУХ')} {random.randint(1,199):02d}"
            elif c == "4":
                txt = f"🏢 <b>КОМПАНИЯ</b>\nНазвание: {random.choice(COMPANIES)}\nОГРН: <code>{random.randint(1000000000000, 9999999999999)}</code>\nИНН: <code>{gen_inn()}</code>\nКПП: <code>{random.randint(100000000, 999999999)}</code>"
            elif c == "5":
                txt = f"🪙 <b>КРИПТА</b>\nBTC: <code>bc1q{''.join(random.choice('acdefghjklmnpqrstuvwxyz023456789') for _ in range(38))}</code>\nETH: <code>0x{''.join(random.choice('0123456789abcdef') for _ in range(40))}</code>"
            elif c == "6":
                txt = f"🛂 <b>ПАСПОРТ РФ</b>\nСерия: <code>{random.randint(10,99)} {random.randint(10,99)}</code>\nНомер: <code>{random.randint(100000,999999)}</code>\nКод подразделения: <code>{random.randint(100,999)}-{random.randint(1,99):03d}</code>\nДата выдачи: {random.randint(1,28):02d}.{random.randint(1,12):02d}.{random.randint(2010,2024)}"
            elif c == "7":
                txt = f"🪪 <b>ВОДИТЕЛЬСКИЕ ПРАВА</b>\nСерия/Номер: <code>{random.randint(10,99)}{random.randint(10,99)} {random.randint(100000,999999)}</code>\nКатегории: {', '.join(random.sample(['A', 'B', 'C', 'D', 'BE', 'CE', 'DE'], random.randint(1,3)))}\nДата выдачи: {random.randint(1,28):02d}.{random.randint(1,12):02d}.{random.randint(2010,2024)}"
            elif c == "8":
                txt = f"🏥 <b>МЕД. КАРТА</b>\nГруппа крови: {random.choice(['O(I)', 'A(II)', 'B(III)', 'AB(IV)'])} {random.choice(['+', '-'])}\nРост: {random.randint(150,200)} см\nВес: {random.randint(50,120)} кг\nАллергии: {random.choice(['Нет', 'Пыль', 'Пенициллин', 'Орехи'])}"
            elif c == "9":
                txt = f"🎓 <b>ДИПЛОМ</b>\nВУЗ: {random.choice(['МГУ', 'СПбГУ', 'МФТИ', 'ВШЭ', 'МГТУ'])}\nСпециальность: {random.choice(['Программист', 'Юрист', 'Экономист', 'Инженер'])}\nНомер: <code>{random.randint(100000,999999)}</code>\nГод: {random.randint(2010,2024)}"
            elif c == "10":
                txt = f"💻 <b>ТЕХ. ДАННЫЕ</b>\nIP: <code>{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}</code>\nMAC: <code>{':'.join(f'{random.randint(0, 255):02x}' for _ in range(6))}</code>\nUUID: <code>{uuid.uuid4()}</code>"
            else: continue
            
            await bot.send_message(config.CHAT_ID, txt, parse_mode="HTML")
            print(colorize("[ОТПРАВЛЕНО В ЧАТ]", "green"))
        except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red"))
        await pause()

# ==========================================
# РАЗДЕЛ 17: OSINT-ПРОБИВ (РАСШИРЕННЫЙ)
# ==========================================
async def menu_osint():
    while True:
        clear_screen(); draw_panel("17. OSINT-ПРОБИВ", ["1. Телефон", "2. Email", "3. Ник", "4. ФИО", "0. Назад"])
        c = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if c == "0": break
        
        target = await asyncio.to_thread(input, colorize("Введи цель: ", "green"))
        if not target: continue
        
        try:
            if c == "1":
                t = re.sub(r'[^\d+]', '', target)
                txt = f"📱 <b>ПРОБИВ: {t}</b>\n\n🔍 <b>Ссылки:</b>\n• <a href='https://www.google.com/search?q={t}'>Google</a>\n• <a href='https://yandex.ru/search/?text={t}'>Yandex</a>\n• <a href='https://vk.com/search?c[section]=people&c[q]={t}'>VK</a>\n• <a href='https://ok.ru/dk?st.cmd=searchResult&st.query={t}'>OK</a>\n• <a href='https://www.avito.ru/rossiya?q={t}'>Avito</a>\n• <a href='https://www.truecaller.com/search/ru/{t}'>Truecaller</a>\n• <a href='https://getcontact.com/ru/'>GetContact</a>"
            elif c == "2":
                user = target.split('@')[0]
                txt = f"📧 <b>ПРОБИВ: {target}</b>\n\n🔍 <b>Ссылки:</b>\n• <a href='https://www.google.com/search?q={target}'>Google</a>\n• <a href='https://vk.com/{user}'>VK</a>\n• <a href='https://github.com/{user}'>GitHub</a>\n• <a href='https://t.me/{user}'>Telegram</a>\n• <a href='https://instagram.com/{user}'>Instagram</a>\n• <a href='https://twitter.com/{user}'>Twitter</a>\n• <a href='https://haveibeenpwned.com/unifiedsearch/{target}'>HIBP (Утечки)</a>"
            elif c == "3":
                txt = f"🕵️ <b>ПРОБИВ: {target}</b>\n\n🔍 <b>Ссылки:</b>\n• <a href='https://vk.com/{target}'>VK</a>\n• <a href='https://t.me/{target}'>Telegram</a>\n• <a href='https://github.com/{target}'>GitHub</a>\n• <a href='https://steamcommunity.com/id/{target}'>Steam</a>\n• <a href='https://www.tiktok.com/@{target}'>TikTok</a>\n• <a href='https://www.twitch.tv/{target}'>Twitch</a>\n• <a href='https://www.reddit.com/user/{target}/'>Reddit</a>\n• <a href='https://www.pinterest.com/{target}/'>Pinterest</a>"
            elif c == "4":
                q = urllib.parse.quote(target)
                txt = f"👤 <b>ПРОБИВ: {target}</b>\n\n🔍 <b>Ссылки:</b>\n• <a href='https://www.google.com/search?q={q}'>Google</a>\n• <a href='https://yandex.ru/search/?text={q}'>Yandex</a>\n• <a href='https://vk.com/search?c[section]=people&c[q]={q}'>VK Люди</a>\n• <a href='https://ok.ru/dk?st.cmd=searchResult&st.query={q}'>OK Люди</a>\n• <a href='https://www.linkedin.com/pub/dir/{q}'>LinkedIn</a>"
            else: continue
            
            await bot.send_message(config.CHAT_ID, txt, parse_mode="HTML", disable_web_page_preview=True)
            print(colorize("[ОТЧЕТ ОТПРАВЛЕН В ЧАТ]", "green"))
        except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red"))
        await pause()

# ==========================================
# ГЛАВНОЕ МЕНЮ
# ==========================================
async def main():
    ask_window_size()
    clear_screen(); print(colorize("Запуск...", "yellow")); await bot.delete_webhook()
    try:
        me = await bot.get_me(); print(colorize(f"[БОТ @{me.username} НА СВЯЗИ!]", "green")); await asyncio.sleep(1)
    except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red")); return

    while True:
        try:
            clear_screen()
            draw_panel("БРО-ПАНЕЛЬ БОТА V18", [
                "1. ТЕКСТ", "10. СМЕНА ТЕМЫ",
                "2. МЕДИА", "11. УТИЛИТЫ",
                "3. СПАМ-ЗОНА", "12. ТАЙМЕР (ОТЛОЖКА)",
                "4. ФИШКИ", "13. СПЕЦ-ОПЕРАЦИИ",
                "5. АДМИНКА", "14. ПРОБИВ ЮЗЕРА",
                "6. НАСТРОЙКИ БОТА", "15. СИСТЕМА",
                "7. ИНФО И ПИНГ", "16. ГЕНЕРАТОР ФЕЙКОВ",
                "8. ГАЙД (ПОМОЩЬ)", "17. OSINT-ПРОБИВ",
                "9. МУЗЫКА", "0. ВЫХОД"
            ])
            
            choice = await asyncio.to_thread(input, colorize("\nВыбери раздел (0-17): ", "green"))

            if choice == "0": print(colorize("Выход...", "yellow")); break
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
            print(colorize("\n\n[БРО] Выходим...", "red"))
            if AUDIO_OK: player.pause()
            break
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
