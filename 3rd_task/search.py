import argparse
import os
import numpy as np
import pandas as pd
import lancedb
from sentence_transformers import SentenceTransformer

# Создаем парсер аргументов командной строки
parser = argparse.ArgumentParser(description="Поиск в таблице")

# Добавляем необязательный аргумент
parser.add_argument("-t", "--text", help="Указать текст для поиска")
parser.add_argument("-n", "--dbname", help="Указать имя базы данных")
parser.add_argument("-p", "--path", help="Путь к вектору, по которому делаем поиск")
parser.add_argument("-k", "--k_neighbors", help="Количество похожих векторов")

# Добавляем флаг
parser.add_argument("-drop", "--droptable", action="store_true", help="Удалить таблицу, если она существует")

# Разбираем аргументы командной строки
args = parser.parse_args()



if args.text or args.path:
    uri = "data/sample-lancedb"
    db = lancedb.connect(uri)
    try:
        tbl = db.open_table(args.dbname)
    except:
        print("Введите название базы данных, используя аргумент -n (Или такой таблицы не существует)")
    if args.text:
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')
        vector = model.encode(args.text)
    elif args.path:
        vector = np.loadtxt(args.path)
    if args.k_neighbors:
        results = tbl.search(vector).limit(int(args.k_neighbors)).to_list()
        print("Результаты (Номера индексов):")
        for result in results:
            print(result["num"])
    else:
        print("Укажите желаемое количество результатов, используя результат -k")
else:
    print("Укажите текст для поиска (аргумент -t), или путь к вектору для поиска (аргумент -p), пропишите --help")