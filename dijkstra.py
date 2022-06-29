import json
import backend
import database
import pandas as pd
import numpy as np
# 生成点对之间的权重图
def generateCostMap(similarity_df):
    cost_map_list= []

    for i in range(similarity_df.shape[0]):
        value_list = similarity_df[str(i)].tolist()
        for j in range(len(value_list)):
            if value_list[j] == 1:
                value_list[j] = 0
            elif value_list[j] == 0:
                value_list[j] = 100000
            else:
                value_list[j] = pow((1 - value_list[j]) * 10, 5)  # 我需要想一个拉伸的好方法！！！
        cost_map_list.append(value_list)
    return cost_map_list

# dijkstra寻路算法
# mgraph = cost_map_list
def dijkstra(end,mgraph):
    # 存储已知最小长度的节点编号 即是顺序
    passed = [end]
    nopass = [x for x in range(len(mgraph)) if x != end]
    dis = mgraph[end]
    # 创建字典 为直接与end节点相邻的节点初始化路径
    all_path_list = []
    for i in range(len(dis)):
        if dis[i] != np.inf:
            all_path_list.append([end])
    while len(nopass):
        idx = nopass[0]
        for i in nopass:
            if dis[i] < dis[idx]: idx = i
        nopass.remove(idx)
        passed.append(idx)
        for i in nopass:
            if dis[idx] + mgraph[idx][i] < dis[i]:
                dis[i] = dis[idx] + mgraph[idx][i]
                all_path_list[i] = all_path_list[i] + [idx]
    # dis=end2all_distance_list 1dim
    return dis, all_path_list

# 找到end的最好起始点与路径
def findBestStartAndPath(start_list,end2all_distance_list,end2all_path_list):
    best_idx = start_list[0]
    for i in range(len(start_list)):
        start_idx = start_list[i]
        if end2all_distance_list[start_idx] < end2all_distance_list[best_idx]:best_idx = start_idx
    path_list=end2all_path_list[best_idx]
    path_list.append(best_idx)
    return path_list

# 为每个end寻找到最好的路径
def getAllPath(start_list,end_list,cost_map_list):
    all_path_list = []
    for i in range(len(end_list)):
        end2all_distance_list, end2all_path_list = dijkstra(end_list[i],cost_map_list)
        path_list = findBestStartAndPath(start_list,end2all_distance_list,end2all_path_list)
        all_path_list.append(path_list)
    return all_path_list

# 获得所需的所有点的序号
def getAllNodeIndex(all_path_list):
    all_node_list = []
    for i in range(len(all_path_list)):
        for j in range(len(all_path_list[i])):
            if all_path_list[i][j] not in all_node_list:
                all_node_list.append(all_path_list[i][j])
    return all_node_list

# 获得所有点序号对应的词
def getAllConcepts(all_node_list,concept_df):
    word_list = concept_df["Id"].tolist()
    all_concept_list = []
    for i in range(len(all_node_list)):
        node_index = all_node_list[i]
        all_concept_list.append(word_list[node_index])
    return all_concept_list

# 获取患者已知词汇的序号
def getStartList(start_word_df,concept_df):
    start_word_list = start_word_df["concept"].tolist()
    word_list = concept_df["Id"].tolist()
    start_list = []
    for i in range(len(start_word_list)):
        index = word_list.index(start_word_list[i])
        # print("word list: {}, start list:{}".format(word_list[index],start_word_list[i]))
        start_list.append(index)
    return start_list
def getStartListByDB(user_id):
    uct_list = database.userConceptTest.query.filter_by(user_id=user_id,state=True).all()
    start_list = []
    for i in range(len(uct_list)):
        temp = uct_list[i]
        start_list.append(temp.concept_id)
    return start_list

