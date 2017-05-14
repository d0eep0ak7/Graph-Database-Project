

from py2neo import Graph, Node, Relationship
from datetime import datetime
import uuid
from models import find,timestamp,date
from models import graph
def addpost(username, title, tags, text,about):
    user = find(username)
    post = Node('Post',
        id=(str(uuid.uuid4()))+username,
        title=title,
        text=text,
        about=about,
        timestamp=timestamp(),
        date=date()
    )
    rel = Relationship(user, 'PUBLISHED', post)
    graph.create(rel)

    tags = [x.strip() for x in tags.lower().split(',')]
    for name in set(tags):
        tag = Node('Tag', name=name)
        graph.merge(tag)   #MERGE command checks whether this node is available in the database or not.

        rel = Relationship(tag, 'TAGGED', post)
        graph.create(rel)



def get_todays_recent_posts():
    query = '''
    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    WHERE post.date = {today}
    RETURN user.username AS username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT 5
    '''

    return graph.run(query, today=date())

def get_recent_posts(username):
    query = '''
    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    WHERE user.username = {username}
    RETURN post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT 5
    '''

    return graph.run(query, username=username)




def get_similar_users(username):
    # Find three users who are most similar to the logged-in user
    # based on tags they've both blogged about.
    query = '''
    MATCH (you:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
          (they:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
    WHERE you.username = {username} AND you <> they
    WITH they , COLLECT(DISTINCT tag.name) AS tags

    ORDER BY SIZE(tags) DESC LIMIT 3
    RETURN they.username AS similar_user, tags
    '''

    return graph.run(query, username=username)





def get_commonality_of_user(username, other):
    # Find how many of the logged-in user's posts the other user
    # has liked and which tags they've both blogged about.
    query = '''
    MATCH (they:User {username: {they} })
    MATCH (you:User {username: {you} })
    OPTIONAL MATCH (they)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
                   (you)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
    RETURN SIZE((they)-[:LIKED]->(:Post)<-[:PUBLISHED]-(you)) AS likes,
           COLLECT(DISTINCT tag.name) AS tags
    '''

    return graph.run(query, they=other, you=username).next



def delete_post(username,post_id):

    print(post_id)
    print("Jadkjsh dkdh fkdhf gjdf gdfk ")
    query='''

    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    WHERE user.username ={username} AND post.id={post_id} Detach Delete post



    '''

    return graph.run(query, username=username,post_id=post_id)


def like_post(username, post_id):
    user = find(username)
    post = graph.find_one('Post', 'id', post_id)
    graph.merge(Relationship(user, 'LIKED', post))
