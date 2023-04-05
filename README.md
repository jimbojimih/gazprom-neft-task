Кейс – Разработчик Backend

*	Необходимо реализовать импорт данных цитат википедии и сервис для поиска статьи по точному совпадению наименования.
*	Дамп данных Википедии можно взять отсюда: https://dumps.wikimedia.org/other/cirrussearch/current/ruwikiquote-<ДД.ММ.ГГГГ>-cirrussearch-general.json.gz Все данные должны быть сохранены в БД (PostgreSQL либо MongoDB). Сервис поиска статьи должен искать статью по полному совпадению наименования без учета регистра. 
*	Импорт данных. Поля необходимые для импорта: create timestamp, timestamp, language, wiki, category, title, auxiliary text. По полю category необходимо составить справочник и создать отношение в БД. Даты должны храниться в виде даты. Тип хранения auxiliary_text – на ваше усмотрение. Разбор дампа можно производить из локальной папки предварительно разархивировав.
*	Сервис поиска статьи. Сервис должен выдавать JSON, где auxiliary_text – массив, а переменные с датами выдаются в виде числа UNIX-времени. Сервис должен иметь возможность выдавать json в виде одной строки, либо форматированный.
Примеры запросов к сервису: /wiki/<зазвание статьи> -ответ-строка, форматированный вывод /wiki/<название статьи>?pretty
*	Дополнительные задания:
вывод статистики по количеству статей для каждой категории
редактирование статьи: текста, названия, списка категорий с изменением поля timestamp*

**Комментарии:  **
1)Подключение к PostgreSQL. 
Перейти в папку \task_OparinDV\wiki
Открыть файл с переменными окружения .env и установить необходимые значения для подключения к локальной БД (имя, пароль и название БД)

2)Инициализация сервиса.
Для запуска сервиса необходимо создать виртуальное окружение python –m vevn env
Перейти в папку \env\Scripts, выполнить команду activate.bat
Перенести в папку файл requirements.txt
Выполнить команду pip install -r requirements.txt
Перейти в папку task_OparinDV\wiki и выполнить команду python manage.py runserver 
 
3)Инициализация импорта данных
Перейти по адресу http://127.0.0.1:8000/import
Нажать на кнопку Start Import и дождаться сообщения Import finished (или-же просто отправить запрос POST по данному адресу)
*файл ruwikiquote-"тут дата"-cirrussearch-general.json положить в корневую папку

4)Комментарии к выполнению.
По адресу http://127.0.0.1:8000/category/ можно получить список категорий с количеством цитат по каждой категории 
Для каждого объекта данных цитат (quote) можно выполнить запрос с методом PATCH для изменения текста (auxiliary_text), названия (title).
Например, при отправке PATCH по адрессу http://127.0.0.1:8000/wiki/reki/?pretty с данными:
 
Получаем изменённый обьект с обновлённым слагом (зависит от title) по адрессу 
http://127.0.0.1:8000/wiki/test/?pretty 
timestamp обновляется автоматически.
