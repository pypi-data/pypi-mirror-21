# Делаем SQLAlchemy удобной 

Не секрет, что [SQLAlchemy](https://www.sqlalchemy.org/) - самая популярная ORM на Python.
Она позволяет писать куда более продвинутые вещи, чем большинство Active Record ORM.
Но хоть Алхимия может и больше, плата за это - более сложный код, иногда слишком сложный для тривиальных задач.

<habracut/>
Вот таких: 
* обновление полей из массива: `post.update(body='new body', user=new_user)`   
* [CRUD](https://ru.wikipedia.org/wiki/CRUD): для простого `create` в Алхимии надо создать объект, да добавить его в [сессию](http://docs.sqlalchemy.org/en/latest/orm/session_basics.html), да сделать flush
* совсем нет магических фильтров как `Post.objects.filter(user__name__startswith='John')` в [Django](https://docs.djangoproject.com/en/1.10/topics/db/queries/#lookups-that-span-relationships))
* вложенный [eager load](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html?highlight=eager%20load#eager-loading), когда нужно с комментарием сразу загрузить пост, а к посту его юзера. В Алхимии он [есть](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.joinedload_all), но не очень удобен 
* элементарный `__repr__`, который совсем малоинформативен: `print(post)` выдаст что-то вроде `<myapp.models.Post at 0x04287A50>`

> Я говорю про верхний слой SQLAlchemy - ORM. Я знаю, что, например, апдейт полей из массива [можно сделать](http://docs.sqlalchemy.org/en/latest/core/selectable.html#sqlalchemy.sql.expression.TableClause.update) на более низком уровне. 

Я понимаю, что многое из описанного - не минусы, а особенности паттерна Data Mapper, и сравнивать его с Active Record я не буду, это [уже сделано](https://habrahabr.ru/post/198450/).
Речь о другом: да, Алхимия наворочена и может больше, но *для тривиальных задач код получается избыточным*.

Поставленные задачи решены и оформлены в [хорошо оттестированный и документированный пакет](https://github.com/absent1706/sqlalchemy-mixins).
А статья о том, как это позволит вам сделать свою работу с Алхимией приятнее и продуктивнее.

<spoiler title="Но ведь есть готовые решения, скажете вы!">
Да, есть, но они либо тяжело внедряются, либо заточены под конкретный фреймворк.
Хотелось иметь *универсальное, легко подключаемое* решение, чтобы, к примеру, написать 

```python
from прекрасный_модуль import ActiveRecordMixin

class User(Base, ActiveRecordMixin):
     pass
```

и иметь готовый Active Record.
Варианты ["инициализируйте Алхимию только через меня"](https://github.com/mardix/active-alchemy/#create-the-model) и [дополнения к flask-sqlalchemy](https://github.com/kofrasa/flask-activerecord) не годятся.

Смотрите [тут](https://github.com/absent1706/sqlalchemy-mixins#comparison-with-existing-solutions), почему не подошли конкретные модули.

</spoiler>

# О примерах в статье
Я буду приводить примеры для простенького блога с типовыми сущностями `User`, `Post`, `Comment`.

<spoiler title="Схема БД">
![DB](http://i.piccy.info/i9/48bcc885c5ac01ac036cccfb9c4cbe74/1489598411/10896/1127895/diagram.png)
</spoiler>

<spoiler title="Код на чистой Алхимии">
ORM классы выглядят примерно так

```python
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    posts = relationship('Post')


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User')
    comments = relationship('Comment')


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    rating = Column(Integer)

    user = relationship('User')
    post = relationship('Post')
```

А полный код [тут](https://gist.github.com/absent1706/6d2b3ce1ecb47aeb6df6fa09f30819f0). 
В нём ORM-классы, инициализация *чистой Алхимии* (*без моего пакета*) и наполнение начальными данными. 
Можете играться с ним, если захочется пощупать код.

<spoiler title="Как запустить">
Установите Алхимию:
```
pip install sqlalchemy
```

Потом сохраните тестовое приложение в файл и запустите: 
```
python файл.py
```
</spoiler>

</spoiler>

Примеры улучшенного кода используют готовый [пакет](https://github.com/absent1706/sqlalchemy-mixins). 

## Active Record

Я начал использовать SQLAlchemy, предварительно работав с [Active Record](http://rusrails.ru/active-record-basics) в Ruby on Rails, c [Eloquent ORM](http://laravel.su/docs/5.0/eloquent) в PHP и c [Django ORM](https://docs.djangoproject.com/en/1.10/topics/db/) и [Peewee](https://habrahabr.ru/post/207110/) в Python.
Все эти ORM имели короткий, красивый код во многом благодаря использованию шаблона Active Record.

Начав работать с Алхимией, я не понимал, почему я должен для создания объекта писать 3 строчки

```python
bob = User(name='Bobby', age=1)
session.add(bob)
session.flush()
```

вместо одной?

```python
 bob = User.create(name='Bobby', age=1)
 ```
 
Я понимаю, что ручной flush [сессии](http://docs.sqlalchemy.org/en/latest/orm/session_basics.html) нужен, чтобы запросы в БД пошли одной пачкой, да и вообще паттерн [unit of work](https://martinfowler.com/eaaCatalog/unitOfWork.html) даёт много преимуществ.

Но в реальных веб-приложениях большинство задач - тривиальный CRUD, и оттого, что в БД будет делаться не 3 запроса, а один, выигрыш невелик. Во всяком случае, он не стоит такого усложнения кода. 
Да и вообще, не зря же создатели Django, Ruby on Rails, Laravel, Yii выбрали ORM с Active Record.
  
Что ж, ничто не мешает реализовать Active Record *поверх* Data Mapper'a!  
Для этого всего-то и надо, что при инициализации приложения сессию передать модели 
  
```python
BaseModel.set_session(session) # это базовый класс ОРМ
# теперь у нас есть доступ к BaseModel.session
```

Теперь ОРМ имеет доступ к сессии, и можно реализовывать [методы save, create, update, delete](https://github.com/absent1706/sqlalchemy-mixins/blob/master/sqlalchemy_mixins/activerecord.py) и т.д.

```python
bob = User.create(name='Bobby', age=1)
bob.update(name='Bob', age=21)
bob.delete()
```

Ну и ещё хочется быстро создать запрос на модель
```python
User.query # вместо session.query(User)
```

и быстро достать первую или все записи 
```python
User.first() # вместо session.query(User).first()
User.all() # вместо session.query(User).all()
```

или найти запись по id, обвалившись ошибкой если надо
```python
User.find(1) # вместо session.query(User).get(1)
User.find_or_fail(123987) # выбросит исключение, если не найдено
```

В итоге у нас получается полноценный Active Record, как в любимых мною Django, Laravel и Ruby on Rails, но под капотом у нас мощный Data Mapper. Таким образом, мы имеем *лучшее из двух миров*.

Вышеприведенное подробно описано [тут](https://github.com/absent1706/sqlalchemy-mixins#active-record).

## Eager Load
Для решения [проблемы N+1 запросов](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html?highlight=eager%20load#eager-loading) каждая уважающая себя ORM имеет свои решения.

Допустим, мы отображаем на странице 10 юзеров и все посты каждого юзера.
Чтобы не вышло 11 запросов (1 на юзеров и 10 на посты), в [SQLAlchemy](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html?highlight=eager%20load#eager-loading) можно эти посты приджойнить
 
 ```python
session.query(User).options(joinedload('posts'))
```

или загрузить отдельным запросом
 
 ```python
session.query(User).options(subqueryload('posts'))
```

см. подробнее [тут](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#using-loader-strategies-lazy-loading-eager-loading).

Что ж, прекрасно! Только вот если ещё захотим в постах отображать комментарии, а к каждому комментарию юзера, сделавшего его?
Алхимия это [позволяет](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.joinedload_all), но пользоваться этим на практике оказалось неудобно.

Хочется задавать иерархию отношений, которые мы хотим подгрузить, декларативно, например так:
```python
User.with_({
    'posts': {
        'comments': {
            'user': None
        }
    }
}.all()
```

можно и без магических строк:
```python
User.with_({
    User.posts: {
        Post.comments: {
            Comment.user: None
        }
    }
}.all()
```

Кроме того, можно задавать стратегию загрузки: [joinedload](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.joinedload)(по умолчанию) или [subqueryload](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.subqueryload).
Следующий код сделает 2 запроса: на посты и на комментарии с приджойненными юзерами:

```python
Post.with_({
    'comments': (SUBQUERYLOAD, {  # load posts in separate query
        'user': None  # but, in this separate query, join user
    })
}}
```
Подробное описание с примерами можно найти [тут](https://github.com/absent1706/sqlalchemy-mixins#eager-load).
P.S. Отдельное спасибо моим коллегам за этот функционал.


## Магические операторы и join отношений, как в Django
 
Первое, что мне бросилось в глаза при изучении Django - это [магические операторы в фильтрах](https://docs.djangoproject.com/en/1.10/topics/db/queries/#retrieving-specific-objects-with-filters):
 
 ```python
Entry.objects.filter(headline__startswith="What")
```

и совсем поразила [фильтрация по связям](https://docs.djangoproject.com/en/1.10/topics/db/queries/#lookups-that-span-relationships):

```python
Entry.objects.filter(blog__name='Beatles Blog')
```

это гораздо приятнее, чем более "правильное" решение в Алхимии:

```python
session.query(Entry).join(Entry.blog).filter(Blog.name=='Beatles Blog')
```

<spoiler title="Хотя...">
Хотя магические строки и могут потенциально дать баг в Runtime, если сделать опечатку, например вместо `blog__name` написать `blogg__name`. Такие строки, в отличие от свойств класса вроде `Entry.blog`, IDE не будет инспектировать. 
</spoiler>

Помимо эстетической красоты, есть возможность строить такие запросы динамически, передавая фильтры с фронтенда:
 ```python
filters =  {'entry__headline__contains': 'Lennon', 'entry__pub_date__year': 2008} # это мог передать фронтенд
Blog.objects.filter(**filters)
```

Это особеннно полезно в приложениях, где пользователь может строить произвольные фильтры.  

Увы, в Алхимии нет возможности строить запросы столь динамично. Максимум, что она позволяет - [простенькую фильтрацию](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.filter_by) типа "колонка=значение":
```python
session.query(MyClass).filter_by(name = 'some name')
```

Что ж, взяв за образец [готовое решение](https://github.com/mitsuhiko/sqlalchemy-django-query) (которого всё же было [недостаточно](https://github.com/absent1706/sqlalchemy-mixins#django-like-queries-1)), удалось это сделать, и теперь можно писать как в Django:

```python
Post.where(rating__in=[2, 3, 4], user___name__like='%Bi%').all()
```

<spoiler title="Как это сделано">

Строка `user___name__like` парсится и мы понимаем, что надо приджойнить отношение `Post.user` и применить фильтр `Post.user.name.like('...')`. 
То есть 
```python
Post.where(user___name__like='%Bi%').all()
```
превращается в

```python
session.query(Post).join(Post.user).filter(User.name.like('%Bi%')).all()
```

<spoiler title="А на самом деле всё сложнее">
Вообще-то может статься так, что в запросе какая-то таблица возникнет 2 раза. 
Допустим, я хочу достать юзеров, посты которых комментировал Вася 

```python
User.where(posts___comments___user___name='Vasya').all()
```
Получается, есть юзер, которого я запрашиваю, а есть юзер в комментарии, по которому я фильтрую.
Проблему решают через [alias'ы](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.aliased), т.е. в [итоговом запросе](http://www.qopy.me/4KOkgXYKTOiXHUbc4R6EnQ) будут присутствовать 2 таблицы: `user` и `user_1`.

Конечно, мы не можем заранее знать, будут ли повторяться таблицы, поэтому делаем каждому отношению, которое джойним, свой alias:
```python
post_alias = User.posts.property.argument() # так можно вытащить целевой класс из relationship
session.query(User).join(post_alias) # и т.д.
```

Вот упрощенный аналог [реального кода](https://github.com/absent1706/sqlalchemy-mixins/blob/master/sqlalchemy_mixins/smartquery.py):
```python
from sqlalchemy.orm import aliased
from sqlalchemy.sql import operators

# Имеем на входе {'posts___comments___user___name__like': 'Vasya'}. Достанем:
relations = ['posts', 'comments', 'user'] # 1. отношения, они были разделены ___
attr_name = 'name' # 2. аттрибут, он был после последнего ___
op_name = 'like' # 3. оператор, он был после __
# получаем оператор Алхимии на основе op_name.
# в реале имеется фиксированное соответствие OPERATORS = {'like': operators.like_op},
# и из него оператор достаётся как OPERATORS[op_name]
operator = operators.like_op

value = 'Vasya'

cls = User # в жизни это статический метод и текущий класс хранится в cls
query = session.query(cls) # делаем начальный запрос

# джойним все связи в цикле
last_alias = cls
for relation in relations:
    relation = getattr(last_alias, relation)
    next_alias = aliased(relation.property.argument())
    query = query.outerjoin(next_alias)
    last_alias = next_alias

# теперь отфильтруем последнее отношение ('user')
attr = getattr(last_alias, attr_name) # получаем реальный аттрибут User.name
query = query.filter(operator(attr, value)) # применим оператор, передав ему аттрибут User.name и Васю
print(query.all())
```
Вот [готовый к запуску вариант](https://gist.github.com/absent1706/6d2b3ce1ecb47aeb6df6fa09f30819f0).  

</spoiler>

</spoiler>

а вдобавок ещё и сортировать:
```python
Post.sort('-rating', 'user___name').all() # sort by rating DESC, user name ASC
```

### Автоматический eager load
Более того, раз уж мы автоматически делаем join связей, логично указать SQLAlchemy, что указанные связи уже при-join-ены, при помощи [`contains_eager`](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.contains_eager).
Теперь, если отношение `Post.user` использовалось в фильтре/сортировке, то мы сможем достать юзера **без дополнительного запроса**:
```python
post = Post.sort('user___name').first()
print(post.user) # не потребуется дополнительного запроса в БД, т.к. юзер был приджойнен
```  

## Всё в одну кучу: фильтры, сортировка, eager load
В реальном мире приходится одновременно фильтровать, сортировать, да ещё и eager load'ить связи.

Допустим, мы фильтруем и сортируем посты по одному и тому же отношению `Post.user`. 
И фильтрация, и сортировка сделают по джоину, и одно и то же отношение будет приджойнено 2 раза
 
<spoiler title="Разве Алхимия не разрулит двойной джоин?">
Если просто писать

```python
session.query(Post).join(Post.user).join(Post.user)
```
то, действительно, Алхимия сделает только один join (немного ругнётся warning-ом, но джоин будет таки один).
Штука в том, что мы для каждого отношения делаем свой alias (см. спойлер выше), и поэтому Алхимии не знает, что 2 alias-а на `Post.user` - это по сути одно и то же, и надо следить за этим самостоятельно. 
</spoiler>

Поэтому фильтрацию, сортировку и eager load (да, его тоже) пришлось сделать в одной функции, чтобы иметь информацию о всех требуемых джоинах (точнее, иметь единый реестр alias-ов, см. спойлер "как это сделано") и делать их только один раз:
 
 ```python
 Comment.smart_query(
     filters={
         'post___public': True,
         'user__isnull': False
     },
     sort_attrs=['user___name', '-created_at'],
     schema={
         'post': {
             'user': None
         }
     }).all()
 ```
 
 Оно-то можно было бы и без 
 
 Подробное описание с примерами можно найти [тут](https://github.com/absent1706/sqlalchemy-mixins#eager-load).