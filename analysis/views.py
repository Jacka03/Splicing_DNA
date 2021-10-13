import json

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


class AssemblyView(View):

    def get_tableData(self, data_list):
        tableData = {}
        for data in data_list:
            tableData[data['name']] = data['data']
        # print(tableData)
        return tableData

    def get(self, request):
        return render(request, 'assembly.html')

    def post(self, request):
        # return JsonResponse({'gene_len': 655, 'gene': 'CGTTTTAAAGGGCCCGCGCGTTGCCGCCCCCTCGGCCCGCCATGCTGCTATCCGTGCCGCTGCTGCTCGGCCTCCTCGGCCTGGCCGTCGCCGAGCCTGCCGTCTACTTCAAGGAGCAGTTTCTGGACGGAGACGGGTGGACTTCCCGCTGGATCGAATCCAAACACAAGTCAGATTTTGGCAAATTCGTTCTCAGTTCCGGCAAGTTCTACGGTGACGAGGAGAAAGATAAAGGTTTGCAGACAAGCCAGGATGCACGCTTTTATGCTCTGTCGGCCAGTTTCGAGCCTTTCAGCAACAAAGGCCAGACGCTGGTGGTGCAGTTCACGGTGAAACATGAGCAGAACATCGACTGTGGGGGCGGCTATGTGAAGCTGTTTCCTAATAGTTTGGACCAGACAGACATGCACGGAGACTCAGAATACAACATCATGTTTGGTCCCGACATCTGTGGCCCTGGCACCAAGAAGGTTCATGTCATCTTCAACTACAAGGGCAAGAACGTGCTGATCAACAAGGACATCCGTTGCAAGGATGATGAGTTTACACACCTGTACACACTGATTGTGCGGCCAGACAACACCTATGAGGTGAAGATTGACAACAGCCAGGTGGAGTCCGGCTCCTTGGAAGACGATTGGGACTTCCTGCCACC', 'res_type': 'Gap', 'info': [['F0', 'CCCGCGCGTTGCCGCCCCCTCGGCCCGCCATGCTGC', 65.86, 19, 36], ['R0', 'CCGAGCAGCAGCGGCACGGATAGCAGCATGGCGGGCCGAGG', 65.93, 19, 41], ['F1', 'CCGTGCCGCTGCTGCTCGGCCTCCTCGGCCTGGCCGTCG', 64.28, 19, 39], ['R1', 'TCCTTGAAGTAGACGGCAGGCTCGGCGACGGCCAGGCCGAGGAG', 65.46, 25, 44], ['F2', 'CCGAGCCTGCCGTCTACTTCAAGGAGCAGTTTCTGGACGGAGACGGGTGGA', 65.39, 25, 51], ['R2', 'TTGTGTTTGGATTCGATCCAGCGGGAAGTCCACCCGTCTCCGTCCAGAAACTG', 65.09, 28, 53], ['F3', 'CTTCCCGCTGGATCGAATCCAAACACAAGTCAGATTTTGGCAAATTCGTTCTCAGTTCCGG', 65.08, 31, 61], ['R3', 'ACCTTTATCTTTCTCCTCGTCACCGTAGAACTTGCCGGAACTGAGAACGAATTTGCCAAAATCTG', 65.64, 34, 65], ['F4', 'CAAGTTCTACGGTGACGAGGAGAAAGATAAAGGTTTGCAGACAAGCCAGGATGCACGCTT', 65.36, 24, 60], ['R4', 'GGCTCGAAACTGGCCGACAGAGCATAAAAGCGTGCATCCTGGCTTGTCTGC', 65.44, 23, 51], ['F5', 'GCTCTGTCGGCCAGTTTCGAGCCTTTCAGCAACAAAGGCCAGACGCTGG', 65.39, 25, 49], ['R5', 'GCTCATGTTTCACCGTGAACTGCACCACCAGCGTCTGGCCTTTGTTGCTGAA', 65.45, 27, 52], ['F6', 'TGGTGCAGTTCACGGTGAAACATGAGCAGAACATCGACTGTGGGGGCGGC', 65.44, 22, 50], ['R6', 'GTCTGGTCCAAACTATTAGGAAACAGCTTCACATAGCCGCCCCCACAGTCGATGTTC', 64.74, 33, 57], ['F7', 'TGTGAAGCTGTTTCCTAATAGTTTGGACCAGACAGACATGCACGGAGACTCAGAATACAACATCA', 65.18, 32, 65], ['R7', 'GGCCACAGATGTCGGGACCAAACATGATGTTGTATTCTGAGTCTCCGTGCATGTCT', 64.43, 24, 56], ['F8', 'TGTTTGGTCCCGACATCTGTGGCCCTGGCACCAAGAAGGTTCATGTCATCTTCA', 64.87, 30, 54], ['R8', 'GTTGATCAGCACGTTCTTGCCCTTGTAGTTGAAGATGACATGAACCTTCTTGGTGCCAG', 65.07, 29, 59], ['F9', 'ACTACAAGGGCAAGAACGTGCTGATCAACAAGGACATCCGTTGCAAGGATGATGAGTTT', 64.37, 30, 59], ['R9', 'CCGCACAATCAGTGTGTACAGGTGTGTAAACTCATCATCCTTGCAACGGATGTCCTT', 64.79, 27, 57], ['F10', 'ACACACCTGTACACACTGATTGTGCGGCCAGACAACACCTATGAGGTGAAGATTGACAAC', 65.4, 33, 60], ['R10', 'GGAGCCGGACTCCACCTGGCTGTTGTCAATCTTCACCTCATAGGTGTTGTCTGG', 65.22, 21, 54], ['F11', 'AGCCAGGTGGAGTCCGGCTCCTTGGAAGACGATTGGGACTTCCTGCCAC', 65.12, 26, 49], ['R11', 'TCACGGTGCCTTAATCTATCTTCAGGAACTGGGTGGCAGGAAGTCCCAATCGTCTTCC', 65.64, 32, 58], ['F12', 'CCAGTTCCTGAAGATAGATTAAGGCACCGTGA', -1, -1, 32], ['F_Primer', 'CCCGCGCGTTGCCGCCC', 66.81, -1, 17], ['R_Primer', 'TCACGGTGCCTTAATCTATCTTCAGGAACTGG', 65.64, -1, 32]], 'resInfo': [{'key': 'min', 'value': 64.28}, {'key': 'max', 'value': 65.93}, {'key': 'range', 'value': 1.65}, {'key': 'mean', 'value': 65.19}, {'key': 'std', 'value': 0.43}], 'tail': 'CAGTTCCTGAAGATAGATTAAGGCACCGTGA'})

        data = json.loads(request.body)
        ion = data.pop('tableData')
        ion = self.get_tableData(ion)
        data.update(ion)
        data['gene'] = data['gene'].replace('\n', '').replace(' ', '').replace('\r', '')
        # print(data)
        splic = Splicing(data)
        # list_g1, list_g2, len1, info = splic.cal()
        next_cal, info = splic.cal()

        # print(next_cal, info)
        res_info = {
            'min': info.get('min'),
            'max': info.get('max'),
            'range': info.get('range'),
            'mean': info.get('mean'),
            'std': info.get('std')
        }
        tem_res = []
        for key, value in res_info.items():
            tem = {
                'key': key,
                'value': value,
            }
            tem_res.append(tem)

        # print(tem_res)

        context = {
            'gene_len': data['remnant'],  # 输入的序列长度
            'gene': data['gene'],  # 输入的序列
            'res_type': data['result_type'],  # 输入的序列
            'info': info.get('result'),
            'resInfo': tem_res
        }
        # print(context)

        if info.get('tail'):
            context['tail'] = info.get('tail')


        if data.get('validation') == 'Yes':
            # 分析过程
            analy = Analysis(next_cal[0], next_cal[1][1:], next_cal[2])
            # info = analy.get_more_info()
            analy_info = analy.analysis_two()

            analy_info.update(analy.analysis_three())

            analy_info_list = []
            for key, value in analy_info.items():
                analy_info_list.append({
                'key': key,
                'value': value,
            })
            context['analyInfoList'] = analy_info_list
            print(context['analyInfoList'])

        return JsonResponse(context)



