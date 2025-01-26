import telebot
from telebot import types
from random import *
import sqlite3

Token_read = open('Token.gitignore')
Token = Token_read.readline()
Token_read.close()

bot = telebot.TeleBot(Token)

temv = 0
# для шаблона ['''''', ['', ], ['', ], ['', ], ['', ], '', '']
# 1 - право 2 - экономика 3 - человек и общество 4 - сфера культуры 5 - политика
vopr = [[
    'Одиннадцатиклассник Дима любит физику. Он много занимается, успешно участвует в конкурсах и олимпиадах, занимает призовые места. Какие качества Димы проявились в данной ситуации?', [' Способности', 1], [' Гениальность', 0], [' Потребности', 0], [' Задатки', 0], 'sov11', '3'], [
    'Известный учёный подарил школе, в которой когда-то учился, оборудование для школьной лаборатории. Данный пример прежде всего иллюстрирует право собственника', ['владеть', 0], ['распоряжаться', 1], ['пользоваться', 0], ['наследовать', 0], 'prv1', '1'],
    ['''Какие суждения о духовной сфере общества верны?

А. Духовная сфера жизни общества охватывает религию, искусство, нравственность.

Б. Духовная сфера взаимодействует с другими сферами общества.''', [' Верно А', 0], [' Верно Б', 0], [' Верно всё', 1], [' Ничто не верно', 0], 'sov12', '34'],
    ['''Что отличает семью от других малых групп?''', ['Единство интересов', 0], ['Общие цели деятельности', 0], ['Наличие правил деятельности', 0], ['Совместный быт', 1], 'sov14', '3'],
    ['''В приведённом перечне действий административным проступком является''', ['нецензурная брань в общественном месте', 1], ['систематический прогул школьных занятий без уважительной причины', 0], ['распространение наркотических веществ на школьной дискотеке', 0], ['отказ от выполнения приказа директора школы', 0], 'prv2', '1'],
    ['''В странах с рыночной экономикой...''', ['производитель самостоятельно определяет, что и сколько производить', 1], ['государство устанавливает размер заработной платы работникам', 0], ['министерство финансов распоряжается прибылью предприятий', 0], ['каждый гражданин обязан трудиться на каком-либо предприятии', 0], 'ek1', '2'],
    ['''Согласно Конституции Российской Федерации Конституционный Суд Российской Федерации''', ['принимает законы', 0], ['осуществляет помилование', 0], ['разрешает споры о компетенции между федеральными органами государственной власти', 1], ['разрабатывает и представляет Государственной Думе федеральный бюджет', 0], 'pov15', '1'],
    ['''Полина работает продавцом в магазине одежды. Её доход зависит от того, сколько и каких вещей она продаст. Такой тип заработной платы называют''', ['окладом', 0], ['бонусом', 0], ['премией', 0], ['сдельным', 1], 'ek2', '2'],
    ['''В государстве Z все государственные органы, должностные лица и граждане в своей деятельности подчиняются требованиям закона; существует несколько партий, каждая из которых активно участвует в политической жизни страны. Какой политический режим установился в государстве Z?''', ['авторитарный', 0], ['демократический', 1], ['диктаторский', 0], ['тоталитарный', 0], 'po1', '5'],
    ['''Дедушка и внук пошли в лес за грибами и нашли клад со старинными монетами. Какие правоотношения возникают в результате этой находки?''', ['гражданские', 1], ['семейные', 0], ['трудовые', 0], ['административные', 0], 'prv1', '1'],
    ['''Гражданин В. получил в банке кредит, на который открыл салон красоты. Он вложил собственные сбережения в рекламную кампанию салона. В первые годы салон не приносил прибыли, но затем стал весьма доходным. Какое экономическое явление иллюстрирует данный пример?''', ['предпринимательство', 1], ['конкуренция', 0], ['торговля', 0], ['инфляция', 0], 'ek2', '2'], ['''Верны ли следующие суждения о личности?

А. Личность формируется в общении с окружающими.

Б. Личность характеризуется различными социальными качествами.''', ['верно только А', 0], ['верно только Б', 0], ['верны оба суждения', 1], ['оба суждения неверны', 0], 'sov11', '3'],
    ['''У общественного объединения Z существует программа и устав. Она имеет разветвлённую сеть региональных организаций и молодёжное подразделение. Её главная цель – участие в государственной власти. Данное общественное объединение является...''', ['профессиональным союзом', 0], ['политической партией', 1], ['общественным движением', 0], ['акционерным обществом', 0], 'pov14', '5'],
    ['''Жители мегаполиса создали и зарегистрировали свою ассоциацию «Город без пробок», которая выступает в защиту их интересов и предлагает правительству своё видение проблемы организации дорожного движения, планов строительства и эксплуатации дорог. Данный пример иллюстрирует...''', ['проведение предвыборных кампаний', 0], ['деятельность муниципальных органов', 0], ['функционирование гражданского общества', 1], ['обсуждение нового законопроекта', 0], 'po12', '5'],
    ['''Слово «экономика» употребляется в различных значениях. Какой из примеров иллюстрирует экономику как хозяйство?''', ['изучение рынка недвижимости', 0], ['производство новой модели автомобиля', 1], ['прогнозирование спроса на товары', 0], ['выявление законов развития рынка', 0], 'shpar3', '2'],
    ['''К какому виду экономической деятельности относится продажа автомобилей  в автосалоне?''', ['производству', 0], ['распределению', 0], ['обмену', 1], ['потреблению', 0], 'ek2', '2'],
    ['''Существуют различные типологии семей. Какой из приведённых ниже типов семьи выделен в зависимости от численного состава?''', ['нуклеарная', 1], ['авторитарная', 0], ['демократическая', 0], ['матриархальная', 0], 'sov14', '3'],
    ['''Иван является владельцем предприятия. Для увеличения прибыли он установил новое оборудование. В данной ситуации он проявил себя, прежде всего, как''', ['потребитель', 0], ['покупатель', 0], ['разработчик', 0], ['предприниматель', 1], 'ek2', '2'],
    ['''Гражданка Н. оформила опекунство над своей несовершеннолетней племянницей, которая потеряла родителей в автокатастрофе. Данный пример иллюстрирует правоотношения, регулируемые нормами права''', ['трудового', 0], ['семейного', 1], ['административного', 0], ['конституционного', 0], 'prv1', '1'],
    ['''Совершеннолетние юноша и девушка подали в органы ЗАГС заявление о регистрации брака. Однако им было отказано. Что могло послужить причиной отказа?''', ['отсутствие постоянных доходов', 0], ['недолгий срок знакомства', 0], ['несогласие родителей на брак', 0], ['недееспособность невесты', 1], 'sov14', '3'],
    ['''Верны ли следующие суждения о познавательной деятельности?

А. Познавательная деятельность направлена на получение информации об окружающем мире.

Б. В процессе познавательной деятельности участвуют органы чувств и интеллект человека.''', ['верно только А', 0], ['верно только Б', 0], ['верны оба суждения', 1], ['оба суждения неверны', 0], 'sov13', '3'],
    ['''Структура общества представлена социальными группами и общностями в многообразии их связей. Какая социальная группа выделена по территориальному (поселенческому) признаку?''', ['женщины', 0], ['подростки', 0], ['программисты', 0], ['петербуржцы', 1], 'sov12', '3'],
    ['''Правонарушением является''', ['находка клада старинных монет', 0], ['дача ложных показаний в суде', 1], ['нарушение слова, данного другу', 0], ['утеря паспорта', 0], 'prv2', '1'],
    ['''Сергей учится в 9 классе. Он очень ответственный и самостоятельный человек. Он занимается в кружке авиамоделирования и в хоккейной секции. Обогащая таким образом собственный социальный опыт, Сергей развивается как''', ['индивид', 0], ['личность', 1], ['потребитель', 0], ['товарищ', 0], 'sov11', '3'],
    ['''Верны ли следующие суждения о религии?

А. Религия опирается на представления людей о влиянии сверхъестественных сил на их жизнь.

Б. Религия устанавливает определённые правила поведения.''', ['верно только А', 0], ['верно только Б', 0], ['верны оба суждения', 1], ['оба суждения неверны', 0], 'kuv21', '4'],
    ['''Дмитрий – отец двоих детей, руководитель предприятия. В свободное время он тренирует дворовую футбольную команду. У Дмитрия много друзей, он общительный, энергичный человек. Обогащая таким образом собственный социальный опыт, Дмитрий развивается как''', ['руководитель', 0], ['личность', 1], ['работник', 0], ['индивид', 0], 'sov11', '3'],
    ['''Совершеннолетние юноша и девушка подали в органы ЗАГС заявление о регистрации брака. Однако им было отказано. Что могло послужить причиной отказа?''', ['отсутствие постоянного источника доходов', 0], ['недолгий срок знакомства', 0], ['отсутствие родительского согласия на брак', 0], ['состояние жениха в другом зарегистрированном браке', 1], 'sov14', '3'],
    ['''Что из перечисленного является преступлением?''', ['причинение тяжкого вреда здоровью по неосторожности', 1], ['употребление лекарственных средств без назначения врача', 0], ['публикация в газете материала, критикующего деятельность парламента', 0], ['несвоевременная оплата коммунальных услуг', 0], 'prv2', '1'],
    ['''Что отличает семью от других малых групп?''', ['совместная деятельность', 0], ['общие цели', 0], ['общий быт', 1], ['	наличие норм поведения', 0], 'sov14', '3'],
    ['''В государстве Z власть принадлежит одной политической партии, которая ограничила права граждан и стремится полностью контролировать их частную жизнь. Все жители страны обязаны придерживаться единой обязательной официальной идеологии. Каков политический режим государства Z?''', ['демократический', 0], ['тоталитарный', 1], ['монархический', 0], ['олигархический', 0], 'po1', '5'],
    ['''17-летний Леонид хотел устроиться на работу ночным сторожем, но администрация магазина отказалась принять его, ссылаясь на закон. Администрация магазина в данном случае опиралась на нормы права''', ['семейного', 0], ['уголовного', 0], ['административного', 0], ['трудового', 1], 'prv1', '1']]

