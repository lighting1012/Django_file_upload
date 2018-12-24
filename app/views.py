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
        title, text = obj.name, sample_text
        context = {"result_list": result_list, "title": title, "text":text}
        return render(request, "result.html", context)


def detail(request):
    return render(request, "detail.html")
