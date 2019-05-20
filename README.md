# Чекер работы API страховых компаний для https://strahovki24.ru

Выполняет запрос к каждой СК. Если в ответе признак ошибки - присылает письмо со списком СК
которые вернули ошибку и текстом ошибки.

Работает на Python 3.7 и выше. Внешних библиотек не требует

Настройки подключения к почтовику хранятся в `.env`

Список СК в справочнике `insurance_companies` внутри скрипта

`request.json` - шаблон тела запроса для расчета котировки