# 获取目标词汇
def getEndList(start_word_df,end_count_dict,laplace_path,word_en_list,concept_df):
    start_word_list = start_word_df["concept"].tolist()
    word_list = concept_df["Id"].tolist()
    end_word_list = []
    for i in range(len(end_count_dict)):
        this_laplace_path = laplace_path + "/" + word_en_list[i] +".csv"
        laplace_count_df = pd.read_csv(this_laplace_path)
        laplace_count_list = laplace_count_df["concept"].tolist()
        count = int(end_count_dict[word_en_list[i]])
        j = 0
        for h in range(len(laplace_count_list)):
            if j<count and laplace_count_list[h] not in start_word_list:
                end_word_list.append(laplace_count_list[h])
                j+=1
    end_list = []
    # print(end_word_list)
    for k in range(len(end_word_list)):
        index = word_list.index(end_word_list[k])
        end_list.append(index)
    # print(end_list,len(end_list))
    return end_list

# 前端需求的返回格式
def getJsonResult(concept_df,all_path_list):
    '''
    返回样例
    result_dict = {
        "nodes":[{
            "id": "钢笔"
        }],
        "edges":[{
            "source": "钢笔",
            "target": "钢笔"
        }]
    }
    '''
    all_node_list = getAllNodeIndex(all_path_list)
    plan_a = {
        "plans":[]
    }
    result_dict = {
        "type": "subgraph",
        "title": "训练路径 1",
        "checked": "false",
        "nodes":[],
        "edges":[]
    }
    for i in range(len(all_node_list)):
        node_dict={}
        temp_list = concept_df.iloc[all_node_list[i],:]
        # node_dict["subcategory"]=temp_list[-3]
        # node_dict["maincategory"]=temp_list[-5]
        node_dict["id"]=temp_list[0]
        result_dict["nodes"].append(node_dict)

    for j in range(len(all_path_list)):
        temp_path_list = all_path_list[j]
        for k in range(len(temp_path_list)-1):
            head_index = temp_path_list[k]
            tail_index = temp_path_list[k+1]
            head_word = concept_df.iloc[head_index,0]
            tail_word = concept_df.iloc[tail_index,0]
            # weight = similarity_df.iloc[head_index,tail_index]
            edge_dict = {}
            # edge_dict["weight"]=weight
            edge_dict["source"]=head_word
            edge_dict["target"]=tail_word
            result_dict["edges"].append(edge_dict)
    plan_a["plans"].append(result_dict)
    # result_json = json.dumps(plan_a,ensure_ascii=False)
    return plan_a



def dijkstraFindWay(user_id,start_filepath,similarity_filepath,concept_filepath,end_count_dict,laplace_path,word_en_list):
    start_word_df = pd.read_csv(start_filepath)
    concept_df = pd.read_csv(concept_filepath)
    similarity_df = pd.read_csv(similarity_filepath)
    # start_list = getStartList(start_word_df,concept_df)R
    start_list = getStartListByDB(user_id)
    end_list = getEndList(start_word_df,end_count_dict,laplace_path,word_en_list,concept_df)
    cost_map_list = generateCostMap(similarity_df)
    all_path_list = getAllPath(start_list,end_list,cost_map_list)
    # print(all_path_list)
    # all_node_list = getAllNodeIndex(all_path_list)
    # print(all_node_list)
    # all_concept_list = getAllConcepts(all_node_list,concept_df)
    plan_a = getJsonResult(concept_df, all_path_list)
    return plan_a

if __name__ == "__main__":
    user_id = 1
    similarity_filepath = "../database/similarity/concept_simi_norm.csv"
    concept_filepath = "../database/CCFD_concept_info.csv"
    start_filepath = "../database/start_words.csv"
    word_en_list = ["artificial_object", "transportation", "animal", "plant", "food", "nature_object", "bodypart"]
    word_cn_list = ["","","","","","",""]
    laplace_path = "../database/laplace"
    end_count_dict = {
        "artificial_object": "3",
        "transportation": "4",
        "animal": "0",
        "plant": "2",
        "food": "3",
        "nature_object": "4",
        "bodypart": "2",
    }
    # print(end_count_dict[word_en_list[1]])
    # start_list = [877, 123, 4, 16]
    # end_list = [191, 79, 52]
    plan_a = dijkstraFindWay(user_id,start_filepath,similarity_filepath,concept_filepath,end_count_dict,laplace_path,word_en_list)
    print(plan_a)