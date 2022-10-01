# packages that we have to used
# request for http request
# bs4 (beautifulsoup)for web scrapping
# smptplib is for email authentication
# email.mime for creating email body
# datetime for manipualting date and time

# u have to install all the libraries inorder to work on this project


import requests
# for web scraping
from bs4 import BeautifulSoup

import smtplib

# for creating email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime

now = datetime.datetime.now()

content = ""

# extracting Hacker News Stories:


def extract_news(url):
    print("Extracting Hacker News Stories")
    cnt = ""
    cnt += ('<b>Hacker News Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        cnt += ((str(i+1)+' :: ' + '<a href="' + tag.a.get('href') + '">' +
                tag.text + '</a>' + "\n" + '<br>') if tag.text != 'More' else '')
        # print(tag.prettify) #find_all('span',attrs={'class':'sitestr'}))
    return (cnt)


cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content += ('<br><br>End of Message')


# lets send the email

print('Composing Email...')

# update your email details
# make sure to update the Google Low App Access settings before

SERVER = 'smtp.gmail.com'
# "your smtp server"
PORT = 587
# your port number
FROM = ''
# "your from email id"
TO = ''
# "your to email ids"  # can be a list
PASS = '*****'
# "your email id's password"

# fp = open(file_name, 'rb')
# Create a text/plain message
# msg = MIMEText('')
msg = MIMEMultipart()

# msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + \
    str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
# fp.close()

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)

#server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)
server.ehlo()

server.starttls()
# server.ehlo(problem here)
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()
