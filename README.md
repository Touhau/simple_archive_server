# simple_archive_server

Основное приложение: server.py

Сторонние библиотеки: requests, aiohttp.

Поддерживает 5 команд. 

Первой командой должна быть: curl -X POST —data '{"login": {login}, "password": {password}}' {site}/auth, логины и пароли можно взять в файле json/auth.json.
После успешной авторазации можно использовать команды:

1)  POST запрос: curl -X POST -F 'url={url}' {site}/archive - для скачивания и разархивирования архивов типа .tar.gz, в ответ на запрос приходит ID архива в системе,
2)  GET запрос: curl {site}/archive/{id} - для вывода информации о состоянии архива,
3)  DELETE запрос: curl -X DELETE {site}/archive/{id} - для удаления архива.
4)  GET запрос: curl  {site}/logout - для разлогинивания.
