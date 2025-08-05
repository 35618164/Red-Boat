# -*- coding: utf-8 -*-
"""
路线规划数据库操作模块
Route Planning Database Operations
专门处理路线规划相关的数据库操作
"""

from backend.models import (
    db, Exhibit, MemorialLayout, UserProfile, 
    RouteHistory, User
)
from datetime import datetime
import json

class RoutePlanningDatabase:
    """路线规划数据库操作类"""
    
    @staticmethod
    def create_exhibit(exhibit_id, name, description, location_x, location_y, 
                      importance=3, visit_duration=10, category="", period=""):
        """创建展品记录"""
        try:
            exhibit = Exhibit(
                id=exhibit_id,
                name=name,
                description=description,
                location_x=location_x,
                location_y=location_y,
                importance=importance,
                visit_duration=visit_duration,
                category=category,
                period=period
            )
            db.session.add(exhibit)
            db.session.commit()
            return {'success': True, 'exhibit_id': exhibit_id}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    @staticmethod
    def get_all_exhibits():
        """获取所有活跃的展品"""
        return Exhibit.query.filter_by(is_active=True).all()
    
    @staticmethod
    def get_exhibit_by_id(exhibit_id):
        """根据ID获取展品"""
        return Exhibit.query.filter_by(id=exhibit_id, is_active=True).first()
    
    @staticmethod
    def create_memorial_layout(name, entrance_x, entrance_y, exit_x, exit_y,
                              restrooms=None, rest_areas=None, emergency_exits=None, walkways=None):
        """创建纪念馆布局"""
        try:
            layout = MemorialLayout(
                name=name,
                entrance_x=entrance_x,
                entrance_y=entrance_y,
                exit_x=exit_x,
                exit_y=exit_y,
                restrooms=json.dumps(restrooms or []),
                rest_areas=json.dumps(rest_areas or []),
                emergency_exits=json.dumps(emergency_exits or []),
                walkways=json.dumps(walkways or [])
            )
            db.session.add(layout)
            db.session.commit()
            return {'success': True, 'layout_id': layout.id}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    @staticmethod
    def get_active_layout():
        """获取当前活跃的布局"""
        return MemorialLayout.query.filter_by(is_active=True).first()
    
    @staticmethod
    def create_user_profile(user_id, age_group, interests, physical_ability='medium',
                          preferred_visit_duration=60, group_type='individual'):
        """创建用户画像"""
        try:
            # 检查是否已存在用户画像
            existing_profile = UserProfile.query.filter_by(user_id=user_id).first()
            if existing_profile:
                # 更新现有画像
                existing_profile.age_group = age_group
                existing_profile.interests = json.dumps(interests)
                existing_profile.physical_ability = physical_ability
                existing_profile.preferred_visit_duration = preferred_visit_duration
                existing_profile.group_type = group_type
                existing_profile.updated_at = datetime.utcnow()
                profile = existing_profile
            else:
                # 创建新画像
                profile = UserProfile(
                    user_id=user_id,
                    age_group=age_group,
                    interests=json.dumps(interests),
                    physical_ability=physical_ability,
                    preferred_visit_duration=preferred_visit_duration,
                    group_type=group_type
                )
                db.session.add(profile)
            
            db.session.commit()
            return {'success': True, 'profile_id': profile.id}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    @staticmethod
    def get_user_profile(user_id):
        """获取用户画像"""
        return UserProfile.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def save_route_history(user_id, route_name, route_data, user_preferences, 
                          estimated_duration, visit_date=None):
        """保存路线历史"""
        try:
            route_history = RouteHistory(
                user_id=user_id,
                route_name=route_name,
                route_data=json.dumps(route_data),
                user_preferences=json.dumps(user_preferences),
                estimated_duration=estimated_duration,
                visit_date=visit_date or datetime.utcnow()
            )
            db.session.add(route_history)
            db.session.commit()
            return {'success': True, 'route_id': route_history.id}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    @staticmethod
    def get_user_route_history(user_id, limit=10):
        """获取用户的路线历史"""
        return RouteHistory.query.filter_by(user_id=user_id)\
                                .order_by(RouteHistory.created_at.desc())\
                                .limit(limit).all()
    
    @staticmethod
    def update_route_feedback(route_id, actual_duration=None, user_rating=None, feedback=None):
        """更新路线反馈"""
        try:
            route_history = RouteHistory.query.get(route_id)
            if not route_history:
                return {'success': False, 'message': '路线记录不存在'}
            
            if actual_duration is not None:
                route_history.actual_duration = actual_duration
            if user_rating is not None:
                route_history.user_rating = user_rating
            if feedback is not None:
                route_history.feedback = feedback
            
            db.session.commit()
            return {'success': True, 'message': '反馈更新成功'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    @staticmethod
    def get_popular_exhibits(limit=10):
        """获取热门展品（基于访问历史）"""
        # 这里可以根据访问统计来获取热门展品
        # 暂时返回按重要程度排序的展品
        return Exhibit.query.filter_by(is_active=True)\
                           .order_by(Exhibit.importance.desc())\
                           .limit(limit).all()
    
    @staticmethod
    def initialize_sample_data():
        """初始化示例数据"""
        try:
            # 检查是否已有数据
            if Exhibit.query.first():
                return {'success': True, 'message': '数据已存在'}
            
            # 创建示例展品
            sample_exhibits = [
                ("001", "中共一大会址", "中国共产党第一次全国代表大会会址", 10, 20, 5, 15, "会议", "建党时期"),
                ("002", "红船模型", "中共一大闭幕会议举行地红船复制模型", 15, 25, 5, 10, "模型", "建党时期"),
                ("003", "党章展示", "历届党章发展历程展示", 20, 15, 4, 8, "文献", "发展历程"),
                ("004", "革命文物", "早期革命活动相关文物", 25, 30, 4, 12, "文物", "革命时期"),
                ("005", "历史照片", "珍贵历史照片集锦", 30, 10, 3, 6, "照片", "历史记录"),
                ("006", "领袖题词", "重要领导人题词墨宝", 35, 20, 4, 8, "书法", "领袖风范"),
                ("007", "多媒体展示", "现代科技展示历史", 40, 25, 3, 10, "多媒体", "现代展示"),
                ("008", "互动体验区", "沉浸式历史体验", 45, 35, 4, 20, "互动", "体验教育"),
            ]
            
            for exhibit_data in sample_exhibits:
                RoutePlanningDatabase.create_exhibit(*exhibit_data)
            
            # 创建示例布局
            RoutePlanningDatabase.create_memorial_layout(
                name="南湖纪念馆标准布局",
                entrance_x=0, entrance_y=0,
                exit_x=50, exit_y=40,
                restrooms=[[15, 5], [35, 35]],
                rest_areas=[[20, 20], [40, 15]],
                emergency_exits=[[10, 40], [45, 0]],
                walkways=[
                    [[0, 0], [10, 10], [20, 20], [30, 30], [40, 40], [50, 40]],
                    [[10, 10], [15, 25], [25, 30]],
                    [[20, 20], [35, 20], [45, 35]]
                ]
            )
            
            return {'success': True, 'message': '示例数据初始化完成'}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
