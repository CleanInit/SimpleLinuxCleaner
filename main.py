import os
import shutil
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename="cleaner.log",
                    filemode="a",
                    )

logs = logging.getLogger(__name__)

def _remove_path(path: str):
    if os.path.exists(path):
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
                logs.info(f"Удален файл: {path}")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                logs.info(f"Удалена папка: {path}")
        except Exception as e:
            logs.error(f'Не удалось удалить: {path} Ошибка:\n{e}')
            
def _clean_app_cache():
    logs.info('Очистка кеша приложений.')
    cache_dir = os.path.expanduser("~/.cache")
    _remove_path(cache_dir)

def _clean_system_logs():
    logs.info("Очистка системных логов.")
    for root, dirs, files in os.walk("/var/log"):
        for name in files:
            path = os.path.join(root, name)
            if not name.startswith(("dpkg", "apt", "Xorg.0")):
                _remove_path(path)

def _clean_apps_logs():
    logs.info("Очистка логов приложений.")
    home = os.path.expanduser("~")
    logs_dir = [os.path.join(home, ".local", "share"), os.path.join(home, ".config")]
    for path in logs_dir:
        for root, dirs, files in os.walk(path):
            for name in files:
                if "log" in name.lower():
                    _remove_path(os.path.join(root, name))

def _clean_package_cache():
    logs.info("Очистка APT-кэша.")
    logs.debug('Выполняется команда "apt clean"')
    subprocess.run("apt clean", shell=True)
    logs.debug('Выполняется команда "apt autoremove -y"')
    subprocess.run("apt autoremove -y", shell=True)
    logs.debug('Выполняется команда "pip3 cache purge"')
    subprocess.run("pip3 cache purge", shell=True)
    logs.debug('Выполняется команда "pip cache purge"')
    subprocess.run("pip cache purge", shell=True)

def _clean_crash_reports():
    logs.info("Очистка отчетов о сбоях.")
    _remove_path("/var/crash")

def _ask(question: str):
    answer_input = input(f"{question} [y/n]: ").strip().lower()
    result = answer_input == "y" or answer_input == "н"
    logs.debug(f'Вопрос: {question} \\ Ответ: "{answer_input}", результат {result}')
    if result:
        return True

def main():

    if _ask("Очистить кеш приложений ?"):
        _clean_app_cache()
    if _ask("Очистить системные логи?"):
        _clean_system_logs()
    if _ask("Очистить логи приложений?"):
        _clean_apps_logs()
    if _ask("Очистить APT-кэш"):
        _clean_package_cache()
    if _ask("Очистить отчёты о сбоях?"):
        _clean_crash_reports()
    
    logs.info(f'Очистка завершена!')

if __name__ == "__main__":
    main()