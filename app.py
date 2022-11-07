import telebot
from telebot import types

bot = telebot.TeleBot('5551745701:AAEE83IgU5-GpeIIDAcHGx7tBdBt3IuKXeI')
CURRENT_COMMON_BALLANSE_PATH = "сdata.txt"

users = {"929204332": "Миша","1629565067":"Илья","1410517822":"Эля"}

def get_current_balans(path):
    file = open(path, 'r')

    try:
        result =  float(file.read())
    except ValueError:
        result =  float(0)
    file.close()
    return result

def write_to_file(amount, user):
    file = open(str(user)  + ".txt", 'w')
    file.write(str(amount))
    file.close


def write_to_own(user, number):
    current_balans = get_current_balans(str(user) + ".txt")
    new_value = current_balans - number
    write_to_file(new_value, user)
    bot.send_message(user, "Записано в личные траты, баланс: " + str(new_value))

def write_to_common(user, number):
    current_balans = get_current_balans("сdata.txt")
    new_value = current_balans - number
    write_to_file(new_value, "сdata")
    for user in users:
        bot.send_message(user, users[str(user)] +  " потратил общак\nОбщий баланс: "+ str(new_value) + "₾")


def write_to_alice(user, number):
    bot.send_message(str(929204332), users[str(user)] +  " потратил на алису\n "+ str(number) + "₾")
    bot.send_message(str(1410517822), users[str(user)] +  " потратил на алису\n "+ str(number) + "₾")
    write_to_own(929204332, number / 2)
    write_to_own(1410517822, number / 2)





@bot.message_handler()
def get_user_text(message):
    user = message.chat.id

    if user == 929204332 or user == 1629565067 or user == 1410517822:
        data = message.text.split()
        text = data[0]
        if len(data) > 1:
            category = data[1]
            if user == 929204332 or user == 1629565067 or user == 1410517822:
                try:
                    new_number = int(text)/1
                    is_number = True
                except ValueError:
                    try:
                        new_number = float(text)
                        is_number = True
                    except ValueError:
                        bot.send_message(user, "Число написано плохо")
                        is_number = False

                if is_number:
                    if category == 'л' or category == 'Л':
                        write_to_own(user, new_number)
                    elif category == 'о' or category == 'О':
                        write_to_common(user, new_number)
                    elif category == 'а' or category == 'А':
                        write_to_alice(user, new_number)
                    else:
                        bot.send_message(user, category)
                        bot.send_message(user, "Введи категорию нормально: Л - личные, О - общие, А - на Алису")
        else:
            bot.send_message(user, "Не распознано, введи значение и категорию правильно: Л - личные, О - общие, А - на Алису")

            bot.send_message(user, "Твой баланс: " + str(get_current_balans(str(user) + ".txt")) + " ₾\nОбщий баланс: " + str(get_current_balans("сdata.txt")))
    else:
        bot.send_message(user, "Вам тут не рады")




if __name__ == '__main__':
    bot.polling(none_stop=True)