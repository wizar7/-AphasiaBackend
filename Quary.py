from flask import Flask, json, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from numpy import *

app = Flask(__name__)
# 协议：mysql+pymysql
# 用户名：root
# 密码：xuweijian
# IP地址：localhost
# 端口：3306
# 数据库名：aphasia
app.config['SECRET_KEY'] = 'xuweijian'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:xuweijian@localhost:3306/aphasia'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

# 表的各种class
class user(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(20), nullable=False)
    password = db.Column(db.VARCHAR(20), nullable=False)


class upperCategory(db.Model):
    __tablename__ = 'upperCategory'
    id = db.Column(db.Integer, primary_key=True)
    upper_cat = db.Column(db.VARCHAR(20), nullable=False)


class subCategory(db.Model):
    __tablename__ = 'subCategory'
    id = db.Column(db.Integer, primary_key=True)
    sub_cat = db.Column(db.VARCHAR(20), nullable=False)
    upper_cat_id = db.Column(db.Integer, db.ForeignKey('upperCategory.id'), nullable=False)


class concept(db.Model):
    __tablename__ = 'concept'
    id = db.Column(db.Integer, primary_key=True)
    concept = db.Column(db.VARCHAR(20), nullable=False)
    importance = db.Column(db.Float, nullable=False)
    sub_cat_id = db.Column(db.Integer, db.ForeignKey('subCategory.id'), nullable=False)
    upper_cat_id = db.Column(db.Integer, db.ForeignKey('upperCategory.id'), nullable=False)


class relation(db.Model):
    __tablename__ = 'relation'
    id = db.Column(db.Integer, primary_key=True)
    relation = db.Column(db.VARCHAR(20), nullable=False)


class bigram(db.Model):
    __tablename__ = 'bigram'
    id = db.Column(db.Integer, primary_key=True)
    concept_id = db.Column(db.Integer, db.ForeignKey('concept.id'), nullable=False)
    relation_id = db.Column(db.Integer, db.ForeignKey('relation.id'), nullable=False)


class conceptSimilarity(db.Model):
    __tablename__ = 'conceptSimilarity'
    id = db.Column(db.Integer, primary_key=True)
    concept_1_id = db.Column(db.Integer, db.ForeignKey('concept.id'), nullable=False)
    concept_2_id = db.Column(db.Integer, db.ForeignKey('concept.id'), nullable=False)
    similarity = db.Column(db.Float, nullable=False)


class userConceptTest(db.Model):
    __tablename__ = 'userConceptTest'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    concept_id = db.Column(db.Integer, db.ForeignKey('concept.id'), nullable=False)
    state = db.Column(db.Integer, nullable=False)
    createDate = db.Column(db.DATE, nullable=False)
    time = db.Column(db.Integer, nullable=False)


class userConceptLearn(db.Model):
    __tablename__ = 'userConceptLearn'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    concept_id = db.Column(db.Integer, db.ForeignKey('concept.id'), nullable=False)
    state = db.Column(db.Integer, nullable=False)
    createDate = db.Column(db.DATE, nullable=False)
    time = db.Column(db.Integer, nullable=True)


class userBigram(db.Model):
    __tablename__ = 'userBigram'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bigram_id = db.Column(db.Integer, db.ForeignKey('bigram.id'), nullable=False)
    state = db.Column(db.BOOLEAN, nullable=False)
    createDate = db.Column(db.DATE, nullable=False)
    answer = db.Column(db.VARCHAR(20), nullable=False)


'''def to_json(obj):#返回 json 格式数据，首先定义处理模型对象的函数
    _dict = vars(obj)
    for i in list(_dict.keys()):
    if i.startswith('_'):
    _dict.pop(i)
    return _dict'''

# 开始查询

def addConceptTest(record):
    #record = {'user_name': '张三', 'name': '自行车', 'result': 4, 'createDate': '2022-6-5', 'time': 10}
    #user表查询user-id, concept表查询concept_id
    user_id=db.session.query(user.id).filter(user.name == record['user_name']).all()
    print('user_id:',user_id[0][0])
    concept_id=db.session.query(concept.id).filter(concept.concept == record['name']).all()
    print('concept_id:', concept_id[0][0])
    uct = userConceptTest(user_id=user_id[0][0], concept_id=concept_id[0][0], state=record['result'],
                          createDate=record['createDate'], time=record['time'])
    db.session.add(uct)
    db.session.commit()
    return 'Storing is completed!'

def addTherapyResult(record):
    record = {'user_name': '张三', 'name': '自行车', 'result': 1, 'createDate': '2022-6-5',
              'reaction': [{"relationship": "属于","feature": "交通工具"},{"relationship": "用于","feature": "驾驶"}]}
    #user表查询user-id, concept表查询concept_id
    user_id=db.session.query(user.id).filter(user.name == record['user_name']).all()
    print('user_id:',user_id[0][0])
    concept_id=db.session.query(concept.id).filter(concept.concept == record['name']).all()
    print('concept_id:', concept_id[0][0])

    #写入userConceptLearn
    uct = userConceptLearn(user_id=user_id[0][0], concept_id=concept_id[0][0],
                           state=record['result'], createDate=record['createDate'], time=0)
    db.session.add(uct)
    db.session.commit()

    # 写入userBigram
    for reaction in record['reaction']:
        #print('reaction is :',reaction)
        relation_id= db.session.query(relation.id).filter(relation.relation == reaction['relationship']).all()
        #print('relation_id:',relation_id[0][0],concept_id[0][0])
        bigram_id = db.session.query(bigram.id).filter(bigram.relation_id == relation_id[0][0], bigram.concept_id == concept_id[0][0]).all()
        #print('bigram_id:',bigram_id)
        uct = userBigram(user_id=user_id[0][0],bigram_id=bigram_id[0][0], state=relation_id[0][0],
                     answer=reaction['feature'], createDate=record['createDate'])
        db.session.add(uct)
        db.session.commit()
    return 'Storing is completed!'

