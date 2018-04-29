from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from model import *

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class NewsResource(Resource):
    def get(self, news_id):
        news = News.query.get_or_404(news_id)
        return jsonify(news.as_json())

    def delete(self, news_id):
        news = News.query.get_or_404(news_id)
        news.changeStatus('deleted')
        db.session.commit()
        return '', 204

    def put(self, news_id):
        news = News.query.get_or_404(news_id)
        news.title = request.form.get('title')
        news.content = request.form.get('content')
        news.status = request.form.get('status')
        
        topics = request.form.getlist('topic')
        new_topics = []
        for topic_name in topics:
            topic = Topics.query.filter_by(name=topic_name).first()
            if not topic:
                new_topic = Topics()
                new_topic.name = topic_name
                db.session.add(new_topic)
                topic = Topics.query.filter_by(name=topic_name).first()
            new_topics.append(topic)
        news.topics = new_topics
        db.session.commit()
        return jsonify(news.as_json())

class NewsStatus(Resource):
    def put(self, news_id, action):
        news = News.query.get_or_404(news_id)
        news.changeStatus(action)
        return jsonify(news.as_json())

class NewsList(Resource):
    def get(self):
        filter_status = request.args.get('status')
        filter_topic = request.args.get('topic')
        if filter_status:
            news_status_validation(filter_status)
            news_list = News.query.filter_by(status = filter_status).all()
            if filter_topic:
                topic = Topics.query.filter_by(name = filter_topic).first_or_404()
                news_list = [value for value in topic.news if value in news_list]
        elif filter_topic:
            topic = Topics.query.filter_by(name = filter_topic).first_or_404()
            news_list = topic.news
        else:
            news_list = News.query.all()
        
        result = []
        for news in news_list:
            result.append(news.as_json())
        return jsonify(dict(
            news= result
            )
        )

    def post(self):
        new_news = News()
        new_news.title = request.form['title']
        new_news.content = request.form['content']
        new_news.status = request.form['status']
        
        topics = request.form.getlist('topic')
        new_news.topics = []
        for topic_name in topics:
            topic = Topics.query.filter_by(name=topic_name).first()
            if not topic:
                new_topic = Topics()
                new_topic.name = topic_name
                db.session.add(new_topic)
                topic = Topics.query.filter_by(name=topic_name).first()
            new_news.topics.append(topic)        
        db.session.add(new_news)
        db.session.commit()
        return "", 201

class TopicResource(Resource):
    def get(self, topic_id):
        topic = Topics.query.get_or_404(topic_id)
        return jsonify(topic.as_json())

    def delete(self, topic_id):
        db.session.delete(Topics.query.get(topic_id))
        db.session.commit()
        return '', 204

    def put(self, topic_id):
        topic = Topics.query.get_or_404(topic_id)
        topic.name = request.form['name']
        db.session.commit()
        return jsonify(topic.as_json())

class TopicList(Resource):
    def get(self):
        topics = Topics.query.all()
        result = []
        for topic in topics:
            result.append(topic.as_json())
        return jsonify(dict(
                topics= result
            ))

    def post(self):
        new_topic = Topics()
        new_topic.name = request.form['name']
        db.session.add(new_topic)
        db.session.commit()
        return "", 201

#################################################################################

api.add_resource(NewsList, '/news')
api.add_resource(NewsResource, '/news/<news_id>')
api.add_resource(NewsStatus, '/news/<news_id>/<action>')
api.add_resource(TopicList, '/topics')
api.add_resource(TopicResource, '/topics/<topic_id>')

if __name__ == '__main__':
     app.run(port=5002)