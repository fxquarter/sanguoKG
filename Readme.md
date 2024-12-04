# sanguoKG
## 该项目是以三国演义人物关系为基础制作的知识图谱。采用python+django+neo4j+echarts实现
### 目录结构解释
   - graph包下是应用结构，主要在views.py中实现视图创建，并在template文件夹下graph.html中通过使用echarts实现前端的展示。
   - neodb文件夹用于实现连接neo4j并通过py2neo实现向数据库中创建节点和关系。
   - raw_data保存处理好的五元组数据，爬虫模块施工ing......(~_~)
   - sanguoKG作为初始创建django框架的配置文件，用于设置文件配置
### 部署方法
   1. 启动neo4j服务，测试localhost:7474能否连接
   2. 运行neodb/create_graph.py在neo4j中创建图数据库
   3. 运行python manage.py runserver启动程序，在localhost:8000中查看
### 2024.12.4更新
   原有基础上加入pagerank算法，使节点间的重要性更加直观
