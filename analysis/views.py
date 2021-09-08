import numpy as np
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
        # gene = data.get('gene_input')
        # print(data.get('res_type'))
        input_info = {
            'gene': data.get('gene_input'),  # 输入基因序列
            'res_type': data.get('res_type'),  # 结果：gepless?gap

            # 各种离子浓度
            'Na': float(data.get('Na')),
            'K': float(data.get('K')),
            'Mg': float(data.get('Mg')),
            'dNTPs': float(data.get('dNTPs')),
            'Tris': float(data.get('Tris')),
            'oligo': float(data.get('oligo')),
            'primer': float(data.get('primer')),
        }

        splic = Splicing(input_info)
        list_g1, list_g2, len1, info = splic.cal()

        # 分析过程
        # analy = Analysis(list_g1, list_g2, len1)
        # info = analy.get_more_info()
        # analy.analysis_two()
        # analy.analysis_three()

        context = {
            'gene_len': len(input_info['gene']),  # 输入的序列长度
            'gene': input_info['gene'],  # 输入的序列
            'info': info.get('result'),
            'min': info.get('min'),
            'max': info.get('max'),
            'range': info.get('range'),
            'mean': info.get('mean'),
            'std': info.get('std'),
            'result_type': data.get('res_type')  # 结果：gepless?gap
        }

        return render(request, 'result.html', context)
