from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View

from analysis.tool.analysis import analysis_all
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
        temp = data.get('temperature')
        Na = data.get('Na')

        # var = request.FILES['gene_file']

        # print(temp, Na)

        d1, d2 = cal(gene)
        analysis_all(d1, d2)

        context = {
            'gene_len': len(gene),
            'gene': gene,
            'd1': d1,
            'd2': d2,
        }

        return render(request, 'result.html', context)
