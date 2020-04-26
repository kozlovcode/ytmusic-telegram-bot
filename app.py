import os
import telebot
import time
from flask import Flask, request
from pytube import YouTube

bot = telebot.TeleBot(os.environ['token'])

server = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, 'Привет, отправь мне ссылку а я скину тебе песню ;-)')


@bot.message_handler(content_types=['text'])
def send_text(message):
	bot.send_chat_action(message.chat.id, 'upload_document')

	link = message.text 

	YouTube(link).streams.get_highest_resolution().download()
	yt = YouTube(link)
	filename = yt.title.replace('.','')
	artist = yt.title.replace('.','').split('-')[0]
	songtitle = yt.title.replace('.','').split('-')[1]

	yt.streams.filter(only_audio=True, mime_type='audio/mp4').order_by('abr')[-0].download()
	time.sleep(0.5)

	os.rename(f'{filename}.mp4', f'{filename}.m4a')
	time.sleep(0.5)
	ytsound = open(f'{filename}.m4a', 'rb')
	
	bot.send_audio(message.chat.id, ytsound, '', '', artist, songtitle)

	os.remove(f'{filename}.m4a')


@server.route('/', methods=['POST'])
def webhook():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200


if __name__ == '__main__':
	server.run()