from peewee import *

db = SqliteDatabase('rbc.db')


class TableTopic(Model):
    """
    Таблица тем. Включает поля:
        заголовок
        url-адрес страницы
        описание
        последнее время обновления
    """
    title = CharField()
    url = CharField()
    description = CharField()
    last_update = DateTimeField()

    class Meta:
        database = db


class TableArticle(Model):
    """
    Таблица статей. Включает поля:
        тема
        заголовок
        url-адрес страницы
        текст
        последнее время обновления
    """
    topic = ForeignKeyField(TableTopic, related_name="articles")
    title = CharField()
    url = CharField()
    text = CharField()
    last_update = DateTimeField()

    class Meta:
        database = db


class TableTag(Model):
    """
    Таблица тэгов. Включает поля:
        тэг
        статья, к которой он прикреплён
    """
    tag = CharField()
    article = ForeignKeyField(TableArticle, related_name="tags")

    class Meta:
        database = db


TableTopic.create_table()
TableArticle.create_table()
TableTag.create_table()
db.close()
