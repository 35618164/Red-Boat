#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库操作函数
这个文件包含所有数据库的增删改查操作
"""

from backend.models import db, User, Post, Comment
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

# 用户相关操作
def create_user(username, email, password):
    """创建新用户"""
    try:
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return {'success': False, 'message': '用户名已存在'}
        
        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first():
            return {'success': False, 'message': '邮箱已被注册'}
        
        # 创建新用户
        password_hash = generate_password_hash(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        
        db.session.add(user)
        db.session.commit()
        
        return {'success': True, 'message': '用户创建成功', 'user_id': user.id}
    
    except IntegrityError:
        db.session.rollback()
        return {'success': False, 'message': '数据库错误，请稍后重试'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'创建用户失败: {str(e)}'}

def get_user_by_username(username):
    """根据用户名查找用户"""
    return User.query.filter_by(username=username).first()

def get_user_by_email(email):
    """根据邮箱查找用户"""
    return User.query.filter_by(email=email).first()

def get_user_by_id(user_id):
    """根据ID查找用户"""
    return User.query.get(user_id)

def get_all_users():
    """获取所有用户"""
    return User.query.filter_by(is_active=True).all()

def verify_password(user, password):
    """验证用户密码"""
    return check_password_hash(user.password_hash, password)

# 文章相关操作
def create_post(title, content, author_id):
    """创建新文章"""
    try:
        # 检查作者是否存在
        author = get_user_by_id(author_id)
        if not author:
            return {'success': False, 'message': '作者不存在'}
        
        post = Post(
            title=title,
            content=content,
            author_id=author_id
        )
        
        db.session.add(post)
        db.session.commit()
        
        return {'success': True, 'message': '文章创建成功', 'post_id': post.id}
    
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'创建文章失败: {str(e)}'}

def get_post_by_id(post_id):
    """根据ID获取文章"""
    return Post.query.get(post_id)

def get_all_posts():
    """获取所有文章"""
    return Post.query.order_by(Post.created_at.desc()).all()

def get_recent_posts(limit=10):
    """获取最新文章"""
    return Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).limit(limit).all()

def get_posts_by_author(author_id):
    """获取指定作者的所有文章"""
    return Post.query.filter_by(author_id=author_id).order_by(Post.created_at.desc()).all()

def update_post(post_id, title=None, content=None, is_published=None):
    """更新文章"""
    try:
        post = get_post_by_id(post_id)
        if not post:
            return {'success': False, 'message': '文章不存在'}
        
        if title:
            post.title = title
        if content:
            post.content = content
        if is_published is not None:
            post.is_published = is_published
        
        db.session.commit()
        return {'success': True, 'message': '文章更新成功'}
    
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'更新文章失败: {str(e)}'}

def delete_post(post_id):
    """删除文章"""
    try:
        post = get_post_by_id(post_id)
        if not post:
            return {'success': False, 'message': '文章不存在'}
        
        # 先删除相关评论
        Comment.query.filter_by(post_id=post_id).delete()
        
        # 然后删除文章
        db.session.delete(post)
        db.session.commit()
        
        return {'success': True, 'message': '文章删除成功'}
    
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'删除文章失败: {str(e)}'}

# 评论相关操作
def create_comment(content, post_id, author_id):
    """创建新评论"""
    try:
        # 检查文章是否存在
        post = get_post_by_id(post_id)
        if not post:
            return {'success': False, 'message': '文章不存在'}
        
        # 检查作者是否存在
        author = get_user_by_id(author_id)
        if not author:
            return {'success': False, 'message': '用户不存在'}
        
        comment = Comment(
            content=content,
            post_id=post_id,
            author_id=author_id
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return {'success': True, 'message': '评论创建成功', 'comment_id': comment.id}
    
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'创建评论失败: {str(e)}'}

def get_comments_by_post(post_id):
    """获取指定文章的所有评论"""
    return Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()

def delete_comment(comment_id):
    """删除评论"""
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            return {'success': False, 'message': '评论不存在'}
        
        db.session.delete(comment)
        db.session.commit()
        
        return {'success': True, 'message': '评论删除成功'}
    
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'删除评论失败: {str(e)}'}

# 数据库初始化
def init_database(app):
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        print("数据库表创建完成！")

def create_sample_data():
    """创建示例数据"""
    try:
        # 创建示例用户
        if not User.query.first():
            sample_users = [
                {'username': 'admin', 'email': 'admin@example.com', 'password': 'admin123'},
                {'username': 'user1', 'email': 'user1@example.com', 'password': 'user123'},
                {'username': 'user2', 'email': 'user2@example.com', 'password': 'user123'}
            ]
            
            for user_data in sample_users:
                create_user(user_data['username'], user_data['email'], user_data['password'])
            
            print("示例用户创建完成！")
        
        # 创建示例文章
        if not Post.query.first():
            admin_user = get_user_by_username('admin')
            if admin_user:
                sample_posts = [
                    {
                        'title': '欢迎使用Flask团队项目',
                        'content': '这是我们的第一篇文章，展示了基本的博客功能。',
                        'author_id': admin_user.id
                    },
                    {
                        'title': '关于我们的项目',
                        'content': '这个项目是为了学习Flask框架和团队协作开发而创建的。',
                        'author_id': admin_user.id
                    }
                ]
                
                for post_data in sample_posts:
                    result = create_post(post_data['title'], post_data['content'], post_data['author_id'])
                    if result['success']:
                        # 发布文章
                        update_post(result['post_id'], is_published=True)
                
                print("示例文章创建完成！")
    
    except Exception as e:
        print(f"创建示例数据失败: {str(e)}")
