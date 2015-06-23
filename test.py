import elasticsearch
import pymysql
from LibreEngine.include.models import *

es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200
def getespost():
    connection = pymysql.connect(host='sv3.al.gl',
                                 user='libredev',
                                 passwd='libre_dev',
                                 db='libredev',
                                 charset='utf8mb4')

    oldsql = "SELECT id FROM `documents` WHERE 1 ORDER BY `documents`.`id` ASC;"

    newcursor = connection.cursor()

    newcursor.execute(oldsql)
    for nrow in newcursor:
        print(nrow)
        print(nrow[0])
        test = str(nrow[0])
        print(test)
        #searchname = "'%"+nrow+"%'"


        cursor = connection.cursor()

        sql = "SELECT `id`, `document` FROM `documents` WHERE id = '" + test + "' ORDER BY `documents`.`id` ASC;"

        cursor.execute(sql)
        #print(cursor.fetchall())
        for row in cursor:
            print(row)
            escontent = row
            id = escontent[0]
            document = escontent[1]


        es.index(index='search', doc_type='mysql', id=id, body={
            'author': 'libredev',
            'document': document,
        })


getespost()
'''
es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200

es.index(index='search', doc_type='mysql', id='1', body={
    'author': 'Santa Clause',
    'blog': '아하하',
    'title': 'Using Celery for distributing gift dispatch',
    'topics': ['slave labor', 'elves', 'python',
               'celery', 'antigravity reindeer'],
    'awesomeness': 0.2
})
'''