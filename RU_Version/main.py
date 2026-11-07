import asyncio
import os
import time
import random
import base64

# Пытаемся подключить pyglet для музыки
try:
    import pyglet
    pyglet.options['shadow_window'] = False # Чтобы не открывалось лишнее окно
    player = pyglet.media.Player()
    AUDIO_OK = True
except ImportError:
    print("[ВНИМАНИЕ] Pyglet не установлен. Выполни в консоли: pip install pyglet")
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
    return asyncio.to_thread(input, "\n[БРО, ГОТОВО!] Жми Enter, чтобы продолжить...")

# ==========================================
# РАЗДЕЛ 1: ТЕКСТ
# ==========================================
async def menu_text():
    while True:
        clear_screen()
        print("=== 1. БРО, ТУТ ТЕКСТ ===")
        print("1. Кинуть обычный текст")
        print("2. Кинуть красивый текст (HTML: <b>жирный</b>)")
        print("3. Эффект 'Бот печатает...'")
        print("4. Текст наоборот (Перевертыш)")
        print("5. КАПС (ОРЁМ)")
        print("6. Мемный текст (ЧеРеДоВаНиЕ)")
        print("7. Base64 Шифрование (секретка)")
        print("8. СЕКРЕТНЫЙ ТЕКСТ (Спойлер, скрыт под черным)")
        print("0. Назад в главное")
        
        choice = await asyncio.to_thread(input, "\nЧё выбираешь, бро? ")
        if choice == "0": break
        elif choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            text = await asyncio.to_thread(input, "Вводи текст, бро:\n> ")
            
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
                print("[БРО, ОТПРАВЛЕНО!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()

# ==========================================
# РАЗДЕЛ 2: МЕДИА
# ==========================================
async def menu_media():
    while True:
        clear_screen()
        print("=== 2. БРО, ТУТ ФАЙЛЫ И МЕДИА ===")
        print("1. Кинуть файл (авто-определение)")
        print("2. Кинуть геолокацию (точка на карте)")
        print("3. Кинуть фейковый контакт")
        print("4. Кинуть стикер")
        print("5. Кинуть кружок (круглое видео)")
        print("0. Назад в главное")
        
        choice = await asyncio.to_thread(input, "\nЧё выбираешь, бро? ")
        if choice == "0": break
        
        elif choice == "1":
            path_input = await asyncio.to_thread(input, "Путь к файлу (перетащи сюда):\n> ")
            path = path_input.strip('"\' ')
            if not os.path.exists(path): print("[ОШИБКА] Нет такого файла, бро."); await pause(); continue
            caption = await asyncio.to_thread(input, "Подпись (Enter - пропустить):\n> ")
            try: await smart_send_file(config.CHAT_ID, path, caption); print("[БРО, ОТПРАВЛЕНО!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()

        elif choice == "2":
            lat = await asyncio.to_thread(input, "Широта (55.7558):\n> ")
            lon = await asyncio.to_thread(input, "Долгота (37.6173):\n> ")
            try: await bot.send_location(config.CHAT_ID, latitude=float(lat), longitude=float(lon)); print("[БРО, КИНУЛ ЛОКАЦИЮ!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()

        elif choice == "3":
            phone = await asyncio.to_thread(input, "Телефон (+7999...):\n> ")
            name = await asyncio.to_thread(input, "Имя:\n> ")
            try: await bot.send_contact(config.CHAT_ID, phone_number=phone, first_name=name); print("[БРО, КОНТАКТ УЛЕТЕЛ!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()

        elif choice == "4":
            path_input = await asyncio.to_thread(input, "Путь к стикеру (.webp):\n> ")
            path = path_input.strip('"\' ')
            try: await bot.send_sticker(config.CHAT_ID, sticker=FSInputFile(path)); print("[БРО, СТИКЕР ЗАЛЕТЕЛ!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()

        elif choice == "5":
            path_input = await asyncio.to_thread(input, "Путь к видео для кружка (.mp4):\n> ")
            path = path_input.strip('"\' ')
            try: await bot.send_video_note(config.CHAT_ID, video_note=FSInputFile(path)); print("[БРО, КРУЖОК ЗАПИСАН!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()

# ==========================================
# РАЗДЕЛ 3: СПАМ-ЗОНА
# ==========================================
async def menu_spam():
    while True:
        clear_screen()
        print("=== 3. БРО, ТУТ СПАМ (ОСТОРОЖНО!) ===")
        print("1. Текстовый спам (контролируемый)")
        print("2. Спам файлом/картинкой")
        print("3. УМНЫЙ СПАМ (ТГ не так быстро банит)")
        print("4. СПАМ КАМНЯМИ (🗿) - жестко")
        print("5. БЕСКОНЕЧНЫЙ СПАМ (Остановить: Ctrl+C в консоли)")
        print("0. Назад в главное")
        
        choice = await asyncio.to_thread(input, "\nЧё выбираешь, бро? ")
        if choice == "0": break
        
        elif choice in ["1", "2", "3", "4", "5"]:
            if choice == "1": text = await asyncio.to_thread(input, "Текст для спама:\n> "); path=None
            elif choice == "2": 
                path_input = await asyncio.to_thread(input, "Путь к файлу:\n> ")
                path = path_input.strip('"\' '); 
                text=None
            elif choice == "4": text = "🗿" * 50; path=None
            elif choice == "5": text = await asyncio.to_thread(input, "Текст для БЕСКОНЕЧНОГО спама:\n> "); path=None
            else: text = await asyncio.to_thread(input, "Текст для умного спама:\n> "); path=None

            if path and not os.path.exists(path): print("[ОШИБКА] Нет файла, бро."); await pause(); continue
            
            try:
                if choice == "5":
                    count = 999999
                    delay = "random"
                    print("\n[ВНИМАНИЕ] Включен бесконечный спам! Чтобы остановить, зажми Ctrl+C в этом окне.")
                else:
                    count = int(await asyncio.to_thread(input, "Сколько раз спамим? "))
                    if choice in ["3", "4"]: delay = "random"
                    else:
                        delay_input = await asyncio.to_thread(input, f"Задержка (Enter для {config.DEFAULT_SPAM_DELAY} сек): ")
                        delay = float(delay_input) if delay_input.strip() else config.DEFAULT_SPAM_DELAY
            except ValueError: continue

            print(f"\nПогнали спамить...")
            for i in range(count):
                try:
                    if path: await smart_send_file(config.CHAT_ID, path)
                    else: await bot.send_message(config.CHAT_ID, text)
                    print(f"[{i+1}/{count if count < 999999 else '∞'}] улетело, бро!")
                    
                    if delay == "random": await asyncio.sleep(random.uniform(1.5, 3.5))
                    else: await asyncio.sleep(delay)
                except Exception as e: 
                    print(f"[БАН ОТ ТГ] {e}"); 
                    break
            await pause()

# ==========================================
# РАЗДЕЛ 4: ФИШКИ
# ==========================================
async def menu_features():
    while True:
        clear_screen()
        print("=== 4. БРО, ТУТ ФИШКИ ===")
        print("1. Создать опрос")
        print("2. Закрепить сообщение")
        print("3. Кинуть КУБИК")
        print("4. Кинуть ДАРТС")
        print("5. Кинуть БАСКЕТБОЛ")
        print("6. Кинуть РУЛЕТКУ (казино)")
        print("7. Кинуть ФУТБОЛ")
        print("8. Рандомное число (1-100)")
        print("0. Назад в главное")
        
        choice = await asyncio.to_thread(input, "\nЧё выбираешь, бро? ")
        if choice == "0": break
        
        elif choice == "1":
            q = await asyncio.to_thread(input, "Вопрос опроса:\n> ")
            o1 = await asyncio.to_thread(input, "Вариант 1:\n> ")
            o2 = await asyncio.to_thread(input, "Вариант 2:\n> ")
            try: await bot.send_poll(chat_id=config.CHAT_ID, question=q, options=[o1, o2]); print("[БРО, ОПРОС СОЗДАН!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()
        elif choice == "2":
            msg = await bot.send_message(config.CHAT_ID, "Закреплено, бро!")
            await bot.pin_chat_message(chat_id=config.CHAT_ID, message_id=msg.message_id); print("[БРО, ЗАКРЕПИЛ!]"); await pause()
        elif choice in ["3", "4", "5", "6", "7"]:
            emoji = "🎲"
            if choice == "4": emoji = "🎯"
            elif choice == "5": emoji = "🏀"
            elif choice == "6": emoji = "🎰"
            elif choice == "7": emoji = "⚽"
            try: await bot.send_dice(chat_id=config.CHAT_ID, emoji=emoji); print("[БРО, ИГРА ПОШЛА!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()
        elif choice == "8":
            num = random.randint(1, 100)
            try: await bot.send_message(config.CHAT_ID, f"Бро, выпало число: {num}"); print("[БРО, ЧИСЛО ОТПРАВЛЕНО!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()

# ==========================================
# РАЗДЕЛ 5: АДМИН-ПАНЕЛЬ
# ==========================================
async def menu_admin():
    while True:
        clear_screen()
        print("=== 5. БРО, ТУТ АДМИНКА ===")
        print("1. Замутить ВСЕХ (типо тишина)")
        print("2. Размутить ВСЕХ (пусть пишут)")
        print("3. Сменить НАЗВАНИЕ группы")
        print("4. Сменить ОПИСАНИЕ группы")
        print("5. ЗАБАНИТЬ по ID (цифры)")
        print("6. ЗАБАНИТЬ по @юзеру (ник)")
        print("7. КИКНУТЬ по ID (цифры)")
        print("8. КИКНУТЬ по @юзеру (ник)")
        print("9. УДАЛИТЬ сообщение (по ID сообщения)")
        print("0. Назад в главное")
        
        choice = await asyncio.to_thread(input, "\nЧё выбираешь, бро? ")
        if choice == "0": break
        
        elif choice == "1":
            try: await bot.set_chat_permissions(chat_id=config.CHAT_ID, permissions=ChatPermissions(can_send_messages=False)); print("[БРО, ВСЕ ЗАМУЧЕНЫ!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()
        elif choice == "2":
            try: await bot.set_chat_permissions(chat_id=config.CHAT_ID, permissions=ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)); print("[БРО, ВСЕ РАЗМУЧЕНЫ!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()
        elif choice == "3":
            t = await asyncio.to_thread(input, "Новое название группы:\n> ")
            try: await bot.set_chat_title(chat_id=config.CHAT_ID, title=t); print("[БРО, ПЕРЕИМЕНОВАЛ!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()
        elif choice == "4":
            d = await asyncio.to_thread(input, "Новое описание группы:\n> ")
            try: await bot.set_chat_description(chat_id=config.CHAT_ID, description=d); print("[БРО, ОПИСАНИЕ СМЕНИЛ!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()
            
        elif choice in ["5", "6", "7", "8"]:
            if choice in ["5", "7"]:
                target = await asyncio.to_thread(input, "Введи цифровой ID пользователя:\n> ")
                try: user_id = int(target)
                except ValueError: print("[ОШИБКА] Это не ID, бро. Нужны цифры."); await pause(); continue
            else:
                target_input = await asyncio.to_thread(input, "Введи @юзернейм (начиная с @):\n> ")
                target = target_input.strip()
                user_id = target

            try:
                if choice in ["5", "6"]: # Бан
                    await bot.ban_chat_member(chat_id=config.CHAT_ID, user_id=user_id)
                    print(f"[БРО, ПОЛЬЗОВАТЕЛЬ {target} В БАНЕ!]")
                else: # Кик
                    await bot.ban_chat_member(chat_id=config.CHAT_ID, user_id=user_id)
                    await bot.unban_chat_member(chat_id=config.CHAT_ID, user_id=user_id)
                    print(f"[БРО, ПОЛЬЗОВАТЕЛЬ {target} ВЫШВЫРНУТ!]")
            except Exception as e:
                print(f"[ОШИБКА] Не вышло. Может юзера нет или бот не админ. ({e})")
            await pause()
            
        elif choice == "9":
            msg_id = await asyncio.to_thread(input, "Введи ID сообщения:\n> ")
            try: await bot.delete_message(chat_id=config.CHAT_ID, message_id=int(msg_id)); print("[БРО, СООБЩЕНИЕ УДАЛЕНО!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()

# ==========================================
# РАЗДЕЛ 6: НАСТРОЙКИ БОТА
# ==========================================
async def menu_bot_settings():
    while True:
        clear_screen()
        print("=== 6. БРО, НАСТРОЙКИ БОТА ===")
        print("1. Задать команды бота (Меню / )")
        print("2. Изменить описание бота")
        print("0. Назад в главное")
        
        choice = await asyncio.to_thread(input, "\nЧё выбираешь, бро? ")
        if choice == "0": break
        elif choice == "1":
            print("\n[ИНФО] Ставлю команды: /start, /help, /spam")
            try:
                commands = [
                    BotCommand(command="start", description="Запустить бота"),
                    BotCommand(command="help", description="Помощь"),
                    BotCommand(command="spam", description="Начать спам")
                ]
                await bot.set_my_commands(commands)
                print("[БРО, КОМАНДЫ УСТАНОВЛЕНЫ!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()
        elif choice == "2":
            d = await asyncio.to_thread(input, "Новое описание бота:\n> ")
            try: await bot.set_my_description(description=d); print("[БРО, ОПИСАНИЕ БОТА СМЕНЕНО!]")
            except Exception as e: print(f"[ОШИБКА] {e}")
            await pause()

# ==========================================
# РАЗДЕЛ 7: ИНФО
# ==========================================
async def menu_settings():
    while True:
        clear_screen()
        print("=== 7. БРО, ТУТ ИНФО ===")
        print("1. Профиль бота")
        print("2. Пинг до серверов ТГ")
        print("3. Инфо о чате")
        print("4. Сколько людей в чате?")
        print("0. Назад в главное")
        
        choice = await asyncio.to_thread(input, "\nЧё выбираешь, бро? ")
        if choice == "0": break
        elif choice == "1":
            me = await bot.get_me(); print(f"\nИмя: {me.first_name}\nЮзер: @{me.username}\nID: {me.id}"); await pause()
        elif choice == "2":
            start = time.time(); await bot.get_me(); print(f"\nПинг: {round((time.time() - start) * 1000, 2)} мс. Всё чётко."); await pause()
        elif choice == "3":
            try:
                chat = await bot.get_chat(config.CHAT_ID)
                print(f"\nНазвание: {chat.title}\nID: {chat.id}\nТип: {chat.type}")
            except Exception as e: print(f"\n[ОШИБКА] {e}")
            await pause()
        elif choice == "4":
            try: print(f"\nВ чате сидит: {await bot.get_chat_member_count(config.CHAT_ID)} человек.")
            except Exception as e: print(f"\n[ОШИБКА] {e}")
            await pause()

# ==========================================
# РАЗДЕЛ 8: ГАЙД (ПОМОЩЬ)
# ==========================================
async def menu_help():
    while True:
        clear_screen()
        print("=== 8. БРО, ТУТ ГАЙД (ЧТО ВСЁ ЗНАЧИТ) ===")
        print("1. Про раздел ТЕКСТ")
        print("2. Про раздел МЕДИА")
        print("3. Про раздел СПАМ")
        print("4. Про раздел ФИШКИ")
        print("5. Про раздел АДМИНКА")
        print("6. Про раздел НАСТРОЙКИ БОТА")
        print("7. Про раздел ИНФО")
        print("8. Про раздел МУЗЫКА")
        print("0. Назад в главное")
        
        choice = await asyncio.to_thread(input, "\nКакой раздел объяснить, бро? ")
        
        clear_screen()
        if choice == "1":
            print("--- ГАЙД: ТЕКСТ ---")
            print("Тут ты просто кидаешь текст в чат.")
            print("• HTML: Позволяет делать текст жирным (<b>), курсивом (<i>) и т.д.")
            print("• Эффект 'Печатает': Бот 1.5 сек показывает в чате, что он 'печатает...', а потом отправляет текст.")
            print("• Перевертыш: Пишет текст задом наперед (Привет -> тевирП).")
            print("• Base64: Шифрует текст в непонятные буквы (для секреток).")
            print("• Секретный текст: Текст скрывается под черным спойлером.")
            await pause()
        elif choice == "2":
            print("--- ГАЙД: МЕДИА ---")
            print("Тут ты отправляешь файлы. Бот САМ понимает, что ты кинул.")
            print("• Кружок: Отправляет видео в формате круглого сообщения (как в ТГ).")
            print("• Геолокация: Отправляет точку на карте по координатам.")
            print("• Контакт: Отправляет фейковый номер телефона с именем.")
            await pause()
        elif choice == "3":
            print("--- ГАЙД: СПАМ-ЗОНА ---")
            print("Тут бот спамит.")
            print("• Обычный: Шлет с той задержкой, которую ты укажешь.")
            print("• УМНЫЙ СПАМ: Бот сам ставит рандомную задержку от 1.5 до 3.5 сек. Телеграм это любит больше.")
            print("• БЕСКОНЕЧНЫЙ: Бот будет спамить пока ты не зажмешь Ctrl+C в окне.")
            print("• СПАМ КАМНЯМИ: Кидает 50 смайликов 🗿 в одном сообщении.")
            await pause()
        elif choice == "4":
            print("--- ГАЙД: ФИШКИ ---")
            print("Тут развлечения.")
            print("• Опрос: Создает голосовалку в чате.")
            print("• Игры (Кубик, Дартс, Рулетка): Отправляет анимированные смайлы ТГ.")
            print("• Закреп: Бот пишет сообщение и закрепляет его вверху чата.")
            await pause()
        elif choice == "5":
            print("--- ГАЙД: АДМИНКА ---")
            print("ВАЖНО: Бот должен быть админом в группе!")
            print("• Мут: Запрещает всем писать.")
            print("• Бан: Выгоняет человека из группы навсегда.")
            print("• Кик: Выгоняет, но человек может вернуться.")
            print("• ID: Это цифры. Юзер: Это @nickname.")
            print("• Удалить: Удаляет сообщение по его внутреннему ID.")
            await pause()
        elif choice == "6":
            print("--- ГАЙД: НАСТРОЙКИ БОТА ---")
            print("• Команды: Добавляет боту синюю кнопку 'Меню' в чате.")
            print("• Описание: Меняет текст, который видит человек при первом запуске бота.")
            await pause()
        elif choice == "7":
            print("--- ГАЙД: ИНФО ---")
            print("Просто показывает данные: имя бота, пинг, сколько людей в группе.")
            await pause()
        elif choice == "8":
            print("--- ГАЙД: МУЗЫКА ---")
            print("Этот раздел включает музыку ПРЯМО У ТЕБЯ НА КОМПЬЮТЕРЕ (через pyglet).")
            print("• Включить: Указываешь путь к mp3 файлу.")
            print("• Пауза/Продолжить: Ставит трек на паузу или возвращает.")
            print("• Громкость: Меняешь от 0.0 до 1.0 (например, 0.5 - это 50%).")
            await pause()
        elif choice == "0":
            break
        else:
            print("Нет такого пункта, бро.")
            await asyncio.sleep(1)

# ==========================================
# РАЗДЕЛ 9: МУЗЫКА (ЛОКАЛЬНЫЙ ПЛЕЕР)
# ==========================================
async def menu_music():
    global player # Объявляем, что будем менять глобальную переменную
    
    if not AUDIO_OK:
        print("\n[ОШИБКА] Pyglet не установлен. Выполни: pip install pyglet")
        await pause()
        return

    while True:
        clear_screen()
        print("=== 9. БРО, ТУТ МУЗЫКА (ПЛЕЕР) ===")
        
        if player.playing:
            print("[СТАТУС] Музыка играет прямо сейчас...")
        else:
            print("[СТАТУС] Тишина или пауза.")

        print("1. Включить трек (путь к файлу)")
        print("2. Пауза / Продолжить")
        print("3. Остановить музыку")
        print("4. Сделать громче (+10%)")
        print("5. Сделать тише (-10%)")
        print("0. Назад в главное")
        
        choice = await asyncio.to_thread(input, "\nЧё выбираешь, бро? ")
        if choice == "0": break
        
        elif choice == "1":
            path_input = await asyncio.to_thread(input, "Путь к mp3 файлу:\n> ")
            path = path_input.strip('"\' ')
            if not os.path.exists(path):
                print("[ОШИБКА] Нет такого файла, бро."); await pause(); continue
            
            try:
                print("[...] Загружаю трек...")
                # Создаем нового плеера, чтобы сбросить старые треки
                player = pyglet.media.Player()
                # Загружаем в отдельном потоке, чтобы консоль не зависла
                source = await asyncio.to_thread(pyglet.media.load, path)
                player.queue(source)
                player.play()
                print("[БРО, МУЗЫКА ЗАИГРАЛА!]")
            except Exception as e:
                print(f"[ОШИБКА] {e}")
            await pause()

        elif choice == "2":
            if player.playing:
                player.pause()
                print("[БРО, ПАУЗА!]")
            else:
                player.play()
                print("[БРО, ПРОДОЛЖАЕМ!]")
            await pause()

        elif choice == "3":
            player.pause()
            player.seek(0) # Отматываем в начало
            print("[БРО, МУЗЫКА ОСТАНОВЛЕНА!]")
            await pause()

        elif choice == "4":
            vol = player.volume
            new_vol = min(1.0, vol + 0.1)
            player.volume = new_vol
            print(f"[БРО, ГРОМКОСТЬ: {int(new_vol*100)}%]")
            await pause()

        elif choice == "5":
            vol = player.volume
            new_vol = max(0.0, vol - 0.1)
            player.volume = new_vol
            print(f"[БРО, ГРОМКОСТЬ: {int(new_vol*100)}%]")
            await pause()

# ==========================================
# ГЛАВНОЕ МЕНЮ
# ==========================================
async def main():
    clear_screen()
    print("Запуск... Подключение...")
    await bot.delete_webhook()
    
    try:
        me = await bot.get_me()
        print(f"[БРО, БОТ @{me.username} НА СВЯЗИ!]")
        await asyncio.sleep(1)
    except Exception as e:
        print(f"[ОШИБКА] {e}")
        return

    while True:
        clear_screen()
        print("=" * 50)
        print("       БРО, ТЫ В ПАНЕЛИ УПРАВЛЕНИЯ")
        print("=" * 50)
        print("1. ТЕКСТ (обычный, мемный, секретный)")
        print("2. МЕДИА (файлы, стикеры, кружки)")
        print("3. СПАМ-ЗОНА (текст, файлы, бесконечный)")
        print("4. ФИШКИ (опросы, кубики, рулетка)")
        print("5. АДМИНКА (мут, бан по ID/@юзеру)")
        print("6. НАСТРОЙКИ БОТА (команды)")
        print("7. ИНФО И ПИНГ")
        print("8. ГАЙД (Что всё это значит?)")
        print("9. МУЗЫКА (Плеер прямо в консоли)")
        print("0. ВЫХОД")
        print("=" * 50)
        
        choice = await asyncio.to_thread(input, "Выбери раздел (0-9): ")

        if choice == "0":
            print("Выход... Давай, бро!")
            if AUDIO_OK:
                player.pause() # Выключаем музыку при выходе
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