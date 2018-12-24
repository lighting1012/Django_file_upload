from django.shortcuts import render
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
        result_title = []
        for element in result_list:
            result_title.append([element[1],element[2],element[3]])
        context = {"result_title": result_title}
        return render(request, "result.html", context)


def detail(request):
    return render(request, "detail.html")
