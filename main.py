import telebot
from telebot import types
import requests

bot = telebot.TeleBot('u token')



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    mess = f"Привет, <b>{message.from_user.first_name}</b>"

    info = types.KeyboardButton('💬 О Боте')
    git = types.KeyboardButton('♻ GitHub')
    main = types.KeyboardButton('Главное меню')

    markup.add(info, git, main)
    bot.send_message(message.chat.id, mess, parse_mode="html", reply_markup=markup)


@bot.message_handler(commands=['main'])
def start_inline(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    add_process = types.InlineKeyboardButton('➕ Добавить процесс', callback_data='ap')
    view_process = types.InlineKeyboardButton('🔍 Просмотр доступных процессов', callback_data='vp')
    delete_process = types.InlineKeyboardButton('❌ Удаление доступных процессов', callback_data='dp')
    run_process = types.InlineKeyboardButton('✅ Запустить доступный процесс', callback_data='rp')

    markup.add(add_process, view_process, delete_process, run_process)
    bot.send_message(message.chat.id, "Возможные действия", reply_markup=markup)

list_proc = set()

def create_proc(owner, repo, workflow):
    return owner + ", " + repo + ", " + workflow

g_owner = ""
g_repo = ""
g_work = ""
g_token = ""
g_ref = ""

@bot.message_handler(commands=['list'])
def show_list(message):
    if len(list_proc) == 0:
        bot.send_message(message.chat.id, "Нет доступных процессов")
    else:
        bot.send_message(message.chat.id, "\n".join(list_proc))


@bot.message_handler(commands=['fill'])
def add_start(message):
    m = bot.send_message(message.chat.id, "Введите owner ")
    bot.register_next_step_handler(m, add_owner)

def add_owner(message):
    print(1)
    global g_owner
    g_owner = message.text
    m = bot.send_message(message.chat.id, "Введите repo ")
    bot.register_next_step_handler(m, add_repo)

def add_repo(message):
    print(2)
    global g_repo
    g_repo = message.text
    m = bot.send_message(message.chat.id, "Введите workflow ")
    bot.register_next_step_handler(m, add_work)

def add_work(message):
    print(3)
    global g_work
    g_work = message.text
    m = bot.send_message(message.chat.id, "Введите token ")
    bot.register_next_step_handler(m, add_ref())

def add_ref(message):
    print(4)
    global g_ref
    g_work = message.text
    m = bot.send_message(message.chat.id, "Введите ref ")
    bot.register_next_step_handler(m, add_token)

def add_token(message):
    print(5)
    global g_token
    g_token = message.text
    bot.send_message(message.chat.id, "Ваши данные: " + g_owner + "/" + g_repo + "/" + g_work + "/" + g_ref + "/\n" + g_token)
    bot.send_message(message.chat.id, "Для добавления пропишите /add\nЕсли ошиблись при вводе пропишите /fill\n Для удаления записи пропишите /drop ")

@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == "ap":
        bot.send_message(callback.message.chat.id, "Пропишите /fill и затем внесите данные\n\nимя пользователя\nназвание репозитория\nназвание файла ")
    elif callback.data == "vp":
        bot.send_message(callback.message.chat.id, "Пропишите /list для просмотра списка") # Исправить
    elif callback.data == "dp":
        bot.send_message(callback.message.chat.id, "Пропишите /fill и введите данные которые хотите удалить") # Надо сделаь
    elif callback.data == "rp":
        bot.send_message(callback.message.chat.id, "Пропишите /run для запуска процесса") # Сделать
    else:
        bot.send_message(callback.message.chat.id, "отмена ")



@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Главное меню"):

        markup = types.InlineKeyboardMarkup(row_width=1)

        add_process = types.InlineKeyboardButton('➕ Добавить процесс', callback_data='ap')
        view_process = types.InlineKeyboardButton('🔍 Просмотр доступных процессов', callback_data='vp')
        delete_process = types.InlineKeyboardButton('❌ Удаление доступных процессов', callback_data='dp')
        run_process = types.InlineKeyboardButton('✅ Запустить доступный процесс', callback_data='rp')

        markup.add(add_process, view_process, delete_process, run_process)
        bot.send_message(message.chat.id, "Возможные действия", reply_markup=markup)

    elif (message.text == "💬 О Боте"):
        mess = (f"<b>Бот для телеграма на языке Python для запуска процессов CI/CD в репозитории на GitHub.com</b>\n\n"
                f"Бот имеет следующие команды:\n\n" 
                f"1. Просмотреть список доступных (сохраненных в боте) процессов CI/CD. Выводятся owner/repo и workflow_id для каждого процесса.\n" 
                f"2. Добавить новый процесс CI/CD в список доступных. При добавлении пользователь должен ввести организацию owner, название репозитория "
                f"repo, имя файла с командами CI/CD или его идентификатор workflow_id, токен для доступа к GitHub API\n"
                f"3. Удалить процесс CI/CD из списка доступных.\n"
                f"4. Выбрать один из доступных CI/CD процессов и запустить.")

        bot.send_message(message.chat.id, mess, parse_mode='html')

    elif (message.text == "♻ GitHub"):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Посетить GitHup.com", url="https://github.com"))
        bot.send_message(message.chat.id, "Нажми, чтобы перейти на сайт", reply_markup=markup)

    elif (message.text == "/add"):
        #g_owner = "suai-os-2022"
        #g_repo = "os-task5-verzunartem"
        #g_work = "bash.yml"
        #g_token = "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"

        print(g_owner, g_repo, g_work)
        response = requests.get("https://api.github.com/repos/" + g_owner + "/" + g_repo + "/actions/workflows/" + g_work, headers={"Authorization": "token " + g_token, "Accept": "application/vnd.github+json"})

        cod = response.status_code
        msg = response.headers
        print("___________MSG___________")
        print(msg)
        print(cod)
        if (cod == 200):
            print(cod)
            bot.send_message(message.chat.id, "Данные успещно добавлены в CI/CD бот")
            list_proc.add(g_owner + ", " + g_repo + ", " + g_work)
        elif (cod != 200):
            bot.send_message(message.chat.id, "Ошибка, попробуйте ввести данные еще раз /fill : ")
            print(cod)
            print("ошибка подключения")
        else:
            print("сбой")

    elif (message.text == "/drop"):
        proc = create_proc(g_owner, g_repo, g_work)

        if proc in list_proc:
           list_proc.remove(proc)
           bot.send_message(message.chat.id, "Данные успешно удалены")
        else:
          print("нет процесса")

    elif (message.text == "/run"):
        #owner = "suai-os-2022"
        #repo = "os-task5-verzunartem"
        #work = "bash.yml"
        #token = "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"

        response = requests.put(
            "https://api.github.com/repos/" + g_owner + "/" + g_repo + "/actions/workflows/" + g_work + "/enable",
            headers={"Authorization": "token " + g_token, "Accept": "application/vnd.github+json"})

        cod = response.status_code
        msg = response.headers
        print("___________MSG1___________")
        print(msg)
        print(cod)
        if (cod == 204):
            print(cod)
            response2 = requests.post(
                "https://api.github.com/repos/" + g_owner + "/" + g_repo + "/actions/workflows/"+g_work+"/dispatches",
                    headers={"Authorization": "token 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", "Accept": "application/vnd.github+json"},
                    data='{"g_ref:"master"}')

            cot = response2.status_code
            mst = response2.content
            print("___________MSG2___________")
            print(cot)
            print(mst)

        elif (cod != 204):
            bot.send_message(message.chat.id, "Ошибка: ")
            print(cod)
            print("ошибка подключения")
        else:
            print("сбой")

    else:
        bot.send_message(message.chat.id, "-")





@bot.message_handler()
def get_user_text(message):
    if message.text == "Привет":
        bot.send_message(message.chat.id, "И тебе привет", parse_mode='html')
    elif message.text == "id":
        bot.send_message(message.chat.id, f"Твой ID: {message.from_user.id}", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю", parse_mode='html')


bot.polling(none_stop=True)
