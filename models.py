from passlib.hash import bcrypt
from py2neo import Graph, Node, Relationship
from datetime import datetime
import os
import uuid

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = os.environ.get('neo4j')
password = os.environ.get('deepak007')

graph = Graph(url + '/db/data/', username=username, password=password)


def register(username,password,email,age,gender,mobile,country,state):
    if not find(username):
        user = Node('User', password=bcrypt.encrypt(password),username=username,email=email,gender=gender,age=age,mobile=mobile,country=country,state=state)
        graph.create(user)

        return True
    else:
        return False



def find(username):
    user = graph.find_one('User', 'username', username)

    return user

def verify_user(username,password):
    user = find(username)
    if user:
        return bcrypt.verify(password, user['password'])
    else:
        return False

def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%Y-%m-%d')