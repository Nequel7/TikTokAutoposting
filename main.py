import os
import typer
from TikTokBot import BotPost, BotAuth
from db import DataBase
from supports import account_exists

app = typer.Typer()
db = DataBase('db_file/db.sqlite3')


# пост
@app.command()
def post(category: str):
    error_accounts = []
    if category == 'all':
        for i, account in enumerate(os.listdir('cookies')):
            bot = BotPost()
            try:
                bot.load_video(account=account, i=i)
                bot.close_browser()
                # selenium.common.exceptions.NoSuchElementException
            except Exception as ex:
                print('ERROR', ex, f'In account: {account.split("_")[0]}')
                error_accounts.append(account)
                bot.close_browser()
                continue
        if len(error_accounts) > 0:
            for i, err_acc in enumerate(error_accounts):
                bot = BotPost()
                try:
                    bot.load_video(account=err_acc, i=i)
                    bot.close_browser()
                except Exception as ex:
                    print('CRITICAL ERROR', ex, f'In account: {err_acc.split("_")[0]}')
                    bot.close_browser()
                    continue
    else:
        if db.category_exists(category):
            error_accounts = []
            for i, account in enumerate(db.get_accounts_in_category(category)):
                bot = BotPost()
                try:
                    bot.load_video(account=account, i=i)
                    bot.close_browser()
                    # selenium.common.exceptions.NoSuchElementException
                except Exception as ex:
                    print('ERROR', ex, f'In account: {account.split("_")[0]}')
                    error_accounts.append(account)
                    bot.close_browser()
                    continue
            if len(error_accounts) > 0:
                for i, err_acc in enumerate(error_accounts):
                    bot = BotPost()
                    try:
                        bot.load_video(account=err_acc, i=i)
                        bot.close_browser()
                    except Exception as ex:
                        print('CRITICAL ERROR', ex, f'In account: {err_acc.split("_")[0]}')
                        bot.close_browser()
                        continue
        else:
            print('❌ Категории с таким название не существует')


@app.command()
def auth(username: str):
    bot = BotAuth()
    bot.auth(username=username)


# добавить категорию
@app.command()
def add_category(category: str):
    if not db.category_exists(category=category):
        db.add_category(category=category)
        print('✅ Категория добавлена')
    else:
        print('❌ Категория с таким название уже существует')


# удалить категорию
@app.command()
def del_category(category: str):
    if db.category_exists(category=category):
        db.del_category(category=category)
        print('✅ Категория удалена')
    else:
        print('❌ Категории с таким название не существует')


# список аккаунтов по категориям
@app.command()
def categories():
    for k, v in db.get_accounts().items():
        accounts = '\n'.join([f"    {a[0]}" for a in v])
        print(f'{k}:\n'
              f'{accounts}')
        print(' ')


# добавление аккаунты в категорию
@app.command()
def add_account(category: str, account: str):
    if db.category_exists(category=category):
        if account_exists(account=account):
            db.add_account_in_category(category=category, account=account)
            print(f'Аккаунт ({account}) добавлен в категорию ({category})')
        else:
            print('❌ Аккаунт с таким названием не найден')

    else:
        print('❌ Категории с таким название не существует')


# удалить аккаунт из категории
@app.command()
def del_account(account: str):
    if account_exists(account):
        db.del_account(account)
        print(f'✅ Аккаунт удален из категории')
    else:
        print('❌ Аккаунт с таким названием не найден')


if __name__ == "__main__":
    app()
# копия видео
# закрывать страницу через крестик
# ожидания везде
# хештеги и собака в название
