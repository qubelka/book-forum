from application import db
from .helper import create_slug

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(100), default='admin')
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, *args, **kwargs):
        super(Message, self).__init__(*args, **kwargs)
        self.slug = create_slug(title=None, type=type(self).__name__)

    def __repr__(self):
        return f'<Message: {self.id}>'

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    slug = db.Column(db.String(80), unique=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    #topic = db.Column(db.String(70), nullable=False)
    messages = db.relationship('Message', backref='thread', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.slug = create_slug(title=self.name, type=type(self).__name__)

    def __repr__(self):
        return f'<Thread: {self.id}, name: {self.name}>'

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    slug = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    threads = db.relationship('Thread', backref='topic', lazy=True)

    def __init__(self, *args, **kwargs):
        super(Topic, self).__init__(*args, **kwargs)
        self.slug = create_slug(title=self.name, type=type(self).__name__)

    def __repr__(self):
        return f'<Topic: {self.id}, name: {self.name}>'