from flask import Flask, request, abort
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

news_status = {'deleted', 'draft', 'publish'}

def news_status_validation(status):
    if status in news_status:
        return True
    return False

news_topics = db.Table('news_topics',
    db.Column('newsid', db.Integer, db.ForeignKey('news.newsid'), primary_key=True),
    db.Column('topicid', db.Integer, db.ForeignKey('topics.topicid'), primary_key=True)
)

class News(db.Model):
    newsid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    topics = db.relationship('Topics', secondary=news_topics, lazy="subquery",
        backref=db.backref('news', lazy=True))

    def as_json(self, topics=True):
        result = dict(
            newsid  = self.newsid,
            title   = self.title,
            content = self.content,
            status  = self.status
            )
        if topics == True:
            result['topics'] = []
            for topic in self.topics:
                result['topics'].append(topic.as_json(False))
        return result

    def changeStatus(self, status):
        if news_status_validation(status):
            self.status = status
        else:
            abort(404, message="Status '{}' doesn't exist".format(status))

class Topics(db.Model):
    topicid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def as_json(self, news=True):
        result = dict(
            topicid  = self.topicid,
            name     = self.name
            )
        if news == True:
            result['news'] = []
            for news in self.news:
                result['news'].append(news.as_json(False))
        return result