import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View

from analysis import models
from analysis.tool.analysis import Analysis
# Create your views here.
from analysis.tool.splicing import Splicing


# from analysis.tool.cal_tm import cal


class DownloadView(View):  # 导出excel数据
    def get(self, request):
        # print("test success")
        return HttpResponse("get")


class AssemblyView(View):
    def get_tableData(self, data_list):
        tableData = {}
        for data in data_list:
            tableData[data['name']] = data['data']

        tableData['Na'] = 1.2
        return tableData

    def get(self, request):
        return render(request, 'assembly.html')

    def get_res_info(self, info):
        res_info = {
            'min': info.get('min'),
            'max': info.get('max'),
            'range': info.get('range'),
            'mean': info.get('mean'),
            'std': info.get('std')
        }

        if info.get('tail'):
            res_info['tail'] = info.get('tail')

        tem_res = []
        for key, value in res_info.items():
            tem = {
                'key': key,
                'value': value,
            }
            tem_res.append(tem)
        return tem_res

    def post(self, request):
        data = json.loads(request.body)

        ion = data.pop('tableData')
        ion = self.get_tableData(ion)
        # add ion to data (dits)
        data.update(ion)
        data['gene'] = data['gene'].replace('\n', '').replace(' ', '').replace('\r', '')
        # print(data)

        # add to db
        models.GeneInfo.objects.create(gene=data['gene'], email=data['email'])

        splic = Splicing(data)
        next_cal, info = splic.cal()

        # add cal info to context
        tem_res = self.get_res_info(info)

        context = {
            'info': info.get('result'),
            'resInfo': tem_res,
            'nextCal': next_cal
        }
        # print(context)
        if data.get('verification') == 'Yes':

            conc = data['concentrations'] * 1e-8
            # 分析过程
            analy = Analysis(next_cal[0], next_cal[1][1:], next_cal[2], data['temperature'], conc)
            analy_info = analy.analysis_two()
            analy_info.update(analy.analysis_three())

            analy_info_list = []
            for key, value in analy_info.items():
                analy_info_list.append({
                    'key': key,
                    'value': value,
                })
            context['analyInfo'] = analy_info_list

        arr = [context]
        # print(arr)
        context = {'arr': arr}
        return JsonResponse(context)


