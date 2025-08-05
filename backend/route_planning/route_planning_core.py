# -*- coding: utf-8 -*-
"""
南湖纪念馆智能路线规划系统
Route Planning System for Nanhu Memorial Hall

作者: Flask团队
日期: 2025年8月6日
"""

from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import random

@dataclass
class Exhibit:
    """展品数据模型"""
    id: str
    name: str
    description: str
    location: Tuple[float, float]  # (x, y) 坐标
    importance: int  # 1-5重要程度
    visit_duration: int  # 建议参观时间(分钟)
    category: str  # 展品类别
    period: str  # 历史时期
    
@dataclass
class UserProfile:
    """用户画像模型"""
    age_group: str  # 年龄组: child, youth, adult, senior
    interests: List[str]  # 兴趣标签
    available_time: int  # 可用时间(分钟)
    physical_ability: str  # 体力状况: low, medium, high
    group_type: str  # 团体类型: individual, family, group
    visit_purpose: str  # 参观目的: education, leisure, research

class MockDataGenerator:
    """模拟数据生成器 - 用于原型开发"""
    
    @staticmethod
    def generate_exhibits() -> List[Exhibit]:
        """生成模拟展品数据"""
        exhibits = [
            Exhibit("001", "中共一大会址", "中国共产党第一次全国代表大会会址", (10, 20), 5, 15, "会议", "建党时期"),
            Exhibit("002", "红船模型", "中共一大闭幕会议举行地红船复制模型", (15, 25), 5, 10, "模型", "建党时期"),
            Exhibit("003", "党章展示", "历届党章发展历程展示", (20, 15), 4, 8, "文献", "发展历程"),
            Exhibit("004", "革命文物", "早期革命活动相关文物", (25, 30), 4, 12, "文物", "革命时期"),
            Exhibit("005", "历史照片", "珍贵历史照片集锦", (30, 10), 3, 6, "照片", "历史记录"),
            Exhibit("006", "领袖题词", "重要领导人题词墨宝", (35, 20), 4, 8, "书法", "领袖风范"),
            Exhibit("007", "多媒体展示", "现代科技展示历史", (40, 25), 3, 10, "多媒体", "现代展示"),
            Exhibit("008", "互动体验区", "沉浸式历史体验", (45, 35), 4, 20, "互动", "体验教育"),
        ]
        return exhibits
    
    @staticmethod
    def generate_layout() -> Dict[str, Any]:
        """生成模拟场馆布局数据"""
        return {
            "entrance": (0, 0),
            "exit": (50, 40),
            "restrooms": [(15, 5), (35, 35)],
            "rest_areas": [(20, 20), (40, 15)],
            "emergency_exits": [(10, 40), (45, 0)],
            "walkways": [
                # 主通道
                [(0, 0), (10, 10), (20, 20), (30, 30), (40, 40), (50, 40)],
                # 分支通道
                [(10, 10), (15, 25), (25, 30)],
                [(20, 20), (35, 20), (45, 35)]
            ]
        }