#
# class HomeView(View):
#     def get(self, request):
#         # return HttpResponse("get")
#         return render(request, 'test.html')
#
#     # def post(self, request):
#     #     data = request.body
#     #     print(data)
#     #
#     #     return render(request, 'assembly.html')
#
#     def post(self, request):
#         data = request.POST
#         tem_gene = data.get('gene_input').replace('\n', '').replace(' ', '').replace('\r', '')
#         input_info = {
#             'gene': tem_gene,  # 输入基因序列
#             'res_type': data.get('res_type'),  # 结果：gepless?gap
#             'result':data.get('result'),
#             'min_len':data.get('min_len'),
#             'max_len':data.get('max_len'),
#             # 各种离子浓度
#             'Na': float(data.get('Na')),
#             'K': float(data.get('K')),
#             'Mg': float(data.get('Mg')),
#             'dNTPs': float(data.get('dNTPs')),
#             'Tris': float(data.get('Tris')),
#             'oligo': float(data.get('oligo')),
#             'primer': float(data.get('primer')),
#         }
#
#         splic = Splicing(input_info)
#         # list_g1, list_g2, len1, info = splic.cal()
#         next_cal, info = splic.cal()
#
#         context = {
#             'gene_len': len(input_info['gene']),  # 输入的序列长度
#             'gene': input_info['gene'],  # 输入的序列
#             'res_type': input_info['res_type'],  # 输入的序列
#             'info': info.get('result'),
#             'min': info.get('min'),
#             'max': info.get('max'),
#             'range': info.get('range'),
#             'mean': info.get('mean'),
#             'std': info.get('std')
#         }
#         if info.get('tail'):
#             context['tail'] = info.get('tail')
#
#         if data.get('veri') == 'yes':
#             # 分析过程
#             analy = Analysis(next_cal[0], next_cal[1][1:], next_cal[2])
#             # info = analy.get_more_info()
#             analy_info_two = analy.analysis_two()
#             analy_info_three = analy.analysis_three()
#             context['analy_info_two'] = analy_info_two
#             context['analy_info_three'] = analy_info_three
#
#         return render(request, 'result.html', context)

