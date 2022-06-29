import pandas as pd
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime

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
    state = db.Column(db.BOOLEAN, nullable=False)
    createDate = db.Column(db.DATE, nullable=False)
    time = db.Column(db.Integer, nullable=False)

class userConceptLearn(db.Model):
    __tablename__ = 'userConceptLearn'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    concept_id = db.Column(db.Integer, db.ForeignKey('concept.id'), nullable=False)
    state = db.Column(db.BOOLEAN, nullable=False)
    createDate=db.Column(db.DATE,nullable=False)
    time = db.Column(db.Integer, nullable=True)

class userBigram(db.Model):
    __tablename__ = 'userBigram'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bigram_id = db.Column(db.Integer, db.ForeignKey('bigram.id'), nullable=False)
    state = db.Column(db.BOOLEAN, nullable=False)
    createDate=db.Column(db.DATE,nullable=False)
    answer =db.Column(db.VARCHAR(20), nullable=False)

# 处理csv
concept_info_df = pd.read_csv("data/CCFD_concept_info.csv")
# upper_cat_list = list(set(concept_info_df["上级类别"]))
sub_cat_df = pd.read_csv("datasetCSV/subCat.csv")
concept_df = pd.read_csv("datasetCSV/concept.csv")
relation_df = pd.read_csv("datasetCSV/relation.csv")
bigram_df = pd.read_csv("datasetCSV/bigram.csv")
concept_simi_df = pd.read_csv("datasetCSV/conceptSimilarity.csv")
userConceptTest_df = pd.read_csv("datasetCSV/userConceptTest.csv")
userConceptLearn_df = pd.read_csv("datasetCSV/userConceptLearn.csv")
userBigram_df=pd.read_csv("datasetCSV/userBigram.csv")
print(userBigram_df)
# 数据导入
def addUserBigram():
    for i in range(userBigram_df.shape[0]):
        temp = userBigram_df.iloc[i, :]
        t = datetime.strptime(temp[4],"%Y-%m-%d")
        t = datetime.date(t)
        uct = userBigram(user_id=temp[1], bigram_id=temp[2], state=temp[3], createDate=t, answer=temp[5])
        db.session.add(uct)
        db.session.commit()

def addUserConceptLearn():
    for i in range(userConceptLearn_df.shape[0]):
        temp = userConceptTest_df.iloc[i, :]
        t = datetime.strptime(temp[4],"%Y-%m-%d")
        t = datetime.date(t)
        uco = userConceptLearn(user_id=temp[1], concept_id=temp[2], state=temp[3], createDate=t, time=temp[5])
        db.session.add(uco)
        db.session.commit()

def addUserConceptTest():
    for i in range(userConceptTest_df.shape[0]):
        temp = userConceptTest_df.iloc[i, :]
        t = datetime.strptime(temp[4],"%Y-%m-%d")
        t = datetime.date(t)
        uct = userConceptTest(user_id=temp[1], concept_id=temp[2], state=temp[3], createDate=t, time=temp[5])
        db.session.add(uct)
        db.session.commit()


def addConceptSimi():
    for i in range(concept_simi_df.shape[0]):
        temp = concept_simi_df.iloc[i, :]
        cs = conceptSimilarity(id=temp[0], concept_1_id=temp[1], concept_2_id=temp[2], similarity=temp[3])
        db.session.add(cs)
        db.session.commit()


def addBigram():
    for i in range(bigram_df.shape[0]):
        temp = bigram_df.iloc[i, :]
        bigram1 = bigram(id=temp[0], concept_id=temp[1], relation_id=temp[2])
        db.session.add(bigram1)
        db.session.commit()


def addRelation():
    for i in range(relation_df.shape[0]):
        temp = relation_df.iloc[i, :]
        relation1 = relation(id=temp[0], relation=temp[1])
        db.session.add(relation1)
        db.session.commit()


def addConcept():
    for i in range(concept_df.shape[0]):
        temp = concept_df.iloc[i, :]
        concept1 = concept(id=temp[0], concept=temp[1], importance=temp[2], sub_cat_id=temp[3], upper_cat_id=temp[4])
        db.session.add(concept1)
        db.session.commit()


def addSubCategory():
    for i in range(sub_cat_df.shape[0]):
        temp = sub_cat_df.iloc[i, :]
        sub_cat = subCategory(id=temp[0], sub_cat=temp[1], upper_cat_id=temp[2])
        db.session.add(sub_cat)
        db.session.commit()


upper_cat_list = ['动物', '交通工具', '自然物', '食物', '人造物', '身体部位', '植物']
# 为避开addUpperCategory()读入list的时候，id号每次有所变化，这里直接使用变量list

def addUpperCategory():  #
    for i in range(len(upper_cat_list)):
        # print(upper_cat_list[i])
        upper_cat = upperCategory(id=i, upper_cat=upper_cat_list[i])
        db.session.add(upper_cat)
        db.session.commit()

#以下为数据读写
if __name__ == '__main__':
    #addUserBigram()
    #addUpperCategory()
    #addSubCategory()
    #addConcept()
    addRelation()
    #addBigram()
    #addUserConceptTest()
    #addUserConceptLearn()
    #addConceptSimi()
    print(0)


