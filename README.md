# Telegram-Bot-Chat

This project is a Telegram bot designed to manage incoming messages and ban/unban users. The admin can ban/unban users and forward incoming messages to the bot owner.

## Features

- **Ban Functionality:** The admin can ban a user, preventing them from sending messages.
- **Unban Functionality:** The admin can unban a previously banned user.
- **Message Forwarding:** Messages sent by users are forwarded to the bot owner (admin).
- **Content Types:** The bot supports handling various content types such as text messages, photos, videos, voice notes, GIFs, documents, and stickers.
- **Banned User Management:** Banned users are stored in a `banned_users.txt` file, ensuring that the list persists even if the bot is restarted.
- **Dynamic File Monitoring:** The `banned_users.txt` file is monitored every 5 seconds, and any manual changes to it are automatically detected.

## Requirements

To run this bot, the following software and libraries are required:

- Python 3.7+
- `pyTelegramBotAPI`
- `python-dotenv` (to load environment variables from a `.env` file)

## Setup Instructions

### 1. Clone the Repository:

```bash
git clone https://github.com/dikeckaan/Telegram-Bot-Chat.git
cd Telegram-Bot-Chat
```

### 2. Install Dependencies:

```bash
pip install pyTelegramBotAPI python-dotenv
```

### 3. Configure Bot Token and Admin Chat ID:

Create a `.env` file in the root directory of the project and add the following information:

```bash
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
FORWARD_CHAT_ID=your-admin-chat-id
```

- `TELEGRAM_BOT_TOKEN`: The token for your bot, which you can get from [BotFather](https://core.telegram.org/bots#botfather).
- `FORWARD_CHAT_ID`: The Telegram chat ID of the bot owner (admin) who will receive forwarded messages.

### 4. Run the Bot:

```bash
python bot.py
```

The bot will now start listening for messages, and any user who is banned will not be able to send messages.

## Bot Commands and Usage

- **/start**: Start the bot and receive a welcome message.
- **Ban a User**: The admin replies to a user’s message with the text "ban" to block that user.
- **Unban a User**: The admin replies to a banned user's message with "unban" to unblock them.

### Example Scenarios

1. **Banning a User**:
   - When the admin replies "ban" to a message, the user is banned, and their messages will no longer be forwarded. The user will also receive a notification: "You have been banned."

2. **Unbanning a User**:
   - When the admin replies "unban" to a message, the user is unbanned, and they can start sending messages again. The user will also receive a notification: "Your ban has been lifted."

## File Management

The bot stores the list of banned users in the `banned_users.txt` file. This list is checked every 5 seconds for updates, meaning if the file is manually edited (to add or remove a banned user), the changes will be reflected in the bot's behavior.

### Dynamic Ban List Checking

The bot continuously checks the `banned_users.txt` file and updates the ban list accordingly. This allows for dynamic management of banned users without needing to restart the bot.

## Contributions

If you'd like to contribute to this project, feel free to fork the repository, create a branch, and submit a pull request. Your contributions are welcome!

## License

This project is licensed under the MIT License.

---

