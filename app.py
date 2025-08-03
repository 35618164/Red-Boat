#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Web Application - 主启动文件
使用模块化结构组织代码
"""

from flask import Flask
import os
from config import Config
from backend.models import db
from backend.routes import init_routes
from backend.database import init_database, create_sample_data

def create_app():
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(Config)
    
    # 确保必要的目录存在
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('database', exist_ok=True)
    
    # 初始化数据库
    db.init_app(app)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
        print("✅ 数据库表创建完成！")
        
        # 创建示例数据（仅在首次运行时）
        create_sample_data()
    
    # 初始化路由
    init_routes(app)
    
    return app

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    print("🚀 启动Flask应用...")
    print("📍 访问地址: http://127.0.0.1:8080")
    print("📊 数据库: SQLite")
    print("🔧 模式: 开发模式")
    print("-" * 50)
    
    # 启动应用 - 使用端口8080避免与AirPlay冲突
    # 只监听本地地址以提高响应速度
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
