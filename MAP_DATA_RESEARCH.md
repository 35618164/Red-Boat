# 开放地图数据接口调研报告

## 1. OpenStreetMap + Leaflet (强烈推荐)

### 优势：
- ✅ 完全免费，无API调用限制
- ✅ 数据开放，可自定义
- ✅ 支持中国地区详细地图
- ✅ 可以展示室内地图
- ✅ 支持自定义标记和路线绘制

### 实现方案：
```javascript
// 1. 引入Leaflet库
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />

// 2. 创建地图实例
var map = L.map('map').setView([30.7617, 120.0106], 15); // 南湖区域坐标

// 3. 添加地图图层
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// 4. 添加纪念馆标记
var memorial = L.marker([30.7617, 120.0106]).addTo(map)
    .bindPopup('南湖纪念馆');
```

### 路线规划集成：
- **GraphHopper API**: 免费每日1000次调用
- **OSRM API**: 完全免费的开源路线规划
- **MapBox Directions**: 免费每月50,000次调用

## 2. 高德地图 API (国内推荐)

### 优势：
- ✅ 国内地图数据最准确
- ✅ 免费额度：每日30万次调用
- ✅ 中文文档完善
- ✅ 支持室内地图

### API接口：
```javascript
// Web API
https://restapi.amap.com/v3/direction/walking?parameters

// JavaScript API
var map = new AMap.Map('container', {
    zoom: 15,
    center: [120.0106, 30.7617]
});
```

## 3. 百度地图 API

### 优势：
- ✅ 免费配额充足
- ✅ 国内覆盖全面
- ✅ 支持个人开发者

### 限制：
- ⚠️ 需要企业认证才能商用
- ⚠️ 室内地图支持有限

## 4. 腾讯地图 API

### 优势：
- ✅ 免费额度：每日10万次
- ✅ 微信生态集成好
- ✅ 数据准确度高

## 5. MapBox (国际方案)

### 优势：
- ✅ 地图样式自定义程度高
- ✅ 免费每月50,000次调用
- ✅ 支持3D地图

### 限制：
- ⚠️ 国内访问速度较慢
- ⚠️ 中国地区数据不如本土地图

## 推荐实施方案

### 方案A: OpenStreetMap + 自定义室内地图 (推荐)
```
成本: 完全免费
技术难度: 中等
适用场景: 纪念馆室内导航
优势: 完全可控，无API限制
```

### 方案B: 高德地图 + 室内地图SDK
```
成本: 免费(30万次/日)
技术难度: 简单
适用场景: 室外+室内综合导航
优势: 数据准确，中文支持好
```

### 方案C: 混合方案
```
室外导航: 高德/百度地图API
室内导航: 自定义SVG/Canvas地图
路线规划: OSRM开源引擎
```

## 具体实现建议

### 1. 纪念馆室内地图
由于纪念馆是室内场所，建议：
- 使用SVG或Canvas绘制室内平面图
- 标记展品位置坐标
- 实现A*算法进行路径规划
- 用Leaflet展示周边环境

### 2. 数据获取方式
- 实地测量展品坐标
- 获取纪念馆建筑图纸
- 使用激光测距仪精确定位
- 建立坐标系统

### 3. 技术栈推荐
```
前端: Leaflet.js + Vue.js
地图数据: OpenStreetMap
室内地图: 自制SVG地图
路线算法: A* 或 Dijkstra
后端: Flask + PostGIS
```
