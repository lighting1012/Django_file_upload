import text_similarity.cosine_similarity as aaa

f = open('text_similarity/received_files/test_3.txt')
sample_text = f.read()
f.close()
result_list = aaa.main(sample_text, 'text_similarity/test.db')
print(sample_text)
print(result_list)
