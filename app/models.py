from app import db

# Model for Task
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    comments = db.relationship('Comment', backref='task', cascade="all, delete-orphan")

    def to_dict(self):
        """Convert Task object to dictionary for JSON responses."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'comments': [comment.to_dict() for comment in self.comments]
        }


# Model for Comment
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)

    def to_dict(self):
        """Convert Comment object to dictionary for JSON responses."""
        return {
            'id': self.id,
            'content': self.content,
            'task_id': self.task_id
        }
