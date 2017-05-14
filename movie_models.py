
from py2neo import Graph, Node, Relationship
from datetime import datetime
import uuid
from models import find,timestamp,date
from models import graph

def get_movies(limit):
    query = '''MATCH (m:Movie)<-[:ACTS_IN]-(a:Person)
             RETURN m.title as movie,m.imdbId as imdbId , m.imageUrl as imageUrl , collect(a.name) as cast Limit {limit}'''
    results = graph.run(query,limit=limit)
    return results

def genres_list(genre_name,limit,skip):

    query='''
                MATCH (n:Movie)where n.genre={genre_name} with count(n) as total  return total     '''


    count=graph.run(query,genre_name=genre_name)




    query = '''MATCH (m:Movie) where m.genre={genre_name}  RETURN m.title as title ,m.imdbId as imdbId ,m.imageUrl as imageUrl Skip {skip} Limit {limit}'''
    results = graph.run(query,genre_name=genre_name,limit=limit,skip=skip)
    for x in count:
        resultscount=x['total']


    return results,resultscount

def rate_movie(username,imdbId,rating):

    query='''MATCH (n:User{username:{username}}),(m:Movie{imdbId:{imdbId}})
    MERGE (n)-[r:RATED]->(m) set r.stars={rating} return r.stars as stars'''
    results = graph.run(query, username=username, imdbId=imdbId,rating=rating)
    return results

def rated_movie(username,skip):
    query = ''' MATCH(n: User
    {username: {username}})-[r: RATED]->(m: Movie) with count(m) as total  return total'''
    count = graph.run(query, username=username)
    for x in count:
        resultscount = x['total']


    query = '''MATCH (n:User{username:{username}})-[r:RATED]->(m:Movie) return m.title as title ,m.imdbId as imdbId ,m.imageUrl as imageUrl, r.stars as stars Skip {skip} Limit 102'''
    results = graph.run(query, username=username,skip=skip)
    return results,resultscount

def random_movies(username):
    query='''MATCH (m: Movie)where NOT (:User{username:{username}})-[:RATED]->(m:Movie)with m,
    rand() AS number return m.title as title , m.imdbId as imdbId ,m.imageUrl as imageUrl, m.description as description ,m.releaseDate as releaseDate ORDER BY number  LIMIT 10 '''
    results = graph.run(query, username=username)
    return results


def update_similarity():
    query='''MATCH (p1:User)-[x:RATED]->(m:Movie)<-[y:RATED]-(p2:User)
          WITH  SUM(x.stars * y.stars) AS xyDotProduct,
          SQRT(REDUCE(xDot = 0.0, a IN COLLECT(x.stars) | xDot + a^2)) AS xLength,
          SQRT(REDUCE(yDot = 0.0, b IN COLLECT(y.stars) | yDot + b^2)) AS yLength,
          p1, p2
          MERGE (p1)-[s:SIMILARITY]-(p2)
          SET   s.similarity = xyDotProduct / (xLength * yLength)

    '''
    results = graph.run(query)

def similar_movies(username):
    query=''' MATCH (b:User)-[r:RATED]->(m:Movie), (b)-[s:SIMILARITY]-(a:User {username:{username}})
WHERE NOT((a)-[:RATED]->(m))
WITH m, s.similarity AS similarity, r.stars AS stars
ORDER BY m.title, similarity DESC
WITH m.title AS movie,m.imageUrl AS imageUrl,m.description AS description ,COLLECT(stars)[0..3] AS ratings
WITH movie,imageUrl,description, REDUCE(s = 0, i IN ratings | s + i)*1.0 / SIZE(ratings) AS reco
ORDER BY reco DESC
RETURN movie AS title, reco AS Recommendation ,imageUrl,description LIMIT 200

    '''
    results = graph.run(query, username=username)

    return results


def suggest_movies(username,gender,companion,emotions,criteria):


        query1=query2=""
        if gender=='female':
            query1,query2=suggest_female_movies(companion,emotions)


        elif gender=='male':
            query1, query2 = suggest_male_movies(companion, emotions)

        else:
            query1, query2 = suggest_general_movies(companion, emotions)




        if criteria=="both":

                results1 = graph.run(query1, username=username)
                results2 = graph.run(query2, username=username)

                set1=set()
                set2=set()

                for row in results1:

                    set1.add(row)

                for row in results2:
                    set2.add(row)


                movies=set1.intersection(set2)

        elif criteria=="emotion":
                movies = graph.run(query1, username=username)

        elif criteria=="companion":
                movies = graph.run(query2, username=username)
        else:
            results1 = graph.run(query1, username=username)
            results2 = graph.run(query2, username=username)

            set1 = set()
            set2 = set()

            for row in results1:
                set1.add(row)

            for row in results2:
                set2.add(row)

            movies = set1.union(set2)

        return movies


