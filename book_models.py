from models import graph



def listmovie(search):
    query = '''MATCH (author:author)-[:author]->(book:Book)<-[:Published]-(publisher:Publisher)
    where book.title STARTS WITH {search}
    return book.title as title , book.year as year, book.isbn as isbn ,book.imageurl as imageurl, publisher.name as publisher,author.name as author '''
    results = graph.run(query, search=search)
    return results


def book_status(username,isbn,status):

    query='''MATCH (n:User{username:{username}}),(b:Book{isbn:{isbn}})
    MERGE (n)-[r:STATUS]->(b) set r.status={status} return r.status as status'''
    results = graph.run(query, username=username, isbn=isbn,status=status)
    return results



def book_recommendations(username):



    query='''

    MATCH(n: User{username: {username}})-[: STATUS]->(: Book)<-[: author]-(a:author)-[: author]->(book:Book) where  not (n: User{username: {username}})-[: STATUS]->(book: Book)
     return DISTINCT book.title as title,book.year as year, book.isbn as isbn ,book.imageurl as imageurl ,a.name as author

    '''

    results = graph.run(query, username=username)

    return results


def my_books(username):
    query = '''

        MATCH(n: User{username: {username}})-[: STATUS{status:'Read'}]->(book: Book)<-[: author]-(a:author)
        return book.title as title,book.year as year, book.isbn as isbn ,book.imageurl as imageurl ,a.name as author'''

    result1 = graph.run(query, username=username)


    return result1

def my_books_to_read(username):

    query = '''

            MATCH(n: User{username: {username}})-[: STATUS{status:'Will Read'}]->(book: Book)<-[: author]-(a:author)
            return book.title as title,book.year as year, book.isbn as isbn ,book.imageurl as imageurl ,a.name as author'''

    result2 = graph.run(query, username=username)

    return result2