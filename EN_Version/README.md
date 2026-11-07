# 🤖 BRO-PANEL BOT (V21)

A powerful console multitool for Telegram. This is not just a bot; it's a true Swiss Army knife for managing chats, sending media, spamming, and even playing music straight from your command line!

## 🚀 Core Features:
* **Section 1: Text** — Send regular, HTML-formatted, encrypted (Base64), and secret (spoiler) text. Includes a "Typing..." effect, reverse text, and CAPS.
* **Section 2: Media** — The bot automatically detects the file type (photo, video, audio, sticker). Send locations, fake contacts, and video notes.
* **Section 3: Spam Zone** — Text and file spam. Includes "Smart Spam" (random delays) and an "Infinite" mode. Also, stone spam 🗿.
* **Section 4: Tricks** — Create polls, pin messages, and send interactive emojis (dice, darts, roulette, basketball, football).
* **Section 5: Admin Panel** — Mute all members, change group title/description, kick and ban (by ID or @username), delete messages.
* **Section 6: Settings** — Set bot commands (the `/` menu button in Telegram) and change the profile description.
* **Section 7: Info** — Display bot profile, ping to servers, and chat stats.
* **Section 8: Guide** — Built-in help that explains every single function.
* **Section 9: Music** — Full local player. Play track, pause, stop, smooth volume control, and current status display.
* **Section 10: Theme Settings** — Customize your console appearance! Choose from 6 colors (red, green, blue, etc.) or a "Rainbow" mode for color-shifting text.
* **Section 11: Utilities** — Base64 decoder, strong password generator, and an in-console calculator.
* **Section 12: Timer (Delayed)** — Send messages with a custom delay in the background without freezing the panel.
* **Section 13: Special Ops** — Coin flip (Heads/Tails), Rock-Paper-Scissors, and custom emoji spam.
* **Section 14: User Info** — Retrieve Telegram user information by ID or @username (name, status).
* **Section 15: System** — View the bot's uptime and current OS information.
* **Section 16: Fake Generator** — Generate not only identities and cards, but also passports, driver's licenses, medical records, diplomas, and tech data (IP, MAC, UUID).
* **Section 17: OSINT Check** — Analyze phones, emails, nicknames, and full names. Expanded link list for search (Truecaller, Avito, HIBP, TikTok, Twitch, LinkedIn, etc.).

## 📱 Remote Control from Telegram (NEW!)

You can now manage the panel directly from the chat! The bot runs in the background and listens for commands:

* 🔄 `/bot_nahui_perezagruska` — **Restart Bot**. The script completely reboots (console closes and reopens).
* 🔴 `/bot_nahui_virubis` — **Shutdown Panel**. The console hides in the system, but the bot stays online in the background.
* 🟢 `/bot_nahui_zapuskaisa` — **Start Panel**. The console window pops back up.

*(Note: after starting the panel via Telegram, press Enter in the console to refresh the menu).*

## 🛠 Installation & Setup

1. **Install Python** (version 3.9 or higher).
2. **Download the project** and open a terminal in the bot's folder.
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt


Configure the bot

Find config_example.py and rename it to config.py.

Paste your token from @BotFather.

Paste your CHAT_ID (you can get it using @userinfobot, don't forget the minus sign at the beginning).

Run the bot:
python main.py

⚠️ Important Warnings

## ⚙️ Telegram Bot Settings

For the bot to work correctly, you need to configure it properly through **@BotFather**.

1. **Disable Group Privacy:**
   * Send the `/setprivacy` command to **@BotFather**.
   * Choose your bot.
   * Click the **Disable** button.
   * *(This is required so the bot can freely read and send messages in groups)*.
2. **Allow Groups:**
   * Send the `/setjoingroups` command.
   * Choose your bot.
   * Click the **Enable** button.
3. **Grant Admin Rights:**
   * Add the bot to your group or channel.
   * Go to group settings -> Members -> promote the bot to **Administrator** (this is mandatory for the "Admin Panel" and Spam features to work).

VPN for Russia: If you are located in Russia, you MUST enable a VPN before running the bot. Telegram blocks direct requests to api.telegram.org from Russian IPs.

Flood Control: Do not spam with a delay of less than 1 second. Telegram will throw a FloodWait error (banning the bot from sending messages for 5-10 minutes).

Bot Rights: For the Admin Panel to work, the bot must be an administrator in the group

