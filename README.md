# file_upload
## process overview
1. $: python manage.py runserver  
2. open browser: 'localhost:8000/upload.html'  
3. choose file to upload  
  the file would be saved in file_upload/text_similarity/received_files  
4. once uploaded the file, 10 most similar text in database would be recommended.  
(the database is file_upload/text_similarity/test.db,there have 20 record in database.)

## cosine similarity
1. 文本分词  
	用python jieba库 -- jieba.cut(text)  
		返回一个generator  
	"今天是个好日子" -- ['今天','是','个','好','日子']  
	"明天是个好心情" -- ['明天','是','个','好','心情']  
2. 列出所有词  
	['今天','明天','是','个','好','日子','心情']  
3. 计算词频向量  
	[1,0,1,1,1,1,0]  
	[0,1,1,1,1,0,1]  
4. 求词频向量余弦值  
	cosine =  
             x1*y1+x2*y2+x3*y3+...+xn*yn  
	——————————————————————  
	sqrt(x1^2+x2^2+...+xn^2)*sqrt(y1^2+y2^2+...+yn^2)  

	余弦值越大，相似度越高  
  
