import argparse
import os
import numpy as np
import pandas as pd
import lancedb

# Создаем парсер аргументов командной строки
parser = argparse.ArgumentParser(description="Создание таблицы")

# Добавляем необязательный аргумент
parser.add_argument("-d", "--directory", help="Указать папку с хранящимися векторами")
parser.add_argument("-n", "--dbname", help="Указать имя базы данных")

# Добавляем флаг
parser.add_argument("-drop", "--droptable", action="store_true", help="Удалить таблицу, если она существует")

# Разбираем аргументы командной строки
args = parser.parse_args()


if args.directory:
    vectors = []  
    for file_name in os.listdir(args.directory):
        if file_name.endswith('.vec'):
            vector = np.loadtxt(os.path.join(args.directory, file_name))
            vectors.append(vector)
    vects_with_num = []
    for i, vect in enumerate(vectors):
        vects_with_num.append({"vector": vect, "num": i})
    df = pd.DataFrame(vects_with_num)
    uri = "data/sample-lancedb"
    db = lancedb.connect(uri)
    if args.droptable:
        try:
            db.drop_table(args.dbname)
            db.create_table(args.dbname, data=df)
        except:
            print("Нет таблицы с таким названием, попробуйте убрать флаг -drop")
    else:
        try:
            db.create_table("my_table", data=df)
        except:
            print("Произошла ошибка при создании таблицы, возможно таблица с таким названием уже существует, попробуйте добавить флаг -drop")
    print("Таблица успешно создана")
else:
    print("Укажите папку и векторами для индексации, а также название таблицы. Попробуйте написать -help")
