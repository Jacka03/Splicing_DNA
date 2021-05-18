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
        d1, d2 = cal(gene)

        context = {
            'gene': gene,
            'd1': d1,
            'd2': d2,
        }

        return render(request, 'result.html', context)
