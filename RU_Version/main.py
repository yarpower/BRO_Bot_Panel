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
# ДВИЖОК ЦВЕТОВ
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
# УМНЫЙ ВЫБОР РАЗМЕРА ОКНА (С ЗАЩИТОЙ ОТ КРЭША)
# ==========================================
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
            sw = user32.GetSystemMetrics(0)
            sh = user32.GetSystemMetrics(1)
            # Безопасный расчет ширины и высоты, чтобы окно не вылезло за края
            max_cols = int(sw / 10) 
            max_lines = int(sh / 22) 
            if max_cols > 200: max_cols = 200 # Ограничитель для ультравайдов
        except:
            max_cols, max_lines = 150, 45

        try:
            if choice == "1":
                os.system('mode con: cols=80 lines=25'); break
            elif choice == "2":
                os.system('mode con: cols=100 lines=30'); break
            elif choice == "3":
                os.system(f'mode con: cols={int(max_cols*0.65)} lines={int(max_lines*0.65)}'); break
            elif choice == "4":
                os.system(f'mode con: cols={int(max_cols*0.85)} lines={int(max_lines*0.85)}'); break
            elif choice == "5":
                os.system(f'mode con: cols={max_cols} lines={max_lines}'); break
            else:
                print("Неверный выбор, бро. Нажми 1-5.")
        except Exception as e:
            print(f"Не удалось изменить размер: {e}")
            break

# ==========================================
# УМНАЯ ОТРИСОВКА (Подстраивается под 100% ширины)
# ==========================================
def draw_panel(title, options):
    cols = shutil.get_terminal_size().columns
    # Оставляем по 2 символа с каждой стороны для отступов
    width = max(60, cols - 4) 
    
    print(colorize("╔" + "═" * width + "╗", "cyan"))
    
    title_str = f"  {title}  "
    left_pad = (width - len(title_str)) // 2
    right_pad = width - len(title_str) - left_pad
    print(colorize("║" + " " * left_pad + title_str + " " * right_pad + "║", "cyan"))
    print(colorize("╠" + "═" * width + "╣", "cyan"))
    
    # Идеальная математика колонок
    col_width = (width - 1) // 2
    right_width = width - 1 - col_width
    
    for i in range(0, len(options), 2):
        left_opt = options[i]
        right_opt = options[i+1] if i+1 < len(options) else ""
        
        left_str = f" {left_opt}"[:col_width].ljust(col_width)
        right_str = f" {right_opt}"[:right_width].ljust(right_width)
        
        print(colorize(f"║{left_str}│{right_str}║", "cyan"))
            
    print(colorize("╚" + "═" * width + "╝", "cyan"))

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
# РАЗДЕЛ 1: ТЕКСТ
# ==========================================
async def menu_text():
    while True:
        clear_screen()
        draw_panel("1. [TXT] БРО, ТУТ ТЕКСТ", [
            "1. Обычный текст", "2. HTML (жирный)", "3. Эффект 'Печатает...'",
            "4. Перевертыш", "5. КАПС (ОРЁМ)", "6. Мемный текст",
            "7. Base64 Шифрование", "8. СЕКРЕТНЫЙ ТЕКСТ", "0. Назад в меню"
        ])
        choice = await asyncio.to_thread(input, colorize("\nЧё выбираешь, бро? -> ", "green"))
        if choice == "0": break
        elif choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            text = await asyncio.to_thread(input, colorize("Вводи текст, бро:\n> ", "green"))
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
                print(colorize("[БРО, ОТПРАВЛЕНО!]", "green"))
            except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red"))
            await pause()

