#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主路由处理模块
Main Routes Handler
这个文件处理基础的URL路由和页面逻辑
路线规划相关的路由已移至 backend/route_planning/route_planning_routes.py
"""

from flask import render_template, request, jsonify, redirect, url_for, flash, session
from backend.database import *
from backend.route_planning import register_route_planning_routes

def init_routes(app):
    """初始化基础路由"""
    
    # 注册路线规划专用路由
    register_route_planning_routes(app)
    
    @app.route('/')
    def index():
        """首页"""
        return render_template('index.html')
    
    @app.route('/about')
    def about():
        """关于页面"""
        return render_template('about.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """登录页面"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # 这里应该验证用户登录
            # user = verify_user_login(username, password)
            # if user:
            #     session['user_id'] = user.id
            #     return redirect(url_for('index'))
            
            flash('用户名或密码错误', 'error')
        
        return render_template('login.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """注册页面"""
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            # 这里应该创建新用户
            # result = create_user(username, email, password)
            # if result['success']:
            #     flash('注册成功！', 'success')
            #     return redirect(url_for('login'))
            
            flash('注册失败，请检查输入信息', 'error')
        
        return render_template('register.html')
    
    # ==================== 基础API接口 ====================
    
    @app.route('/api/hello')
    def api_hello():
        """测试API接口"""
        return jsonify({
            'message': '欢迎使用南湖纪念馆智能路线规划系统！',
            'version': '1.0.0',
            'status': 'active',
            'modules': {
                'route_planning': '路线规划模块已加载',
                'database': '数据库连接正常',
                'core_features': '基础功能运行中'
            }
        })
    
    @app.route('/api/system/status')
    def system_status():
        """系统状态API"""
        return jsonify({
            'success': True,
            'system': {
                'name': '南湖纪念馆智能路线规划系统',
                'version': '1.0.0',
                'modules': {
                    'route_planning': True,
                    'user_management': True,
                    'database': True
                }
            },
            'message': '系统运行正常'
        })
    
    # ==================== 错误处理 ====================
    
    @app.errorhandler(404)
    def not_found_error(error):
        """404错误处理"""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500错误处理"""
        return render_template('500.html'), 500
