#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库模型定义
这个文件定义了数据库中的表结构
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建数据库实例
db = SQLAlchemy()

class User(db.Model):
    """用户表模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """将用户对象转换为字典格式"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active
        }

class Post(db.Model):
    """文章表模型"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    
    # 关系定义
    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    def to_dict(self):
        """将文章对象转换为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author.username if self.author else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_published': self.is_published
        }

class Comment(db.Model):
    """评论表模型"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系定义
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))
    author = db.relationship('User', backref=db.backref('comments', lazy=True))
    
    def __repr__(self):
        return f'<Comment {self.id}>'
    
    def to_dict(self):
        """将评论对象转换为字典格式"""
        return {
            'id': self.id,
            'content': self.content,
            'post_id': self.post_id,
            'author': self.author.username if self.author else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# ==================== 路线规划相关模型 ====================

class Exhibit(db.Model):
    """展品表 - 存储展品信息"""
    __tablename__ = 'exhibits'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location_x = db.Column(db.Float, nullable=False)
    location_y = db.Column(db.Float, nullable=False)
    importance = db.Column(db.Integer, default=3)  # 1-5重要程度
    visit_duration = db.Column(db.Integer, default=10)  # 建议参观时间(分钟)
    category = db.Column(db.String(100))
    period = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': (self.location_x, self.location_y),
            'importance': self.importance,
            'visit_duration': self.visit_duration,
            'category': self.category,
            'period': self.period,
            'is_active': self.is_active
        }

class MemorialLayout(db.Model):
    """纪念馆布局表 - 存储场馆布局信息"""
    __tablename__ = 'memorial_layouts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    entrance_x = db.Column(db.Float, nullable=False)
    entrance_y = db.Column(db.Float, nullable=False)
    exit_x = db.Column(db.Float, nullable=False)
    exit_y = db.Column(db.Float, nullable=False)
    restrooms = db.Column(db.Text)  # JSON格式存储洗手间位置
    rest_areas = db.Column(db.Text)  # JSON格式存储休息区位置
    emergency_exits = db.Column(db.Text)  # JSON格式存储紧急出口
    walkways = db.Column(db.Text)  # JSON格式存储通道信息
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'name': self.name,
            'entrance': (self.entrance_x, self.entrance_y),
            'exit': (self.exit_x, self.exit_y),
            'restrooms': json.loads(self.restrooms) if self.restrooms else [],
            'rest_areas': json.loads(self.rest_areas) if self.rest_areas else [],
            'emergency_exits': json.loads(self.emergency_exits) if self.emergency_exits else [],
            'walkways': json.loads(self.walkways) if self.walkways else []
        }

class UserProfile(db.Model):
    """用户画像表 - 存储用户偏好信息"""
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    age_group = db.Column(db.String(20))  # child, youth, adult, senior
    interests = db.Column(db.Text)  # JSON格式存储兴趣标签
    physical_ability = db.Column(db.String(20), default='medium')  # low, medium, high
    preferred_visit_duration = db.Column(db.Integer, default=60)  # 偏好参观时长
    group_type = db.Column(db.String(20), default='individual')  # individual, family, group
    accessibility_needs = db.Column(db.Text)  # 无障碍需求
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref='profile')
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'age_group': self.age_group,
            'interests': json.loads(self.interests) if self.interests else [],
            'physical_ability': self.physical_ability,
            'preferred_visit_duration': self.preferred_visit_duration,
            'group_type': self.group_type,
            'accessibility_needs': self.accessibility_needs
        }

class RouteHistory(db.Model):
    """路线历史表 - 存储用户生成的路线记录"""
    __tablename__ = 'route_histories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    route_name = db.Column(db.String(200))
    route_data = db.Column(db.Text)  # JSON格式存储完整路线数据
    user_preferences = db.Column(db.Text)  # JSON格式存储用户偏好
    estimated_duration = db.Column(db.Integer)  # 预计时长
    actual_duration = db.Column(db.Integer)  # 实际花费时间
    user_rating = db.Column(db.Integer)  # 用户评分 1-5
    feedback = db.Column(db.Text)  # 用户反馈
    visit_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref='route_histories')
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'route_name': self.route_name,
            'route_data': json.loads(self.route_data) if self.route_data else {},
            'user_preferences': json.loads(self.user_preferences) if self.user_preferences else {},
            'estimated_duration': self.estimated_duration,
            'actual_duration': self.actual_duration,
            'user_rating': self.user_rating,
            'feedback': self.feedback,
            'visit_date': self.visit_date.isoformat() if self.visit_date else None,
            'created_at': self.created_at.isoformat()
        }