class AssemblyPoolsView(View):
    def get_tableData(self, data_list):
        tableData = {}
        for data in data_list:
            tableData[data['name']] = data['data']
        # print(tableData)
        tableData['Na'] = 1.2
        return tableData

    def get_res_info(self, info):
        res_info = {
            'min': info.get('min'),
            'max': info.get('max'),
            'range': info.get('range'),
            'mean': info.get('mean'),
            'std': info.get('std')
        }

        if info.get('tail'):
            res_info['tail'] = info.get('tail')

        tem_res = []
        for key, value in res_info.items():
            tem = {
                'key': key,
                'value': value,
            }
            tem_res.append(tem)
        return tem_res

    def post(self, request):
        data = json.loads(request.body)
        # print(data)
        # context = {'arr': [{'gene_len': 638,
        #                     'gene': 'taagcacctgtaggatcgtacaggtttacgcaagaaaatggtttgttatagtcgaataacaccgtgcgtgttgactattttacctctggcggtgatatactagagaaagaggagaaatactagatgaccatgattacgccaagcgcgcaattaaccctcactaaagggaacaaaagctggagctccaccgcggtggcggcagcactagagctagtggatcccccgggctgtagaaattcgatatcaagcttatcgataccgtcgacctcgagggggggcccggtacccaattcgccctatagtgagtcgtattacgcgcgctcactggccgtcgttttacaacgtcgtgactgggaaaaccctggcgttacccaacttaatcgccttgcagcacatccccctttcgccagctggcgtaatagcgaagaggcccgcaccgatcgcccttcccaacagttgcgcagcctgaataataacgctgatagtgctagtgtagatcgctactagagccaggcatcaaataaaacgaaaggctcagtcgaaagactgggcctttcgttttatctgttgtttgtcggtgaacgctctctactagagtcacactggctcaccttcgggtgggcctttctgcgtttata',
        #                     'res_type': 'Gap',
        #                     'info': [['F0', 'TAAGCACCTGTAGGATCGTACAGGTTTACGCAAGAAAATGGTTTGTT', 56.55, 25, 47],
        #                              ['R0', 'ACGCACGGTGTTATTCGACTATAACAAACCATTTTCTTGCGTAAACC', 56.39, 22, 47],
        #                              ['F1', 'ATAGTCGAATAACACCGTGCGTGTTGACTATTTTACCTCTGGCGG', 56.39, 23, 45],
        #                              ['R1', 'TCTAGTATTTCTCCTCTTTCTCTAGTATATCACCGCCAGAGGTAAAATAGTCAAC', 56.7, 32, 55],
        #                              ['F2', 'TGATATACTAGAGAAAGAGGAGAAATACTAGATGACCATGATTACGCCAAGCG', 57.71, 21, 53],
        #                              ['R2', 'TTCCCTTTAGTGAGGGTTAATTGCGCGCTTGGCGTAATCATGGTCA', 58.45, 25, 46],
        #                              ['F3', 'CGCAATTAACCCTCACTAAAGGGAACAAAAGCTGGAGCTCCACCG', 58.18, 20, 45],
        #                              ['R3', 'AGTGCTGCCGCCACCGCGGTGGAGCTCCAGCTTTTG', 58.31, 16, 36],
        #                              ['F4', 'CGGTGGCGGCAGCACTAGAGCTAGTGGATCCCCCGG', 57.81, 19, 36],
        #                              ['R4', 'CGATAAGCTTGATATCGAATTTCTACAGCCCGGGGGATCCACTAGCTC', 58.6, 29, 48],
        #                              ['F5', 'GCTGTAGAAATTCGATATCAAGCTTATCGATACCGTCGACCTCGAGGGG', 58.98, 19, 49],
        #                              ['R5', 'CGAATTGGGTACCGGGCCCCCCCTCGAGGTCGACGGTA', 59.63, 19, 38],
        #                              ['F6', 'GGGCCCGGTACCCAATTCGCCCTATAGTGAGTCGTATTACGCG', 57.69, 24, 43],
        #                              ['R6', 'ACGACGGCCAGTGAGCGCGCGTAATACGACTCACTATAGGG', 58.13, 17, 41],
        #                              ['F7', 'CGCTCACTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACC', 59.12, 22, 43],
        #                              ['R7', 'GCGATTAAGTTGGGTAACGCCAGGGTTTTCCCAGTCACGACGTTG', 58.08, 22, 45],
        #                              ['F8', 'TGGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTC', 58.64, 21, 43],
        #                              ['R8', 'CGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAG', 57.96, 19, 40],
        #                              ['F9', 'GCCAGCTGGCGTAATAGCGAAGAGGCCCGCACCGATCG', 57.4, 16, 38],
        #                              ['R9', 'GCGCAACTGTTGGGAAGGGCGATCGGTGCGGGCCT', 58.31, 19, 35],
        #                              ['F10', 'CCCTTCCCAACAGTTGCGCAGCCTGAATAATAACGCTGATAGTGC', 57.66, 25, 45],
        #                              ['R10', 'CCTGGCTCTAGTAGCGATCTACACTAGCACTATCAGCGTTATTATTCAGGC', 57.75, 23, 51],
        #                              ['F11', 'TGTAGATCGCTACTAGAGCCAGGCATCAAATAAAACGAAAGGCTCAGTCG', 57.71, 26, 50],
        #                              ['R11', 'CAGATAAAACGAAAGGCCCAGTCTTTCGACTGAGCCTTTCGTTTTATTTGAT', 58.07, 24, 52],
        #                              ['F12', 'AGACTGGGCCTTTCGTTTTATCTGTTGTTTGTCGGTGAACGCTCTC', 58.17, 22, 46],
        #                              ['R12', 'AGGTGAGCCAGTGTGACTCTAGTAGAGAGCGTTCACCGACAAACAA', 57.92, 22, 46],
        #                              ['F13', 'CTAGAGTCACACTGGCTCACCTTCGGGTGGGCCTTTCTGCGT', 58.54, 18, 42],
        #                              ['R13', 'GTGCCTTAATCTATCTTCAGGAACTGTATAAACGCAGAAAGGCCCACCC', 58.94, 31, 49],
        #                              ['F14', 'TTATACAGTTCCTGAAGATAGATTAAGGCAC', -1, -1, 31],
        #                              ['F_Primer', 'TAAGCACCTGTAGGATCGTACA', 54.73, -1, 22],
        #                              ['R_Primer', 'GTGCCTTAATCTATCTTCAGGAACTGTATAA', 58.94, -1, 31]],
        #                     'resInfo': [{'key': 'min', 'value': 56.39}, {'key': 'max', 'value': 59.63},
        #                                 {'key': 'range', 'value': 3.24}, {'key': 'mean', 'value': 57.99},
        #                                 {'key': 'std', 'value': 0.78}], 'tail': 'CAGTTCCTGAAGATAGATTAAGGCAC'},
        #                    {'gene_len': 638,
        #                     'gene': 'taagcacctgtaggatcgtacaggtttacgcaagaaaatggtttgttatagtcgaataacaccgtgcgtgttgactattttacctctggcggtgatatactagagaaagaggagaaatactagatgaccatgattacgccaagcgcgcaattaaccctcactaaagggaacaaaagctggagctccaccgcggtggcggcagcactagagctagtggatcccccgggctgtagaaattcgatatcaagcttatcgataccgtcgacctcgagggggggcccggtacccaattcgccctatagtgagtcgtattacgcgcgctcactggccgtcgttttacaacgtcgtgactgggaaaaccctggcgttacccaacttaatcgccttgcagcacatccccctttcgccagctggcgtaatagcgaagaggcccgcaccgatcgcccttcccaacagttgcgcagcctgaataataacgctgatagtgctagtgtagatcgctactagagccaggcatcaaataaaacgaaaggctcagtcgaaagactgggcctttcgttttatctgttgtttgtcggtgaacgctctctactagagtcacactggctcaccttcgggtgggcctttctgcgtttata',
        #                     'res_type': 'Gap',
        #                     'info': [['F0', 'TAAGCACCTGTAGGATCGTACAGGTTTACGCAAGAAAATGGTTTGTT', 56.55, 25, 47],
        #                              ['R0', 'ACGCACGGTGTTATTCGACTATAACAAACCATTTTCTTGCGTAAACC', 56.39, 22, 47],
        #                              ['F1', 'ATAGTCGAATAACACCGTGCGTGTTGACTATTTTACCTCTGGCGG', 56.39, 23, 45],
        #                              ['R1', 'TCTAGTATTTCTCCTCTTTCTCTAGTATATCACCGCCAGAGGTAAAATAGTCAAC', 56.7, 32, 55],
        #                              ['F2', 'TGATATACTAGAGAAAGAGGAGAAATACTAGATGACCATGATTACGCCAAGCG', 57.71, 21, 53],
        #                              ['R2', 'TTCCCTTTAGTGAGGGTTAATTGCGCGCTTGGCGTAATCATGGTCA', 58.45, 25, 46],
        #                              ['F3', 'CGCAATTAACCCTCACTAAAGGGAACAAAAGCTGGAGCTCCACCG', 58.18, 20, 45],
        #                              ['R3', 'AGTGCTGCCGCCACCGCGGTGGAGCTCCAGCTTTTG', 58.31, 16, 36],
        #                              ['F4', 'CGGTGGCGGCAGCACTAGAGCTAGTGGATCCCCCGG', 57.81, 19, 36],
        #                              ['R4', 'CGATAAGCTTGATATCGAATTTCTACAGCCCGGGGGATCCACTAGCTC', 58.6, 29, 48],
        #                              ['F5', 'GCTGTAGAAATTCGATATCAAGCTTATCGATACCGTCGACCTCGAGGGG', 58.98, 19, 49],
        #                              ['R5', 'CGAATTGGGTACCGGGCCCCCCCTCGAGGTCGACGGTA', 59.63, 19, 38],
        #                              ['F6', 'GGGCCCGGTACCCAATTCGCCCTATAGTGAGTCGTATTACGCG', 57.69, 24, 43],
        #                              ['R6', 'ACGACGGCCAGTGAGCGCGCGTAATACGACTCACTATAGGG', 58.13, 17, 41],
        #                              ['F7', 'CGCTCACTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACC', 59.12, 22, 43],
        #                              ['R7', 'GCGATTAAGTTGGGTAACGCCAGGGTTTTCCCAGTCACGACGTTG', 58.08, 22, 45],
        #                              ['F8', 'TGGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTC', 58.64, 21, 43],
        #                              ['R8', 'CGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAG', 57.96, 19, 40],
        #                              ['F9', 'GCCAGCTGGCGTAATAGCGAAGAGGCCCGCACCGATCG', 57.4, 16, 38],
        #                              ['R9', 'GCGCAACTGTTGGGAAGGGCGATCGGTGCGGGCCT', 58.31, 19, 35],
        #                              ['F10', 'CCCTTCCCAACAGTTGCGCAGCCTGAATAATAACGCTGATAGTGC', 57.66, 25, 45],
        #                              ['R10', 'CCTGGCTCTAGTAGCGATCTACACTAGCACTATCAGCGTTATTATTCAGGC', 57.75, 23, 51],
        #                              ['F11', 'TGTAGATCGCTACTAGAGCCAGGCATCAAATAAAACGAAAGGCTCAGTCG', 57.71, 26, 50],
        #                              ['R11', 'CAGATAAAACGAAAGGCCCAGTCTTTCGACTGAGCCTTTCGTTTTATTTGAT', 58.07, 24, 52],
        #                              ['F12', 'AGACTGGGCCTTTCGTTTTATCTGTTGTTTGTCGGTGAACGCTCTC', 58.17, 22, 46],
        #                              ['R12', 'AGGTGAGCCAGTGTGACTCTAGTAGAGAGCGTTCACCGACAAACAA', 57.92, 22, 46],
        #                              ['F13', 'CTAGAGTCACACTGGCTCACCTTCGGGTGGGCCTTTCTGCGT', 58.54, 18, 42],
        #                              ['R13', 'GTGCCTTAATCTATCTTCAGGAACTGTATAAACGCAGAAAGGCCCACCC', 58.94, 31, 49],
        #                              ['F14', 'TTATACAGTTCCTGAAGATAGATTAAGGCAC', -1, -1, 31]],
        #                     'resInfo': [{'key': 'min', 'value': 56.39}, {'key': 'max', 'value': 59.63},
        #                                 {'key': 'range', 'value': 3.24}, {'key': 'mean', 'value': 57.99},
        #                                 {'key': 'std', 'value': 0.78}], 'tail': 'CAGTTCCTGAAGATAGATTAAGGCAC'}]}

        # return JsonResponse(context)
        ion = data.pop('tableData')
        ion = self.get_tableData(ion)
        data.update(ion)
        data['gene'] = data['gene'].replace('\n', '').replace(' ', '').replace('\r', '')
        models.GeneInfo.objects.create(gene=data['gene'], email=data['email'])

        pools = int(data['pools'])
        # print("pools:{0}".format(pools))
        splic = Splicing(data)
        index, tm = splic.cal_for_pool()
        index = [int(i) for i in index]

        # print("index_len:{0}, len_tm:{1}".format(len(index), len(tm)))
        # print(index)
        # print(tm)

        # overlap of each pool
        each_pool = int(len(index) / pools)
        each_pool = each_pool + 1 if each_pool % 2 == 0 else each_pool
        # print("after pools:{0}".format(each_pool))

        gene = data['gene']
        # print("gene:{0}".format(len(gene)))
        arr = []
        for i in range(pools):
            if i == 0:
                index_list = index[i * each_pool: (i+1)*each_pool]
                # print(gene[0:index_list[-1]])
                # print(index_list)
                # print(0, index_list[-1])
                gene_list = gene[0: index_list[-1]]
                tm_list = tm[i * each_pool: (i+1)*each_pool]
                # print(tm_list)
            elif i == pools - 1:
                # print(index[(pools-1)*each_pool: -1])
                index_list = index[(pools-1)*each_pool: -1]
                # print()
                # print(index_list)
                # print(index[(pools-1) * each_pool - 1], index_list[-1])
                gene_list = gene[index[(pools-1) * each_pool - 1]: len(gene)]

                index_list = [x-index[(pools-1) * each_pool - 1] for x in index_list]
                # print(index_list)

                tm_list = tm[(pools-1)*each_pool: -1]
                # print(tm_list)
            elif i > 0:
                index_list = index[i * each_pool: (i+1)*each_pool]
                # print(index_list)
                # print(index[i * each_pool - 1], index_list[-1])
                gene_list = gene[index[i * each_pool - 1]: index_list[-1]]

                index_list = [x-index[i * each_pool - 1] for x in index_list]
                # print(index_list)

                tm_list = tm[i * each_pool: (i+1)*each_pool]
                # print(tm_list)

            # print(index_list)
            # print(tm_list)
            # print(gene_list)
            data['gene'] = gene_list

            splic = Splicing(data)
            next_cal, info = splic.cal_for_each_pool(index_list, tm_list)

            tem_res = self.get_res_info(info)

            context = {
                'info': info.get('result'),
                'resInfo': tem_res,
                'nextCal': next_cal,
                'temperature': data['temperature'],
                'concentrations': data['concentrations']
            }
            # print(context)

            arr.append(context)

        context = {'arr': arr}
        return JsonResponse(context)


