# -*- coding: utf-8 -*-
"""
南湖纪念馆路线规划模块
Route Planning Module for Nanhu Memorial Hall

这个模块包含了所有与路线规划相关的功能：
- 路线优化算法
- 数据库操作  
- API接口
- 工具函数
"""

from .route_planning_core import (
    RouteOptimizer,
    MockDataGenerator, 
    LLMIntegration,
    UserProfile as RoutePlannerUserProfile,
    create_sample_route
)

from .route_planning_database import RoutePlanningDatabase
from .route_planning_utils import RoutePlanningUtils
from .route_planning_routes import register_route_planning_routes

__all__ = [
    # 核心功能
    'RouteOptimizer',
    'MockDataGenerator',
    'LLMIntegration', 
    'RoutePlannerUserProfile',
    'create_sample_route',
    
    # 数据库操作
    'RoutePlanningDatabase',
    
    # 工具函数
    'RoutePlanningUtils',
    
    # 路由注册
    'register_route_planning_routes'
]

# 模块信息
__version__ = '1.0.0'
__author__ = 'Flask团队 - 路线规划小组'
__description__ = '南湖纪念馆智能路线规划系统'
