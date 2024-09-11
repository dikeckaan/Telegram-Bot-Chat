import os
import telebot
import time
import threading
from dotenv import load_dotenv

# .env dosyasını yükleyin
load_dotenv()

# .env dosyasından token ve forward chat ID'sini alıyoruz
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_CHAT_ID = os.getenv("FORWARD_CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)

# Banlı kullanıcıları sakladığımız dosyanın adı
BANNED_USERS_FILE = 'banned_users.txt'

# Banlı kullanıcıları dosyadan oku
def load_banned_users():
    if not os.path.exists(BANNED_USERS_FILE):
        return []
    with open(BANNED_USERS_FILE, 'r') as file:
        banned_users = file.read().splitlines()
        return [int(user_id) for user_id in banned_users]

# Banlı kullanıcıları dosyaya yaz
def save_banned_users():
    with open(BANNED_USERS_FILE, 'w') as file:
        for user_id in banned_users:
            file.write(f"{user_id}\n")

# Banlı kullanıcıları saklamak için bir liste
banned_users = load_banned_users()

# Dosyayı düzenli olarak kontrol eden fonksiyon
def monitor_banned_users():
    global banned_users
    while True:
        time.sleep(5)  # Her 5 saniyede bir dosyayı kontrol et
        updated_banned_users = load_banned_users()
        if updated_banned_users != banned_users:
            banned_users = updated_banned_users
            print("Banned users list updated from file.")

# Dosya kontrolünü arka planda çalıştır
threading.Thread(target=monitor_banned_users, daemon=True).start()

# Chat ID öğrenmek için /start komutu ile mesaj gönderiyoruz
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot çalışıyor! Komutları dinliyor...")

# Gelen mesajların logunu oluşturup bot sahibine gönderen fonksiyon
def log_message(message):
    if str(message.chat.id) != OWNER_CHAT_ID:  # Admin değilse logla
        user = message.from_user
        log_text = f"Kullanıcı: {user.first_name} {user.last_name or ''} (ID: {user.id}) bir mesaj gönderdi."
        bot.send_message(OWNER_CHAT_ID, log_text)

# Ban komutu ile kullanıcıyı engelleme
@bot.message_handler(func=lambda message: message.reply_to_message and message.text.lower() == "ban")
def ban_user(message):
    try:
        if str(message.chat.id) == OWNER_CHAT_ID:  # Sadece admin komutu kullanabilir
            banned_user_id = message.reply_to_message.forward_from.id  # Banlanan kullanıcının ID'si
            if banned_user_id not in banned_users:
                banned_users.append(banned_user_id)  # Kullanıcıyı banlananlar listesine ekle
                save_banned_users()  # Banlı kullanıcıları dosyaya kaydet
                bot.send_message(banned_user_id, "Üzgünüz, banlandınız.")  # Kullanıcıya bilgi mesajı gönder
                bot.reply_to(message, f"Kullanıcı (ID: {banned_user_id}) başarıyla banlandı.")
            else:
                bot.reply_to(message, f"Kullanıcı (ID: {banned_user_id}) zaten banlanmış.")
        else:
            bot.reply_to(message, "Bu komutu sadece admin kullanabilir.")
    except Exception as e:
        print(f"Kullanıcı banlanırken hata oluştu: {e}")
        bot.reply_to(message, f"Kullanıcı banlanırken hata oluştu: {e}")

# Unban komutu ile kullanıcıyı engelini kaldırma
@bot.message_handler(func=lambda message: message.reply_to_message and message.text.lower() == "unban")
def unban_user(message):
    try:
        if str(message.chat.id) == OWNER_CHAT_ID:  # Sadece admin komutu kullanabilir
            unbanned_user_id = message.reply_to_message.forward_from.id  # Unbanlanan kullanıcının ID'si
            if unbanned_user_id in banned_users:
                banned_users.remove(unbanned_user_id)  # Kullanıcıyı banlananlar listesinden çıkar
                save_banned_users()  # Banlı kullanıcıları dosyaya kaydet
                bot.send_message(unbanned_user_id, "Banınız kaldırıldı, artık mesaj gönderebilirsiniz.")  # Kullanıcıya bilgi mesajı gönder
                bot.reply_to(message, f"Kullanıcı (ID: {unbanned_user_id}) başarıyla unbanlandı.")
            else:
                bot.reply_to(message, f"Kullanıcı (ID: {unbanned_user_id}) zaten banlanmamış.")
        else:
            bot.reply_to(message, "Bu komutu sadece admin kullanabilir.")
    except Exception as e:
        print(f"Kullanıcı unbanlanırken hata oluştu: {e}")
        bot.reply_to(message, f"Kullanıcı unbanlanırken hata oluştu: {e}")

# Mesajları kontrol eden handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        if message.from_user.id in banned_users:
            bot.send_message(message.chat.id, "Üzgünüz, banlandınız. Artık mesaj gönderemezsiniz.")
            return

        log_message(message)  # Mesajı logla

        # Eğer bu bir reply ise
        if message.reply_to_message and message.chat.id == int(OWNER_CHAT_ID):
            if message.reply_to_message.forward_from:
                original_sender_id = message.reply_to_message.forward_from.id
                reply_message = message.text

                bot.send_message(original_sender_id, reply_message)
                bot.send_message(message.chat.id, f"Mesaj başarıyla orijinal kullanıcıya gönderildi.")
            else:
                bot.reply_to(message, "Yanıt verilen mesaj forward edilmemiş.")
        elif str(message.chat.id) != OWNER_CHAT_ID:
            bot.forward_message(OWNER_CHAT_ID, message.chat.id, message.message_id)
            bot.reply_to(message, "Mesajınız iletildi.")
    except Exception as e:
        print(f"Yanıt gönderilirken hata oluştu: {e}")
        bot.send_message(message.chat.id, f"Yanıt gönderilirken hata oluştu: {e}")

# Botu başlat
print("Bot çalışıyor ve komutları dinliyor...")
bot.polling(none_stop=True)