class AnalysisView(View):

    def get(self, request):
        return render(request, 'assembly.html')

    def post(self, request):
        next_cal = json.loads(request.body)
        # print(data)
        # context = {'analyInfoList': [{'key': 'F11,F12', 'value': 9.92911740074282e-09},
        #                              {'key': 'F6,R9', 'value': 6.798673356931505e-09},
        #                              {'key': 'F12,R13', 'value': 6.085966565061968e-09},
        #                              {'key': 'R3,R3', 'value': 2.256725521101852e-09},
        #                              {'key': 'F4,R8', 'value': 2.2327214044932395e-09},
        #                              {'key': 'R2,R6', 'value': 1.6723188372039826e-09},
        #                              {'key': 'R8,R8', 'value': 1.6120679688082714e-09},
        #                              {'key': 'F11,F12,R10', 'value': 9.984953284034626e-09},
        #                              {'key': 'F11,F12,R12', 'value': 9.927465499273197e-09},
        #                              {'key': 'F12,R12,R13', 'value': 6.18041569880846e-09},
        #                              {'key': 'F12,F14,R13', 'value': 6.116150845405556e-09},
        #                              {'key': 'F4,F9,R8', 'value': 2.524657669197511e-09}]}
        # # print(context)
        # return JsonResponse(context)

        # next_cal = data['nextCal']
        # 分析过程

        temp = next_cal[4] * 1e-8
        # print(temp)
        analy = Analysis(next_cal[0], next_cal[1][1:], next_cal[2], next_cal[3], temp)
        analy_info = analy.analysis_two()

        analy_info.update(analy.analysis_three())
        analy_info_list = []
        context = {}
        for key, value in analy_info.items():
            analy_info_list.append({
                'key': key,
                'value': value,
            })
        context['analyInfo'] = analy_info_list

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
#             analy = Analysis(next_cal[0], next_cal[1][1:], next_cal[2], next_cal[3], temp)
#             # info = analy.get_more_info()
#             analy_info_two = analy.analysis_two()
#             analy_info_three = analy.analysis_three()
#             context['analy_info_two'] = analy_info_two
#             context['analy_info_three'] = analy_info_three
#
#         return render(request, 'result.html', context)
