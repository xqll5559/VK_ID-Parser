import vk_api
import logging
import colorama
import tqdm
from typing import List

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO, encoding='utf-8')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def authenticate(api_token: str) -> vk_api.vk_api.VkApi:
    """Аутентификация в VK API."""
    try:
        vk_session = vk_api.VkApi(token=api_token)
        vk = vk_session.get_api()
        logger.info(colorama.Fore.GREEN + "Успешная аутентификация в VK API." + colorama.Style.RESET_ALL)
        return vk
    except vk_api.exceptions.ApiError as e:
        logger.error(colorama.Fore.RED + f"Ошибка при аутентификации в VK API: {e}" + colorama.Style.RESET_ALL)
        raise
    except ValueError as ve:
        logger.error(colorama.Fore.RED + f"Ошибка при аутентификации в VK API: {ve}" + colorama.Style.RESET_ALL)
        raise


def get_group_members_ids(vk: vk_api.vk_api.VkApi, group_id: str, count: int = 1000) -> List[int]:
    """Получение всех ID подписчиков сообщества."""
    members_ids = []
    total_members_count = 0

    try:
        offset = 0
        total_members = vk.groups.getMembers(group_id=group_id, v=5.131)['count']

        with tqdm.tqdm(total=total_members, desc='Получение ID подписчиков') as pbar:
            while True:
                members_chunk = vk.groups.getMembers(group_id=group_id, v=5.131, offset=offset, count=count)
                members_chunk_ids = members_chunk['items']
                members_ids.extend(members_chunk_ids)
                total_members_count += len(members_chunk_ids)

                pbar.update(len(members_chunk_ids))

                if len(members_chunk_ids) < count:
                    break
                offset += count

        logging.info(colorama.Fore.YELLOW + f"Получено {total_members_count} ID подписчиков."+ colorama.Style.RESET_ALL)
    except vk_api.exceptions.ApiError as e:
        logging.error(colorama.Fore.RED + f"Ошибка при получении подписчиков: {e}"+ colorama.Style.RESET_ALL)
        raise

    return members_ids

def save_ids_to_file(user_ids: List[int], filename: str):
    """Сохранение ID в текстовый файл."""
    with open(filename, 'w') as file:
        for user_id in user_ids:
            file.write(str(user_id) + '\n')

def main(api_token: str, group_id: str, output_file: str):
    """Основная функция парсера."""
    vk = authenticate(api_token)
    members_ids = get_group_members_ids(vk, group_id)
    save_ids_to_file(members_ids, output_file)

   
