Курсовая работа 6

Задание
В рамках проекта вам необходимо получить данные о компаниях и вакансиях с сайта hh.ru, спроектировать таблицы в БД PostgreSQL и загрузить 
полученные данные в созданные таблицы.

Структура проекта

Корень проекта
- main.py: главный фаил с программой
- Readme.MD: описание проекта
- pyproject.toml: конфигурационный файл проекта
- poetry.lock: зависимости

Папка classes:
- headhunter.py: класс HeadHunter - предназначен извлечения и хранения вакансий с сайта hh.ru в формате списка словарей, содержит также 
   информацию о работодателях в формате списка словарей.
- dbmanаger.py: класс DBManager - предназначен для создания и наполнения БД, а также предоставления дополнительной информации по
   желанию пользователя.

Папка utils:
- config.py: содержит функцию config(), которая извлекает необходимые для подключения к СУБД Postgres параметры из файла database.ini.


Принцип работы:
1. Создается экземпляр класса HeadHunter, в который при помощи метода get_vacancies в поле vacancies заносятся вакансии 10 работодателей.
    От каждого работодателя берется максимум 2000 вакансий, но игнорируются вакансии с пустым значением "зарпалата".
    Вакансии хранятся в виде словарей со следующими данными: id вакансии, id работодателя, название вакансии, описание, опыт, зарплата от,
    зарплата до, город, ссылка на вакансию, дата размещения.
2. Создается экземпляр класса DBManager, создается БД с таблицами "вакансии"(vacancies) и "работодатели"(employers) в СУБД Postgres.
3. Таблицы БД заполняются данными, хранящимися в экземпляре класса HeadHunter.
4. Пользователя извещают об окончании сбора информации в БД и предлагается на выбор получить следующую информацию:
    - Список всех компаний и количества вакансий у каждой компании.
    - Список всех вакансий всех компаний.
    - Список средней зарплаты по вакансиям компаний.
    - Список всех вакансий, у которых зарплата выше средней по всем вакансиям.
    - Список всех вакансий, содержащих ключевое слово.
 5. Пользователь может выбрать какое либо действие, либо отказаться и завершить работу программы.



