import io
import json

import django_excel as excel
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from openpyxl import load_workbook

from analysis import models
from analysis.tool.analysis import Analysis
# Create your views here.
from analysis.tool.splicing import Splicing


# from analysis.tool.cal_tm import cal


class DownloadView(View):  # 导出excel数据
    def get(self, request):
        # print("test success")
        return HttpResponse("get")

    # 将dataform转换成django-excel下载是的sheet
    def post(self, request):
        tem = json.loads(request.body)
        output = io.BytesIO()  # 配置一个BytesIO 这个是为了转二进制流
        count = 0
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for i in range(len(tem)):
                # pool
                data = pd.DataFrame(data=['pool:{0}'.format(i + 1)])
                data.to_excel(writer, startrow=count, index=False, header=None)
                count += 1

                # analysis result
                res_info = tem[i]['resInfo']
                data = pd.DataFrame(data=res_info)
                data.to_excel(writer, startrow=count, startcol=6, index=False)

                if 'analyInfo' in tem[i]:
                    # analysis result
                    analy_info = tem[i]['analyInfo']
                    data = pd.DataFrame(data=analy_info)
                    data.to_excel(writer, startrow=count, startcol=9, index=False)

                # result
                info = tem[i]['info']
                data = pd.DataFrame(data=info, columns=['index', 'gene', 'tm', 'overlap', 'length'])
                data.to_excel(writer, startrow=count, index=False)
                count += data.shape[0] + 2

        # data.to_excel(output, index=False)  # index=False 是为了不建立索引
        # append_df_to_excel(data, output, sheet_name='Sheet1', startcol=10,startrow=0,index=False)
        output.seek(0)  # 把游标归0

        response = HttpResponse()  # 创建一个HttpResponse
        # response["Content-Type"] = "application/vnd.ms-excel"  # 类型
        file_name = 'comment.xlsx'  # 文件名称 自定义
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        response.write(output.getvalue())  # 写入数据
        output.close()  # 关闭
        return response  # 返回


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
        try:
            data = json.loads(request.body)
            # 1 / 0
            ion = data.pop('tableData')
            ion = self.get_tableData(ion)
            # add ion to data (dits)
            data.update(ion)
            data['gene'] = data['gene'].replace('\n', '').replace(' ', '').replace('\r', '')
            # print(data)
            # add to db
            models.GeneInfo.objects.create(email=data['email'], gene_len=data['geneLen'],
                                           pools=data['pools'], min_len=data['minLen'], max_len=data['maxLen'])
            # print(data)
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
        except:
            print("error")
            context = {'error': 'error'}

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
        try:
            data = json.loads(request.body)

            ion = data.pop('tableData')
            ion = self.get_tableData(ion)
            data.update(ion)
            data['gene'] = data['gene'].replace('\n', '').replace(' ', '').replace('\r', '')
            models.GeneInfo.objects.create(email=data['email'], gene_len=data['geneLen'],
                                           pools=data['pools'], min_len=data['minLen'], max_len=data['maxLen'])

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
                    index_list = index[i * each_pool: (i + 1) * each_pool]
                    # print(gene[0:index_list[-1]])
                    # print(index_list)
                    # print(0, index_list[-1])
                    gene_list = gene[0: index_list[-1]]
                    tm_list = tm[i * each_pool: (i + 1) * each_pool]
                    # print(tm_list)
                elif i == pools - 1:
                    # print(index[(pools-1)*each_pool: -1])
                    index_list = index[(pools - 1) * each_pool: -1]
                    # print()
                    # print(index_list)
                    # print(index[(pools-1) * each_pool - 1], index_list[-1])
                    gene_list = gene[index[(pools - 1) * each_pool - 1]: len(gene)]

                    index_list = [x - index[(pools - 1) * each_pool - 1] for x in index_list]
                    # print(index_list)

                    tm_list = tm[(pools - 1) * each_pool: -1]
                    # print(tm_list)
                elif i > 0:
                    index_list = index[i * each_pool: (i + 1) * each_pool]
                    # print(index_list)
                    # print(index[i * each_pool - 1], index_list[-1])
                    gene_list = gene[index[i * each_pool - 1]: index_list[-1]]

                    index_list = [x - index[i * each_pool - 1] for x in index_list]
                    # print(index_list)

                    tm_list = tm[i * each_pool: (i + 1) * each_pool]
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
        except:
            print("error")
            context = {'error': 'error'}

        return JsonResponse(context)


class AnalysisView(View):

    def get(self, request):
        return render(request, 'assembly.html')

    def post(self, request):
        next_cal = json.loads(request.body)
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