class RouteOptimizer:
    """路线优化算法"""
    
    def __init__(self, exhibits: List[Exhibit], layout: Dict[str, Any]):
        self.exhibits = exhibits
        self.layout = layout
    
    def calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """计算两点间距离"""
        return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
    
    def filter_exhibits_by_interests(self, user: UserProfile) -> List[Exhibit]:
        """根据用户兴趣筛选展品"""
        if not user.interests:
            return self.exhibits
        
        # 兴趣匹配算法（简化版）
        relevant_exhibits = []
        for exhibit in self.exhibits:
            # 根据兴趣标签匹配展品类别
            if any(interest in exhibit.category.lower() or 
                   interest in exhibit.description.lower() for interest in user.interests):
                relevant_exhibits.append(exhibit)
        
        # 如果匹配结果太少，添加高重要度展品
        if len(relevant_exhibits) < 3:
            high_importance = [e for e in self.exhibits if e.importance >= 4]
            relevant_exhibits.extend(high_importance)
        
        return list(set(relevant_exhibits))  # 去重
    
    def optimize_route(self, user: UserProfile) -> Dict[str, Any]:
        """优化参观路线"""
        # 1. 根据兴趣筛选展品
        candidate_exhibits = self.filter_exhibits_by_interests(user)
        
        # 2. 根据时间约束筛选
        selected_exhibits = self._select_by_time_constraint(candidate_exhibits, user.available_time)
        
        # 3. 根据体力状况调整
        route = self._adjust_for_physical_ability(selected_exhibits, user.physical_ability)
        
        # 4. 优化访问顺序
        optimized_route = self._optimize_visit_order(route)
        
        # 5. 生成详细路线信息
        return self._generate_route_details(optimized_route, user)
    
    def _select_by_time_constraint(self, exhibits: List[Exhibit], available_time: int) -> List[Exhibit]:
        """根据时间约束筛选展品"""
        # 按重要程度排序
        sorted_exhibits = sorted(exhibits, key=lambda x: x.importance, reverse=True)
        
        selected = []
        total_time = 0
        
        for exhibit in sorted_exhibits:
            if total_time + exhibit.visit_duration <= available_time * 0.8:  # 留20%缓冲时间
                selected.append(exhibit)
                total_time += exhibit.visit_duration
        
        return selected
    
    def _adjust_for_physical_ability(self, exhibits: List[Exhibit], ability: str) -> List[Exhibit]:
        """根据体力状况调整路线"""
        if ability == "low":
            # 体力较弱，减少展品数量，优先选择重要展品
            return sorted(exhibits, key=lambda x: x.importance, reverse=True)[:5]
        elif ability == "high":
            # 体力较好，可以参观更多展品
            return exhibits
        else:
            # 中等体力，适中选择
            return exhibits[:7]
    
    def _optimize_visit_order(self, exhibits: List[Exhibit]) -> List[Exhibit]:
        """优化访问顺序 - 简化版最近邻算法"""
        if not exhibits:
            return []
        
        # 从入口开始
        current_pos = self.layout["entrance"]
        route = []
        remaining = exhibits.copy()
        
        while remaining:
            # 找到距离当前位置最近的展品
            nearest = min(remaining, key=lambda e: self.calculate_distance(current_pos, e.location))
            route.append(nearest)
            remaining.remove(nearest)
            current_pos = nearest.location
        
        return route
    
    def _generate_route_details(self, route: List[Exhibit], user: UserProfile) -> Dict[str, Any]:
        """生成详细路线信息"""
        total_time = sum(exhibit.visit_duration for exhibit in route)
        total_distance = 0
        
        # 计算总距离
        positions = [self.layout["entrance"]] + [e.location for e in route] + [self.layout["exit"]]
        for i in range(len(positions) - 1):
            total_distance += self.calculate_distance(positions[i], positions[i + 1])
        
        return {
            "route": [
                {
                    "id": exhibit.id,
                    "name": exhibit.name,
                    "description": exhibit.description,
                    "location": exhibit.location,
                    "visit_duration": exhibit.visit_duration,
                    "importance": exhibit.importance,
                    "category": exhibit.category
                } for exhibit in route
            ],
            "summary": {
                "total_exhibits": len(route),
                "estimated_time": total_time,
                "total_distance": round(total_distance, 2),
                "difficulty": self._calculate_difficulty(route, user.physical_ability)
            },
            "recommendations": self._generate_recommendations(route, user),
            "generated_at": datetime.now().isoformat()
        }
    
    def _calculate_difficulty(self, route: List[Exhibit], ability: str) -> str:
        """计算路线难度"""
        if len(route) <= 3:
            return "简单"
        elif len(route) <= 6:
            return "适中"
        else:
            return "具有挑战性"
    
    def _generate_recommendations(self, route: List[Exhibit], user: UserProfile) -> List[str]:
        """生成个性化建议"""
        recommendations = []
        
        if user.age_group == "child":
            recommendations.append("建议多关注互动体验区，增强学习趣味性")
        if user.group_type == "family":
            recommendations.append("建议在休息区适当停留，照顾不同年龄成员需求")
        if len(route) > 6:
            recommendations.append("路线较长，建议中途在休息区稍作休息")
        if user.available_time < 60:
            recommendations.append("时间较紧，建议重点关注核心展品")
        
        return recommendations

class LLMIntegration:
    """大模型集成模块（模拟版本）"""
    
    @staticmethod
    def generate_exhibit_description(exhibit: Exhibit, user_context: str) -> str:
        """生成个性化展品介绍"""
        # 这里将来集成真实的大模型API
        templates = {
            "child": f"小朋友，{exhibit.name}是一个很特别的地方...",
            "adult": f"{exhibit.name}具有重要的历史意义...",
            "researcher": f"从学术角度来看，{exhibit.name}..."
        }
        return templates.get(user_context, exhibit.description)
    
    @staticmethod
    def optimize_route_with_llm(route_data: Dict[str, Any], user: UserProfile) -> Dict[str, Any]:
        """使用大模型优化路线建议"""
        # 模拟大模型优化建议
        enhanced_recommendations = route_data.get("recommendations", [])
        enhanced_recommendations.append("AI建议：根据您的兴趣偏好，建议在某某展品处多停留片刻")
        
        route_data["recommendations"] = enhanced_recommendations
        route_data["llm_enhanced"] = True
        
        return route_data

# 使用示例
def create_sample_route():
    """创建示例路线"""
    # 生成模拟数据
    exhibits = MockDataGenerator.generate_exhibits()
    layout = MockDataGenerator.generate_layout()
    
    # 创建用户画像
    user = UserProfile(
        age_group="adult",
        interests=["历史", "文物", "革命"],
        available_time=90,  # 90分钟
        physical_ability="medium",
        group_type="individual",
        visit_purpose="education"
    )
    
    # 创建路线优化器
    optimizer = RouteOptimizer(exhibits, layout)
    
    # 生成优化路线
    route = optimizer.optimize_route(user)
    
    # 大模型增强
    enhanced_route = LLMIntegration.optimize_route_with_llm(route, user)
    
    return enhanced_route

if __name__ == "__main__":
    # 测试运行
    sample_route = create_sample_route()
    print("="*50)
    print("南湖纪念馆智能路线规划系统 - 测试运行")
    print("="*50)
    print(f"推荐路线包含 {sample_route['summary']['total_exhibits']} 个展品")
    print(f"预计参观时间: {sample_route['summary']['estimated_time']} 分钟")
    print(f"路线难度: {sample_route['summary']['difficulty']}")
    print("\n推荐路线:")
    for i, exhibit in enumerate(sample_route['route'], 1):
        print(f"{i}. {exhibit['name']} (预计 {exhibit['visit_duration']} 分钟)")
    print("\n个性化建议:")
    for rec in sample_route['recommendations']:
        print(f"• {rec}")
