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
# ДВИЖОК ЦВЕТОВ (ANSI-коды)
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
    print(colorize("\n[БРО, ГОТОВО!] Жми Enter, чтобы продолжить...", "yellow"))
    return asyncio.to_thread(input)

# ==========================================
# РАЗДЕЛ 1: ТЕКСТ
# ==========================================
async def menu_text():
    while True:
        clear_screen()
        print(colorize("=== 1. БРО, ТУТ ТЕКСТ ===", "cyan"))
        print("1. Обычный текст\n2. HTML (жирный)\n3. Эффект 'Печатает...'\n4. Перевертыш\n5. КАПС (ОРЁМ)")
        print("6. Мемный текст\n7. Base64 Шифрование\n8. СЕКРЕТНЫЙ ТЕКСТ (Спойлер)\n0. Назад")
        
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
        print(colorize("=== 2. БРО, ТУТ ФАЙЛЫ И МЕДИА ===", "cyan"))
        print("1. Файл\n2. Геолокация\n3. Контакт\n4. Стикер\n5. Кружок\n0. Назад")
        
        choice = await asyncio.to_thread(input, colorize("\nЧё выбираешь, бро? -> ", "green"))
        if choice == "0": break
        
        elif choice == "1":
            path = (await asyncio.to_thread(input, colorize("Путь к файлу:\n> ", "green"))).strip('"\' ')
            if not os.path.exists(path): print(colorize("[ОШИБКА] Нет файла.", "red")); await pause(); continue
            caption = await asyncio.to_thread(input, colorize("Подпись (Enter - пропустить):\n> ", "green"))
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
        print(colorize("=== 3. БРО, ТУТ СПАМ ===", "cyan"))
        print("1. Текст\n2. Файл\n3. УМНЫЙ СПАМ (рандом)\n4. КАМНИ 🗿\n5. БЕСКОНЕЧНЫЙ\n0. Назад")
        
        choice = await asyncio.to_thread(input, colorize("\nЧё выбираешь, бро? -> ", "green"))
        if choice == "0": break
        elif choice in ["1", "2", "3", "4", "5"]:
            if choice == "1": text = await asyncio.to_thread(input, colorize("Текст:\n> ", "green")); path=None
            elif choice == "2": path = (await asyncio.to_thread(input, colorize("Путь к файлу:\n> ", "green"))).strip('"\' '); text=None
            elif choice == "4": text = "🗿" * 50; path=None
            elif choice == "5": text = await asyncio.to_thread(input, colorize("Текст:\n> ", "green")); path=None
            else: text = await asyncio.to_thread(input, colorize("Текст:\n> ", "green")); path=None

            if path and not os.path.exists(path): print(colorize("[ОШИБКА] Нет файла.", "red")); await pause(); continue
            try:
                count = 999999 if choice == "5" else int(await asyncio.to_thread(input, colorize("Сколько раз? ", "green")))
                delay = "random" if choice in ["3", "4", "5"] else float(await asyncio.to_thread(input, colorize(f"Задержка (Enter для {config.DEFAULT_SPAM_DELAY}): ", "green")) or config.DEFAULT_SPAM_DELAY)
            except ValueError: 
                print(colorize("[ОШИБКА] Нужно ввести число!", "red"))
                await pause()
                continue

            print(colorize("\nПогнали...", "yellow"))
            for i in range(count):
                try:
                    if path: await smart_send_file(config.CHAT_ID, path)
                    else: await bot.send_message(config.CHAT_ID, text)
                    print(colorize(f"[{i+1}/{count if count < 999999 else '∞'}] ок", "green"))
                    await asyncio.sleep(random.uniform(1.5, 3.5) if delay == "random" else delay)
                except Exception as e: print(colorize(f"[БАН] {e}", "red")); break
            await pause()

