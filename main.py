import logging
import colorama
import configparser
from vk_parser import main

config = configparser.ConfigParser()
config.read('config.ini')
colorama.init()

TOKEN = config["Token"]["accesstoken"]
GROUP_ID = int(config["GroupId"]["groupid"])

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    try:
        api_token = TOKEN
        group_id = GROUP_ID
        output_file = "VKid.txt"

        logging.info(colorama.Fore.GREEN + "Запуск скрипта."+ colorama.Style.RESET_ALL)

        main(api_token, group_id, output_file)

        logging.info(colorama.Fore.GREEN +"Скрипт успешно завершил работу."+ colorama.Style.RESET_ALL)
    except Exception as e:
        logging.error(colorama.Fore.RED +f"Произошла ошибка: {e}"+ colorama.Style.RESET_ALL)
