from application import db
from random import randint

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    #slug = db.Column(db.String(140), unique=True)
    slug = db.Column(db.Integer, unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super(Message, self).__init__(*args, **kwargs)
        self.slug = randint(1,1000)

    def __repr__(self):
        return f'<Message: {self.id}, title: {self.title}>'

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    #slug = db.Column(db.String(140), unique=True)
    slug = db.Column(db.Integer, unique=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    topic = db.Column(db.String(70), nullable=False)
    messages = db.relationship('Message', backref='thread', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.slug = randint(1,1000)

    def __repr__(self):
        return f'<Thread: {self.id}, name: {self.name}>'


