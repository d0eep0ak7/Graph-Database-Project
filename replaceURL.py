from py2neo import Graph, Node, Relationship
from datetime import datetime
import time
import uuid
from models import find, timestamp, date
from models import graph
import json
import requests
import os


url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = os.environ.get('neo4j')
password = os.environ.get('deepak007')

newgraph = Graph(url + '/db/data/', username=username, password=password)



query = '''MATCH (m:Movie) where m.imdbRating='Rating Not Available' RETURN m.title as movie,m.imdbId as imdbId'''
results = graph.run(query)

count=0
URL={}





for row in results:

    imdbId=(row['imdbId']).strip()


    if not (imdbId==''):
        try:
            count = count + 1

            print(imdbId)
            r = requests.get('http://www.omdbapi.com/?i=' + imdbId)
            data = json.loads(r.text)
            source = float(data['imdbRating'])
            print(source)

            query = '''MATCH(n: Movie) where
                 n.imdbId = {imdbId} SET n.imdbRating={source}'''
            result = newgraph.run(query, imdbId=imdbId, source=source)

            print(count)

        except Exception:
             print("Key 2 is not exist!")
             source="Rating Not Available"
             query = '''MATCH(n: Movie) where
                            n.imdbId = {imdbId} SET n.imdbRating={source}'''
             result = newgraph.run(query, imdbId=imdbId, source=source)
    else:
        print("imdbRating not available")
        count = count + 1
        print(count)
        print(imdbId)