# ==========================================
# РАЗДЕЛ 2: МЕДИА
# ==========================================
async def menu_media():
    while True:
        clear_screen()
        draw_panel("2. [MED] БРО, ТУТ МЕДИА", [
            "1. Отправить файл", "2. Геолокация", "3. Контакт", 
            "4. Стикер", "5. Кружок", "0. Назад в меню"
        ])
        choice = await asyncio.to_thread(input, colorize("\nЧё выбираешь, бро? -> ", "green"))
        if choice == "0": break
        elif choice == "1":
            path = (await asyncio.to_thread(input, colorize("Путь к файлу:\n> ", "green"))).strip('"\' ')
            if not os.path.exists(path): print(colorize("[ОШИБКА] Нет файла.", "red")); await pause(); continue
            caption = await asyncio.to_thread(input, colorize("Подпись:\n> ", "green"))
            try: await smart_send_file(config.CHAT_ID, path, caption); print(colorize("[БРО, ОТПРАВЛЕНО!]", "green"))
            except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red"))
            await pause()
        elif choice == "2":
            try:
                lat = await asyncio.to_thread(input, colorize("Широта:\n> ", "green"))
                lon = await asyncio.to_thread(input, colorize("Долгота:\n> ", "green"))
                await bot.send_location(config.CHAT_ID, float(lat), float(lon)); print(colorize("[БРО, ЛОКАЦИЯ!]", "green"))
            except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red"))
            await pause()
        elif choice == "3":
            phone = await asyncio.to_thread(input, colorize("Телефон:\n> ", "green"))
            name = await asyncio.to_thread(input, colorize("Имя:\n> ", "green"))
            try: await bot.send_contact(config.CHAT_ID, phone, name); print(colorize("[БРО, КОНТАКТ!]", "green"))
            except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red"))
            await pause()
        elif choice == "4":
            path = (await asyncio.to_thread(input, colorize("Путь к стикеру:\n> ", "green"))).strip('"\' ')
            try: await bot.send_sticker(config.CHAT_ID, FSInputFile(path)); print(colorize("[БРО, СТИКЕР!]", "green"))
            except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red"))
            await pause()
        elif choice == "5":
            path = (await asyncio.to_thread(input, colorize("Путь к видео (.mp4):\n> ", "green"))).strip('"\' ')
            try: await bot.send_video_note(config.CHAT_ID, FSInputFile(path)); print(colorize("[БРО, КРУЖОК!]", "green"))
            except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red"))
            await pause()

# ==========================================
# РАЗДЕЛ 3: СПАМ-ЗОНА
# ==========================================
async def menu_spam():
    while True:
        clear_screen()
        draw_panel("3. [SPM] БРО, ТУТ СПАМ", [
            "1. Текст", "2. Файл", "3. УМНЫЙ СПАМ",
            "4. КАМНИ (STONE)", "5. БЕСКОНЕЧНЫЙ", "0. Назад в меню"
        ])
        choice = await asyncio.to_thread(input, colorize("\nЧё выбираешь, бро? -> ", "green"))
        if choice == "0": break
        elif choice in ["1", "2", "3", "4", "5"]:
            if choice == "1": text = await asyncio.to_thread(input, colorize("Текст:\n> ", "green")); path=None
            elif choice == "2": path = (await asyncio.to_thread(input, colorize("Путь к файлу:\n> ", "green"))).strip('"\' '); text=None
            elif choice == "4": text = "STONE " * 50; path=None
            elif choice == "5": text = await asyncio.to_thread(input, colorize("Текст:\n> ", "green")); path=None
            else: text = await asyncio.to_thread(input, colorize("Текст:\n> ", "green")); path=None

            if path and not os.path.exists(path): print(colorize("[ОШИБКА] Нет файла.", "red")); await pause(); continue
            try:
                count = 999999 if choice == "5" else int(await asyncio.to_thread(input, colorize("Сколько раз? ", "green")))
                delay = "random" if choice in ["3", "4", "5"] else float(await asyncio.to_thread(input, colorize(f"Задержка: ", "green")) or config.DEFAULT_SPAM_DELAY)
            except ValueError: 
                print(colorize("[ОШИБКА] Нужно ввести число!", "red"))
                await pause()
                continue

            print(colorize("\nПогнали...", "yellow"))
            for i in range(count):
                try:
                    if path: await smart_send_file(config.CHAT_ID, path)
                    else: await bot.send_message(config.CHAT_ID, text)
                    print(colorize(f"[{i+1}/{count if count < 999999 else 'INF'}] ок", "green"))
                    await asyncio.sleep(random.uniform(1.5, 3.5) if delay == "random" else delay)
                except Exception as e: print(colorize(f"[БАН] {e}", "red")); break
            await pause()

