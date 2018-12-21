# encoding=utf-8
# Compute the consine similarity of two documents
# python 3.6，need install additional module jieba
# Written by Jiaquan Xu

import jieba 	# pip install jieba
import sys
import sqlite3
from math import sqrt


def read_db(db_path, execmd):
	# 从数据库中读取数据，返回一个list
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	conn.row_factory = sqlite3.Row
	c.execute(execmd)
	rows = c.fetchall()
	conn.close()
	return rows


def create_cosine_table(sample_text, db_path):
	# 根据文本创建一个新表（id，余弦相似度）
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	rows = read_db(db_path, "SELECT * FROM recommondation")
	c.execute("DROP TABLE IF EXISTS cosine")
	c.execute("CREATE TABLE cosine (id int primary key, cosine text)")
	for line in rows:
		id = line[0]
		context = line[2]
		cosine_value = cosine(sample_text, context)
		c.execute("INSERT INTO cosine VALUES (?, ?)", [id, cosine_value])
	conn.commit()
	conn.close()


def get_split_text(text):
	# 用jieba模块进行语句分词（精确模式）
	# 输入文本，返回分词结果（List）
	punctuation_set = {'，', '。', '：', '；', '？', '！', '@', '#', '￥',
	'%', '&', '+', '-', '*', '/', '“', '”', '（', '）', '【', '】', '{', '}', '、', ' ', '\n'}
	Result = jieba.cut(text)
	List = []
	for i in Result:
		if i not in punctuation_set:
			List.append(i)
	return List


def frequency_vector(L1, L2):
	# 根据两段文字的分词结果，计算词频，求词频向量
	# L1 = ['我','爱','北京']
	# L2 = ['我','爱','南京']
	# 列出所有词： 我，爱，北京，南京
	# 词频向量：L1 = [1,1,1,0]; L2 = [1,1,0,1]
	v1 = []
	v2 = []
	word_list = list(set(L1+L2))
	for i in word_list:
		v1.append(L1.count(i))
		v2.append(L2.count(i))
	return v1, v2


def _cosine(V1, V2):
	# V1 = [x0,x1,...,xn]
	# V2 = [y0,y1,...,yn]
	# 返回两个n维向量的余弦值
	numerator = 0
	d1 = 0
	d2 = 0
	for i in range(0, len(V1)):
		numerator += V1[i]*V2[i]
		d1 += (V1[i]*V1[i])
		d2 += (V2[i]*V2[i])
	denominator = sqrt(d1) * sqrt(d2)
	return numerator/denominator


def cosine(text1, text2):
	l1 = get_split_text(text1)
	l2 = get_split_text(text2)
	v1, v2 = frequency_vector(l1, l2)
	return _cosine(v1, v2)


def main(sample_text, db_path):
	create_cosine_table(sample_text, db_path)
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute('''SELECT * FROM (
					SELECT recommondation.id, recommondation.title, recommondation.context, cosine.cosine
					FROM recommondation,cosine
					WHERE recommondation.id = cosine.id
					ORDER BY cosine DESC
					) LIMIT 10
		''')
	result = c.fetchall()
	conn.commit()
	conn.close()
	return result


if __name__ == '__main__':
	# 假设received_files文件夹新加进来一个文本
	# 根据内容会建一张新表（id, cosine），记录新内容和数据库里所有内容的的相似度
	f = open(sys.argv[1])
	sample_text = f.read()
	f.close()
	result = main(sample_text, 'test.db')
	print(result)
