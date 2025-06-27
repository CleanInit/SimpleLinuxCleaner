# SimpleLinuxCleaner

## Мини очистка вашей системы.
Очищает:
* ~/.cache (Очистка кеша приложений.)
* /var/log (Очистка логов приложений.)
* ~/.local, ~/share, ~/.config (Очистка логов приложений.)
* /var/crash (Очистка отчетов о сбоях.)

Выполняет следующие команды для очистки кеша (Очистка APT-кэша.):
* apt clean
* apt autoremove -y
* pip3 cache purge
* pip cache purge

## Запуск:
```
python main.py
```
или
```
python3 main.py
```
