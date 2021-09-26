import numpy as np
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View

from analysis.tool.analysis import Analysis
# from analysis.tool.cal_tm import cal


# Create your views here.
from analysis.tool.splicing import Splicing


class DownloadView(View):     # 导出excel数据
    def get(self, request):
        print("test success")
        return HttpResponse("get")


# class AnalysisView(View):
#
#     def get(self, request):
#         # return HttpResponse("get")
#         return render(request, 'result.html')
#
#     def post(self, request):
#         return HttpResponse('post')


class HomeView(View):
    def get(self, request):
        # return HttpResponse("get")
        return render(request, 'test.html')

    def post(self, request):
        data = request.POST
        tem_gene = data.get('gene_input').replace('\n', '').replace(' ', '').replace('\r', '')
        input_info = {
            'gene': tem_gene,  # 输入基因序列
            'res_type': data.get('res_type'),  # 结果：gepless?gap
            'result':data.get('result'),
            'min_len':data.get('min_len'),
            'max_len':data.get('max_len'),
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
        # list_g1, list_g2, len1, info = splic.cal()
        next_cal, info = splic.cal()

        context = {
            'gene_len': len(input_info['gene']),  # 输入的序列长度
            'gene': input_info['gene'],  # 输入的序列
            'res_type': input_info['res_type'],  # 输入的序列
            'info': info.get('result'),
            'min': info.get('min'),
            'max': info.get('max'),
            'range': info.get('range'),
            'mean': info.get('mean'),
            'std': info.get('std')
        }
        if info.get('tail'):
            context['tail'] = info.get('tail')

        if data.get('veri') == 'yes':
            # 分析过程
            analy = Analysis(next_cal[0], next_cal[1][1:], next_cal[2])
            # info = analy.get_more_info()
            analy_info_two = analy.analysis_two()
            analy_info_three = analy.analysis_three()
            context['analy_info_two'] = analy_info_two
            context['analy_info_three'] = analy_info_three

        return render(request, 'result.html', context)

