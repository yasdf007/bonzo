<img align="right" src="static/bonzo.png" width="160" height="160">

## bonzo v1.13.1 stacknox2
## made by /bonzoTeam & others
### Модульный Discord-бот с открытым исходным кодом.

На данный момент [лицензия](LICENSE) запрещает любое использование исходного кода bonzo в иных проектах. Мы планируем изменение лицензии на более свободную в последующих обновлениях. Подробные новости о разработке bonzo предоставляются посредством соответствующих каналов в [AloneClub.](https://discord.gg/XDZWus5)

### Полезные ссылки:
   Пригласить bonzo на свой сервер: [тык!](https://discordapp.com/api/oauth2/authorize?client_id=680132907859443790&amp;permissions=8&amp;scope=bot)\
   Сервер поддержки и новостей о bonzo (AloneClub): [тык!](https://discord.gg/XDZWus5)

### Запуск собственной инстанции:
I. PREREQUISITE
   1. Клон репозитория bonzo в удобной директории (без кириллических символов в пути)
   2. Приложение с токеном на [Discord Developer Portal](https://discord.com/developers/applications)
    
   3. Установленные инструменты
      - [Python 3.9+](https://www.python.org/downloads/release/python-397/)
      - [Java 13+](https://www.oracle.com/java/technologies/downloads/) (для музыки)
      - [Postgresql](https://www.postgresql.org/download/) (для опыта и настроек)
  
      <div align='center'> ИЛИ </div>
      
      - [Docker](https://docs.docker.com/get-docker/) и [docker compose](https://docs.docker.com/compose/install/)

   4. [Lavalink](https://github.com/freyacodes/Lavalink) (для музыки)

II. CONFIGURATION
- Используя образец конфигурационного файла .env.example, создайте и заполните конфигурационный файл .env в корневой папке.
- Скопировать `Lavalink.jar` и `application.yml` в папку `lavalink`

III. RUNNING NODE

**Используя Docker**:
- >$ docker-compose up


**Используя нативные инструменты:**
* TBA


Запуск собственной инстанции на данный момент рекомендуется только разработчикам. Помощь по запуску инстанции можно запросить на сервере поддержки.

powered by [discord.py](https://github.com/Rapptz/discord.py) and [discord-interactions](https://github.com/discord-py-slash-commands/discord-py-interactions) 

остальные используемые библиотеки описаны в [requirements.txt](/requirements.txt)
