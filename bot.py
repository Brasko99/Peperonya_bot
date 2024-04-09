import telebot
from telebot import types
import json 
import subprocess
import os
import time


TOKEN = "7050930461:AAEyhz6SLz5mX2NShlLmaX071eO8mOUQmV8"
bot = telebot.TeleBot(TOKEN)
###Создаем папку для отработки поиска по ключевому слову. Он будет хранить не более 10 файлов .txt
if not os.path.exists('Search_history'):
    os.mkdir('Search_history')
###Создаем файл для хранения badwords
filename = "badwords.txt"
if not os.path.exists(filename):
    with open(filename, 'w'):
        pass    
###Создаем файл для хранения списка администраторов
filename = "admins.txt"
if not os.path.exists(filename):
    with open(filename, 'w'):
        pass
###Создаем файл для хранения списка администраторов
filename = "search_scripts.txt"
if not os.path.exists(filename):
    with open(filename, 'w'):
        pass
###Список переменных для переменного окружения
os.environ['COMMENT_CHANNEL'] = '@channel'


###Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    if if_admin(message):
        bot.send_message(message.chat.id, f"Привет! Я бот пепероня и я помогаю с работой в телеграмм ☺️\nВыберите в меню что именно вы хотите сделать)")


###Функция для проверки на администратора бота
def if_admin(message):
    with open('admins.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    values = data.split('\n')
    username = message.from_user.username
    if username in values:
        return True
    else:
        bot.send_message(message.chat.id, 'Вы не являетесь администратором бота. К сожалению, я не могу с Вами разговаривать 😔')
        return False


###Добавление/удаление администраторов
@bot.message_handler(commands=["admin"])
def admin_main(message):
    if if_admin(message):
        bot.send_message(message.chat.id, '🍕 Выберите функцию:\n\n/new_admin - добавить администратора\n/delete_admin - убрать администратора\n/show_admins - показать всех администраторов')


###Добавить администратора
@bot.message_handler(commands=["new_admin"])
def new_admin(message):
    if if_admin(message):
        bot.send_message(message.chat.id, 'Чтобы добавить администратора напишите мне его никнейм без "@".\n◽️ Пример:\n\nvova_vova123.')
        bot.register_next_step_handler(message, new_admin2)
def new_admin2(message):
    word = message.text.lower()
    with open('admins.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    values = data.split('\n')
    if word not in values:    
        with open('admins.txt', 'a', encoding='utf-8') as file:
            file.write(f"{word}\n")
        bot.send_message(message.chat.id, f"✅ Администратор \"{word}\" добавлен в список администраторов\n\n/new_admin - добавить ещё одного администратора\n/admin - назад")
    else:
        bot.send_message(message.chat.id, f"✅ Администратор \"{word}\" уже есть в списке администраторов\n\n/new_admin - добавить ещё одного администратора\n/admin - назад")


###Удалить администратора из списка
@bot.message_handler(commands=["delete_admin"])
def delete_admin(message):
    if if_admin(message):
        bot.send_message(message.chat.id, 'Чтобы удалить администратора напишите мне его никнейм без "@".\n◽️ Пример:\n\nvova_vova123')
        bot.register_next_step_handler(message, delete_admin2)
def delete_admin2(message):
    del_admin = message.text
    with open('admins.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    with open('admins.txt', 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip() != del_admin:
                file.write(line)
    bot.send_message(message.chat.id, f"✅ Администратор \"{del_admin}\" удален из списка администраторов\n\n/delete_admin - удалить ещё одного администратора\n/admin - назад")


###Показать список администраторов
@bot.message_handler(commands=["show_admins"])
def show_admins(message):
    if if_admin(message):
        with open('admins.txt', 'r', encoding='utf-8') as file:
            bot.send_message(message.chat.id, f"🍕 Список администраторов:\n\n{', '.join([line.strip() for line in file])}\n\n/admin - назад")
        admin_main(message)


###Управление модератором комментариев
@bot.message_handler(commands=["moderator"])
def moderation(message):
    if if_admin(message):
        bot.send_message(message.chat.id, '🍕 Выберите функцию модератора:\n\n/change_forward_channel - сменить канал для пересылки комментариев\n/add_word - добавить слово в словарь\n/remove_word - удалить слово из словаря\n/show_bad_words - показать все слова из словаря\n/clear_badwords - очистить словарь')


###Смена канала для приема комментариев
@bot.message_handler(commands=["change_forward_channel"])
def com_dump(message):
    if if_admin(message):
        frwrd_chnnl = os.environ.get('COMMENT_CHANNEL')
        bot.send_message(message.chat.id, f'Канал для пересылки комментариев: {frwrd_chnnl}\nЧтобы сменить канал, в который будут пересылаться все комментарии сообщества, отправьте мне его юзернейм.\n◽️ Пример:\n\n@channel')
        bot.register_next_step_handler(message, Save_channels_with_comments)
def Save_channels_with_comments(message):    
    if '@' in message.text:
        try:
            channel = message.text  
            bot.send_message(channel, 'Проверочное сообщение!')
            os.environ['COMMENT_CHANNEL'] = message.text
            bot.send_message(message.chat.id, '✅ Канал для приема комментариев успешно установлен!\n\n/moderator - назад')
            moderation(message)
        except Exception: 
            bot.send_message(message.chat.id, '❗️ Боту не удалось отправить сообщение. Пожалуйста проверьте настройки доступа в указанный канал!\n\nПосле того как вы убедились что канал открыт для бота, отправьте его никнейм снова. Пример:\n@channel')     
            bot.register_next_step_handler(message, Save_channels_with_comments)
    else:
        bot.send_message(message.chat.id, '❗️ Неверный формат! Отправьте ещё раз в нужном формате. Пример:\n\n@channel')
        bot.register_next_step_handler(message, Save_channels_with_comments)


# Команда для добавления слова в файл badwords.txt
@bot.message_handler(commands=['add_word'])
def add_word_to_badwords(message):
    if if_admin(message):
        bot.send_message(message.chat.id, 'Чтобы добавить слово в словарь просто напишите мне его.\n\nP.S. Регистр букв не важен, бот обработает любую вариацию этого слова из больших и маленьких букв.')
        bot.register_next_step_handler(message, add_word_to_badwords2)
def add_word_to_badwords2(message):    
    word = message.text.lower()
    with open('badwords.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    values = data.split('\n')
    if word not in values:    
        with open('badwords.txt', 'a', encoding='utf-8') as file:
            file.write(f"{word}\n")
        bot.send_message(message.chat.id, f"✅ Слово \"{word}\" добавлено в словарь запрещенных слов\n\n/add_word - добавить ещё одно слово\n/moderator - назад")
    else:
        bot.send_message(message.chat.id, f"✅ Слово \"{word}\" уже есть в словаре запрещенных слов\n\n/add_word - добавить ещё одно слово\n/moderator - назад")


# Команда для показа текущего списка запрещенных слов
@bot.message_handler(commands=['show_bad_words'])
def show_bad_words(message):
    if if_admin(message):
        with open('badwords.txt', 'r', encoding='utf-8') as file:
            bot.send_message(message.chat.id, f"Список запрещенных слов:\n\n{', '.join([line.strip() for line in file])}\n\n/moderator - назад")


# Команда для удаления слова из файла badwords.txt
@bot.message_handler(commands=['remove_word'])
def remove_word_from_badwords(message):
    if if_admin(message):
        bot.send_message(message.chat.id, 'Чтобы убрать слово из словаря просто напишите мне его.\n\nP.S. Регистр букв не важен, бот обработает любую вариацию этого слова из больших и маленьких букв.')
        bot.register_next_step_handler(message, remove_word_from_badwords2)
def remove_word_from_badwords2(message):
    word_to_remove = message.text.lower()
    with open('badwords.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    with open('badwords.txt', 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip() != word_to_remove:
                file.write(line)
    bot.send_message(message.chat.id, f"✅ Слово \"{word_to_remove}\" удалено из списка запрещенных слов\n\n/remove_word - добавить ещё одно слово\n/moderator - назад")


### Команда для очистки файла badwords.txt
@bot.message_handler(commands=['clear_badwords'])
def clear_bad_words(message):
    if if_admin(message):
        open('badwords.txt', 'w').close()
        bot.reply_to(message, "✅ Список запрещенных слов очищен\n\n/moderator - назад")
        

###Информация и настройка скриптов для поиска
@bot.message_handler(commands=["keyword_find"])
def keyword_find(message):
    bot.send_message(message.chat.id, '🍕 Выберите функцию:\n\n/new_scripts - добавить новый скрипт в панель\n/delete_scripts - удалить скрипт из панели\n/keyword_search - осуществить поиск по ключевому слову')


###Добавить скрипт в панель
@bot.message_handler(commands=["new_scripts"])
def new_scripts(message):
    if if_admin(message):
        bot.send_message(message.chat.id, 'Чтобы добавить новый скрипт напишите мне его в формате.')
        bot.send_message(message.chat.id, 'Напишите: \n1. Название канала, в которм будем искать\n2. Сколько последних постов будем проверять\n3. Ключевое слово для поиска (Регистр важен!)\n4. В какой канал сохраняем\n\n◽️ Пример ввода:\nSearch_channel 10 keyword my_channel')
        bot.register_next_step_handler(message, new_scripts2)
def new_scripts2(message):
    word = message.text.lower()
    with open('search_scripts.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    values = data.split('\n')
    if word not in values:    
        with open('search_scripts.txt', 'a', encoding='utf-8') as file:
            file.write(f"{word}\n")
        bot.send_message(message.chat.id, f"Скрипт успешно добавлен в панель\n\n/new_scripts - добавить ещё скрипт\n/keyword_search - осуществить поиск по ключевому слову")


###Убрать скрипт из панели
@bot.message_handler(commands=["delete_scripts"])
def delete_scripts(message):
    if if_admin(message):
        bot.send_message(message.chat.id, 'Чтобы убрать скрипт напишите мне его в таком же формате, как он представлен ниже (можно просто скопировать из сообщения).')
        with open('search_scripts.txt', 'r', encoding='utf-8') as file:
            data = file.read()
        values = data.split('\n')
        text = ""
        for value in values:
            text += value + "\n\n"
        bot.send_message(message.chat.id, f'◽️ Список имеющихся скриптов:\n\n{text}')    
        bot.register_next_step_handler(message, delete_scripts2)
def delete_scripts2(message):
    script_to_remove = message.text
    with open('search_scripts.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open('search_scripts.txt', 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip() != script_to_remove:
                file.write(line)
    bot.send_message(message.chat.id, f"✅ Скрипт успешно удален из списка.\n\n/delete_scripts - удалить ещё скрипт\n/keyword_search - осуществить поиск по ключевому слову")


###Поиск по ключевому слову в указанной группе на указанное количество постов
@bot.message_handler(commands=["keyword_search"])
def keyword_search(message):
    if not os.path.exists('./Search_history'):
        os.makedirs('./Search_history')
    with open('search_scripts.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    values = data.split('\n')
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(value) for value in values])      
    bot.send_message(message.chat.id, 'Напишите: \n1. Название канала, в которм будем искать\n2. Сколько последних постов будем проверять\n3. Ключевое слово для поиска (Регистр важен!)\n4. В какой канал сохраняем\n\n◽️ Пример ввода:\nSearch_channel 10 keyword my_channel ', reply_markup=keyboard)
    bot.register_next_step_handler(message, send_posts)
def collect_posts(channel, keyword):
    with open(f"./Search_history/{channel}.txt") as file:
        file = file.readlines()
    posts = []
    for n, line in enumerate(file):
        file[n] = json.loads(file[n])
        links = [link for link in file[n]['outlinks'] if channel not in link]
        p = str(file[n]['content']) + "\n" + str("\n".join(links) + "\n\n\n" + str(file[n]['url']) + "\n" + str(file[n]['date'].split("T")))
        if keyword in p:
            posts.append(p)
    return posts 
def upload_posts(num_posts, channel):
    command = f'snscrape --max-result {num_posts} --jsonl telegram-channel {channel} > ./Search_history/{channel}.txt'
    subprocess.run(command, shell=True)
def send_posts(message):
    try:
        channel, num_posts, keyword, target_channel = str(message.text).split()
        target_channel = "@"+target_channel

        upload_posts(num_posts, channel)
        posts = collect_posts(channel, keyword)
        while posts:
            bot.send_message(target_channel, posts.pop())
            time.sleep(1)
        
        bot.reply_to(message, "✅ Поиск завершен, все посты отправлены в указанную группу 🥳\n\nP.S. Если ничего не отправлено - постов, содержащих данное слово среди изученых нет.\nP.S.S. На всякий случай можете попробовать заглавные буквы или склонения. Поиск строгий, поэтому может пропустить пост с аналогичным словом с заглавной буквы, например.", reply_markup=None)
        clear_search_history()
    except:
        bot.reply_to(message, "❗️ Неправильный формат 🥲\nНажми /keyword_find, чтобы увидеть правильный формат ввода", reply_markup=None)


###Очищаем историю (удаляем 2 самых старых, если файлов больше 10)
def clear_search_history():
    directory = './Search_history'
    files = os.listdir(directory)
    if len(files) > 10:
        # Сортируем файлы по времени последнего доступа (самые старые файлы будут в начале списка)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        # Удаляем два самых старых файла
        for i in range(len(files) - 10):
            os.remove(os.path.join(directory, files[i]))


###Модерация и пересылка комментариев
@bot.message_handler(func=lambda message: True)
def check_bad_words_and_forward(message):
    if check_bad_words(message):
        bot.delete_message(message.chat.id, message.message_id)
    else:
        frwrd_chnnl = os.environ.get('COMMENT_CHANNEL')
        if message.reply_to_message:
            if message.chat.id != message.from_user.id:
                bot.send_message(frwrd_chnnl, f"{'@' + message.from_user.username}\n\n{message.text}")
def check_bad_words(message):
    bad_word_found = False
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_username = message.from_user.username
    text = message.text.lower()
    with open('badwords.txt', 'r', encoding='utf-8') as file:
        bad_words = [line.strip() for line in file]
    try:
        with open('warnings.txt', 'r') as file:
            warnings = json.load(file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        warnings = {}
    for word in bad_words:
        if word.lower() in text:            
            if user_username not in warnings:
                warnings[user_username] = 1
                bot.reply_to(message, f"Предупреждение 1: @{user_username}, пожалуйста, не используйте плохие слова.")
                bad_word_found = True
                break
            elif warnings[user_username] == 1:
                warnings[user_username] = 2
                bot.reply_to(message, f"Предупреждение 2: @{user_username}, пожалуйста, не используйте плохие слова. Последнее предупреждение перед блокировкой возможности комментирования.")
                bad_word_found = True
                break
            else:
                bot.restrict_chat_member(chat_id, user_id, can_send_messages=False)
                bot.reply_to(message, f"@{user_username}, Вы заблокированы за использование плохих слов.")                
                bad_word_found = True
                break
    with open('warnings.txt', 'w') as file:
        json.dump(warnings, file)
    return bad_word_found


bot.polling(non_stop=True)    
