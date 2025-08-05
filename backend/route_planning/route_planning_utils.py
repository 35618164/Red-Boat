# -*- coding: utf-8 -*-
"""
路线规划工具函数模块
Route Planning Utilities
专门处理路线规划相关的工具函数
"""

import math
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

class RoutePlanningUtils:
    """路线规划工具类"""
    
    @staticmethod
    def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """计算两点间的欧几里得距离"""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    @staticmethod
    def calculate_manhattan_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """计算两点间的曼哈顿距离（更适合室内导航）"""
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
    
    @staticmethod
    def estimate_walking_time(distance: float, walking_speed: float = 1.2) -> int:
        """估算步行时间（米/秒）"""
        # 默认步行速度 1.2 m/s（约4.3 km/h，适合室内参观）
        return int(distance / walking_speed / 60)  # 转换为分钟
    
    @staticmethod
    def validate_user_preferences(preferences: Dict[str, Any]) -> Dict[str, Any]:
        """验证和标准化用户偏好设置"""
        validated = {}
        
        # 年龄组验证
        valid_age_groups = ['child', 'youth', 'adult', 'senior']
        validated['age_group'] = preferences.get('age_group', 'adult')
        if validated['age_group'] not in valid_age_groups:
            validated['age_group'] = 'adult'
        
        # 体力状况验证
        valid_abilities = ['low', 'medium', 'high']
        validated['physical_ability'] = preferences.get('physical_ability', 'medium')
        if validated['physical_ability'] not in valid_abilities:
            validated['physical_ability'] = 'medium'
        
        # 参观类型验证
        valid_group_types = ['individual', 'family', 'group']
        validated['group_type'] = preferences.get('group_type', 'individual')
        if validated['group_type'] not in valid_group_types:
            validated['group_type'] = 'individual'
        
        # 时间验证
        validated['available_time'] = max(30, min(300, preferences.get('available_time', 60)))
        
        # 兴趣标签验证
        interests = preferences.get('interests', [])
        if isinstance(interests, list):
            validated['interests'] = interests
        else:
            validated['interests'] = []
        
        return validated
    
    @staticmethod
    def calculate_route_statistics(route_data: Dict[str, Any]) -> Dict[str, Any]:
        """计算路线统计信息"""
        if 'route' not in route_data:
            return {}
        
        route = route_data['route']
        stats = {
            'total_exhibits': len(route),
            'total_duration': sum(exhibit.get('visit_duration', 0) for exhibit in route),
            'importance_distribution': {},
            'category_distribution': {},
            'period_distribution': {}
        }
        
        # 重要程度分布
        for exhibit in route:
            importance = exhibit.get('importance', 3)
            stats['importance_distribution'][importance] = stats['importance_distribution'].get(importance, 0) + 1
        
        # 类别分布
        for exhibit in route:
            category = exhibit.get('category', '未分类')
            stats['category_distribution'][category] = stats['category_distribution'].get(category, 0) + 1
        
        # 时期分布
        for exhibit in route:
            period = exhibit.get('period', '未知时期')
            stats['period_distribution'][period] = stats['period_distribution'].get(period, 0) + 1
        
        return stats
    
    @staticmethod
    def format_route_for_export(route_data: Dict[str, Any], format_type: str = 'json') -> str:
        """格式化路线数据用于导出"""
        if format_type.lower() == 'json':
            return json.dumps(route_data, ensure_ascii=False, indent=2)
        
        elif format_type.lower() == 'text':
            text_output = []
            text_output.append("="*50)
            text_output.append("南湖纪念馆参观路线")
            text_output.append("="*50)
            
            if 'summary' in route_data:
                summary = route_data['summary']
                text_output.append(f"展品数量: {summary.get('total_exhibits', 0)} 个")
                text_output.append(f"预计时间: {summary.get('estimated_time', 0)} 分钟")
                text_output.append(f"路线难度: {summary.get('difficulty', '未知')}")
                text_output.append("")
            
            if 'route' in route_data:
                text_output.append("详细路线:")
                text_output.append("-"*30)
                for i, exhibit in enumerate(route_data['route'], 1):
                    text_output.append(f"{i}. {exhibit.get('name', '未知展品')}")
                    text_output.append(f"   描述: {exhibit.get('description', '暂无描述')}")
                    text_output.append(f"   建议停留: {exhibit.get('visit_duration', 0)} 分钟")
                    text_output.append(f"   重要程度: {'⭐' * exhibit.get('importance', 3)}")
                    text_output.append("")
            
            if 'recommendations' in route_data:
                text_output.append("个性化建议:")
                text_output.append("-"*30)
                for rec in route_data['recommendations']:
                    text_output.append(f"• {rec}")
                text_output.append("")
            
            text_output.append("="*50)
            text_output.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return "\n".join(text_output)
        
        return str(route_data)
    
    @staticmethod
    def generate_route_sharing_info(route_data: Dict[str, Any]) -> Dict[str, str]:
        """生成路线分享信息"""
        sharing_info = {
            'title': '我的南湖纪念馆参观路线',
            'description': f"包含 {route_data.get('summary', {}).get('total_exhibits', 0)} 个展品的精心规划路线",
            'hashtags': ['#南湖纪念馆', '#红色旅游', '#智能路线规划']
        }
        
        if 'route' in route_data and route_data['route']:
            highlights = [exhibit.get('name', '') for exhibit in route_data['route'][:3]]
            sharing_info['highlights'] = '、'.join(highlights)
            sharing_info['description'] += f"，重点参观：{sharing_info['highlights']}"
        
        return sharing_info
    
    @staticmethod
    def calculate_accessibility_score(route_data: Dict[str, Any]) -> Dict[str, Any]:
        """计算路线无障碍友好程度"""
        if 'route' not in route_data:
            return {'score': 0, 'suggestions': []}
        
        route = route_data['route']
        accessibility_score = 0
        suggestions = []
        
        # 基于展品数量评分
        exhibit_count = len(route)
        if exhibit_count <= 5:
            accessibility_score += 30
        elif exhibit_count <= 8:
            accessibility_score += 20
        else:
            accessibility_score += 10
            suggestions.append("路线包含较多展品，建议适当休息")
        
        # 基于总时长评分
        total_duration = route_data.get('summary', {}).get('estimated_time', 0)
        if total_duration <= 60:
            accessibility_score += 30
        elif total_duration <= 90:
            accessibility_score += 20
        else:
            accessibility_score += 10
            suggestions.append("参观时间较长，建议在休息区适当停留")
        
        # 基于路线复杂度评分
        if route_data.get('summary', {}).get('difficulty') == '简单':
            accessibility_score += 40
        elif route_data.get('summary', {}).get('difficulty') == '适中':
            accessibility_score += 30
        else:
            accessibility_score += 20
            suggestions.append("路线具有一定挑战性，建议量力而行")
        
        return {
            'score': min(100, accessibility_score),
            'level': '优秀' if accessibility_score >= 80 else '良好' if accessibility_score >= 60 else '一般',
            'suggestions': suggestions
        }
    
    @staticmethod
    def optimize_route_order_by_time(exhibits: List[Dict], current_time: datetime) -> List[Dict]:
        """根据当前时间优化路线顺序"""
        # 根据一天中的时间调整路线
        hour = current_time.hour
        
        # 上午（9-11点）：从重要展品开始
        if 9 <= hour < 11:
            return sorted(exhibits, key=lambda x: x.get('importance', 3), reverse=True)
        
        # 中午（11-13点）：选择较轻松的展品
        elif 11 <= hour < 13:
            interactive_exhibits = [e for e in exhibits if '互动' in e.get('category', '')]
            other_exhibits = [e for e in exhibits if '互动' not in e.get('category', '')]
            return interactive_exhibits + other_exhibits
        
        # 下午（13-16点）：平衡安排
        elif 13 <= hour < 16:
            return exhibits  # 保持原顺序
        
        # 傍晚（16点后）：优先安排必看展品
        else:
            high_importance = [e for e in exhibits if e.get('importance', 3) >= 4]
            other_exhibits = [e for e in exhibits if e.get('importance', 3) < 4]
            return high_importance + other_exhibits[:3]  # 限制展品数量
    
    @staticmethod
    def generate_route_qr_code_data(route_id: int) -> Dict[str, Any]:
        """生成路线二维码数据"""
        return {
            'type': 'nanhu_memorial_route',
            'route_id': route_id,
            'generated_at': datetime.now().isoformat(),
            'url': f"https://example.com/route/{route_id}"  # 实际部署时需要修改
        }
