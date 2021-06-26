from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View

from analysis.tool.analysis import analysis_all, analysis_two, analysis_three
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

        d1, d2, len1 = cal(gene)
        # analysis_two(d1, d2, len1)
        analysis_three(d1, d2, len1)

        context = {
            'gene_len': len(gene),
            'gene': gene,
            'd1': d1,
            'lend1':len(d1),
            'd2': d2,
        }

        return render(request, 'result.html', context)
