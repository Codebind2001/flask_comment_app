from flask import Blueprint, jsonify, request
from app import db
from app.models import Task, Comment

# Create a Blueprint (used to group routes)
bp = Blueprint('main', __name__)

# ---------------------- TASK ROUTES ----------------------

# Get all tasks
@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200


# Create a new task
@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


# Update an existing task
@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)

    db.session.commit()
    return jsonify(task.to_dict()), 200


# Delete a task
@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200


# ---------------------- COMMENT ROUTES ----------------------

# Get all comments for a specific task
@bp.route('/tasks/<int:task_id>/comments', methods=['GET'])
def get_comments(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify([comment.to_dict() for comment in task.comments]), 200


# Add a comment to a specific task
@bp.route('/tasks/<int:task_id>/comments', methods=['POST'])
def add_comment(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    comment = Comment(content=content, task=task)
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201


# Update a comment
@bp.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json()
    comment.content = data.get('content', comment.content)

    db.session.commit()
    return jsonify(comment.to_dict()), 200


# Delete a comment
@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'}), 200
