## Бот для запуска процессов CI/CD в репозитории на GitHub.com

### Бот имеет следующие команды:

* Просмотр списка доступных (сохраненных в боте) процессов CI/CD. Выводятся {owner}/{repo} и {workflow_id} для каждого процесса.
* Добавление нового процесса CI/CD в список доступных. При добавлении пользователь должен ввести организацию {owner}, название репозитория {repo}, имя файла с командами CI/CD или его идентификатор {workflow_id}, токен для доступа к GitHub API и название ветки {ref}.
* Удаление процесса CI/CD из списка доступных.
* Выбор одного из доступных CI/CD процессов и его запуск.