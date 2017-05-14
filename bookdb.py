import csv
from py2neo import Graph, Node, Relationship
import time
import os


url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = os.environ.get('neo4j')
password = os.environ.get('deepak007')

graph = Graph(url + '/db/data/', username=username, password=password)


with open('g:/books.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    count=0
    for row in readCSV:
        isbn=row[0]
        title=row[1]
        author= row[2]
        year= row[3]
        publisher= row[4]
        imageurl= row[7]



        try:

            book = Node('Book',
                        isbn=isbn,
                        title=title,

                        year=year,
                        imageurl=imageurl
                        )
            graph.merge(book)

            publisher = Node('Publisher', name=publisher)
            graph.merge(publisher)

            rel = Relationship(publisher, 'Published', book)
            graph.create(rel)



            author = Node('author', name=author)
            graph.merge(author)

            rel = Relationship(author, 'author', book)
            graph.create(rel)






            count = count + 1
            print(count)



        except Exception as e:
             print("Error storing in DB!"+str(e))