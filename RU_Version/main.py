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
import sys

try:
    import pyglet
    pyglet.options['shadow_window'] = False
    player = pyglet.media.Player()
    AUDIO_OK = True
except ImportError:
    AUDIO_OK = False

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import FSInputFile, ChatPermissions, BotCommand, Message
from aiogram.enums import ChatAction
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher() 
START_TIME = time.time()
PANEL_ACTIVE = True

# ==========================================
# СКРЫТИЕ И ПОКАЗ ОКНА
# ==========================================
def hide_console():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0: ctypes.windll.user32.ShowWindow(whnd, 0)

def show_console():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 1)
        ctypes.windll.user32.SetForegroundWindow(whnd)

# ==========================================
# КОМАНДЫ УПРАВЛЕНИЯ (СТАРЫЕ УДАЛЕНЫ)
# ==========================================
@dp.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "🤖 <b>Мои команды:</b>\n\n"
        "🔹 <code>/status</code> — Узнать, как я поживаю\n"
        "🔹 <code>/say [текст]</code> — Скажу твоим голосом\n"
        "🔹 <code>/spam [кол-во] [текст]</code> — Заспамлю чат\n"
        "🔹 <code>/osint [тип] [цель]</code> — Пробью инфу (тип: phone, email, nick)\n"
        "🔹 <code>/fake [тип]</code> — Сгенерирую фейк (тип: person, card, car)\n"
        "🔹 <code>/restart</code> — Перезагружусь\n"
        "🔹 <code>/sleep</code> — Уйду в оффлайн\n"
        "🔹 <code>/wakeup</code> — Вернусь в сеть"
    )
    await message.answer(text, parse_mode="HTML")

@dp.message(Command("restart"))
async def cmd_restart(message: Message):
    await message.answer("🔄 <b>Перезагружаюсь... Скоро вернусь!</b>", parse_mode="HTML")
    await asyncio.sleep(1)
    os.execl(sys.executable, sys.executable, *sys.argv)

@dp.message(Command("sleep"))
async def cmd_shutdown(message: Message):
    global PANEL_ACTIVE
    PANEL_ACTIVE = False
    await message.answer("💤 <b>Я ухожу в оффлайн. Пока, бро!</b>", parse_mode="HTML")
    await asyncio.sleep(0.5)
    hide_console()

@dp.message(Command("wakeup"))
async def cmd_start(message: Message):
    global PANEL_ACTIVE
    if not PANEL_ACTIVE:
        PANEL_ACTIVE = True
        show_console()
        await message.answer("🟢 <b>Я снова в сети! Чем могу помочь?</b>", parse_mode="HTML")
    else:
        await message.answer("🟢 <b>Я и так на связи, бро!</b>", parse_mode="HTML")

@dp.message(Command("status"))
async def cmd_status(message: Message):
    up = int(time.time() - START_TIME)
    await message.answer(f"📊 <b>Статус:</b>\nЯ работаю уже: {up//3600}ч {(up%3600)//60}м\nМоя ОС: {platform.system()}", parse_mode="HTML")

@dp.message(Command("say"))
async def cmd_say(message: Message):
    text = message.text.replace("/say", "").strip()
    if text: await bot.send_message(config.CHAT_ID, text)
    else: await message.answer("А что сказать-то?")

@dp.message(Command("spam"))
async def cmd_spam(message: Message):
    args = message.text.replace("/spam", "").strip().split(" ", 1)
    if len(args) == 2:
        try:
            count = int(args[0])
            text = args[1]
            await message.answer(f"🚀 Начинаю спам ({count} раз)...")
            for _ in range(count):
                await bot.send_message(config.CHAT_ID, text)
                await asyncio.sleep(1)
            await message.answer("✅ Спам завершен!")
        except ValueError: await message.answer("❌ Формат: /spam 10 Привет")
    else: await message.answer("❌ Формат: /spam 10 Привет")

