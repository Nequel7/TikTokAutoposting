import dotenv
import os
from TikTokBot import BotPost
from multiprocessing import Pool

url = 'https://www.tiktok.com/'
dotenv.load_dotenv()


def load_mp(cookie):
    error_accounts = []
    bot = BotPost()
    try:
        bot.load_video(account=cookie, i=os.listdir('cookies').index(f'{cookie}'))
        # selenium.common.exceptions.NoSuchElementException
    except Exception as ex:
        print('ERROR' f'In account: {cookie.split("_")[0]}')
        error_accounts.append(cookie)
    finally:
        bot.close_browser()
    if len(error_accounts) > 0:
        for i, err_acc in enumerate(error_accounts):
            bot = BotPost()
            try:
                bot.load_video(account=err_acc, i=i)
            except Exception as ex:
                print('CRITICAL ERROR' f'In account: {err_acc.split("_")[0]}')
            finally:
                bot.close_browser()


# if len(error_accounts) > 0:
#     for i, err_acc in enumerate(error_accounts):
#         bot = BotPost()
#         try:
#             bot.load_video(account=err_acc, i=i)
#             bot.close_browser()
#         except Exception as ex:
#             print('CRITICAL ERROR', ex, f'In account: {err_acc.split("_")[0]}')
#             bot.close_browser()
#             continue


# if __name__ == '__main__':
#     p = Pool(processes=5)
#     p.map(load_mp, os.listdir('cookies'))
