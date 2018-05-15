from peewee import *

db = SqliteDatabase('rbc.db')


class TableTopic(Model):
    title = CharField()
    url = CharField()
    description = CharField()
    last_update = DateTimeField()

    class Meta:
        database = db


class TableArticle(Model):
    topic = ForeignKeyField(TableTopic, related_name="articles")
    title = CharField()
    url = CharField()
    text = CharField()
    last_update = DateTimeField()

    class Meta:
        database = db


class TableTag(Model):
    tag = CharField()
    article = ForeignKeyField(TableArticle, related_name="tags")

    class Meta:
        database = db


TableTopic.create_table()
TableArticle.create_table()
TableTag.create_table()
db.close()