# ==========================================
# РАЗДЕЛ 4: ФИШКИ
# ==========================================
async def menu_features():
    while True:
        clear_screen()
        draw_panel("4. [FUN] ФИШКИ", [
            "1. Опрос", "2. Закреп", "3. Кубик",
            "4. Дартс", "5. Баскетбол", "6. Рулетка",
            "7. Футбол", "8. Рандом (1-100)", "0. Назад в меню"
        ])
        choice = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if choice == "0": break
        elif choice == "1":
            q = await asyncio.to_thread(input, "Вопрос: "); o1 = await asyncio.to_thread(input, "Вар 1: "); o2 = await asyncio.to_thread(input, "Вар 2: ")
            try: await bot.send_poll(config.CHAT_ID, q, [o1, o2]); print(colorize("[ОПРОС!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            try:
                msg = await bot.send_message(config.CHAT_ID, "Закреплено!")
                await bot.pin_chat_message(config.CHAT_ID, msg.message_id); print(colorize("[ЗАКРЕП!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice in ["3", "4", "5", "6", "7"]:
            emoji = {"3":"🎲", "4":"🎯", "5":"🏀", "6":"🎰", "7":"⚽"}[choice] 
            try: await bot.send_dice(config.CHAT_ID, emoji=emoji); print(colorize("[ИГРА!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "8":
            try: await bot.send_message(config.CHAT_ID, f"Число: {random.randint(1, 100)}"); print(colorize("[ЧИСЛО!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()

# ==========================================
# РАЗДЕЛ 5: АДМИНКА
# ==========================================
async def menu_admin():
    while True:
        clear_screen()
        draw_panel("5. [ADM] АДМИНКА", [
            "1. Мут всем", "2. Размут всем", "3. Сменить название",
            "4. Сменить описание", "5. Бан по ID", "6. Бан по @юзеру",
            "7. Кик по ID", "8. Кик по @юзеру", "9. Удалить сообщение",
            "0. Назад в меню"
        ])
        choice = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if choice == "0": break
        elif choice == "1":
            try: await bot.set_chat_permissions(config.CHAT_ID, ChatPermissions(can_send_messages=False)); print(colorize("[МУТ!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            try: await bot.set_chat_permissions(config.CHAT_ID, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)); print(colorize("[РАЗМУТ!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "3":
            t = await asyncio.to_thread(input, "Новое название: ")
            try: await bot.set_chat_title(config.CHAT_ID, t); print(colorize("[OK]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "4":
            d = await asyncio.to_thread(input, "Новое описание: ")
            try: await bot.set_chat_description(config.CHAT_ID, d); print(colorize("[OK]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice in ["5", "6", "7", "8"]:
            if choice in ["5", "7"]:
                try: target = int(await asyncio.to_thread(input, "ID: "))
                except ValueError: print(colorize("[ERROR] Нужны цифры", "red")); await pause(); continue
            else: target = (await asyncio.to_thread(input, "@юзер: ")).strip()
            try:
                if choice in ["5", "6"]: await bot.ban_chat_member(config.CHAT_ID, target); print(colorize("[ЗАБАНЕН!]", "green"))
                else:
                    await bot.ban_chat_member(config.CHAT_ID, target); await bot.unban_chat_member(config.CHAT_ID, target); print(colorize("[КИКНУТ!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "9":
            try: msg_id = int(await asyncio.to_thread(input, "ID сообщения: ")); await bot.delete_message(config.CHAT_ID, msg_id); print(colorize("[УДАЛЕНО!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()

# ==========================================
# РАЗДЕЛ 6-10
# ==========================================
async def menu_bot_settings():
    while True:
        clear_screen(); draw_panel("6. [SET] НАСТРОЙКИ БОТА", ["1. Задать команды", "2. Описание бота", "0. Назад"])
        choice = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if choice == "0": break
        elif choice == "1":
            try: await bot.set_my_commands([BotCommand(command="start", description="Start")]); print(colorize("[ОК!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            d = await asyncio.to_thread(input, "Описание: ")
            try: await bot.set_my_description(d); print(colorize("[OK]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()

async def menu_settings():
    while True:
        clear_screen(); draw_panel("7. [INF] ИНФО", ["1. Профиль", "2. Пинг", "3. Инфо чата", "4. Люди", "0. Назад"])
        choice = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if choice == "0": break
        elif choice == "1":
            me = await bot.get_me(); print(colorize(f"\nИмя: {me.first_name}\nЮзер: @{me.username}", "white")); await pause()
        elif choice == "2":
            start = time.time(); await bot.get_me(); print(colorize(f"\nПинг: {round((time.time() - start) * 1000, 2)} мс", "white")); await pause()
        elif choice == "3":
            try:
                chat = await bot.get_chat(config.CHAT_ID); print(colorize(f"\nНазвание: {chat.title}", "white"))
            except Exception as e: print(colorize(f"\n[ERROR] {e}", "red"))
            await pause()
        elif choice == "4":
            try: print(colorize(f"\nЛюдей: {await bot.get_chat_member_count(config.CHAT_ID)}", "white"))
            except Exception as e: print(colorize(f"\n[ERROR] {e}", "red"))
            await pause()

async def menu_help():
    while True:
        clear_screen(); draw_panel("8. [HLP] ГАЙД", ["1. Текст", "2. Медиа", "3. Спам", "4. Фишки", "5. Админка", "6. Настройки", "7. Инфо", "8. Музыка", "0. Назад"])
        choice = await asyncio.to_thread(input, colorize("\nКакой раздел? ", "green"))
        if choice == "0": break
        print(colorize("\nТУТ ОБЪЯСНЕНИЕ ДЛЯ ЭТОГО РАЗДЕЛА...", "yellow")); await pause()

async def menu_music():
    global player
    if not AUDIO_OK: print(colorize("\n[ОШИБКА] Pyglet не установлен!", "red")); await pause(); return
    while True:
        clear_screen(); draw_panel("9. [MUS] МУЗЫКА", ["1. Включить", "2. Пауза/Продолжить", "3. Стоп", "4. Громче (+10%)", "5. Тише (-10%)", "0. Назад"])
        print(colorize("[СТАТУС] " + ("Играет..." if player.playing else "Тишина"), "green"))
        choice = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if choice == "0": break
        elif choice == "1":
            path = (await asyncio.to_thread(input, "Путь к mp3: ")).strip('"\' ')
            try: 
                player = pyglet.media.Player()
                # streaming=True позволяет не грузить весь файл в память сразу
                source = await asyncio.to_thread(pyglet.media.load, path, streaming=True)
                player.queue(source); player.play(); print(colorize("[ИГРАЕТ!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            if player.playing: player.pause(); print(colorize("[ПАУЗА]", "green"))
            else: player.play(); print(colorize("[ПРОДОЛЖАЕМ]", "green"))
            await pause()
        elif choice == "3": player.pause(); player.seek(0); print(colorize("[СТОП]", "green")); await pause()
        elif choice == "4": player.volume = min(1.0, player.volume + 0.1); print(colorize(f"[ГРОМКОСТЬ: {int(player.volume*100)}%]", "green")); await pause()
        elif choice == "5": player.volume = max(0.0, player.volume - 0.1); print(colorize(f"[ГРОМКОСТЬ: {int(player.volume*100)}%]", "green")); await pause()

async def menu_theme():
    global CURRENT_THEME
    while True:
        clear_screen(); draw_panel("10. [THM] СМЕНА ТЕМЫ", ["1. (RED) Красный", "2. (GRN) Зеленый", "3. (BLU) Синий", "4. (YLW) Желтый", "5. (PPL) Фиолетовый", "6. (CYN) Голубой", "7. (RGB) РАДУГА", "0. Назад"])
        choice = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if choice == "0": break
        elif choice == "1": CURRENT_THEME = "red"
        elif choice == "2": CURRENT_THEME = "green"
        elif choice == "3": CURRENT_THEME = "blue"
        elif choice == "4": CURRENT_THEME = "yellow"
        elif choice == "5": CURRENT_THEME = "purple"
        elif choice == "6": CURRENT_THEME = "cyan"
        elif choice == "7": CURRENT_THEME = "rainbow"
        else: continue
        print(colorize("\n[ТЕМА ИЗМЕНЕНА!]", "green")); await pause()

# ==========================================
# ГЛАВНОЕ МЕНЮ
# ==========================================
async def main():
    ask_window_size()
    clear_screen()
    print(colorize("Запуск...", "yellow")); await bot.delete_webhook()
    try:
        me = await bot.get_me(); print(colorize(f"[БОТ @{me.username} НА СВЯЗИ!]", "green")); await asyncio.sleep(1)
    except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red")); return

    while True:
        clear_screen()
        draw_panel("БРО-ПАНЕЛЬ БОТА V14", [
            "1. [TXT] ТЕКСТ", "6. [SET] НАСТРОЙКИ БОТА",
            "2. [MED] МЕДИА", "7. [INF] ИНФО И ПИНГ",
            "3. [SPM] СПАМ-ЗОНА", "8. [HLP] ГАЙД (ПОМОЩЬ)",
            "4. [FUN] ФИШКИ", "9. [MUS] МУЗЫКА",
            "5. [ADM] АДМИНКА", "10. [THM] СМЕНА ТЕМЫ",
            "0. [EXT] ВЫХОД", ""
        ])
        
        choice = await asyncio.to_thread(input, colorize("\nВыбери раздел (0-10): ", "green"))

        if choice == "0": 
            print(colorize("Выход...", "yellow"))
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