def getFullRecord(userid):
    #userid = 1  # 筛选条件：userid确定登录身份，需要和前端GET配合
    # 查询Picturenaming
    therapyTest = db.session.query(userConceptTest.user_id, concept.concept, userConceptTest.createDate,
                                   userConceptTest.state, userConceptTest.time, concept.id) \
        .join(concept, concept.id == userConceptTest.concept_id, isouter=True) \
        .filter(userConceptTest.user_id == userid) \
        .all()
    therapyLearn = db.session.query(userConceptLearn.user_id, concept.concept, userConceptLearn.createDate,
                                    userConceptLearn.state, userConceptLearn.time, concept.id) \
        .join(concept, concept.id == userConceptLearn.concept_id, isouter=True) \
        .filter(userConceptLearn.user_id == userid) \
        .all()
    # print(therapyLearn)
    pictureNaming = {}  # 字典型数据
    for record in therapyLearn:  # 取到数组中的每一项
        # print(record)
        current = pictureNaming.get(record[1], [])  # 取到learn[1]即"自行车"，返回一个数组
        current.append({'result': record[3],
                        'time': record[4],
                        'date': record[2].__format__('%Y-%m-%d')
                        })
    pictureNaming[record[1]] = current
    for record in therapyTest:
        # print(record)
        current = pictureNaming.get(record[1], [])
        current.append({
            'result': record[3],
            'time': record[4],
            'date': record[2].__format__('%Y-%m-%d')
        })
        pictureNaming[record[1]] = current

    # 查询SFA
    therapySFA = db.session.query(userBigram.user_id, concept.concept, userBigram.answer, userBigram.createDate,
                                  relation.relation) \
        .join(bigram, userBigram.bigram_id == bigram.id) \
        .join(concept, bigram.concept_id == concept.id) \
        .join(relation, bigram.relation_id == relation.id) \
        .filter(userBigram.user_id == userid) \
        .all()
    print('therapySFA', therapySFA)

    SFA = {}  # 字典型数据
    for record in therapySFA:  # record是list
        # print(record)
        current1 = SFA.get(record[1], [])
        current1.append({'reaction': {'relationship': record[4], 'feature': record[2]},
                         'date': record[3].__format__('%Y-%m-%d')
                         })
        SFA[record[1]] = current1
    print('SFA记录：', SFA)

    # 开始合成Picturenaming和SFA
    fullRecord = []
    for record in SFA:
        # print(record)
        fullRecord.append({'id': record,
                              'PictureNaming': [],
                              'SFA': SFA[record]
                              })
    # print(therapyRecord)
    for record in pictureNaming:
        # print(record)
        if record not in SFA.keys():  # 这个id在SFA中没出现过
            fullRecord.append({'id': record,
                                  'PictureNaming': pictureNaming[record],
                                  'SFA': []
                                  })
        else:  # 这个id在SFA中出现过
            for i in fullRecord:
                if fullRecord[i]['id'] == record:
                    fullRecord[i]['PictureNaming'] = pictureNaming[record]
    print('结果是：', fullRecord)

    # test
    # print('pictureNaming:',pictureNaming.keys())
    # print('SFA:',SFA.keys())
    print("测试的结果是：")
    for item in fullRecord:
        if item['id'] == '安全带':
            print(item['SFA'])

    # print(json.dumps(therapyRecord))
    return fullRecord

def getExperimentMangement(userid):
    userid=1 #筛选条件：userid确定登录身份，需要和前端GET配合
    # 查询SFA
    therapySFA = db.session.query(userBigram.user_id,func.count(concept.concept),userBigram.createDate)\
        .join(bigram, userBigram.bigram_id==bigram.id)\
        .join(concept,bigram.concept_id==concept.id)\
        .filter(userBigram.user_id==userid)\
        .group_by(userBigram.createDate)\
        .all()
    print('therapySFA结果是:',therapySFA)

    SFA = {"current": 1,"PN_ImageAmount": 120,"SFAData":[]} # 字典型数据
    for record in therapySFA:
        #print(record)
        SFA["SFAData"].append({
            'date':record[2].__format__('%Y-%m-%d'),
            'dose': record[1]
        })
    print('SFA记录：',SFA)
    return SFA


if __name__ == "__main__":
    user_id = 1
    testRecord = {'user_name': '张三', 'name': '自行车', 'result': 4, 'createDate': '2022-6-5', 'time': 10}
    therapyRecord = {'user_name': '张三', 'name': '自行车', 'result': 4, 'createDate': '2022-6-5',
              'reaction': [{"relationship": "属于", "feature": "交通工具"}, {"relationship": "用于", "feature": "驾驶"}]}
    #getFullRecord(user_id)
    #getExperimentMangement(userid)
    #addConceptTest(testRecord)
    addTherapyResult(therapyRecord)

