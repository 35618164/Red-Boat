# -*- coding: utf-8 -*-
"""
路线规划API路由模块
Route Planning API Routes
专门处理路线规划相关的API接口
"""

from flask import request, jsonify, render_template, session
from backend.route_planning import (
    RouteOptimizer, MockDataGenerator, LLMIntegration, 
    RoutePlannerUserProfile
)
from backend.route_planning.route_planning_database import RoutePlanningDatabase
import json

def register_route_planning_routes(app):
    """注册路线规划相关的路由"""
    
    @app.route('/route-planner')
    def route_planner_page():
        """路线规划页面 - 集成地图功能"""
        return render_template('route_planning_with_map.html')
    
    @app.route('/api/route-planning/generate', methods=['POST'])
    def generate_route():
        """生成智能路线API"""
        try:
            data = request.get_json()
            
            # 创建用户画像
            user_profile = RoutePlannerUserProfile(
                age_group=data.get('age_group', 'adult'),
                interests=data.get('interests', []),
                available_time=int(data.get('available_time', 60)),
                physical_ability=data.get('physical_ability', 'medium'),
                group_type=data.get('group_type', 'individual'),
                visit_purpose=data.get('visit_purpose', 'education')
            )
            
            # 生成模拟数据（后续会从数据库获取）
            exhibits = MockDataGenerator.generate_exhibits()
            layout = MockDataGenerator.generate_layout()
            
            # 创建路线优化器
            optimizer = RouteOptimizer(exhibits, layout)
            
            # 生成优化路线
            route = optimizer.optimize_route(user_profile)
            
            # 大模型增强
            enhanced_route = LLMIntegration.optimize_route_with_llm(route, user_profile)
            
            # 如果用户已登录，保存路线历史
            user_id = session.get('user_id')
            if user_id:
                RoutePlanningDatabase.save_route_history(
                    user_id=user_id,
                    route_name=f"智能路线_{data.get('age_group', 'adult')}",
                    route_data=enhanced_route,
                    user_preferences=data,
                    estimated_duration=enhanced_route['summary']['estimated_time']
                )
            
            return jsonify({
                'success': True,
                'data': enhanced_route,
                'message': '路线生成成功！'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'路线生成失败: {str(e)}'
            }), 500
    
    @app.route('/api/route-planning/exhibits')
    def get_exhibits():
        """获取所有展品信息API"""
        try:
            # 优先从数据库获取，如果没有数据则使用模拟数据
            db_exhibits = RoutePlanningDatabase.get_all_exhibits()
            
            if db_exhibits:
                exhibits_data = [exhibit.to_dict() for exhibit in db_exhibits]
            else:
                # 使用模拟数据
                exhibits = MockDataGenerator.generate_exhibits()
                exhibits_data = [
                    {
                        'id': exhibit.id,
                        'name': exhibit.name,
                        'description': exhibit.description,
                        'location': exhibit.location,
                        'importance': exhibit.importance,
                        'visit_duration': exhibit.visit_duration,
                        'category': exhibit.category,
                        'period': exhibit.period
                    } for exhibit in exhibits
                ]
            
            return jsonify({
                'success': True,
                'data': exhibits_data
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'获取展品信息失败: {str(e)}'
            }), 500
    
    @app.route('/api/route-planning/layout')
    def get_layout():
        """获取场馆布局信息API"""
        try:
            # 优先从数据库获取
            db_layout = RoutePlanningDatabase.get_active_layout()
            
            if db_layout:
                layout_data = db_layout.to_dict()
            else:
                # 使用模拟数据
                layout_data = MockDataGenerator.generate_layout()
            
            return jsonify({
                'success': True,
                'data': layout_data
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'获取布局信息失败: {str(e)}'
            }), 500
    
    @app.route('/api/route-planning/save', methods=['POST'])
    def save_route():
        """保存用户路线API"""
        try:
            data = request.get_json()
            user_id = session.get('user_id')
            
            if not user_id:
                return jsonify({
                    'success': False,
                    'message': '请先登录'
                }), 401
            
            result = RoutePlanningDatabase.save_route_history(
                user_id=user_id,
                route_name=data.get('route_name', '我的路线'),
                route_data=data.get('route_data', {}),
                user_preferences=data.get('user_preferences', {}),
                estimated_duration=data.get('estimated_duration', 60)
            )
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'路线保存失败: {str(e)}'
            }), 500
    
    @app.route('/api/route-planning/history')
    def get_route_history():
        """获取用户历史路线API"""
        try:
            user_id = session.get('user_id')
            
            if not user_id:
                return jsonify({
                    'success': False,
                    'message': '请先登录'
                }), 401
            
            routes = RoutePlanningDatabase.get_user_route_history(user_id)
            routes_data = [route.to_dict() for route in routes]
            
            return jsonify({
                'success': True,
                'data': routes_data
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'获取历史路线失败: {str(e)}'
            }), 500
    
    @app.route('/api/route-planning/feedback', methods=['POST'])
    def submit_feedback():
        """提交路线反馈API"""
        try:
            data = request.get_json()
            user_id = session.get('user_id')
            
            if not user_id:
                return jsonify({
                    'success': False,
                    'message': '请先登录'
                }), 401
            
            result = RoutePlanningDatabase.update_route_feedback(
                route_id=data.get('route_id'),
                actual_duration=data.get('actual_duration'),
                user_rating=data.get('rating'),
                feedback=data.get('feedback')
            )
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'反馈提交失败: {str(e)}'
            }), 500
    
    @app.route('/api/route-planning/recommendations')
    def get_recommendations():
        """获取推荐路线模板API"""
        try:
            # 模拟推荐数据（后续可以从数据库获取）
            recommendations = [
                {
                    'id': 1,
                    'name': '经典红色之旅',
                    'description': '追寻革命足迹，感受红色精神',
                    'duration': 90,
                    'difficulty': '适中',
                    'target_audience': '成人游客',
                    'highlights': ['红船模型', '中共一大会址', '革命文物']
                },
                {
                    'id': 2,
                    'name': '亲子教育路线',
                    'description': '寓教于乐，适合家庭参观',
                    'duration': 60,
                    'difficulty': '简单',
                    'target_audience': '家庭游客',
                    'highlights': ['互动体验区', '多媒体展示', '历史照片']
                },
                {
                    'id': 3,
                    'name': '深度学术研究',
                    'description': '详细了解历史背景和文献资料',
                    'duration': 120,
                    'difficulty': '具有挑战性',
                    'target_audience': '研究学者',
                    'highlights': ['党章展示', '历史文献', '领袖题词']
                }
            ]
            
            return jsonify({
                'success': True,
                'data': recommendations
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'获取推荐失败: {str(e)}'
            }), 500
    
    @app.route('/api/route-planning/popular-exhibits')
    def get_popular_exhibits():
        """获取热门展品API"""
        try:
            popular_exhibits = RoutePlanningDatabase.get_popular_exhibits(limit=5)
            exhibits_data = [exhibit.to_dict() for exhibit in popular_exhibits]
            
            return jsonify({
                'success': True,
                'data': exhibits_data
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'获取热门展品失败: {str(e)}'
            }), 500
    
    @app.route('/api/route-planning/init-sample-data', methods=['POST'])
    def init_sample_data():
        """初始化示例数据API（管理员功能）"""
        try:
            # 这里可以添加管理员权限检查
            result = RoutePlanningDatabase.initialize_sample_data()
            return jsonify(result)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'初始化数据失败: {str(e)}'
            }), 500
