import sys
import sqlite3
from phone_record_repository import PhoneRecordRepository
from phone_pattern_error import PhonePatternError

def open_menu():
    scenestr = input('''

    番号を入力してください。
    1:電話番号を検索
    2:電話番号を登録
    3:電話番号を削除
    4:電話番号を一覧
    0:プログラムの終了
    -> '''[1:])

    if scenestr == '0':
        print('プログラムを終了します')
        sys.exit()

    elif scenestr == '1':
        name = input('検索する名前を入力してください：')
        try:
            record = repository.find_by_name(name)
            print('名前：{}'.format(record[1]) + ' 電話番号：{}'.format(record[2]))
        except:
            print('名前：{} は登録されていません'.format(name))

        open_menu()

    elif scenestr == '2':
        name = input('登録する名前を入力してください：')
        phone_number = input('電話番号（ハイフンあり）を入力してください（例：080-1234-5678）：')
        try:
            repository.save(name, phone_number)
            print('名前：{}'.format(name) + ' 電話番号：{}'.format(phone_number) + ' で登録しました')
        except PhonePatternError as e:
            print('正しい形式で電話番号を入力してください')

        open_menu()

    elif scenestr == '3':
        name = input('削除する名前を入力してください：')
        try:
            repository.delete(name)
            print('名前：{}'.format(name) + ' の電話番号は削除されました')
        except:
            print('名前：{} は登録されていません'.format(name))

        open_menu()

    elif scenestr == '4':
        all = repository.fetch_all()
        for row in all:
            print('名前：{}'.format(row[1]) + ' 電話番号：{}'.format(row[2]))
        open_menu()

    else:
        print('正しい番号（半角）を入力してください')
        open_menu()

repository = PhoneRecordRepository()
conn = sqlite3.connect(repository.DB_NAME)
c = conn.cursor()

try:
    c.execute('CREATE TABLE IF NOT EXISTS phone_records (id INTEGER PRIMARY KEY AUTOINCREMENT, person_name TEXT NOT NULL, phone_number TEXT NOT NULL)')

    open_menu()

except sqlite3.Error as e:
    print('sqlite3.Error occurred:', e.args[0])
