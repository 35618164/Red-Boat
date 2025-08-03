#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数文件
这个文件包含项目中用到的各种工具函数
"""

import re
from datetime import datetime, timedelta
import hashlib
import secrets

def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """验证用户名格式"""
    # 用户名：3-20个字符，只能包含字母、数字、下划线
    if not username or len(username) < 3 or len(username) > 20:
        return False
    
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username) is not None

def validate_password(password):
    """验证密码强度"""
    # 密码：至少6个字符
    if not password or len(password) < 6:
        return False, "密码至少需要6个字符"
    
    # 检查是否包含字母和数字
    has_letter = re.search(r'[a-zA-Z]', password)
    has_digit = re.search(r'\d', password)
    
    if not (has_letter and has_digit):
        return False, "密码需要同时包含字母和数字"
    
    return True, "密码强度合格"

def format_datetime(dt, format_type='default'):
    """格式化日期时间"""
    if not dt:
        return ""
    
    formats = {
        'default': '%Y-%m-%d %H:%M:%S',
        'date': '%Y-%m-%d',
        'time': '%H:%M:%S',
        'chinese': '%Y年%m月%d日 %H:%M',
        'relative': None  # 相对时间，如"3分钟前"
    }
    
    if format_type == 'relative':
        return get_relative_time(dt)
    
    return dt.strftime(formats.get(format_type, formats['default']))

def get_relative_time(dt):
    """获取相对时间描述"""
    now = datetime.utcnow()
    diff = now - dt
    
    if diff.days > 0:
        return f"{diff.days}天前"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours}小时前"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes}分钟前"
    else:
        return "刚刚"

def generate_random_string(length=32):
    """生成随机字符串"""
    return secrets.token_urlsafe(length)

def generate_file_hash(file_content):
    """生成文件内容的哈希值"""
    return hashlib.md5(file_content).hexdigest()

def sanitize_filename(filename):
    """清理文件名，移除危险字符"""
    # 移除路径分隔符和其他危险字符
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # 限制长度
    if len(filename) > 255:
        filename = filename[:255]
    return filename

def truncate_text(text, max_length=100, suffix='...'):
    """截断文本"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def format_file_size(size_bytes):
    """格式化文件大小"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def parse_search_query(query):
    """解析搜索查询"""
    # 简单的搜索词分割
    if not query:
        return []
    
    # 按空格分割，移除空词
    words = [word.strip() for word in query.split() if word.strip()]
    return words

def create_pagination_info(total_count, page, per_page):
    """创建分页信息"""
    import math
    
    total_pages = math.ceil(total_count / per_page)
    has_prev = page > 1
    has_next = page < total_pages
    
    return {
        'total_count': total_count,
        'total_pages': total_pages,
        'current_page': page,
        'per_page': per_page,
        'has_prev': has_prev,
        'has_next': has_next,
        'prev_page': page - 1 if has_prev else None,
        'next_page': page + 1 if has_next else None
    }

def safe_int(value, default=0):
    """安全转换为整数"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    """安全转换为浮点数"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

class ResponseHelper:
    """API响应辅助类"""
    
    @staticmethod
    def success(data=None, message="操作成功"):
        """成功响应"""
        response = {
            'status': 'success',
            'message': message
        }
        if data is not None:
            response['data'] = data
        return response
    
    @staticmethod
    def error(message="操作失败", error_code=None):
        """错误响应"""
        response = {
            'status': 'error',
            'message': message
        }
        if error_code:
            response['error_code'] = error_code
        return response
    
    @staticmethod
    def paginated(items, pagination_info, message="获取成功"):
        """分页响应"""
        return {
            'status': 'success',
            'message': message,
            'data': items,
            'pagination': pagination_info
        }
