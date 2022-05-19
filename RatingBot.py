import telebot
import pymysql

bot = telebot.TeleBot("xxx", parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    newMessage = sendMessage(message)
    if newMessage:
	    bot.reply_to(message, newMessage)

def sendMessage(message):
    userId = message.from_user.id
    sign = getMessageSign(message.text)
    if sign:
        if isUserInDB(userId):
            newRating = setNewRatingBySign(sign, userId)
            return 'Новый рейтинг: ' + str(newRating)
        else:
            setNewUser(userId)
            newRating = setNewRatingBySign(sign, userId)
            return 'Новый рейтинг: ' + str(newRating)
    else:
        return


def getMessageSign(messageText):
    if messageText[0] == '+':
        return '+'
    elif messageText[0] == '-':
        return '-'
    else:
        return False

def getUserRating(userId):
    con = setDbConnection()
    with con:

        cur = con.cursor()
        cur.execute('SELECT rating FROM ratings WHERE user_id=%s', userId)

        rating = cur.fetchone()

        return rating[0]

def setNewRatingBySign(sign, userId):
    currentRating = getUserRating(userId)
    if sign == '+':
        currentRating += 1
    elif sign == '-':
        currentRating -= 1
    con = setDbConnection()
    with con:
        cur = con.cursor()
        cur.execute('UPDATE ratings SET rating=%s WHERE user_id=%s', (currentRating, userId))
        con.commit()
    return currentRating

def setDbConnection():
    return pymysql.connect(host='localhost', user='root', passwd='', db='ratingbot')
    
def isUserInDB(userId):
    con = setDbConnection()
    with con:

        cur = con.cursor()
        cur.execute('SELECT * FROM ratings WHERE user_id=%s', userId)

        rowCount = cur.rowcount

        if rowCount == 0:
            return False
        return True

def setNewUser(userId):
    con = setDbConnection()
    with con:

        cur = con.cursor()
        cur.execute('INSERT INTO ratings (`user_id`) VALUES (%s)', str(userId))

        con.commit()

def changeRatingByMessage(message):
    return message

bot.infinity_polling()
