from django.shortcuts import render
from django.shortcuts import HttpResponse
import text_similarity.cosine_similarity as cosine
import os


def upload(request):
    if request.method == 'GET':
        return render(request, 'upload.html')
    elif request.method == 'POST':
        obj = request.FILES.get('fafafa')
        f = open(os.path.join('text_similarity/received_files', obj.name), 'wb')
        for line in obj.chunks():
            f.write(line)
        f.close()
        f = open(os.path.join('text_similarity/received_files', obj.name))
        sample_text = f.read()
        f.close()
        result_list = cosine.main(sample_text, 'text_similarity/test.db')
        result_string = ''
        for element in result_list:
            result_string += element[1]
            result_string += element[2]
            result_string += '\n相似度：\n'
            result_string += element[3]
        return HttpResponse(result_string)

        # return render(request,"")