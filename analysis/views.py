from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from analysis.tool.cal_tm import cal


# Create your views here.

class AnalysisView(View):

    def get(self, request):
        # return HttpResponse("get")
        return render(request, 'result.html')

    def post(self, request):
        return HttpResponse('post')


class HomeView(View):
    def get(self, request):
        # return HttpResponse("get")
        return render(request, 'test.html')

    def post(self, request):
        data = request.POST
        gene = data.get('gene_input')
        context = {
            'gene': gene,
        }
        # print(gene)
        # d1, d2 = cal(gene)
        # print(d1)
        # print(d2)
        # context = dict(d1.items() + context.items())
        # return JsonResponse(context)

        return render(request, 'result.html', context)
