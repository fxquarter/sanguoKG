from django.shortcuts import render
from py2neo import Graph


# 连接到 Neo4j 数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "chen8525"))


def get_graph_data():
    # 查询人物节点和人物关系
    query = """
    MATCH (p1:Person)-[r]->(p2:Person)
    RETURN p1.name AS person1, p2.name AS person2, type(r) AS relation, p1.camp AS camp1, p2.camp AS camp2
    """
    result = graph.run(query)

    nodes = {}
    edges = []

    # 提取节点和关系数据
    for record in result:
        person1 = record["person1"]
        person2 = record["person2"]
        relation = record["relation"]
        camp1 = record["camp1"]
        camp2 = record["camp2"]

        # 创建人物节点
        if person1 not in nodes:
            nodes[person1] = {"name": person1, "camp": camp1}
        if person2 not in nodes:
            nodes[person2] = {"name": person2, "camp": camp2}

        # 创建边（关系）
        edges.append({
            "source": person1,
            "target": person2,
            "relation": relation or 'undefined'
        })

    return {"nodes": list(nodes.values()), "edges": edges}


def graph_view(request):
    data = get_graph_data()
    return render(request, "graph/graph.html", {"graph_data": data})