vib = []


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('dann.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER primary key, filt INTEGER)')
    cur.execute("INSERT or IGNORE INTO users (id, filt) VALUES ('%d', '%d')" % (bot.get_me().id, 0))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    zad = types.InlineKeyboardButton('Хочу практиковаться!', callback_data='edit')
    tem = types.InlineKeyboardButton('Хочу посмотреть теорию!', callback_data='edit1')
    markup.row(zad)
    markup.row(tem)
    bot.send_message(message.chat.id,
                     'Здравствуйте, пожалуйста, выберите интересующее вас действие:',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global vib
    global temv
    conn = sqlite3.connect('dann.sql')
    cur = conn.cursor()
    if callback.data == 'edit0':
        global temv
        while True:
            cur.execute("SELECT filt FROM users WHERE id = ?", (bot.get_me().id, ))
            lp = cur.fetchall()
            print(bot.get_me().id)
            for i in lp:
                pl = i
            pl = pl[0]
            print(pl)
            if pl == 0:
                sp = choice(vopr)
                break
            else:
                sp = choice(vopr)
                if str(pl) in sp[6]:
                    break
                else:
                    pass
        cur.close()
        conn.close()
        vib = []
        vib = sp
        s = sp[0] + '\n 1.' + sp[1][0] + '\n 2.' + sp[2][0] + '\n 3.' + sp[3][0] + '\n 4.' + sp[4][0]
        markup = types.InlineKeyboardMarkup()
        otv1 = types.InlineKeyboardButton('1', callback_data='editzad1')
        otv2 = types.InlineKeyboardButton('2', callback_data='editzad2')
        otv3 = types.InlineKeyboardButton('3', callback_data='editzad3')
        otv4 = types.InlineKeyboardButton('4', callback_data='editzad4')
        tem = types.InlineKeyboardButton('Изучить темы', callback_data='edit1')
        tem1 = types.InlineKeyboardButton('Поменять тему', callback_data='edit')
        markup.row(otv1, otv2)
        markup.row(otv3, otv4)
        markup.row(tem)
        markup.row(tem1)
        bot.edit_message_text(s, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'editzad1':
        if vib[1][1] == 1:
            markup = types.InlineKeyboardMarkup()
            sigma = types.InlineKeyboardButton('Дальше', callback_data='edit0')
            markup.row(sigma)
            bot.edit_message_text('Правильно!', callback.message.chat.id, callback.message.message_id,
                                  reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            antisigma = types.InlineKeyboardButton('Посмотреть связанную тему', callback_data=vib[5])
            dal = types.InlineKeyboardButton('Решать дальше', callback_data='edit0')
            markup.row(antisigma)
            markup.row(dal)
            l = 0
            for i in range(1, 5):
                if vib[i][1] == 1:
                    l = i
                    break
                else:
                    pass
            bot.edit_message_text(f'''Неправильно! Правильный ответ: {vib[l][0]}

Вопрос: {vib[0]}''', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'editzad2':
        if vib[2][1] == 1:
            markup = types.InlineKeyboardMarkup()
            sigma = types.InlineKeyboardButton('Дальше', callback_data='edit0')
            markup.row(sigma)
            bot.edit_message_text('Правильно!', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            antisigma = types.InlineKeyboardButton('Посмотреть связанную тему', callback_data=vib[5])
            dal = types.InlineKeyboardButton('Решать дальше', callback_data='edit0')
            markup.row(antisigma)
            markup.row(dal)
            l = 0
            for i in range(1, 5):
                if vib[i][1] == 1:
                    l = i
                    break
                else:
                    pass
            bot.edit_message_text(f'''Неправильно! Правильный ответ: {vib[l][0]}

Вопрос: {vib[0]}''', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'editzad3':
        if vib[3][1] == 1:
            markup = types.InlineKeyboardMarkup()
            sigma = types.InlineKeyboardButton('Дальше', callback_data='edit0')
            markup.row(sigma)
            bot.edit_message_text('Правильно!', callback.message.chat.id, callback.message.message_id,
                                  reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            antisigma = types.InlineKeyboardButton('Посмотреть связанную тему', callback_data=vib[5])
            dal = types.InlineKeyboardButton('Решать дальше', callback_data='edit0')
            markup.row(antisigma)
            markup.row(dal)
            l = 0
            for i in range(1, 5):
                if vib[i][1] == 1:
                    l = i
                    break
                else:
                    pass
            bot.edit_message_text(f'''Неправильно! Правильный ответ: {vib[l][0]}

Вопрос: {vib[0]}''', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'editzad4':
        if vib[4][1] == 1:
            markup = types.InlineKeyboardMarkup()
            sigma = types.InlineKeyboardButton('Дальше', callback_data='edit0')
            markup.row(sigma)
            bot.edit_message_text('Правильно!', callback.message.chat.id, callback.message.message_id,
                                  reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            antisigma = types.InlineKeyboardButton('Посмотреть связанную тему', callback_data=vib[5])
            dal = types.InlineKeyboardButton('Решать дальше', callback_data='edit0')
            markup.row(antisigma)
            markup.row(dal)
            l = 0
            for i in range(1, 5):
                if vib[i][1] == 1:
                    l = i
                    break
                else:
                    pass
            bot.edit_message_text(f'''Неправильно! Правильный ответ: {vib[l][0]}

Вопрос: {vib[0]}''', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'edit':
        markup = types.InlineKeyboardMarkup()
        otv0 = types.InlineKeyboardButton('Любая тема', callback_data='term0')
        otv1 = types.InlineKeyboardButton('Право', callback_data='term1')
        otv2 = types.InlineKeyboardButton('Экономика', callback_data='term2')
        otv3 = types.InlineKeyboardButton('Человек и общество', callback_data='term3')
        otv4 = types.InlineKeyboardButton('Сфера культуры', callback_data='term4')
        otv5 = types.InlineKeyboardButton('Политика', callback_data='term5')
        teo = types.InlineKeyboardButton('Теория', callback_data='edit1')
        markup.row(otv0)
        markup.row(otv1)
        markup.row(otv2)
        markup.row(otv3)
        markup.row(otv4)
        markup.row(otv5)
        markup.row(teo)
        bot.edit_message_text('''Какие задания будем решать?''', callback.message.chat.id, callback.message.message_id,
                              reply_markup=markup)
    elif callback.data == 'edit1':
        markup = types.InlineKeyboardMarkup()
        tem1 = types.InlineKeyboardButton('Право', callback_data='shpar1')
        tem3 = types.InlineKeyboardButton('Экономика', callback_data='shpar3')
        tem4 = types.InlineKeyboardButton('Человек и общество', callback_data='shpar4')
        tem5 = types.InlineKeyboardButton('Сфера культуры', callback_data='shpar5')
        tem6 = types.InlineKeyboardButton('Политика', callback_data='shpar6')
        resh = types.InlineKeyboardButton('Задания', callback_data='edit')
        markup.row(tem1)
        markup.row(tem3)
        markup.row(tem4)
        markup.row(tem5)
        markup.row(tem6)
        markup.row(resh)
        bot.edit_message_text('Вы можете просмотреть материал по следующим темам:', callback.message.chat.id,
                              callback.message.message_id, reply_markup=markup)
    elif callback.data == 'term0':
        conn = sqlite3.connect('dann.sql')
        cur = conn.cursor()
        cur.execute("UPDATE users SET filt = ? WHERE id = ?", (0, bot.get_me().id))
        conn.commit()
        cur.close()
        conn.close()
        markup = types.InlineKeyboardMarkup()
        pr = types.InlineKeyboardButton('Приступаем!', callback_data='edit0')
        markup.row(pr)
        bot.edit_message_text('''Нажмите на кнопку чтобы начать''', callback.message.chat.id,
                              callback.message.message_id, reply_markup=markup)
    elif callback.data == 'term1':
        conn = sqlite3.connect('dann.sql')
        cur = conn.cursor()
        cur.execute("UPDATE users SET filt = ? WHERE id = ?", (1, bot.get_me().id))
        conn.commit()
        cur.close()
        conn.close()
        temv = 1
        markup = types.InlineKeyboardMarkup()
        pr = types.InlineKeyboardButton('Приступаем!', callback_data='edit0')
        markup.row(pr)
        bot.edit_message_text('''Нажмите на кнопку чтобы начать''', callback.message.chat.id,
                              callback.message.message_id, reply_markup=markup)
    elif callback.data == 'term2':
        conn = sqlite3.connect('dann.sql')
        cur = conn.cursor()
        cur.execute("UPDATE users SET filt = ? WHERE id = ?", (2, bot.get_me().id))
        conn.commit()
        cur.close()
        conn.close()
        temv = 2
        markup = types.InlineKeyboardMarkup()
        pr = types.InlineKeyboardButton('Приступаем!', callback_data='edit0')
        markup.row(pr)
        bot.edit_message_text('''Нажмите на кнопку чтобы начать''', callback.message.chat.id,
                              callback.message.message_id, reply_markup=markup)
    elif callback.data == 'term3':
        conn = sqlite3.connect('dann.sql')
        cur = conn.cursor()
        cur.execute("UPDATE users SET filt = ? WHERE id = ?", (3, bot.get_me().id))
        conn.commit()
        cur.close()
        conn.close()
        temv = 3
        markup = types.InlineKeyboardMarkup()
        pr = types.InlineKeyboardButton('Приступаем!', callback_data='edit0')
        markup.row(pr)
        bot.edit_message_text('''Нажмите на кнопку чтобы начать''', callback.message.chat.id,
                              callback.message.message_id, reply_markup=markup)
    elif callback.data == 'term4':
        conn = sqlite3.connect('dann.sql')
        cur = conn.cursor()
        cur.execute("UPDATE users SET filt = ? WHERE id = ?", (4, bot.get_me().id))
        conn.commit()
        cur.close()
        conn.close()
        temv = 4
        markup = types.InlineKeyboardMarkup()
        pr = types.InlineKeyboardButton('Приступаем!', callback_data='edit0')
        markup.row(pr)
        bot.edit_message_text('''Нажмите на кнопку чтобы начать''', callback.message.chat.id,
                              callback.message.message_id, reply_markup=markup)
    elif callback.data == 'term5':
        conn = sqlite3.connect('dann.sql')
        cur = conn.cursor()
        cur.execute("UPDATE users SET filt = ? WHERE id = ?", (5, bot.get_me().id))
        conn.commit()
        cur.close()
        conn.close()
        temv = 5
        markup = types.InlineKeyboardMarkup()
        pr = types.InlineKeyboardButton('Приступаем!', callback_data='edit0')
        markup.row(pr)
        bot.edit_message_text('''Нажмите на кнопку чтобы начать''', callback.message.chat.id,
                              callback.message.message_id, reply_markup=markup)
    elif callback.data == 'shpar3':  # ЭКОНОМИКА
        markup = types.InlineKeyboardMarkup()
        ekv1 = types.InlineKeyboardButton('Как устроена экономика?', callback_data='ek1')
        ekv2 = types.InlineKeyboardButton('Роли челоека в экономике', callback_data='ek2')
        ekv3 = types.InlineKeyboardButton('Основные аспекты экономики', callback_data='ek3')
        naz = types.InlineKeyboardButton('Назад', callback_data='edit1')
        markup.row(ekv2)
        markup.row(ekv3)
        markup.row(ekv1)
        markup.row(naz)
        bot.edit_message_text(
            '''Слово экономика может быть воспринято по-разному. Может подразумеваться как теоретическая часть экономики (экономика как наука), так и её практическая часть (экономика как хозяйство). Рекомендуем изучать дальнейший материал в следующем порядке: роли человека в экономике > основные аспекты экономики > как устроена экономика''',
            callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'ek1':
        markup = types.InlineKeyboardMarkup()
        ekv11 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv12 = types.InlineKeyboardButton('Назад', callback_data='shpar3')
        markup.row(ekv11)
        markup.row(ekv12)
        bot.edit_message_text('''Выделяют 4 экономических системы: традиционная, плановая, рыночная и смешанная.

В традиционной экономической системе преобладает натуральное хозяйство. Натуральное хозяйство - хозяйство, в котором производитель является главным потребителем своих товаров. Например наши далекие предки питались тем, что сами вырастили.

В плановой (командной) экономике производство и распределение благ полностью контролируется государством.

В рыночной экономике наоборот, государство дает свободу предпринимателям самим решать, как они будут отвечать на основные вопросы экономики.

Ну и конечно экономическая система может быть средним между плановой и рыночной, она называется смешанной

Также эконимики разных стран можно разделить по этапам их развития:
1. Аграрная экономика, большую часть экономики страны составляет сельское хозяйство, для лучшей жизни необходима земля
2. Индустриальая экономика, большую часть экономики страны занимает промышленное производство, для лучшей жизни нужен капитал
3. Информационная (постиндустриальная) экономика, большую часть экономики страны занимает сфера услуг, для лучшей жизни нужна информация

''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'ek2':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Назад', callback_data='shpar3')
        markup.row(ekv21)
        markup.row(ekv22)
        bot.edit_message_text('''В экономике есть две главные роли: производитель и потребитель.

Производитель (предприниматель) - это человек, организующий предприятия (производства) для производства товаров или услуг ради получения прибыли (заработка)

Рабочий - это человек, продающий свой труд

Существуют следующие виды оплаты труда:
1. Заработная плата (оклад) - это фиксированная плата, которая выплачивается работнику за время работы, а не за её объем
2. Сдельная плата - это фиксированная плата, которая выплачивается работнику за объем произведенной работы

Также работник может быть поощрен премией (единоразовая выплата от начальника к подчинённому, обычно дающаяся за хорошую работу)

Потребитель - это субъект, цель которого удовлетворить свою потребность, потребив благо или услугу

Потребитель и производитель обмениваются ради получения выгоды.
Обмен бывает как просто товарный (бартер), так и более знакомый нам товарно-денежный обмен

Также надо упомянуть основные закономерности экономики:
1. Чем ниже цена на благо, тем больше на него спрос и наоборот. Также спрос потребителя зависит от его изначальной мотивации покупки
2. Если благо в избытке, то цена понижается, пока спрос и предложение не пришли в баланс. И наоборот, дифицитное благо повышается в цене''', callback.message.chat.id,
                              callback.message.message_id, reply_markup=markup)
    elif callback.data == 'ek3':
        markup = types.InlineKeyboardMarkup()
        ekv31 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv32 = types.InlineKeyboardButton('Назад', callback_data='shpar3')
        markup.row(ekv31)
        markup.row(ekv32)
        bot.edit_message_text('''Экономика - это сложная система, цель которой - создавать и распределять блага.

У экономики есть основные вопросы, на которые отвечает каждый предприниматель:
1. Что производить?
2. Как производить?
3. Для кого производить?

Ответ на эти вопросы нужен из-за основной, фундаментальной проблемы экономики - удовлетворение неограниченных, постоянно растущих потребностей при ограниченных ресурсах

Потребность - это необходимость в чём-либо для поддержания и развития жизнедеятельности человека и общества в целом

Ресурсы (факторы производства):
1. Земля (и все её ресурсы, такие как ископаемые или вода)
2. Труд
3. Капитал (капитал - это все средства производства, от денег до зданий заводов)
4. Информация
5. Предпринимательские способности''', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'shpar6':  # ПОЛИТИКА
        markup = types.InlineKeyboardMarkup()
        pov1 = types.InlineKeyboardButton('Что такое государство?', callback_data='po1')
        pov2 = types.InlineKeyboardButton('Функции государства', callback_data='po2')
        pov3 = types.InlineKeyboardButton('Власть', callback_data='po3')
        naz = types.InlineKeyboardButton('Назад', callback_data='edit1')
        markup.row(pov3)
        markup.row(pov1)
        markup.row(pov2)
        markup.row(naz)
        bot.edit_message_text('''Политика имеет несколько определений, например:
 1. Политика как искусство управления государством
 2. Политика как область жизнедеятельности людей, которая сложилась в ходе появления и развития власти и регулирует жизнь всего общества

Рекомендуем смотреть дальнейший материал в следующем порядке: власть > что такое государство > функции государства''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'po3':
        markup = types.InlineKeyboardMarkup()
        pov31 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        pov32 = types.InlineKeyboardButton('Назад', callback_data='shpar6')
        markup.row(pov31)
        markup.row(pov32)
        bot.edit_message_text('''Власть - это возможность оказывать влияние на поведение людей

Политическая власть отличается тем, что она оказывает влияние на всех членов общества. Политическая власть является публичной, все знают, кто именно является её источником

Власть обладает чертой легетимности. Она показывает то, насколько правомерной власть воспринимает население''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'po1':
        markup = types.InlineKeyboardMarkup()
        pov11 = types.InlineKeyboardButton('Что такое разделение властей?', callback_data='po11')
        pov12 = types.InlineKeyboardButton('Что такое гражданское общество?', callback_data='po12')
        pov13 = types.InlineKeyboardButton('Признаки демократических выборов', callback_data='po13')
        pov14 = types.InlineKeyboardButton('Что такое партии?', callback_data='pov14')
        pov15 = types.InlineKeyboardButton('Распределение полномочий в РФ', callback_data='pov15')
        naz = types.InlineKeyboardButton('Назад', callback_data='shpar6')
        markup.row(pov11)
        markup.row(pov12)
        markup.row(pov13)
        markup.row(pov14)
        markup.row(pov15)
        markup.row(naz)
        bot.edit_message_text('''Государство - это политическая организация. Есть следующие признаки государства:
1. Территория
2. Граждане
3. Свод законов
4. Бюрократический аппарат
5. Наличие центральной власти
6. Сбор налогов
7. Аппарат защиты и принуждения (Армия и полиция)

Существуют 3 главных параметра государств:
1. Форма правления
2. Политический режим
3. Форма территориального устройства

Формы правления бывают следующие:
1. Абсолютная монархия (абсолютизм). При ней вся власть принадлежит одному человеку, монарху, а передается по наследству (пример: Оман, Бахрейн, Бруней)
2.1. Парламентская (конституционная) монархия. При ней титул монарха становится номинальным, а всё решает парламент (пример: Япония, Великобритания, Испания, Швеция)
2.2. Дуалистическая монархия. Консититуционная монархия, но монарх остается фактическим правителем, деля власть с парламентом и президентом 
3. Теократическая монархия. Это тот же абсолютизм, но монарх так же является религиозной главой (пример: Ватикан, Саудовская Аравия)
4. Парламентская республика. Большая часть полномочий сосредоточена у избраного парламента, он же, проведя внутреннее голосование избирает президента (Примеры: Индия, Германия, Италия)
5. Смешанная республика. Полномочия поделены между Парламентом и президентом, парламент и президент избираются отдельно всенародным голосованием (Примеры: Россия, Франция, Австрия)
6. Президентская республика. Президент имеет больше полномочий, чем парламент, он же и является главой исполнительной власти (поянтие "исполнительная власть" раскрыто ниже) (примеры: США, Бразилия, Казахстан)

Парламент в РФ называется Федеральным Собранием, он состоит из нижней палаты (Государственная Дума, депутатов избирает весь народ) и верхней палаты (Совет Федерации, сенаторы избираются по 2 от каждого региона)

В нашей стране президент имеет возможность помиловать конкретного человека, а парламент может провести амнистию, сократив срок лишения свободы группы заключённых

Теперь переходим к политическим режимам:
1. Демократия. Её признаков настолько много, что они будут выделены отдельно
2. Авториторизм. При нём часть прав человека не соблюдаются, источником политической власти является аппарат принуждения
3. Тоталитаризм. При нём права человека не имеют значения, оппозиция активно подавляется, политическая власть все также обеспечивается аппаратом принуждения

А теперь к признакам демократии:
1. Разделение властей
2. Источником политической власти является воля народа
3. Политический плюрализм (существование многообразия политических сил с конкуренцией между ними за представительство в органах государственной власти)
4. Легальность оппозиции
5. Равзитое гражданское общество
6. Наличие демократических выборов

И последнее, территориальное устройство:
1. Унитарное устройство. При унитарном устройстве государство делится на равные между собой регионы, которые имеют минимальные полномочия, во всем государстве действуют единые законы. Пример: Франция, Греция, Вьетнам
2. Федерация. В федерациях политика разделяется на федеральную и региональную. Регионы имеют право на проведение собственной региональной политики. Примеры: Россия, США, Германия
3. Конфедерация. Конфедерация - это союз государств, сохраняющих свой суверенитет. Пример: Европейский союз, Швейцария, СНГ (Содружество Независимых Государств)''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'po11':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Вернуться к теме', callback_data='shpar6')
        ekv23 = types.InlineKeyboardButton('Назад', callback_data='po1')
        markup.row(ekv21)
        markup.row(ekv23)
        bot.edit_message_text('''Разделение властей - это политическая практика, при которой все политические власти независимы друг от друга. Есть следующие типы власти:
1. Законодательная власть. Её представителем в республиках является парламент, представители законодательной власти наделены правом законотворчества
2. Исполнительная власть. Это та власть в государстве, целью которой является реализация целей и задач государственной политики. Пример: министерства
3. Судебная власть. Суды работают для разрешения конфликтов согласно законам в правовом поле''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'po12':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Вернуться к теме', callback_data='shpar6')
        ekv23 = types.InlineKeyboardButton('Назад', callback_data='po1')
        markup.row(ekv21)
        markup.row(ekv23)
        bot.edit_message_text('''Гражданское общество - это система инициативных негосударственных объединений граждан, призванная удовлетворять их личные потребности и интересы.
Пример: профсоюзы, благотворительные организации''', callback.message.chat.id, callback.message.message_id,
                              reply_markup=markup)
    elif callback.data == 'po13':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Вернуться к теме', callback_data='shpar6')
        ekv23 = types.InlineKeyboardButton('Назад', callback_data='po1')
        markup.row(ekv21)
        markup.row(ekv23)
        bot.edit_message_text('''У демократических выборов есть следующие признаки:
1. Всеобщий характер выборов (все неосужденные и *дееспособные граждане имеют голос)
2. Равное избирательное право (все голоса равны между собой)
3. Прямое голосование (каждый голос идёт непосредственно за того или иного кандидата)
4. Тайное голосование (это сделано ради безопасности голосующего, чтобы его не смогли принудить к голосованию)

* Дееспособность - это способность распоряжаться своими провами и нести обязанности. Недееспособные люди - люди, не достигшие совершеннолетия или имеющие определённые психические заболевания''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'pov14':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Вернуться к теме', callback_data='shpar6')
        ekv23 = types.InlineKeyboardButton('Назад', callback_data='po1')
        markup.row(ekv21)
        markup.row(ekv23)
        bot.edit_message_text('''Политическая партия - это организованная группа лиц с общими взглядами на политическое устройство, стремящаяся захватить власть и участвовать в политике

У партий есть следующие разновидности:
1. Легальные - нелегальные
2. Правящие - оппозиционные
3. Массовые - кадровые

У партий есть признаки:
1. Партия имеет чёткую структуру и соблюдает все формальности (наличие доменов, руководящих органов и документы)
2. Наличие общих взглядов на политику среди членов партии
3. Планы на будущее
4. Главная цель - завоевание власти
5. Многочисленность

У партий есть устав. Это учредительный документ, в котором указана структура партии, её порядок деятельности, права и обязанности участников

Программа партии - это документ, в котором изложены цели, задачи и методы их достижения 

Общественно-политические движения - это массоввые неформальные объединения людей, поддерживающих определённые изменения в обществе

Отличия от партии:
1. Неформальный характер (отсутствие четкой структуры)
2. Непостоянство состава
3. Цель движения - не достижения власти, а достижения определённых изменений, например защита окружающей среды''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'pov15':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Вернуться к теме', callback_data='shpar6')
        ekv23 = types.InlineKeyboardButton('Назад', callback_data='po1')
        markup.row(ekv21)
        markup.row(ekv23)
        bot.edit_message_text('''Давайте разберёмся, чем отличаются полномочия президента, Государственной Думы и Совета Федерации

Президент:
1. Руководство над внешней политикой
2. Является Верховным Главнокомандующим Вооруженными Силами РФ
3. Имеет право предоставить гражданство и политическое убежище
4. Награждает государственными наградами и званиями
5. Имеет право помиловать
6. Формирует правительство
7. Назначает выборы в Государственную Думу
8. Назначает проведение референдумов

Государственная Дума:
1. Назначение главы Центрального Банка РФ
2. Объявление амнистии
3. Принятие законов
4. Решение вопроса о доверии правительству (импичмент)

Совет федерации:
1. Изменение границ субъектов РФ (регионов)
2. Решении об использовании Вооруженных Сил РФ за пределами РФ
3. Назначает проведение выборов на должность президента
4. Назначение на должность по представлению Президента РФ, Председателя Конституционного и Верховного Судов

Также важно знать полномочия Конституционного Суда:
1. Разрешение дел о соответствии законов актов Конституции
2. Разрешение дел о соответствии международных договоров РФ Конституции
3. Оценка законопроектов на предмет соответствия Конституции
4. Толкование Конституции
5. Разрешение споров о компетенции между органами государственной власти''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'po2':
        markup = types.InlineKeyboardMarkup()
        pov31 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        pov32 = types.InlineKeyboardButton('Назад', callback_data='shpar6')
        markup.row(pov31)
        markup.row(pov32)
        bot.edit_message_text('''Функции государства разделяют на внешние и внутренние.

Внешние функции заключаются во взаимодействии государства с другими странами, а также в решении глобальных проблем

Внутренние функции связаны с деятельностью государства в своих границах, например:
1. Охрана правопорядка
2. Регулирование экономики
3. Социальная поддержка уязвимых слоёв населения
4. Участие в формировании культуры, воспитание патриотизма
''', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'shpar5':  # КУЛЬТУРА
        markup = types.InlineKeyboardMarkup()
        kuv1 = types.InlineKeyboardButton('Материальная культура', callback_data='kuv1')
        kuv2 = types.InlineKeyboardButton('Духоная культура', callback_data='kuv2')
        naz = types.InlineKeyboardButton('Назад', callback_data='edit1')
        markup.row(kuv1)
        markup.row(kuv2)
        markup.row(naz)
        bot.edit_message_text('''Культура - это весь результат деятельности человека во всём его многообразии, её также называют второй природой. 

Культура делится на материальную и духовную

Также выделяют массовую, элетарную и народную культуры.

Массовая культура направлена на большие массы людей, зачастую имеет малую художественную ценность

Элитарная культура как правило направлена на высокообразованную часть общества и имеет большую художественную ценность

Народная культура присуща определённым народам. Это фольлор, обычаи с традициями или народные праздники


Главные цели культуры:
1. Удовлетворение духовных потребностей человека
2. Адаптивная функция
3. Регулятивная функция
4. Социализационная (воспитательная) функция
5. Накопительная функция
6. Познавательная (информационная) функция
7. Коммуникативная функция
8. Интегративная функция (объединение людей в группы)
9. Творческая функция
10. Мировоззренческая функция''', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'kuv1':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Назад', callback_data='shpar5')
        markup.row(ekv21)
        markup.row(ekv22)
        bot.edit_message_text(
            '''Материальная культура - это то, что создал человек, то, что используется для удовлетворения биологических потребностей. Материальная культура всегда существует физически''',
            callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'kuv2':
        markup = types.InlineKeyboardMarkup()
        kuv21 = types.InlineKeyboardButton('Религия', callback_data='kuv21')
        kuv22 = types.InlineKeyboardButton('Мораль', callback_data='kuv22')
        kuv23 = types.InlineKeyboardButton('Образование', callback_data='kuv23')
        kr = types.InlineKeyboardButton('Назад', callback_data='shpar5')
        markup.row(kuv21)
        markup.row(kuv22)
        markup.row(kuv23)
        markup.row(kr)
        bot.edit_message_text('''Духовная культура - это совокупность духовных ценностей и творческой деятельности по их производству, освоению и применению. 

У духовной культуры есть 5 основных разделов:
1. Искусство
2. Религия
3. Мораль
4. Наука
5. Образование

Фундаментальными элемантами культуры являются:
1. Символы
2. Образы
3. Ритуалы
4. Ценности
''', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'kuv21':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Вернуться к вопросам', callback_data='shpar5')
        kuv32 = types.InlineKeyboardButton('Назад', callback_data='kuv2')
        markup.row(ekv21)
        markup.row(kuv32)
        bot.edit_message_text('''Религия - мировоззрение и соответствующее поведение человека, основанное на вере в сверхъестественное

В религии важна вера. Религиозная вера - это особая эмоциональная связь между человеком и Богом. Вера не требует доказательств

Древние религии имеют следующую классификацию:
1. Анимизм - вера в то, что у предметов и явлений природы есть душа
2. Фетишизм - вера в сверхъестественные способности неживого предмета
3. Тотемизм - почитание священных животных и растений

Религии делятся на национальные (синтоизм, иудаизм) и Мировые (буддизм, христианство и ислам (буддизм - самая старая религия, ислам - самая молодая))

Свобода совести - это естественное право человека иметь любые убеждения и руководствоваться ими''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'kuv23':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Вернуться к вопросам', callback_data='shpar5')
        kuv32 = types.InlineKeyboardButton('Назад', callback_data='kuv2')
        markup.row(ekv21)
        markup.row(kuv32)
        bot.edit_message_text('''Образование - это социальный институт, связанный с воспитанием и развитием интеллектуальных и творческих способностей, мировоззрением, личностными качествами человека

Цели образования:
1. Экономическая
2. Социальная
3. Культурная
4. Воспитательная

Современное образование имеет следующие тенденции:
1. Демократизация (становление массовым) образования
2. Удлиннение образования
3. Образование становится непрерывным
4. Гуманизация образования (внимание школы, педагогов направлено к личности учащегося, его интересам, запросам, индивидуальным особенностям, сохранению и укреплению его здоровья)
5. Гуманитаризация образования (повышение роли общественных дисциплин (философии, психологии, экономики, политологии, права) в образовательном процессе)
6. Компьютеризация образования''', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'kuv22':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Вернуться к вопросам', callback_data='shpar5')
        kuv32 = types.InlineKeyboardButton('Назад', callback_data='kuv2')
        markup.row(ekv21)
        markup.row(kuv32)
        bot.edit_message_text('''Мораль - это принятые в обществе нравственные нормы поведения, отношений с людьми

У моральных норм есть следующие функции:
1. Оценочная
2. Регулятивная
3. Воспитательная
4. Контролирующая
5. Ценностно-ориентировачная

В теме морали важны следующие понятия:
Долг - это осознание безусловной необходимости исполнения того, что предписано моральным идеалом
Совесть - это критическое осознание долга, внутренний самоконтроль человека
Стыд - это чувство человека, для которого характерно сильное смущение, осуждение себя за поступок или поведение
Этика - это филосовская наука, изучающая проблемы морали и нравственности
Добро - это то, что делает жизнь лучше, благо
Зло - это противоположность добру''', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'shpar1':
        markup = types.InlineKeyboardMarkup()
        ekv11 = types.InlineKeyboardButton('Что такое правоотношения?', callback_data='prv1')
        ekv21 = types.InlineKeyboardButton('Что такое правонарушение?', callback_data='prv2')
        ekv31 = types.InlineKeyboardButton('Какие бывают права?', callback_data='prv3')
        naz = types.InlineKeyboardButton('Назад', callback_data='edit1')
        markup.row(ekv11)
        markup.row(ekv21)
        markup.row(ekv31)
        markup.row(naz)
        bot.edit_message_text(
            '''Право - это наука, изучающая совокупность устанавливаемых и охраняемых государством норм и правил, регулирующих отношения людей в обществе''',
            callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'prv1':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Назад', callback_data='shpar1')
        markup.row(ekv21)
        markup.row(ekv22)
        bot.edit_message_text('''Правоотношение - это урегулированное нормами права общественное отношение, участники которого обладают взаимными правами и обязанностями, гарантированными государством

Виды правоотношений:
1. Административные
2. Трудовые
3. Гражданские
4. Конституционные
5. Семейные
6. Уголовные

Административное право - это отрасль права, которая призвана регулировать права и обязанности физических и юридических лиц, их отношение с государством

Уголовное право - отрасль права, представляющая собой совокупность норм, определяющих преступность и наказуемость деяний

Гражднаское право - это отрасль права, которая регулирует имущественные (интеллектуальное имущество в том числе) и личные неимущественные отношения

Семейное право - это отрасль права, которая регулирует вопросы заключения и расторжения брака, личные и имущественные отношения в семье

Трудовое право - это отрасль права, которая регулирует отношения между работником и работадателем

Говоря о гражданском праве, очень важно понимать права собственника:
1. Право владеть
2. Право пользоваться
3. Право распоряжаться (к примеру возможность отдать кому-то)

Субъект правоотношений - это физические и юридические лица, участвующие в правоотношениях

Физическое лицо - конкретный человек, гражданин гоусдарства, иностранный подданный или лицо без гражданства, находящиеся на территории государства

Юридическое лицо - предприятия, учереждения или организации

Объект правоотношений - предмет, по поводу которого возникает правоотношение

Особенности правоотношения:
1. Возникают в обществе между субъектами
2. Носят сознательных характер
3. Регулируются нормами права''', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'prv2':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Назад', callback_data='shpar1')
        markup.row(ekv21)
        markup.row(ekv22)
        bot.edit_message_text('''Правонарушение - это действие или бездействие человека, запрещённое законом под угрозой наказания

Признаки правонарушения:
1. Вина нарушителя
2. Нарушение закона
3. Общественно опасный характер
4. Наказуемость

Правонарушения делятся на проступки и преступления

Проступок (административное или иное нарушение) - это противозаконное поведение, нарушающее общественный порядок и права окружающих

Преступление - это противозаконное поведение, имеющее большую социальную опасность и запрещенное Уголовным кодексом

За правонарушениями следует юридическая ответственность

Юридическая ответственность - это мера воздействия государства на правонарушителя с целью восстановить нарушенный порядок и справедливость

Виды юридической ответственности:
1. Гражданская - возмещение убытков, вреда
2. Дисциплинарная - замечание, выговор, увольнение или исключение
3. Административная - штраф, арест, лишение профессиональных прав (запрет работы учителем, лишение водительских прав)
4. Уголовная - лишение свободы, исправительные работы''', callback.message.chat.id, callback.message.message_id,
                              reply_markup=markup)
    elif callback.data == 'prv3':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Назад', callback_data='shpar1')
        markup.row(ekv21)
        markup.row(ekv22)
        bot.edit_message_text('''У каждого человека с рождения есть естественные права, которые являются неотчуждаемыми и признаются высшей социальной ценностью, а их защита является обязанностью государства. К таким правам относится право на жизнь, свободу передвижения и т.д.

Важно рассказать про основной закон государства, который гарантирует эти права - конституцию

Конституция - это сборник главных законов государства. Её функции:
1. Правовая
2. Учредительная
3. Мировоззренческая
4. Социально-политическая

Конституция носит всеохватывающий характер, она - высшая юридическая сила

Конституция РФ разделяет права человека на 5 групп:
1. Гражданские (личные)
2. Политические
3. Экономические
4. Социальные
5. Духовные

Также Конституция РФ выделяет обязанности:
1. Соблюдать Конституцию и законы РФ
2. Уплачивать налоги
3. Защищать Отечество и нести военную службу
4. Получить основное общее образование (9 классов школы)
5. Сохранять природу и окружающую среду
6. Заботиться о сохранении культурных и исторических памятников
7. Родители обязаны заботиться о несовершеннолетних детях, а совершеннолетние дети о нетрудоспособных родителях

Правоспособность - это установленная законом способность быть носителем прав и обязанностей. Правоспособность начинается при рождении и прекращается в случае смерти

Дееспособность - это способность распоряжаться своими правами и нести обязанность. Получается по достижении совершеннолетия, или путём эмансипации (вступление в брак при наличии доходов). Дееспособность прекращается после смерти или по решению суда. У недееспособных людей есть опекун, он берёт на себя обязанность по содержанию опекаемого. Дети с 6 лет считаются частично дееспособными, они приобретают права совершать некоторые сделки самостоятельно, а некоторые с согласия попечителей (зачастую родителей)''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'shpar4':
        markup = types.InlineKeyboardMarkup()
        sov11 = types.InlineKeyboardButton('Потребности и способности человека', callback_data='sov11')
        sov12 = types.InlineKeyboardButton('Устройство общества', callback_data='sov12')
        sov13 = types.InlineKeyboardButton('Виды деятельности', callback_data='sov13')
        sov14 = types.InlineKeyboardButton('Семья', callback_data='sov14')
        naz = types.InlineKeyboardButton('Назад', callback_data='edit1')
        markup.row(sov11)
        markup.row(sov12)
        markup.row(sov13)
        markup.row(sov14)
        markup.row(naz)
        bot.edit_message_text('''Человек - это биосоциальное существо. Определений общества несколько:
1. В самом широком смысле общество - это человечество на всём протяжении истории
2. Второе определение общества звучит так: Общество - это обособившаяся от природы, но тесно с ней связанная часть материального мира, состоящая из индивидуумов и включающая в себя различные формы взаимодействия и способы объединения людей
3. Общество в узком смысле - это объединение людей по интересам, целям, общей деятельности''', callback.message.chat.id,
                              callback.message.message_id, reply_markup=markup)
    elif callback.data == 'sov11':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Назад', callback_data='shpar4')
        markup.row(ekv21)
        markup.row(ekv22)
        bot.edit_message_text('''Потребность - это необходимость человека в чём-либо для организма, личности и духовного мира, важно заметить, что с развитием общества потребности постоянно растут

Классификация потребностей:
1. Биологичиске - они естественны и необходимы для поддержания жизни, например потребность в еде или сне
2. Духовные и социальные потребности - они связаны с внутренним миром человека, с развитием личности

Личность - это совокупность социально значимых качеств и навыков, которые приобретаются на всей протяжённости жизни

Следует отличать личность от иднивида

Индивид - это отдельный представитель человеческого рода

Также для классификации потребностей психолог Маслоу создал пирамиду потребностей. Перечисляем от самых фундаментальных к вершине пирамиды:
1. Биологические
2. Потребность в безопасности
3. Потребность в общении и связах с другими людьми
4. Потребность в уважении
5. Потребность в познании
6. Потребность в красоте
7. Потребность в самореализации

Самореализация - это реализация задатков и способностей человека через определённую деятельность

Способности - это индивидуальные особенности человека, которые нужны, чтобы его деятельность была успешной. В способности человека входят таланты, задатки, интересы''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'sov12':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Назад', callback_data='shpar4')
        markup.row(ekv21)
        markup.row(ekv22)
        bot.edit_message_text('''Общество - это сложная система, в которой каждый элемент взаимодействует друг с другом

Жизнь общества разделена на сферы жизни общества. Выделяют следующие сферы:
1. Экономическая - люди вступают в отношения с целью производства, обмена или потребления благ
2. Политическая - люди вступают в отношения по поводу власти и управления обществом, а также для разрешения вопросов между большими группами людей
3. Социальная - взаимоотношение социальных групп, а также мобильность человека в социуме (обществе)
4. Духовная - взаимоотношения людей происходят из-за и ради духовных ценностей

Статус - это положение человека в обществе, связанное с его ролью
Роль - это набор паттернов поведения, соблюдение которых ожидается от людей

Социальная мобильность - это изменение положения индивида или группы индивидов в социуме, а также сама возможность этого изменения. Способы для изменения своего положения называют социальными лифтами

Социальная мобильность бывает вертикальной, а бывает горизонтальной. Вертикальная мобильность подразумевает повышение или понижение статуса, а при горизонтальной отсутствие изменения этого самого статуса

Социальная стратификация - это деление общества на страты (группы), где одна группа имеет больше благ, чем другая

Надо добавить, что внутренние элементы общества взаимодействуют не только между собой, но и с окружающей средой

Человек и природа неразрывно связаны. В начале человек был полностью подчинён природе, а влиять на неё почти не мог. Но потом, с развитием общества, человек начал эксплуатировать природу, считая её своей мастерской. В современном обществе человек понял, насколько опасно его пагубное воздействие на окружающий мир, поэтому сегодня люди более осторожны.''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'sov13':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Назад', callback_data='shpar4')
        markup.row(ekv21)
        markup.row(ekv22)
        bot.edit_message_text('''Деятельность - это особый вид активности, присущий только человеку

Признаки деятельности:
1. Деятельность носит осознанный характер
2. Деятельность имеет цель
3. Деятельность зачастую носит творческий характер
4. Деятельность зачастую использует орудия труда
5. Деятельность зачастую направлена на преобразование окружающей среды

Элементы деятельности:
1. Субъект - тот, кто делает
2. Объект - то, над чем проводится работа и на что она направлена
3. Мотив - причина деятельности
4. Цель - то, чего человек добивается
5. Методы - это способ, которым выполняется деятельность
6. Процесс - само действие
7. Результат

Есть несколько видов деятельности:
1. Труд. Цель - достижение конкретного результата
2. Учение. Цель - приобретение опыта или информации, а также приобретение и развитие навыков
3. Общение. Цель - обмен опытом, информацией или эмоциями
4. Творчество. Цель - создание чего-либо нового
5. Игра. Цель - наслаждение процессом. Происходит в условной обстановке (с правилами)''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == 'sov14':
        markup = types.InlineKeyboardMarkup()
        ekv21 = types.InlineKeyboardButton('Вернуться к темам', callback_data='edit1')
        ekv22 = types.InlineKeyboardButton('Назад', callback_data='shpar4')
        markup.row(ekv21)
        markup.row(ekv22)
        bot.edit_message_text('''Семья - это малая социальная группа, основанная на браке или кровном родстве, члены которого связаны взаимопомощью, моральной и правовой ответственностью

Есть следующие виды семей:
1.Полные - неполные
2.Многодетные - малодетные - бездетные
3.Традиционные (патриархальные) - демократические (партнёрские)
4.Нулеарные (двухпоколенные) - расширенные (многопоколенные)

Брак - это добровольный союз мужчины и женщины, каждый из них имеет взаимные права и обязанности

Брак, заключённый в ЗАГСе является гражданским, а если брак не зарегистрирован, но люди ведут совместный быт, то это называется сожительством

Брак, заключенный ради выгоды, называется фиктивным

Условия заключения брака:
1. Достижение брачного возраста
2. Добровольное согласие
3. Отсутствие другого брака
4. Отсутствие близкого родства
5. Дееспособность обоих партнеров (понятие "дееспособность" подробно раскрыто в теме "Право")

Функции брака:
1. Репродуктивная
2. Экономическая
3. Досуговая
4. Воспитательная

Важно заметить, что родители обязаны заботиться о несовершеннолетних детях, а совершеннолетние дети обязаны заботиться о нетрудоспосбных родителях''',
                              callback.message.chat.id, callback.message.message_id, reply_markup=markup)


bot.polling(non_stop=True)