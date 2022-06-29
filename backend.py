from flask import Flask, request, abort
from flask_cors import CORS, cross_origin
import pandas as pd
import networkx as nx
import json
from networkx.readwrite import json_graph
import dijkstra
import Quary
from flask import request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app, resources={r"/foo": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'
# CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    return "Hello, World!"


df_complete = pd.read_csv('data/Complete-Data.csv')

with open('data/MasterConceptNetwork_Word2Vec-0.62_Baseline-Test.json') as f:
    js_graph = json.load(f)
    G_MasterConceptNetwork = json_graph.node_link_graph(js_graph)

# @app.route("/<concept>",methods=['GET','POST'])
# def List_Semantic_Feature(concept):
#     feature_list = list(df_complete[df_complete['Concept']==str(concept)].sort_values(by=['cue_validity'],ascending=False)['Feature'])
#     if request.method == 'GET':
#         return feature_list[0]
#     else:
#         return 'POST'



@app.route("/experimentProgress",methods=['GET','POST'])
# @cross_origin(origin='*',headers=['Content-Type','Authorization'])
def Experiment_Progress():
    if not request.json:
        abort(400)
    user_id=request.json
    experiment_progress = Quary.getExperimentMangement(user_id)
    return experiment_progress

# replace this with test record data
@app.route("/fullRecord",methods=['GET','POST'])
# @cross_origin(origin='*',headers=['Content-Type','Authorization'])
def Full_Record():
    if not request.json:
        abort(400)
    user_id=request.json
    full_record=Quary.getFullRecord(user_id)
    return full_record



@app.route("/therapyPlan/",methods=['GET','POST'])
# @cross_origin(origin='*',headers=['Access-Control-Allow-Origin','Content-Type','Authorization'])
def Therapy_Plan():
    if not request.json:
        abort(400)
    similarity_filepath = "data/concept_simi_norm.csv"
    concept_filepath = "data/CCFD_concept_info.csv"
    start_filepath = "data/start_words.csv"
    word_en_list = ["artificial_object", "transportation", "animal", "plant", "food", "nature_object", "bodypart"]
    laplace_path = "data/laplace"
    end_count_dict = request.json #收到前端的参数
    plan_a = dijkstra.dijkstraFindWay(start_filepath, similarity_filepath, concept_filepath, end_count_dict, laplace_path,
                                           word_en_list)
    plan_2 = {
            "type":"subgraph",
            "title": "训练路径 2",
            "checked": "false",
            "nodes": [{
                "id": "钢笔"
            }, {
                "id": "画笔"
            }, {
                "id": "画纸"
            }, {
                "id": "记号笔"
            }, {
                "id": "蜡笔"
            }, {
                "id": "手"
            }, {
                "id": "手臂"
            }, {
                "id": "手掌"
            }, {
                "id": "手指"
            }, {
                "id": "臀部"
            }],
            "edges": [{
                "source": "钢笔",
                "target": "画笔"
            }, {
                "source": "钢笔",
                "target": "画纸"
            }, {
                "source": "钢笔",
                "target": "记号笔"
            }, {
                "source": "钢笔",
                "target": "蜡笔"
            }, {
                "source": "钢笔",
                "target": "手"
            }, {
                "source": "钢笔",
                "target": "手臂"
            }, {
                "source": "钢笔",
                "target": "手掌"
            }, {
                "source": "钢笔",
                "target": "手指"
            }, {
                "source": "画笔",
                "target": "画纸"
            }, {
                "source": "画笔",
                "target": "记号笔"
            }, {
                "source": "画笔",
                "target": "蜡笔"
            }, {
                "source": "画笔",
                "target": "手"
            }, {
                "source": "画笔",
                "target": "手臂"
            }, {
                "source": "画笔",
                "target": "手掌"
            }, {
                "source": "画笔",
                "target": "手指"
            }, {
                "source": "画纸",
                "target": "记号笔"
            }, {
                "source": "画纸",
                "target": "蜡笔"
            }, {
                "source": "画纸",
                "target": "手"
            }, {
                "source": "画纸",
                "target": "手臂"
            }, {
                "source": "画纸",
                "target": "手掌"
            }, {
                "source": "画纸",
                "target": "手指"
            }, {
                "source": "记号笔",
                "target": "蜡笔"
            }, {
                "source": "记号笔",
                "target": "手"
            }, {
                "source": "记号笔",
                "target": "手臂"
            }, {
                "source": "记号笔",
                "target": "手掌"
            }, {
                "source": "记号笔",
                "target": "手指"
            }, {
                "source": "蜡笔",
                "target": "手"
            }, {
                "source": "蜡笔",
                "target": "手臂"
            }, {
                "source": "蜡笔",
                "target": "手掌"
            }, {
                "source": "蜡笔",
                "target": "手指"
            }, {
                "source": "手",
                "target": "手臂"
            }, {
                "source": "手",
                "target": "手掌"
            }, {
                "source": "手",
                "target": "手指"
            }, {
                "source": "手",
                "target": "臀部"
            }, {
                "source": "手臂",
                "target": "手掌"
            }, {
                "source": "手臂",
                "target": "手指"
            }, {
                "source": "手臂",
                "target": "臀部"
            }, {
                "source": "手掌",
                "target": "手指"
            }, {
                "source": "手掌",
                "target": "臀部"
            }, {
                "source": "手指",
                "target": "臀部"
            }]
        }
    plan_3 = {
            "type":"subgraph",
            "title": "训练路径 3",
            "checked": "false",
            "nodes": [{
                "id": "钢笔"
            }, {
                "id": "画笔"
            }, {
                "id": "画纸"
            }, {
                "id": "记号笔"
            }, {
                "id": "蜡笔"
            }, {
                "id": "手"
            }, {
                "id": "手臂"
            }, {
                "id": "手掌"
            }, {
                "id": "手指"
            }, {
                "id": "臀部"
            }],
            "edges": [{
                "source": "钢笔",
                "target": "画笔"
            }, {
                "source": "钢笔",
                "target": "画纸"
            }, {
                "source": "钢笔",
                "target": "记号笔"
            }, {
                "source": "钢笔",
                "target": "蜡笔"
            }, {
                "source": "钢笔",
                "target": "手"
            }, {
                "source": "钢笔",
                "target": "手臂"
            }, {
                "source": "钢笔",
                "target": "手掌"
            }, {
                "source": "钢笔",
                "target": "手指"
            }, {
                "source": "画笔",
                "target": "画纸"
            }, {
                "source": "画笔",
                "target": "记号笔"
            }, {
                "source": "画笔",
                "target": "蜡笔"
            }, {
                "source": "画笔",
                "target": "手"
            }, {
                "source": "画笔",
                "target": "手臂"
            }, {
                "source": "画笔",
                "target": "手掌"
            }, {
                "source": "画笔",
                "target": "手指"
            }, {
                "source": "画纸",
                "target": "记号笔"
            }, {
                "source": "画纸",
                "target": "蜡笔"
            }, {
                "source": "画纸",
                "target": "手"
            }, {
                "source": "画纸",
                "target": "手臂"
            }, {
                "source": "画纸",
                "target": "手掌"
            }, {
                "source": "画纸",
                "target": "手指"
            }, {
                "source": "记号笔",
                "target": "蜡笔"
            }, {
                "source": "记号笔",
                "target": "手"
            }, {
                "source": "记号笔",
                "target": "手臂"
            }, {
                "source": "记号笔",
                "target": "手掌"
            }, {
                "source": "记号笔",
                "target": "手指"
            }, {
                "source": "蜡笔",
                "target": "手"
            }, {
                "source": "蜡笔",
                "target": "手臂"
            }, {
                "source": "蜡笔",
                "target": "手掌"
            }, {
                "source": "蜡笔",
                "target": "手指"
            }, {
                "source": "手",
                "target": "手臂"
            }, {
                "source": "手",
                "target": "手掌"
            }, {
                "source": "手",
                "target": "手指"
            }, {
                "source": "手",
                "target": "臀部"
            }, {
                "source": "手臂",
                "target": "手掌"
            }, {
                "source": "手臂",
                "target": "手指"
            }, {
                "source": "手臂",
                "target": "臀部"
            }, {
                "source": "手掌",
                "target": "手指"
            }, {
                "source": "手掌",
                "target": "臀部"
            }, {
                "source": "手指",
                "target": "臀部"
            }]
    }
    plan_a["plans"].append(plan_2)
    plan_a["plans"].append(plan_3)
    return plan_a


@app.route("/shortestPath/<concept>",methods=['GET','POST'])
# @cross_origin(origin='*',headers=['Access-Control-Allow-Origin','Content-Type','Authorization'])
def Shortest_Path(concept):
    target_maincategory = df_complete[df_complete['Concept']==concept]['上级类别'].unique()[0]

    nodes = []
    for n in G_MasterConceptNetwork.nodes:
        if 'picture_naming_result' in G_MasterConceptNetwork.nodes[n]:
            if (G_MasterConceptNetwork.nodes[n]['maincategory']==target_maincategory) & (G_MasterConceptNetwork.nodes[n]['picture_naming_result']==True):
                nodes.append(n)

    shortest_length = 1000
    shortest_path = []

    for node in nodes:
        path = nx.dijkstra_path(G_MasterConceptNetwork, node, concept)
        if(len(path)<shortest_length):
            shortest_length = len(path)
            shortest_path = path
        subgraph = G_MasterConceptNetwork.subgraph(shortest_path)

    return json.dumps(json_graph.node_link_data(subgraph),ensure_ascii=False).replace('links','edges')


@app.route("/nodeRecord/<concept>",methods=['GET','POST'])
# @cross_origin(origin='*',headers=['Access-Control-Allow-Origin','Content-Type','Authorization'])
def Node_Record(concept):
    node_record = {
        "id":concept,
        "PictureNaming":[{
            "result":"false",
            "time":20.0,
            "date":"2022-02-28"
        },{
            "result":"true",
            "time":3.2,
            "date":"2022-03-12"
        },],
        "SFA":[{
            "reaction":[{
                "relationship":"属于",
                "feature":"交通工具",
            },{
                "relationship":"能够",
                "feature":"驾驶",
            },],
            "date":"2022-02-28"
        },{
            "reaction":[{
                "relationship":"属于",
                "feature":"交通工具",
            },{
                "relationship":"能够",
                "feature":"驾驶",
            },],
            "date":"2022-02-28"
        }
        ]
    }
    return node_record



@app.route("/planGraph",methods=['GET','POST'])
# @cross_origin(origin='*',headers=['Access-Control-Allow-Origin','Content-Type','Authorization'])
def Plan_Graph():

    plan_graph = {
        "nodes": [{
            "subcategory": "工具",
            "maincategory": "人造物",
            "id": "钢笔"
        }, {
            "subcategory": "工具",
            "maincategory": "人造物",
            "id": "画笔"
        }, {
            "subcategory": "工具",
            "maincategory": "人造物",
            "id": "画纸"
        }, {
            "subcategory": "工具",
            "maincategory": "人造物",
            "id": "记号笔"
        }, {
            "subcategory": "工具",
            "maincategory": "人造物",
            "id": "蜡笔"
        }, {
            "subcategory": "身体部位",
            "maincategory": "身体部位",
            "id": "手"
        }, {
            "subcategory": "身体部位",
            "maincategory": "身体部位",
            "id": "手臂"
        }, {
            "subcategory": "身体部位",
            "maincategory": "身体部位",
            "id": "手掌"
        }, {
            "subcategory": "身体部位",
            "maincategory": "身体部位",
            "id": "手指"
        }, {
            "subcategory": "身体部位",
            "maincategory": "身体部位",
            "id": "臀部"
        }],
        "edges": [{
            "weight": 1.0,
            "source": "钢笔",
            "target": "钢笔"
        }, {
            "weight": 0.833563665,
            "source": "钢笔",
            "target": "画笔"
        }, {
            "weight": 0.729334454,
            "source": "钢笔",
            "target": "画纸"
        }, {
            "weight": 0.806783151,
            "source": "钢笔",
            "target": "记号笔"
        }, {
            "weight": 0.789160661,
            "source": "钢笔",
            "target": "蜡笔"
        }, {
            "weight": 0.461681547,
            "source": "钢笔",
            "target": "手"
        }, {
            "weight": 0.522326804,
            "source": "钢笔",
            "target": "手臂"
        }, {
            "weight": 0.452785838,
            "source": "钢笔",
            "target": "手掌"
        }, {
            "weight": 0.503370717,
            "source": "钢笔",
            "target": "手指"
        }, {
            "weight": 1.0,
            "source": "画笔",
            "target": "画笔"
        }, {
            "weight": 0.824119591,
            "source": "画笔",
            "target": "画纸"
        }, {
            "weight": 0.904647908,
            "source": "画笔",
            "target": "记号笔"
        }, {
            "weight": 0.868122534,
            "source": "画笔",
            "target": "蜡笔"
        }, {
            "weight": 0.524525185,
            "source": "画笔",
            "target": "手"
        }, {
            "weight": 0.594872923,
            "source": "画笔",
            "target": "手臂"
        }, {
            "weight": 0.513030702,
            "source": "画笔",
            "target": "手掌"
        }, {
            "weight": 0.577260057,
            "source": "画笔",
            "target": "手指"
        }, {
            "weight": 1.0,
            "source": "画纸",
            "target": "画纸"
        }, {
            "weight": 0.740142568,
            "source": "画纸",
            "target": "记号笔"
        }, {
            "weight": 0.913701008,
            "source": "画纸",
            "target": "蜡笔"
        }, {
            "weight": 0.540371419,
            "source": "画纸",
            "target": "手"
        }, {
            "weight": 0.577401642,
            "source": "画纸",
            "target": "手臂"
        }, {
            "weight": 0.532365153,
            "source": "画纸",
            "target": "手掌"
        }, {
            "weight": 0.571582634,
            "source": "画纸",
            "target": "手指"
        }, {
            "weight": 1.0,
            "source": "记号笔",
            "target": "记号笔"
        }, {
            "weight": 0.806684534,
            "source": "记号笔",
            "target": "蜡笔"
        }, {
            "weight": 0.460387208,
            "source": "记号笔",
            "target": "手"
        }, {
            "weight": 0.499090958,
            "source": "记号笔",
            "target": "手臂"
        }, {
            "weight": 0.453705377,
            "source": "记号笔",
            "target": "手掌"
        }, {
            "weight": 0.500626342,
            "source": "记号笔",
            "target": "手指"
        }, {
            "weight": 1.0,
            "source": "蜡笔",
            "target": "蜡笔"
        }, {
            "weight": 0.563729515,
            "source": "蜡笔",
            "target": "手"
        }, {
            "weight": 0.605572089,
            "source": "蜡笔",
            "target": "手臂"
        }, {
            "weight": 0.555566419,
            "source": "蜡笔",
            "target": "手掌"
        }, {
            "weight": 0.600878023,
            "source": "蜡笔",
            "target": "手指"
        }, {
            "weight": 1.0,
            "source": "手",
            "target": "手"
        }, {
            "weight": 0.852983229,
            "source": "手",
            "target": "手臂"
        }, {
            "weight": 0.864065397,
            "source": "手",
            "target": "手掌"
        }, {
            "weight": 0.887756355,
            "source": "手",
            "target": "手指"
        }, {
            "weight": 0.585001422,
            "source": "手",
            "target": "臀部"
        }, {
            "weight": 1.0,
            "source": "手臂",
            "target": "手臂"
        }, {
            "weight": 0.883878504,
            "source": "手臂",
            "target": "手掌"
        }, {
            "weight": 0.916958628,
            "source": "手臂",
            "target": "手指"
        }, {
            "weight": 0.684903322,
            "source": "手臂",
            "target": "臀部"
        }, {
            "weight": 1.0,
            "source": "手掌",
            "target": "手掌"
        }, {
            "weight": 0.804232548,
            "source": "手掌",
            "target": "手指"
        }, {
            "weight": 0.625284889,
            "source": "手掌",
            "target": "臀部"
        }, {
            "weight": 1.0,
            "source": "手指",
            "target": "手指"
        }, {
            "weight": 0.625265234,
            "source": "手指",
            "target": "臀部"
        }, {
            "weight": 1.0,
            "source": "臀部",
            "target": "臀部"
        }]
    }

    return 1


@app.route("/nodeInfo/<concept>",methods=['GET','POST'])
# @cross_origin(origin='*',headers=['Access-Control-Allow-Origin','Content-Type','Authorization'])
def Node_Info(concept):
    node_info={
        "id":"摩托车",
        "maincategory":"交通工具",
        "subcategory":"车辆",
        "features": {
            "范畴": ["车", "船", "飞机"],
            "用途": ["行驶", "乘坐", "开", "骑"],
            "动作": ["司机", "维护", "修理", "加油"],
            "属性": ["方向盘", "车身", "车厢", "仪表盘"],
            "场所": [],
            "联想": ["房屋", "货车", "轿车", "电动车"]
        }
    }
    return node_info

@app.route("/edgeInfo/<parameters>",methods=['GET','POST'])
# @cross_origin(origin='*',headers=['Access-Control-Allow-Origin','Content-Type','Authorization'])
def Edge_Info(parameters):
    edge_info={
        "source":"画笔",
        "target":"手臂",
        "shared_features": {
            "范畴": ["车", "船", "飞机"],
            "用途": ["行驶", "乘坐", "开", "骑"],
            "动作": ["司机", "维护", "修理", "加油"],
            "属性": ["方向盘", "车身", "车厢", "仪表盘"],
            "场所": [],
            "联想": ["房屋", "货车", "轿车", "电动车"]
        }
    }
    return edge_info


if __name__ == '__main__':
    app.run()