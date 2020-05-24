# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import datetime

from CafesFile import Cafes, Cafe
from HandlerFile import Users, Handler
from MediaFileClass import MediaFiles, MediaFile
from MyHTTPServerFile import MyHTTPServer
from ReviewsFile import Reviews, Review
from UsersFile import User



def fill_users(users: Users):
    u1 = User('PizzaOwner', 'lovepizza1')
    u2 = User('PubOwner', 'lovepub1')
    u3 = User('SushiOwner', 'lovesushi1')
    u4 = User('VasyaPupkin', 'lovepupok1')
    u5 = User('PanAleha', 'loveAleha1')
    u6 = User('LesyaSuper', 'loveLesya1')
    u7 = User('MrMops', 'loveMops1')
    users.put(u1)
    users.put(u2)
    users.put(u3)
    users.put(u4)
    users.put(u5)
    users.put(u6)
    users.put(u7)

def fill_cafes(cafes: Cafes):
     c1 = Cafe('PizzaOwner', 'PizzaDay', 'Very tasty pizza', 'Dnepr')
     c2 = Cafe('PubOwner', 'Duck Pub', 'We have cool tea', 'Kiev')
     c3 = Cafe('SushiOwner', 'Sushi Iz Karasya', 'Only Japan Fish', 'Cherkasi')
     cafes.put(c1)
     cafes.put(c2)
     cafes.put(c3)

def fill_media(mfiles: MediaFiles):
    m1 = MediaFile(1, "photo")
    mfiles.put_init(m1)

def now() -> str:
    return str(datetime.datetime.now())

def fill_reviews(reviews: Reviews):
    r1 = Review('PanAleha', 3, 5, now(), 'Вкусный осетр', )
    r2 = Review('PanAleha', 1, 3, now(), 'Ребята, пирожки у них просто невероятные!', )
    r3 = Review('VasyaPupkin', 1, 5, now(), 'Мясная пицца лучшая :)', )
    r4 = Review('VasyaPupkin', 2, 5, now(), 'У них на сцене поющая уточка, вечер удался)))', )
    r5 = Review('LesyaSuper', 2, 2, now(), 'Долго обслуживали, разве что крякали прикольно', )
    r6 = Review('LesyaSuper', 3, 1, now(), 'Да это не из осетра, а из карася!!!', )
    r7 = Review('MrMops', 3, 5, now(), 'Изысканная кухня', )
    r8 = Review('MrMops', 1, 4, now(), 'Пирожок был еле теплый, но все равно вкусно', )
    reviews.put(r1)
    reviews.put(r2)
    reviews.put(r3)
    reviews.put(r4)
    reviews.put(r5)
    reviews.put(r6)
    reviews.put(r7)
    reviews.put(r8)


if __name__ == '__main__':
    host = ''
    port = 9090
    name = 'MyServer'

    users = Users()
    cafes = Cafes()
    media_files = MediaFiles()
    cafe_reviews = Reviews()

    fill_users(users)
    fill_cafes(cafes)
    fill_reviews(cafe_reviews)
    fill_media(media_files)

    handler = Handler(users, cafes, media_files, cafe_reviews)

    serv = MyHTTPServer(host, port, name, handler)
    try:
        serv.serve_forever()
    except Exception as e:
        print('Serving failed', e)

# TODO:
# 1. replace len(...) in repositories (CafesFile, ...)



