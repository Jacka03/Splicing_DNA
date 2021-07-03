
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
        input_info = {
            'temp': data.get('temperature'),
            'Na': data.get('Na'),
            'K': data.get('K'),
            'Mg': data.get('Mg'),
            'Mon': data.get('Mon'),
            'dNTPs': data.get('dNTPs'),
            'Tris': data.get('Tris'),
            't': data.get('t'),
        }

        splic = Splicing(gene, input_info)
        list_g1, list_g2, len1 = splic.cal()

        analy = Analysis(list_g1, list_g2, len1)
        info = analy.get_more_info()
        analy.analysis_two()
        analy.analysis_three()

        context = {
            'gene_len': len(gene),  # 输入的序列长度
            'gene': gene,  # 输入的序列
            'info': info,

        }

        return render(request, 'result.html', context)