@dp.message(Command("osint"))
async def cmd_osint(message: Message):
    args = message.text.replace("/osint", "").strip().split(" ", 1)
    if len(args) == 2:
        t_type, target = args[0].lower(), args[1]
        try:
            if t_type == "phone":
                t = re.sub(r'[^\d+]', '', target)
                txt = f"📱 <b>Инфа по {t}:</b>\n• <a href='https://www.google.com/search?q={t}'>Google</a>\n• <a href='https://vk.com/search?c[section]=people&c[q]={t}'>VK</a>\n• <a href='https://www.truecaller.com/search/ru/{t}'>Truecaller</a>"
            elif t_type == "email":
                user = target.split('@')[0]
                txt = f"📧 <b>Инфа по {target}:</b>\n• <a href='https://vk.com/{user}'>VK</a>\n• <a href='https://github.com/{user}'>GitHub</a>\n• <a href='https://t.me/{user}'>Telegram</a>"
            elif t_type == "nick":
                txt = f"🕵️ <b>Инфа по {target}:</b>\n• <a href='https://vk.com/{target}'>VK</a>\n• <a href='https://t.me/{target}'>Telegram</a>\n• <a href='https://github.com/{target}'>GitHub</a>"
            else: await message.answer("❌ Тип: phone, email или nick"); return
            await bot.send_message(config.CHAT_ID, txt, parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e: await message.answer(f"❌ Ошибка: {e}")
    else: await message.answer("❌ Формат: /osint phone +79991234567")

@dp.message(Command("fake"))
async def cmd_fake(message: Message):
    f_type = message.text.replace("/fake", "").strip().lower()
    try:
        if f_type == "person":
            txt = f"👤 <b>Личность:</b>\nИмя: {random.choice(['Иван', 'Петр', 'Алексей'])} {random.choice(['Иванов', 'Смирнов'])}\nТел: +7 (9{random.randint(10,99)}) {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}"
        elif f_type == "card":
            txt = f"💳 <b>Карта:</b>\nНомер: <code>4276 {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}</code>\nCVV: <code>{random.randint(100,999)}</code>"
        elif f_type == "car":
            txt = f"🚗 <b>Авто:</b>\nVIN: <code>{''.join(random.choice('ABCDEFGHJKLMNPRSTUVWXYZ0123456789') for _ in range(17))}</code>\nНомер: {random.choice('АВЕКМНОРСТУХ')}{random.randint(100,999)}{random.choice('АВЕКМНОРСТУХ')}{random.choice('АВЕКМНОРСТУХ')}"
        else: await message.answer("❌ Тип: person, card или car"); return
        await bot.send_message(config.CHAT_ID, txt, parse_mode="HTML")
    except Exception as e: await message.answer(f"❌ Ошибка: {e}")

# ==========================================
# ЦВЕТА И ИНТЕРФЕЙС (ДЛЯ ТЕБЯ)
# ==========================================
os.system('') 
THEMES = {"red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m", "blue": "\033[94m", "purple": "\033[95m", "cyan": "\033[96m", "white": "\033[97m"}
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
        except Exception as e: break

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

def pause():
    print(colorize("\n[БРО, ГОТОВО!] Жми Enter, чтобы продолжить...", "yellow"))
    return asyncio.to_thread(input)

# ==========================================
# ФУНКЦИИ РАЗДЕЛОВ (ВСТАВЬ СВОЙ КОД ИЗ V18/V21)
# ==========================================
# (Чтобы не раздувать сообщение, я оставил только заглушки. 
# Скопируй сюда свои функции menu_text(), menu_spam(), menu_fake_gen() и т.д. 
# В каждой из них не забудь проверку if not PANEL_ACTIVE: return)

# ==========================================
# ГЛАВНОЕ МЕНЮ
# ==========================================
async def main():
    global PANEL_ACTIVE
    ask_window_size()
    clear_screen(); print(colorize("Запуск...", "yellow")); 
    
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(dp.start_polling(bot))
    
    try:
        me = await bot.get_me(); print(colorize(f"[БОТ @{me.username} НА СВЯЗИ!]", "green")); await asyncio.sleep(1)
    except Exception as e: print(colorize(f"[ОШИБКА] {e}", "red")); return

    while True:
        try:
            if not PANEL_ACTIVE:
                await asyncio.sleep(2)
                continue
                
            clear_screen()
            draw_panel("БРО-ПАНЕЛЬ БОТА V22.1", [
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

            if choice == "0": 
                print(colorize("Выход...", "yellow")); break
            # ... Здесь твои elif choice == "1": await menu_text() и т.д.

        except (KeyboardInterrupt, asyncio.CancelledError):
            print(colorize("\n\n[БРО] Выходим...", "red"))
            if AUDIO_OK: player.pause()
            break
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
