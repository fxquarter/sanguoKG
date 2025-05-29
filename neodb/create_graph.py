from py2neo import Graph, Node, Relationship
import csv

# 连接到 Neo4j 数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "chen8525"))

# 读取五元组数据并处理
with open('../raw_data/newRelation.csv', 'r', encoding='GBK') as f:
    # 删除所有现有节点和关系
    graph.run("MATCH (n) DETACH DELETE n")
    print("Deleted all nodes and relationships")

    reader = csv.reader(f)
    next(reader)  # 如果有表头的话，跳过表头

    for row in reader:
        p1, p2, relation, camp1, camp2 = row

        # 创建人物1节点，带有阵营标签
        node1 = Node("Person", name=p1, camp=camp1)
        node1.add_label(f"{camp1}")  # 根据阵营给人物1添加标签
        graph.merge(node1, "Person", "name")

        # 创建人物2节点，带有阵营标签
        node2 = Node("Person", name=p2, camp=camp2)
        node2.add_label(f"{camp2}")  # 根据阵营给人物2添加标签
        graph.merge(node2, "Person", "name")

        # 创建人物之间的关系
        rel = Relationship(node1, relation, node2)
        graph.merge(rel)

        print(f"Created nodes and relationships: {p1} -[{relation}]-> {p2} (with camps {camp1} and {camp2})")

print("知识图谱构建完成！")
