from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View

from analysis.tool.analysis import Analysis
# from analysis.tool.cal_tm import cal


# Create your views here.
from analysis.tool.splicing import Splicing


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

        splic = Splicing(gene)
        list_g1, list_g2, len1 = splic.cal()
        # list_g1, list_g2, len1 = cal(gene)
        # analysis_two(list_g1, list_g2, len1)
        # analysis_three(list_g1, list_g2, len1)
        analy = Analysis(list_g1, list_g2, len1)
        analy.analysis_two()
        # analy.analysis_three()

        context = {
            'gene_len': len(gene),
            'gene': gene,
            'list_g1': list_g1,
            'lend1':len(list_g1),
            'list_g2': list_g2,
        }

        return render(request, 'result.html', context)
