import os
import telebot
#from keep_alive import keep_alive
import requests


#keep_alive()

bot = telebot.TeleBot(os.environ['TOKEN'])

user_names = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_names[user_id] = user_name
    bot.reply_to(message, f"Hey My Love {user_name} ! Please Talk With Me 😘")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text:
        user_id = message.from_user.id
        response_message = get_brainshop_response(message.text, user_id)
        bot.reply_to(message, response_message)
    elif message.photo:
        handle_photo_message(message)


def get_brainshop_response(text, user_id):
    user_name = user_names.get(user_id, "User")
    api_url = f"http://api.brainshop.ai/get?bid=177202&key=QJWn3z1t6mYrYs1J&uid={user_id}&msg={text}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        response_data = response.json()
        return f" {response_data['cnt']}"
    except requests.exceptions.RequestException as e:
        return "404 Error Found @KWEL999 "

def handle_photo_message(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"
    
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        
        photo_file_path = f"downloaded_photos/{file_path}"
        os.makedirs(os.path.dirname(photo_file_path), exist_ok=True)
        with open(photo_file_path, 'wb') as photo_file:
            photo_file.write(response.content)
        
        bot.reply_to(message, "Thanks for the photo!")
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, "Sorry, I couldn't download the photo. Error: " + str(e))

bot.polling(non_stop=True)