# ==========================================
# РАЗДЕЛ 4: ФИШКИ
# ==========================================
async def menu_features():
    while True:
        clear_screen()
        print(colorize("=== 4. ФИШКИ ===", "cyan"))
        print("1. Опрос\n2. Закреп\n3. Кубик\n4. Дартс\n5. Баскетбол\n6. Рулетка\n7. Футбол\n8. Рандом (1-100)\n0. Назад")
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
        print(colorize("=== 5. АДМИНКА ===", "cyan"))
        print("1. Мут всем\n2. Размут всем\n3. Сменить название\n4. Сменить описание")
        print("5. Бан по ID\n6. Бан по @юзеру\n7. Кик по ID\n8. Кик по @юзеру\n9. Удалить сообщение\n0. Назад")
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
# РАЗДЕЛ 6-8: НАСТРОЙКИ, ИНФО, ГАЙД
# ==========================================
async def menu_bot_settings():
    while True:
        clear_screen(); print(colorize("=== 6. НАСТРОЙКИ БОТА ===", "cyan"))
        print("1. Задать команды\n2. Описание бота\n0. Назад")
        choice = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if choice == "0": break
        elif choice == "1":
            try:
                await bot.set_my_commands([BotCommand(command="start", description="Start"), BotCommand(command="help", description="Help")])
                print(colorize("[КОМАНДЫ УСТАНОВЛЕНЫ!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            d = await asyncio.to_thread(input, "Описание: ")
            try: await bot.set_my_description(d); print(colorize("[OK]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()

async def menu_settings():
    while True:
        clear_screen(); print(colorize("=== 7. ИНФО ===", "cyan"))
        print("1. Профиль\n2. Пинг\n3. Инфо чата\n4. Сколько людей\n0. Назад")
        choice = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if choice == "0": break
        elif choice == "1":
            me = await bot.get_me(); print(colorize(f"\nИмя: {me.first_name}\nЮзер: @{me.username}\nID: {me.id}", "white")); await pause()
        elif choice == "2":
            start = time.time(); await bot.get_me(); print(colorize(f"\nПинг: {round((time.time() - start) * 1000, 2)} мс", "white")); await pause()
        elif choice == "3":
            try:
                chat = await bot.get_chat(config.CHAT_ID)
                print(colorize(f"\nНазвание: {chat.title}\nID: {chat.id}\nТип: {chat.type}", "white"))
            except Exception as e: print(colorize(f"\n[ERROR] {e}", "red"))
            await pause()
        elif choice == "4":
            try: print(colorize(f"\nЛюдей: {await bot.get_chat_member_count(config.CHAT_ID)}", "white"))
            except Exception as e: print(colorize(f"\n[ERROR] {e}", "red"))
            await pause()

async def menu_help():
    while True:
        clear_screen(); print(colorize("=== 8. ГАЙД ===", "cyan"))
        print("1. Текст\n2. Медиа\n3. Спам\n4. Фишки\n5. Админка\n6. Настройки\n7. Инфо\n8. Музыка\n0. Назад")
        choice = await asyncio.to_thread(input, colorize("\nКакой раздел объяснить? ", "green"))
        clear_screen()
        if choice == "1": print(colorize("ТУТ ОБЪЯСНЕНИЕ ПРО ТЕКСТ (HTML, Base64 и т.д.)", "yellow")); await pause()
        elif choice == "2": print(colorize("ТУТ ОБЪЯСНЕНИЕ ПРО МЕДИА (Кружки, Гео)", "yellow")); await pause()
        elif choice == "3": print(colorize("ТУТ ОБЪЯСНЕНИЕ ПРО СПАМ (Умный, Бесконечный)", "yellow")); await pause()
        elif choice == "4": print(colorize("ТУТ ОБЪЯСНЕНИЕ ПРО ИГРЫ И ОПРОСЫ", "yellow")); await pause()
        elif choice == "5": print(colorize("ТУТ ОБЪЯСНЕНИЕ ПРО БАНЫ И МУТЫ", "yellow")); await pause()
        elif choice == "6": print(colorize("ТУТ ОБЪЯСНЕНИЕ ПРО КОМАНДЫ БОТА", "yellow")); await pause()
        elif choice == "7": print(colorize("ТУТ ОБЪЯСНЕНИЕ ПРО ПИНГ И СТАТИСТИКУ", "yellow")); await pause()
        elif choice == "8": print(colorize("ТУТ ОБЪЯСНЕНИЕ ПРО МУЗЫКУ (Pyglet)", "yellow")); await pause()
        elif choice == "0": break

# ==========================================
# РАЗДЕЛ 9: МУЗЫКА
# ==========================================
async def menu_music():
    global player
    if not AUDIO_OK: print(colorize("\n[ОШИБКА] Pyglet не установлен!", "red")); await pause(); return

    while True:
        clear_screen(); print(colorize("=== 9. МУЗЫКА ===", "cyan"))
        print(colorize("[СТАТУС] " + ("Играет..." if player.playing else "Тишина/Пауза"), "green"))
        print("1. Включить\n2. Пауза/Продолжить\n3. Стоп\n4. Громче (+10%)\n5. Тише (-10%)\n0. Назад")
        
        choice = await asyncio.to_thread(input, colorize("\nВыбор: ", "green"))
        if choice == "0": break
        elif choice == "1":
            path = (await asyncio.to_thread(input, "Путь к mp3:\n> ")).strip('"\' ')
            if not os.path.exists(path): print(colorize("[ОШИБКА] Нет файла", "red")); await pause(); continue
            try:
                player = pyglet.media.Player(); source = await asyncio.to_thread(pyglet.media.load, path); player.queue(source); player.play()
                print(colorize("[МУЗЫКА ИГРАЕТ!]", "green"))
            except Exception as e: print(colorize(f"[ERROR] {e}", "red"))
            await pause()
        elif choice == "2":
            if player.playing: player.pause(); print(colorize("[ПАУЗА]", "green"))
            else: player.play(); print(colorize("[ПРОДОЛЖАЕМ]", "green"))
            await pause()
        elif choice == "3":
            player.pause(); player.seek(0); print(colorize("[СТОП]", "green")); await pause()
        elif choice == "4":
            player.volume = min(1.0, player.volume + 0.1); print(colorize(f"[ГРОМКОСТЬ: {int(player.volume*100)}%]", "green")); await pause()
        elif choice == "5":
            player.volume = max(0.0, player.volume - 0.1); print(colorize(f"[ГРОМКОСТЬ: {int(player.volume*100)}%]", "green")); await pause()

# ==========================================
# РАЗДЕЛ 10: СМЕНА ТЕМЫ
# ==========================================
async def menu_theme():
    global CURRENT_THEME
    while True:
        clear_screen()
        print(colorize("=== 10. СМЕНА ТЕМЫ ===", "cyan"))
        print("1. 🔴 Красный\n2. 🟢 Зеленый\n3. 🔵 Синий\n4. 🟡 Желтый")
        print("5. 🟣 Фиолетовый\n6. 🔷 Голубой\n7. 🌈 РАДУГА\n0. Назад")
        
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
    clear_screen()
    print(colorize("Запуск...", "yellow")); await bot.delete_webhook()
    try:
        me = await bot.get_me(); print(colorize(f"[БОТ @{me.username} НА СВЯЗИ!]", "green")); await asyncio.sleep(1)
    except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red")); return

    while True:
        clear_screen()
        print(colorize("╔════════════════════════════════════════════════╗", "cyan"))
        print(colorize("║          🤖 БРО-ПАНЕЛЬ БОТА V11 🤖          ║", "cyan"))
        print(colorize("╠════════════════════════════════════════════════╣", "cyan"))
        print(colorize("║ 1. 📝 ТЕКСТ          │ 6. ⚙️ НАСТРОЙКИ БОТА   ║", "cyan"))
        print(colorize("║ 2. 📁 МЕДИА          │ 7. ℹ️ ИНФО И ПИНГ      ║", "cyan"))
        print(colorize("║ 3. 💣 СПАМ-ЗОНА      │ 8. 📖 ГАЙД (ПОМОЩЬ)    ║", "cyan"))
        print(colorize("║ 4. 🎲 ФИШКИ          │ 9. 🎵 МУЗЫКА           ║", "cyan"))
        print(colorize("║ 5. 👑 АДМИНКА        │ 10. 🎨 СМЕНА ТЕМЫ      ║", "cyan"))
        print(colorize("╠════════════════════════════════════════════════╣", "cyan"))
        print(colorize("║ 0. 🚪 ВЫХОД                                    ║", "cyan"))
        print(colorize("╚════════════════════════════════════════════════╝", "cyan"))
        
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
