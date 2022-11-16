from random import seed, randrange
from time import time



import telebot
from telebot import types

bot = telebot.TeleBot(TOKEN)

bot.set_my_commands([
    telebot.types.BotCommand("/start", "Начать работу"),
    telebot.types.BotCommand("/help", "Памагити"),
    telebot.types.BotCommand("/ban", "Забанить пользователя(нужно ответить на его сообщение), доступно только админам"),
    telebot.types.BotCommand("/unban", "Разбанить пользователя(нужно ответить на его сообщение), доступно только админам"),
    telebot.types.BotCommand("/promote", "Сделать пользователя админом(нужно ответить на его сообщение), доступно только админам"),
    telebot.types.BotCommand("/statistics", "Получить стастистику"),
    telebot.types.BotCommand("/leave", "Заставить бота уйти из чата")
])


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Вот что я умею: \n'+
                                      '1) Помогать админиминистратором банить/разбанить/сделать админом человека\n' +
                                      '2) Получить статистику по чату\n' +
                                       '3) Уйти из чата(\n' +
                                       '4) Приветствовать новых участников\n')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Привет! Я могу помочь с администрированием группы.')


@bot.message_handler(commands=['ban'])
def ban(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).can_restrict_members != True and bot.get_chat_member(
            message.chat.id, message.from_user.id).status != "creator":
        bot.send_message(message.chat.id,
                         f'{message.from_user.username}, у вас нет прав для совершения действия!')
        return
    if message.reply_to_message is not None:
        user_id_to_ban = message.reply_to_message.from_user.id
        if user_id_to_ban == bot.user.id:
            bot.send_message(message.chat.id, f'Не могу заблокировать себя(((')
            return
        if bot.get_chat_member(message.chat.id, user_id_to_ban).status in ["kicked", "left"]:
            bot.send_message(message.chat.id, f'Пользователь {message.reply_to_message.from_user.username} уже заблокирован или вышел из чата.')
        else:
            result = bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id_to_ban)
            if result:
                bot.send_message(message.chat.id, f'Пользователь {message.reply_to_message.from_user.username} успешно заблокирован!')
            else:
                bot.send_message(message.chat.id, f'Не получилось(')
    else:
        bot.send_message(message.chat.id, f'Что-то пошло не так! Чтобы заблокировать пользователя нужно ответить на его сообщение текстом /ban.')

@bot.message_handler(commands=['unban'])
def unban(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).can_restrict_members != True and bot.get_chat_member(message.chat.id, message.from_user.id).status != "creator":
        bot.send_message(message.chat.id,
                         f'{message.from_user.username}, у вас нет прав для совершения действия!')
        return
    if message.reply_to_message is not None:
        user_id_to_unban = message.reply_to_message.from_user.id
        if bot.get_chat_member(message.chat.id, user_id_to_unban).status in ["kicked"]:
            result = bot.unban_chat_member(chat_id=message.chat.id, user_id=user_id_to_unban, only_if_banned=True)
            if result:
                bot.send_message(message.chat.id,
                                 f'Пользователь {message.reply_to_message.from_user.username} успешно разблокирован!')
            else:
                bot.send_message(message.chat.id, f'Не получилось(')
        else:
            bot.send_message(message.chat.id,
                             f'Пользователь {message.reply_to_message.from_user.username} не заблокирован в чате.')
    else:
        bot.send_message(message.chat.id, f'Что-то пошло не так! Чтобы разблокировать пользователя нужно ответить на его сообщение текстом /unban.')

@bot.message_handler(commands=['promote'])
def promote(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).can_restrict_members != True and bot.get_chat_member(message.chat.id, message.from_user.id).status != "creator":
        bot.send_message(message.chat.id,
                         f'{message.from_user.username}, у вас нет прав для совершения действия!')
        return
    if message.reply_to_message is not None:
        user_id_to_promote = message.reply_to_message.from_user.id
        status = bot.get_chat_member(message.chat.id, user_id_to_promote).status
        if status in ["kicked", "left"]:
            bot.send_message(message.chat.id, f'Пользователь  {message.reply_to_message.from_user.username} уже заблокирован или вышел из чата.')
        elif status in ["creator", "administrator"]:
            bot.send_message(message.chat.id, f'Пользователь  {message.reply_to_message.from_user.username} уже является администратором или владельцем группы.')
        else:
            result = bot.promote_chat_member(chat_id=message.chat.id, user_id=user_id_to_promote,
                                            can_delete_messages=True, can_restrict_members=True,
                                            can_promote_members=True, can_change_info=True, can_invite_users=True,
                                            can_pin_messages=True, can_manage_chat=True, can_manage_video_chats=True)
            if result:
                bot.send_message(message.chat.id, f'Пользователь {message.reply_to_message.from_user.username} успешно стал администратором!')
            else:
                bot.send_message(message.chat.id, f'Не получилось(')
    else:
        bot.send_message(message.chat.id, f'Что-то пошло не так! Чтобы сделать пользователя  администратором нужно ответить на его сообщение текстом /promote.')


@bot.message_handler(commands=['leave'])
def leave(message):
    bot.send_message(message.chat.id, f'Пока-пока!')
    bot.leave_chat(message.chat.id)

@bot.message_handler(commands=['statistics'])
def statistics(message):
    bot.send_message(message.chat.id, f'Количество участников группы: {bot.get_chat_member_count(message.chat.id)} \n'
                                      f'Количество админов: {len(bot.get_chat_administrators(message.chat.id))}')
@bot.message_handler(content_types=["new_chat_members"])
def new_member(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_1 = types.KeyboardButton("Да!!!!")
    item_2 = types.KeyboardButton("ОЧЕНЬ")
    markup.add(item_1, item_2)
    bot.send_message(message.chat.id, f'{message.from_user.username}, вы любите папугов?', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def hide_keybord(message):
    if message.text in ["Да!!!!", "ОЧЕНЬ"] and message.reply_to_message is not None and message.reply_to_message.text == f"{message.from_user.username}, вы любите папугов?":
        bot.send_message(message.chat.id, text = "Поздравляю, ты прошел проверку!", reply_markup=types.ReplyKeyboardRemove())

bot.polling(timeout=1, interval=0)

