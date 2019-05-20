import os
from dotenv import load_dotenv

import requests
import datetime
import json

import smtplib
from email.mime.text import MIMEText
from email.header import Header


def insurance_single_quote_get(insurance_company_id = 10):
    start_date = datetime.date.today() + datetime.timedelta(5)
    end_date = start_date + datetime.timedelta(7)

    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    with open('request.json', 'r') as request_file:
        data = json.load(request_file)

    data['startDate'] = start_date
    data['endDate'] = end_date
    json_string = json.dumps(data)

    url = 'https://strahovki24.ru/TravelNew/insuranceSingleQuoteGet'
    payload = {
        'insuranceCompanyId': insurance_company_id,
        'json': json_string
    }

    try:
        response = requests.post(url, data=payload)
        response_json = json.loads(response.text)
        is_ok = response_json.get('isOk')
        insurance_price = response_json.get('data').get('insurancePrice') if is_ok else 0

        if is_ok and insurance_price == 0:
            is_ok = False
            result_text = 'Нулевая цена полиса'
        else:
            result_text = response_json.get('resultText')
    except:
        is_ok = False
        result_text = 'Ошибка выполнения запроса'

    return is_ok, result_text


def email_send(emails, subject, body_text):
    load_dotenv()
    host = os.getenv('EMAIL_HOST')
    port = os.getenv('EMAIL_PORT')
    from_address = os.getenv('EMAIL_FROM_ADDRESS')
    login = os.getenv('EMAIL_LOGIN')
    password = os.getenv('EMAIL_PASSWORD')

    msg = MIMEText(body_text, 'plain', 'utf-8')
    msg['From'] = from_address
    msg['Subject'] = Header(subject, 'utf-8')

    if isinstance(emails, (list,)):
        msg['To'] = ", ".join(emails)
    else:
        msg['To'] = emails

    try:
        server = smtplib.SMTP_SSL(host, port)
        server.login(login, password)
        server.sendmail(msg['From'], emails, msg.as_string())
        server.quit()
    except smtplib.SMTPResponseException as e:
        return e.smtp_code, e.smtp_error

    return True


if __name__ == '__main__':
    insurance_companies = {
        1: 'Гайде',
        2: 'Ренессанс Страхование',
        3: 'Согласие',
        7: 'Альфастрахование',
        8: 'Либерти Страхование',
        9: 'Уралсиб Страхование',
        10: 'Абсолют Страхование',
        12: 'Ингосстрах',
        13: 'ВТБ Страхование',
        14: 'Альянс',
        15: 'Тинькофф Страхование',
    }

    checklist = []
    for id, name in insurance_companies.items():
        is_ok, result_text = insurance_single_quote_get(id)
        if not is_ok:
            checklist.append((name, is_ok, result_text))

    if len(checklist) > 0:
        mail_text = 'Ошибка расчета котировки в одной или нескольких СК на сайте https://strahovki24.ru/\n\n'
        for insurance_company, _, result_text in checklist:
            mail_text += f'\n{insurance_company} {result_text}'

        email_send('grepto@gmail.com', '[strahovki24.ru] Отвалилась страховая компания', mail_text)











