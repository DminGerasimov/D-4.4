from django.contrib.auth.models import User
from news.models import *

# Чтобы прогнать набор комманд в django shell, необходимо удалить из БД "следы отладки":
# вход в админку: Dmin:Dminqwerty
User.objects.exclude(username = 'Dmin').delete()
Category.objects.all().delete()

# 1. Создать двух пользователей (с помощью метода User.objects.create_user).
u1_name, u2_name = 'User1', 'User2'
User.objects.create_user(username=u1_name, password='easy password')
User.objects.create_user(username=u2_name, password='easy password')

# 2. Создать два объекта модели Author, связанные с пользователями.
a1 = Author.objects.create(user_id=User.objects.all().values().filter(username=u1_name)[0]['id'])
a2 = Author.objects.create(user_id=User.objects.all().values().filter(username=u2_name)[0]['id'])

# 3. Добавить 4 категории в модель Category.
cat1 = Category.objects.create(news_category='Спорт')
cat2 = Category.objects.create(news_category='Досуг')
cat3 = Category.objects.create(news_category='Погода')
cat4 = Category.objects.create(news_category='Курс валют')

# 4. Добавить 2 статьи и 1 новость.
p1 = Post.objects.create(author=a1, type_news_article = 'AR', chapter ='Заголовок первой статьи', text ='Текст первой статьи(съешь еще этих мягких пирожков,съешь еще этих мягких пирожков,съешь еще этих мягких пирожков,съешь еще этих мягких пирожков)')
p2 = Post.objects.create(author=a2, type_news_article = 'AR', chapter ='Заголовок второй статьи', text ='Текст второй статьи(не садись на пенек, не ешь пирожок!не садись на пенек, не ешь пирожок!не садись на пенек, не ешь пирожок!не садись на пенек, не ешь пирожок!)')
p3 = Post.objects.create(author=a1, type_news_article = 'NE', chapter ='Заголовок новости', text ="""Арбитражный суд Москвы признал основателя шоколадной фабрики "А. Коркунов", основного акционера казанского "Анкор Банка" Андрея Коркунова банкротом и открыл процедуру реализации его имущества.Данные об этом содержатся в картотеке арбитражных дел, в графе "Информация о принятом судебном акте". Подробности пока не сообщаются.""")

# 5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
p1.category.add(cat1, cat3, cat4)
p2.category.add(cat3, cat4)
p3.category.add(cat2, cat4)

# Проверка присвоения категорий
p1.category.all().values()
p2.category.all().values()
p3.category.all().values()

# 6. Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
c1 = Comment.objects.create(post = p1, user = a1, comment_text ='1 Комментарий к посту 1 пользователя User1')
c2 = Comment.objects.create(post = p1, user = a1, comment_text ='2 Комментарий к посту 1 пользователя User1')
c3 = Comment.objects.create(post = p2, user = a2, comment_text ='Комментарий к посту 2 пользователя User2')
c4 = Comment.objects.create(post = p3, user = a2, comment_text ='Комментарий к посту 3 пользователя User2')
c5 = Comment.objects.create(post = p3, user = a1, comment_text ='Комментарий к посту 3 пользователя User1')

# 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
Comment.objects.all().values('id') #определяем id комментариев и прописываем их в id-поля методов get:

_ = Comment.objects.get(id=16)
_.like()
_.like()
_.like()
_.save()
_ = Comment.objects.get(id=17)
_.like()
_.dislike()
_.dislike()
_.save()
_ = Comment.objects.get(id=18)
_.dislike()
_.dislike()
_.dislike()
_.save()
_ = Comment.objects.get(id=19)
_.like()
_.like()
_.dislike()
_.save()
_ = Comment.objects.get(id=20)
_.like()
_.like()
_.dislike()
_.save()


Post.objects.all().values('id') #определяем id статей\новостей и прописываем их в id-поля методов get

_ = Post.objects.get(id=22)
_.like()
_.like()
_.like()
_.save()

_ = Post.objects.get(id=23)
_.like()
_.dislike()
_.like()
_.save()

_ = Post.objects.get(id=24)
_.dislike()
_.dislike()
_.dislike()
_.save()

# 8. Обновить рейтинги пользователей.
Author.objects.all().values('id') # определяем id авторов и прописываем их в id-поля методов get

Author.objects.get(id=13).update_rating()
Author.objects.get(id=14).update_rating()

# 9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best = Author.objects.all().order_by('-rating').values('user_id','rating')[0]
f"""username: {User.objects.filter(id=int(best['user_id'])).values('username')[0]['username']}"""
f"""higly rating: {best['rating']}"""


# 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
    
# получаем словарь с полями лучшей статьи (наибольший article_news_rate)
_ = Post.objects.all().order_by('-article_news_rate').values('author','article_news_rate', 'chapter','id', 'time_in')[0]

# получаем дату добавления лучшей статьи
p = Post.objects.get(id = int(_['id']))
p.time_in

# получаем user_id автора лучшей статьи
u_id = Author.objects.filter(id = int(_['author'])).values('user_id')[0]['user_id']

# получаем username пользователя лучшей статьи
User.objects.filter(id = int(u_id)).values('username')[0]['username']

# получаем рейтинг лучшей статьи
p.article_news_rate

# получаем заголовок и превью лучшей статьи
p.chapter
p.preview()

# 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.

# получаем словарь с полями лучшей статьи (наибольший article_news_rate)
_ = Post.objects.all().order_by('-article_news_rate').values('author','article_news_rate', 'chapter','id', 'time_in')[0]

# печатаем список словарей всех комментариев лучшей статьи с полями (дата, пользователь, рейтинг, текст)
[print(a) for a in Comment.objects.filter(post__id = int(_['id'])).values('time_creation', 'user', 'comment_rate', 'comment_text')]
