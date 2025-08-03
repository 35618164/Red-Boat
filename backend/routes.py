#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路由处理文件
这个文件定义了所有的网址路由和对应的处理函数
"""

from flask import render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
from backend.models import db, User, Post, Comment
from backend.database import *

def init_routes(app):
    """初始化所有路由"""
    
    @app.route('/')
    def index():
        """首页路由"""
        # 获取最新的几篇文章
        recent_posts = get_recent_posts(limit=5)
        return render_template('index.html', 
                             title='Flask团队项目',
                             current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             posts=recent_posts)
    
    @app.route('/about')
    def about():
        """关于页面路由"""
        team_members = [
            {'name': '成员1', 'role': '前端开发'},
            {'name': '成员2', 'role': '后端开发'},
            {'name': '成员3', 'role': '数据库设计'},
            {'name': '成员4', 'role': '项目管理'}
        ]
        return render_template('about.html', 
                             title='关于我们',
                             team_members=team_members)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """登录页面路由"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # 这里应该验证用户名和密码
            # 简化版本，实际开发中需要密码验证
            user = get_user_by_username(username)
            if user:
                flash('登录成功！', 'success')
                return redirect(url_for('index'))
            else:
                flash('用户名或密码错误！', 'error')
        
        return render_template('login.html', title='用户登录')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """注册页面路由"""
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            # 创建新用户
            result = create_user(username, email, password)
            if result['success']:
                flash('注册成功！请登录。', 'success')
                return redirect(url_for('login'))
            else:
                flash(result['message'], 'error')
        
        return render_template('register.html', title='用户注册')
    
    # API路由
    @app.route('/api/hello')
    def api_hello():
        """API示例 - 返回JSON数据"""
        return jsonify({
            'message': 'Hello from Flask!',
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0'
        })
    
    @app.route('/api/users')
    def api_users():
        """API - 获取所有用户"""
        users = get_all_users()
        return jsonify({
            'status': 'success',
            'count': len(users),
            'users': [user.to_dict() for user in users]
        })
    
    @app.route('/api/posts')
    def api_posts():
        """API - 获取所有文章"""
        posts = get_all_posts()
        return jsonify({
            'status': 'success',
            'count': len(posts),
            'posts': [post.to_dict() for post in posts]
        })
    
    @app.route('/api/posts', methods=['POST'])
    def api_create_post():
        """API - 创建新文章"""
        data = request.get_json()
        if not data or not all(k in data for k in ('title', 'content', 'author_id')):
            return jsonify({'status': 'error', 'message': '缺少必要字段'}), 400
        
        result = create_post(
            title=data['title'],
            content=data['content'],
            author_id=data['author_id']
        )
        
        if result['success']:
            return jsonify({'status': 'success', 'message': '文章创建成功', 'post_id': result['post_id']}), 201
        else:
            return jsonify({'status': 'error', 'message': result['message']}), 400
    
    # 错误处理
    @app.errorhandler(404)
    def not_found_error(error):
        """404错误处理"""
        return render_template('404.html', title='页面未找到'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500错误处理"""
        db.session.rollback()  # 回滚数据库事务
        return render_template('500.html', title='服务器错误'), 500
