from bs4 import BeautifulSoup
import requests
import schedule
import subprocess
import json
from glucose import glucose_value

def bot_send_text(bot_message):
    
    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def report():
    #Glucose results
    actual_glucose, previous_glucose = glucose_value() 
    if actual_glucose > 180:
        glucose_result = f'Current: {actual_glucose}, HIGH'
    if actual_glucose < 70:
        glucose_result = f'Current: {actual_glucose}, LOW'
    if actual_glucose > 180 and previous_glucose > 180:
        glucose_result = f'Current: {actual_glucose}, STILL HIGH'
    if actual_glucose < 70 and previous_glucose < 70:
        glucose_result = f'Current:{actual_glucose}, STILL LOW'
    if actual_glucose > 70 and actual_glucose < 180:
        glucose_result = f'Current: {actual_glucose}, FUCK YEAH'

    #Glucose results add info if previous glucose is by 20 units higher or lower
    if actual_glucose - previous_glucose > 20:
        glucose_result = glucose_result + f', ⬆️'
    if previous_glucose - actual_glucose > 20:
        glucose_result = glucose_result + f', ⬇️'


    bot_send_text(glucose_result)


if __name__ == '__main__':
    
    schedule.every(20).minutes.do(report)
    
    while True:
        schedule.run_pending()