def suggest_female_movies(companion,emotions):
        query=""

        if emotions=='happy':
            query='''MATCH(m: Movie)where
            NOT(: User
            {username: {username}})-[: RATED]->(m: Movie) AND
            m.imdbRating >= 7.5
            AND(m.genre = 'Romance' OR m.genre = 'Comedy' OR m.genre = 'Family') with m,
            rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre,m.description as description ORDER BY number LIMIT 50'''

        elif emotions=='sad':
            query='''MATCH(m: Movie)where
            NOT(: User
            {username: {username}})-[: RATED]->(m: Movie) AND
            m.imdbRating >= 7.5
            AND(m.genre = 'Comedy' OR m.genre = 'Family' OR m.genre = 'Animation') with m,
            rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

        elif emotions=='excited':
            query='''MATCH(m: Movie)where
            NOT(: User
            {username: {username}})-[: RATED]->(m: Movie) AND
            m.imdbRating >= 7.5
            AND(m.genre = 'Romance' OR m.genre = 'Thriller') with m,
            rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

        elif emotions=='bored':
            query='''MATCH(m: Movie)where
            NOT(: User
            {username: {username}})-[: RATED]->(m: Movie) AND
            m.imdbRating >= 7.5
            AND(m.genre = 'Romance' OR m.genre = 'Comedy' OR m.genre = 'Horror') with m,
            rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''


        elif emotions=='angry':
            query='''MATCH(m: Movie)where
            NOT(: User
            {username: {username}})-[: RATED]->(m: Movie) AND
            m.imdbRating >= 7.5
            AND(m.genre = 'Action' OR m.genre = 'Comedy' OR m.genre = 'Thriller') with m,
            rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''






        query2 = ""
        if companion=='alone':
            query2='''MATCH(m: Movie)where
            NOT(: User
            {username: {username}})-[: RATED]->(m: Movie) AND
            m.imdbRating >= 7.5
            AND(m.genre = 'Romance' OR m.genre = 'Comedy' OR m.genre = 'Horror') with m,
            rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''


        elif companion=='family':
            query2='''MATCH(m: Movie)where
            NOT(: User
            {username: {username}})-[: RATED]->(m: Movie) AND
            m.imdbRating >= 7.5
            AND(m.genre = 'Drama' OR m.genre = 'Comedy' OR m.genre = 'Family') with m,
            rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

        elif companion=='friends':
            query2='''MATCH(m: Movie)where
            NOT(: User
            {username: {username}})-[: RATED]->(m: Movie) AND
            m.imdbRating >= 7.5
            AND(m.genre = 'Thriller' OR m.genre = 'Comedy' OR m.genre = 'Horror') with m,
            rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''


        elif companion=='sibling':
            query2='''MATCH(m: Movie)where
            NOT(: User
            {username: {username}})-[: RATED]->(m: Movie) AND
            m.imdbRating >= 7.5
            AND(m.genre = 'Fantasy' OR m.genre = 'Comedy' OR m.genre = 'Horror') with m,
            rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

        elif companion== 'soulmate':
            query2= '''MATCH(m: Movie)where
                NOT(: User
                {username: {username}})-[: RATED]->(m: Movie) AND
                m.imdbRating >= 7.5
                AND(m.genre = 'Romance' OR m.genre = 'Comedy' OR m.genre = 'Family') with m,
                rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

        return query,query2


def suggest_male_movies(companion, emotions):
    query = ""

    if emotions == 'happy':
        query = '''MATCH(m: Movie)where
               NOT(: User
               {username: {username}})-[: RATED]->(m: Movie) AND
               m.imdbRating >= 7.5
               AND(m.genre = 'Action' OR m.genre = 'Comedy' OR m.genre = 'Animation') with m,
               rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    elif emotions == 'sad':
        query = '''MATCH(m: Movie)where
               NOT(: User
               {username: {username}})-[: RATED]->(m: Movie) AND
               m.imdbRating >= 7.5
               AND(m.genre = 'Comedy' OR m.genre = 'Romance' OR m.genre = 'Adventure') with m,
               rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    elif emotions == 'excited':
        query = '''MATCH(m: Movie)where
               NOT(: User
               {username: {username}})-[: RATED]->(m: Movie) AND
               m.imdbRating >= 7.5
               AND(m.genre = 'Adventure' OR m.genre = 'Action' OR m.genre = 'Thriller') with m,
               rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    elif emotions == 'bored':
        query = '''MATCH(m: Movie)where
               NOT(: User
               {username: {username}})-[: RATED]->(m: Movie) AND
               m.imdbRating >= 7.5
               AND(m.genre = 'Action' OR m.genre = 'Comedy' OR m.genre = 'Horror') with m,
               rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''


    elif emotions == 'angry':
        query = '''MATCH(m: Movie)where
        NOT(: User
        {username: {username}})-[: RATED]->(m: Movie) AND
        m.imdbRating >= 7.5
        AND(m.genre = 'Action' OR m.genre = 'Comedy' OR m.genre = 'Fantasy') with m,
        rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    query2 = ""
    if companion == 'alone':
        query2 = '''MATCH(m: Movie)where
               NOT(: User
               {username: {username}})-[: RATED]->(m: Movie) AND
               m.imdbRating >= 7.5
               AND(m.genre = 'Romance' OR m.genre = 'Science Fiction' OR m.genre = 'Thriller') with m,
               rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''


    elif companion == 'family':
        query2 = '''MATCH(m: Movie)where
               NOT(: User
               {username: {username}})-[: RATED]->(m: Movie) AND
               m.imdbRating >= 7.5
               AND(m.genre = 'Drama' OR m.genre = 'Comedy' OR m.genre = 'Family') with m,
               rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    elif companion == 'friends':
        query2 = '''MATCH(m: Movie)where
               NOT(: User
               {username: {username}})-[: RATED]->(m: Movie) AND
               m.imdbRating >= 7.5
               AND(m.genre = 'Thriller' OR m.genre = 'Comedy' OR m.genre = 'Horror') with m,
               rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''


    elif companion == 'sibling':
        query2 = '''MATCH(m: Movie)where
               NOT(: User
               {username: {username}})-[: RATED]->(m: Movie) AND
               m.imdbRating >= 7.5
               AND(m.genre = 'Family' OR m.genre = 'Comedy' OR m.genre = 'Horror') with m,
               rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    elif companion == 'soulmate':
        query2 = '''MATCH(m: Movie)where
                   NOT(: User
                   {username: {username}})-[: RATED]->(m: Movie) AND
                   m.imdbRating >= 7.5
                   AND(m.genre = 'Romance' OR m.genre = 'Comedy' OR m.genre = 'Fantasy') with m,
                   rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    return query, query2







def suggest_general_movies(companion, emotions):
    query = ""

    if emotions == 'happy':
        query = '''MATCH(m: Movie)where
                   NOT(: User
                   {username: {username}})-[: RATED]->(m: Movie) AND
                   m.imdbRating >= 7.5
                   AND(m.genre = 'Romance' OR m.genre = 'Comedy' OR m.genre = 'Animation') with m,
                   rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    elif emotions == 'sad':
        query = '''MATCH(m: Movie)where
                   NOT(: User
                   {username: {username}})-[: RATED]->(m: Movie) AND
                   m.imdbRating >= 7.5
                   AND(m.genre = 'Comedy' OR m.genre = 'Family' OR m.genre = 'Animation') with m,
                   rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    elif emotions == 'excited':
        query = '''MATCH(m: Movie)where
                   NOT(: User
                   {username: {username}})-[: RATED]->(m: Movie) AND
                   m.imdbRating >= 7.5
                   AND(m.genre = 'Adventure' OR m.genre = 'Romance' OR m.genre = 'Thriller') with m,
                   rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    elif emotions == 'bored':
        query = '''MATCH(m: Movie)where
                   NOT(: User
                   {username: {username}})-[: RATED]->(m: Movie) AND
                   m.imdbRating >= 7.5
                   AND(m.genre = 'Thriller' OR m.genre = 'Comedy' OR m.genre = 'Horror') with m,
                   rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''


    elif emotions == 'angry':
        query = '''MATCH(m: Movie)where
            NOT(: User
            {username: {username}})-[: RATED]->(m: Movie) AND
            m.imdbRating >= 7.5
            AND(m.genre = 'Action' OR m.genre = 'Comedy' OR m.genre = 'Fantasy') with m,
            rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    query2 = ""
    if companion == 'alone':
        query2 = '''MATCH(m: Movie)where
                   NOT(: User
                   {username: {username}})-[: RATED]->(m: Movie) AND
                   m.imdbRating >= 7.5
                   AND(m.genre = 'Romance' OR m.genre = 'Comedy' OR m.genre = 'Thriller') with m,
                   rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''


    elif companion == 'family':
        query2 = '''MATCH(m: Movie)where
                   NOT(: User
                   {username: {username}})-[: RATED]->(m: Movie) AND
                   m.imdbRating >= 7.5
                   AND(m.genre = 'Drama' OR m.genre = 'Comedy' OR m.genre = 'Family') with m,
                   rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    elif companion == 'friends':
        query2 = '''MATCH(m: Movie)where
                   NOT(: User
                   {username: {username}})-[: RATED]->(m: Movie) AND
                   m.imdbRating >= 7.5
                   AND(m.genre = 'Thriller' OR m.genre = 'Comedy' OR m.genre = 'Horror') with m,
                   rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''


    elif companion == 'sibling':
        query2 = '''MATCH(m: Movie)where
                   NOT(: User
                   {username: {username}})-[: RATED]->(m: Movie) AND
                   m.imdbRating >= 7.5
                   AND(m.genre = 'Fantasy' OR m.genre = 'Comedy' OR m.genre = 'Horror') with m,
                   rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    elif companion == 'soulmate':
        query2 = '''MATCH(m: Movie)where
                       NOT(: User{username: {username}})-[: RATED]->(m: Movie) AND
                       m.imdbRating >= 7.5
                       AND(m.genre = 'Romance' OR m.genre = 'Comedy' OR m.genre = 'Family') with m,
                       rand() AS number return m.title as title, m.imdbId as imdbId,m.imageUrl as imageUrl, m.imdbRating as imdbRating, m.genre as genre ,m.description as description ORDER BY number LIMIT 50'''

    return query, query2