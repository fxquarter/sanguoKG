# sanguoKG
## 该项目是以三国演义人物关系为基础制作的知识图谱。采用python+django+neo4j+echarts实现
### 目录结构解释
   - graph包下是应用结构，主要在views.py中实现视图创建，并在template文件夹下graph.html中通过使用echarts实现前端的展示。
   - neodb文件夹用于实现连接neo4j并通过py2neo实现向数据库中创建节点和关系。
   - raw_data保存处理好的五元组数据
   - spider为爬虫模块，用于爬取所需数据
   - sanguoKG作为初始创建django框架的配置文件，用于设置文件配置
   - graphrag文件夹是graphrag的实现部分，可以实现对文本内容提取知识图谱从而进行更精确的问答（就是太慢了-_-||）
### 部署方法
   1. 启动neo4j服务，测试localhost:7474能否连接
   2. 运行neodb/create_graph.py在neo4j中创建图数据库
   3. 运行python manage.py runserver启动程序，在localhost:8000中查看
