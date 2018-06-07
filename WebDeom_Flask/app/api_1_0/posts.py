from ..models import Post, Permission
from . import api
from .errors import forbidden, bad_request
from .decorators import permission_required
from flask import request, g, jsonify, url_for, current_app
from .. import db
from sqlalchemy.exc import DatabaseError


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    try:
        db.session.add(post)
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        return bad_request('新增失败.请重试.')
    return jsonify(post.to_json()), 201,\
           {'Location': url_for('api.get_post', id=post.id, _external=True)}


@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestap.desc()).paginate(
        page, per_page=current_app.config['H2D_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        perv = url_for('api.get_posts', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
        return forbidden('没权限修改')
    post.body = request.json.get('body', post.body)
    try:
        db.session.add(post)
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        return bad_request('修改失败')
    return jsonify(post.to_json())
