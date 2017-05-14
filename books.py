import csv
import json
import requests
import time
with open('g:/books.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    count=0
    for row in readCSV:

        isbn=row[0]
        print(row[0])
        time.sleep(1)
        #r = requests.get('https://www.googleapis.com/books/v1/volumes?key=AIzaSyAjtcK9GDybChYSjaR1ZNiKFzD6UdYoHUw&q=isbn:' + isbn)
        r = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn)

        book = json.loads(r.text)
        try:

            source = (book['items'][0]['volumeInfo']['title']);
            print(source)

            count = count + 1
            print(count)
        except Exception:
             print("ISBN not exist!")