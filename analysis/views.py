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

        data = json.loads(request.body)

        # print(data['validation'], data['result'])
        # if data['validation'] == 'No':
        #     if data['result'] == 'res1':
        #         context = {'arr':[{'gene_len': 638,
        #          'gene': 'taagcacctgtaggatcgtacaggtttacgcaagaaaatggtttgttatagtcgaataacaccgtgcgtgttgactattttacctctggcggtgatatactagagaaagaggagaaatactagatgaccatgattacgccaagcgcgcaattaaccctcactaaagggaacaaaagctggagctccaccgcggtggcggcagcactagagctagtggatcccccgggctgtagaaattcgatatcaagcttatcgataccgtcgacctcgagggggggcccggtacccaattcgccctatagtgagtcgtattacgcgcgctcactggccgtcgttttacaacgtcgtgactgggaaaaccctggcgttacccaacttaatcgccttgcagcacatccccctttcgccagctggcgtaatagcgaagaggcccgcaccgatcgcccttcccaacagttgcgcagcctgaataataacgctgatagtgctagtgtagatcgctactagagccaggcatcaaataaaacgaaaggctcagtcgaaagactgggcctttcgttttatctgttgtttgtcggtgaacgctctctactagagtcacactggctcaccttcgggtgggcctttctgcgtttata',
        #          'res_type': 'Gap', 'info': [['F0', 'TAAGCACCTGTAGGATCGTACAGGTTTACGCAAGAAAATGGTTTGTT', 56.55, 25, 47],
        #                                      ['R0', 'ACGCACGGTGTTATTCGACTATAACAAACCATTTTCTTGCGTAAACC', 56.39, 22, 47],
        #                                      ['F1', 'ATAGTCGAATAACACCGTGCGTGTTGACTATTTTACCTCTGGCGG', 56.39, 23, 45],
        #                                      ['R1', 'TCTAGTATTTCTCCTCTTTCTCTAGTATATCACCGCCAGAGGTAAAATAGTCAAC', 56.7, 32, 55],
        #                                      ['F2', 'TGATATACTAGAGAAAGAGGAGAAATACTAGATGACCATGATTACGCCAAGCG', 57.71, 21, 53],
        #                                      ['R2', 'TTCCCTTTAGTGAGGGTTAATTGCGCGCTTGGCGTAATCATGGTCA', 58.45, 25, 46],
        #                                      ['F3', 'CGCAATTAACCCTCACTAAAGGGAACAAAAGCTGGAGCTCCACCG', 58.18, 20, 45],
        #                                      ['R3', 'AGTGCTGCCGCCACCGCGGTGGAGCTCCAGCTTTTG', 58.31, 16, 36],
        #                                      ['F4', 'CGGTGGCGGCAGCACTAGAGCTAGTGGATCCCCCGG', 57.81, 19, 36],
        #                                      ['R4', 'CGATAAGCTTGATATCGAATTTCTACAGCCCGGGGGATCCACTAGCTC', 58.6, 29, 48],
        #                                      ['F5', 'GCTGTAGAAATTCGATATCAAGCTTATCGATACCGTCGACCTCGAGGGG', 58.98, 19, 49],
        #                                      ['R5', 'CGAATTGGGTACCGGGCCCCCCCTCGAGGTCGACGGTA', 59.63, 19, 38],
        #                                      ['F6', 'GGGCCCGGTACCCAATTCGCCCTATAGTGAGTCGTATTACGCG', 57.69, 24, 43],
        #                                      ['R6', 'ACGACGGCCAGTGAGCGCGCGTAATACGACTCACTATAGGG', 58.13, 17, 41],
        #                                      ['F7', 'CGCTCACTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACC', 59.12, 22, 43],
        #                                      ['R7', 'GCGATTAAGTTGGGTAACGCCAGGGTTTTCCCAGTCACGACGTTG', 58.08, 22, 45],
        #                                      ['F8', 'TGGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTC', 58.64, 21, 43],
        #                                      ['R8', 'CGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAG', 57.96, 19, 40],
        #                                      ['F9', 'GCCAGCTGGCGTAATAGCGAAGAGGCCCGCACCGATCG', 57.4, 16, 38],
        #                                      ['R9', 'GCGCAACTGTTGGGAAGGGCGATCGGTGCGGGCCT', 58.31, 19, 35],
        #                                      ['F10', 'CCCTTCCCAACAGTTGCGCAGCCTGAATAATAACGCTGATAGTGC', 57.66, 25, 45],
        #                                      ['R10', 'CCTGGCTCTAGTAGCGATCTACACTAGCACTATCAGCGTTATTATTCAGGC', 57.75, 23, 51],
        #                                      ['F11', 'TGTAGATCGCTACTAGAGCCAGGCATCAAATAAAACGAAAGGCTCAGTCG', 57.71, 26, 50],
        #                                      ['R11', 'CAGATAAAACGAAAGGCCCAGTCTTTCGACTGAGCCTTTCGTTTTATTTGAT', 58.07, 24, 52],
        #                                      ['F12', 'AGACTGGGCCTTTCGTTTTATCTGTTGTTTGTCGGTGAACGCTCTC', 58.17, 22, 46],
        #                                      ['R12', 'AGGTGAGCCAGTGTGACTCTAGTAGAGAGCGTTCACCGACAAACAA', 57.92, 22, 46],
        #                                      ['F13', 'CTAGAGTCACACTGGCTCACCTTCGGGTGGGCCTTTCTGCGT', 58.54, 18, 42],
        #                                      ['R13', 'GTGCCTTAATCTATCTTCAGGAACTGTATAAACGCAGAAAGGCCCACCC', 58.94, 31, 49],
        #                                      ['F14', 'TTATACAGTTCCTGAAGATAGATTAAGGCAC', -1, -1, 31],
        #                                      ['F_Primer', 'TAAGCACCTGTAGGATCGTACA', 54.73, -1, 22],
        #                                      ['R_Primer', 'GTGCCTTAATCTATCTTCAGGAACTGTATAA', 58.94, -1, 31]],
        #          'resInfo': [{'key': 'min', 'value': 56.39}, {'key': 'max', 'value': 59.63},
        #                      {'key': 'range', 'value': 3.24}, {'key': 'mean', 'value': 57.99},
        #                      {'key': 'std', 'value': 0.78}], 'tail': 'CAGTTCCTGAAGATAGATTAAGGCAC'}, {'gene_len': 638,
        #          'gene': 'taagcacctgtaggatcgtacaggtttacgcaagaaaatggtttgttatagtcgaataacaccgtgcgtgttgactattttacctctggcggtgatatactagagaaagaggagaaatactagatgaccatgattacgccaagcgcgcaattaaccctcactaaagggaacaaaagctggagctccaccgcggtggcggcagcactagagctagtggatcccccgggctgtagaaattcgatatcaagcttatcgataccgtcgacctcgagggggggcccggtacccaattcgccctatagtgagtcgtattacgcgcgctcactggccgtcgttttacaacgtcgtgactgggaaaaccctggcgttacccaacttaatcgccttgcagcacatccccctttcgccagctggcgtaatagcgaagaggcccgcaccgatcgcccttcccaacagttgcgcagcctgaataataacgctgatagtgctagtgtagatcgctactagagccaggcatcaaataaaacgaaaggctcagtcgaaagactgggcctttcgttttatctgttgtttgtcggtgaacgctctctactagagtcacactggctcaccttcgggtgggcctttctgcgtttata',
        #          'res_type': 'Gap', 'info': [['F0', 'TAAGCACCTGTAGGATCGTACAGGTTTACGCAAGAAAATGGTTTGTT', 56.55, 25, 47],
        #                                      ['R0', 'ACGCACGGTGTTATTCGACTATAACAAACCATTTTCTTGCGTAAACC', 56.39, 22, 47],
        #                                      ['F1', 'ATAGTCGAATAACACCGTGCGTGTTGACTATTTTACCTCTGGCGG', 56.39, 23, 45],
        #                                      ['R1', 'TCTAGTATTTCTCCTCTTTCTCTAGTATATCACCGCCAGAGGTAAAATAGTCAAC', 56.7, 32, 55],
        #                                      ['F2', 'TGATATACTAGAGAAAGAGGAGAAATACTAGATGACCATGATTACGCCAAGCG', 57.71, 21, 53],
        #                                      ['R2', 'TTCCCTTTAGTGAGGGTTAATTGCGCGCTTGGCGTAATCATGGTCA', 58.45, 25, 46],
        #                                      ['F3', 'CGCAATTAACCCTCACTAAAGGGAACAAAAGCTGGAGCTCCACCG', 58.18, 20, 45],
        #                                      ['R3', 'AGTGCTGCCGCCACCGCGGTGGAGCTCCAGCTTTTG', 58.31, 16, 36],
        #                                      ['F4', 'CGGTGGCGGCAGCACTAGAGCTAGTGGATCCCCCGG', 57.81, 19, 36],
        #                                      ['R4', 'CGATAAGCTTGATATCGAATTTCTACAGCCCGGGGGATCCACTAGCTC', 58.6, 29, 48],
        #                                      ['F5', 'GCTGTAGAAATTCGATATCAAGCTTATCGATACCGTCGACCTCGAGGGG', 58.98, 19, 49],
        #                                      ['R5', 'CGAATTGGGTACCGGGCCCCCCCTCGAGGTCGACGGTA', 59.63, 19, 38],
        #                                      ['F6', 'GGGCCCGGTACCCAATTCGCCCTATAGTGAGTCGTATTACGCG', 57.69, 24, 43],
        #                                      ['R6', 'ACGACGGCCAGTGAGCGCGCGTAATACGACTCACTATAGGG', 58.13, 17, 41],
        #                                      ['F7', 'CGCTCACTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACC', 59.12, 22, 43],
        #                                      ['R7', 'GCGATTAAGTTGGGTAACGCCAGGGTTTTCCCAGTCACGACGTTG', 58.08, 22, 45],
        #                                      ['F8', 'TGGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTC', 58.64, 21, 43],
        #                                      ['R8', 'CGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAG', 57.96, 19, 40],
        #                                      ['F9', 'GCCAGCTGGCGTAATAGCGAAGAGGCCCGCACCGATCG', 57.4, 16, 38],
        #                                      ['R9', 'GCGCAACTGTTGGGAAGGGCGATCGGTGCGGGCCT', 58.31, 19, 35],
        #                                      ['F10', 'CCCTTCCCAACAGTTGCGCAGCCTGAATAATAACGCTGATAGTGC', 57.66, 25, 45],
        #                                      ['R10', 'CCTGGCTCTAGTAGCGATCTACACTAGCACTATCAGCGTTATTATTCAGGC', 57.75, 23, 51],
        #                                      ['F11', 'TGTAGATCGCTACTAGAGCCAGGCATCAAATAAAACGAAAGGCTCAGTCG', 57.71, 26, 50],
        #                                      ['R11', 'CAGATAAAACGAAAGGCCCAGTCTTTCGACTGAGCCTTTCGTTTTATTTGAT', 58.07, 24, 52],
        #                                      ['F12', 'AGACTGGGCCTTTCGTTTTATCTGTTGTTTGTCGGTGAACGCTCTC', 58.17, 22, 46],
        #                                      ['R12', 'AGGTGAGCCAGTGTGACTCTAGTAGAGAGCGTTCACCGACAAACAA', 57.92, 22, 46],
        #                                      ['F13', 'CTAGAGTCACACTGGCTCACCTTCGGGTGGGCCTTTCTGCGT', 58.54, 18, 42],
        #                                      ['R13', 'GTGCCTTAATCTATCTTCAGGAACTGTATAAACGCAGAAAGGCCCACCC', 58.94, 31, 49],
        #                                      ['F14', 'TTATACAGTTCCTGAAGATAGATTAAGGCAC', -1, -1, 31]],
        #          'resInfo': [{'key': 'min', 'value': 56.39}, {'key': 'max', 'value': 59.63},
        #                      {'key': 'range', 'value': 3.24}, {'key': 'mean', 'value': 57.99},
        #                      {'key': 'std', 'value': 0.78}], 'tail': 'CAGTTCCTGAAGATAGATTAAGGCAC'} ]}
        #         print("validation:No+res1")
        #     elif data['result'] == 'res2':
        #         context = {'gene_len': 638, 'gene': 'taagcacctgtaggatcgtacaggtttacgcaagaaaatggtttgttatagtcgaataacaccgtgcgtgttgactattttacctctggcggtgatatactagagaaagaggagaaatactagatgaccatgattacgccaagcgcgcaattaaccctcactaaagggaacaaaagctggagctccaccgcggtggcggcagcactagagctagtggatcccccgggctgtagaaattcgatatcaagcttatcgataccgtcgacctcgagggggggcccggtacccaattcgccctatagtgagtcgtattacgcgcgctcactggccgtcgttttacaacgtcgtgactgggaaaaccctggcgttacccaacttaatcgccttgcagcacatccccctttcgccagctggcgtaatagcgaagaggcccgcaccgatcgcccttcccaacagttgcgcagcctgaataataacgctgatagtgctagtgtagatcgctactagagccaggcatcaaataaaacgaaaggctcagtcgaaagactgggcctttcgttttatctgttgtttgtcggtgaacgctctctactagagtcacactggctcaccttcgggtgggcctttctgcgtttata', 'res_type': 'Gap', 'info': [['F0', 'ACGGAATTAGATAGAAGTCCTTGACTAAGCACCTGTAGGATCGTACAGGTTTACG', 59.09, 25, 55], ['R0', 'GTGTTATTCGACTATAACAAACCATTTTCTTGCGTAAACCTGTACGATCCTACAGGT', 58.55, 32, 57], ['F1', 'CAAGAAAATGGTTTGTTATAGTCGAATAACACCGTGCGTGTTGACTATTTTACCTCTG', 59.98, 26, 58], ['R1', 'TTTCTCCTCTTTCTCTAGTATATCACCGCCAGAGGTAAAATAGTCAACACGCACG', 59.72, 29, 55], ['F2', 'GCGGTGATATACTAGAGAAAGAGGAGAAATACTAGATGACCATGATTACGCCAAGC', 60.42, 26, 56], ['R2', 'CCCTTTAGTGAGGGTTAATTGCGCGCTTGGCGTAATCATGGTCATCTAGT', 59.51, 24, 50], ['F3', 'GCGCAATTAACCCTCACTAAAGGGAACAAAAGCTGGAGCTCCACCGC', 59.68, 20, 47], ['R3', 'CTCTAGTGCTGCCGCCACCGCGGTGGAGCTCCAGCTTTT', 59.56, 19, 39], ['F4', 'GGTGGCGGCAGCACTAGAGCTAGTGGATCCCCCGGGCTG', 59.57, 18, 39], ['R4', 'ACGGTATCGATAAGCTTGATATCGAATTTCTACAGCCCGGGGGATCCACT', 59.52, 30, 50], ['F5', 'GAAATTCGATATCAAGCTTATCGATACCGTCGACCTCGAGGGGGGGC', 60.38, 17, 47], ['R5', 'CTATAGGGCGAATTGGGTACCGGGCCCCCCCTCGAGGTCG', 59.78, 23, 40], ['F6', 'CCGGTACCCAATTCGCCCTATAGTGAGTCGTATTACGCGCGCTC', 59.57, 21, 44], ['R6', 'GACGTTGTAAAACGACGGCCAGTGAGCGCGCGTAATACGACTCA', 59.43, 22, 44], ['F7', 'CTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACCCTGGCGT', 60.54, 21, 44], ['R7', 'GCTGCAAGGCGATTAAGTTGGGTAACGCCAGGGTTTTCCCAGTCA', 59.6, 22, 45], ['F8', 'CCCAACTTAATCGCCTTGCAGCACATCCCCCTTTCGCCAGCTG', 60.28, 20, 43], ['R8', 'GCGGGCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATG', 60.39, 21, 42], ['F9', 'CGTAATAGCGAAGAGGCCCGCACCGATCGCCCTTCCCAACA', 60.04, 20, 41], ['R9', 'AGCGTTATTATTCAGGCTGCGCAACTGTTGGGAAGGGCGATCGGT', 59.84, 23, 45], ['F10', 'TGCGCAGCCTGAATAATAACGCTGATAGTGCTAGTGTAGATCGCTACTAGAGC', 59.88, 26, 53], ['R10', 'ACTGAGCCTTTCGTTTTATTTGATGCCTGGCTCTAGTAGCGATCTACACTAGCAC', 60.18, 27, 55], ['F11', 'GGCATCAAATAAAACGAAAGGCTCAGTCGAAAGACTGGGCCTTTCGTTTTATC', 60.27, 26, 53], ['R11', 'GAGAGCGTTCACCGACAAACAACAGATAAAACGAAAGGCCCAGTCTTTCG', 59.7, 23, 50], ['F12', 'GTTGTTTGTCGGTGAACGCTCTCTACTAGAGTCACACTGGCTCACCTT', 59.9, 24, 48], ['R12', 'AAACGCAGAAAGGCCCACCCGAAGGTGAGCCAGTGTGACTCTAGT', 59.94, 20, 45], ['F13', 'GGGTGGGCCTTTCTGCGTTT', -1, -1, 20], ['F_Primer', 'ACGGAATTAGATAGAAGTCCTTGACTAAGC', 60.35, -1, 30], ['R_Primer', 'AAACGCAGAAAGGCCCACCC', 59.94, -1, 20]], 'resInfo': [{'key': 'min', 'value': 58.55}, {'key': 'max', 'value': 60.54}, {'key': 'range', 'value': 1.99}, {'key': 'mean', 'value': 59.82}, {'key': 'std', 'value': 0.44}], 'tail': 'TACTAGAGTCACACTGGCTCACCTTCGGGTGGGCCTTTCTGCGTTT'}
        #         print("validation:No+res2")
        #
        # elif data['validation'] == 'Yes':
        #     if data['result'] == 'res1':
        #         context = {'gene_len': 638, 'gene': 'taagcacctgtaggatcgtacaggtttacgcaagaaaatggtttgttatagtcgaataacaccgtgcgtgttgactattttacctctggcggtgatatactagagaaagaggagaaatactagatgaccatgattacgccaagcgcgcaattaaccctcactaaagggaacaaaagctggagctccaccgcggtggcggcagcactagagctagtggatcccccgggctgtagaaattcgatatcaagcttatcgataccgtcgacctcgagggggggcccggtacccaattcgccctatagtgagtcgtattacgcgcgctcactggccgtcgttttacaacgtcgtgactgggaaaaccctggcgttacccaacttaatcgccttgcagcacatccccctttcgccagctggcgtaatagcgaagaggcccgcaccgatcgcccttcccaacagttgcgcagcctgaataataacgctgatagtgctagtgtagatcgctactagagccaggcatcaaataaaacgaaaggctcagtcgaaagactgggcctttcgttttatctgttgtttgtcggtgaacgctctctactagagtcacactggctcaccttcgggtgggcctttctgcgtttata',
        #                    'res_type': 'Gap', 'info': [['F0', 'TAAGCACCTGTAGGATCGTACAGGTTTACGCAAGAAAATGGTTTGTT', 56.55, 25, 47], ['R0', 'ACGCACGGTGTTATTCGACTATAACAAACCATTTTCTTGCGTAAACC', 56.39, 22, 47], ['F1', 'ATAGTCGAATAACACCGTGCGTGTTGACTATTTTACCTCTGGCGG', 56.39, 23, 45], ['R1', 'TCTAGTATTTCTCCTCTTTCTCTAGTATATCACCGCCAGAGGTAAAATAGTCAAC', 56.7, 32, 55], ['F2', 'TGATATACTAGAGAAAGAGGAGAAATACTAGATGACCATGATTACGCCAAGCG', 57.71, 21, 53], ['R2', 'TTCCCTTTAGTGAGGGTTAATTGCGCGCTTGGCGTAATCATGGTCA', 58.45, 25, 46], ['F3', 'CGCAATTAACCCTCACTAAAGGGAACAAAAGCTGGAGCTCCACCG', 58.18, 20, 45], ['R3', 'AGTGCTGCCGCCACCGCGGTGGAGCTCCAGCTTTTG', 58.31, 16, 36], ['F4', 'CGGTGGCGGCAGCACTAGAGCTAGTGGATCCCCCGG', 57.81, 19, 36], ['R4', 'CGATAAGCTTGATATCGAATTTCTACAGCCCGGGGGATCCACTAGCTC', 58.6, 29, 48], ['F5', 'GCTGTAGAAATTCGATATCAAGCTTATCGATACCGTCGACCTCGAGGGG', 58.98, 19, 49], ['R5', 'CGAATTGGGTACCGGGCCCCCCCTCGAGGTCGACGGTA', 59.63, 19, 38], ['F6', 'GGGCCCGGTACCCAATTCGCCCTATAGTGAGTCGTATTACGCG', 57.69, 24, 43], ['R6', 'ACGACGGCCAGTGAGCGCGCGTAATACGACTCACTATAGGG', 58.13, 17, 41], ['F7', 'CGCTCACTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACC', 59.12, 22, 43], ['R7', 'GCGATTAAGTTGGGTAACGCCAGGGTTTTCCCAGTCACGACGTTG', 58.08, 22, 45], ['F8', 'TGGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTC', 58.64, 21, 43], ['R8', 'CGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAG', 57.96, 19, 40], ['F9', 'GCCAGCTGGCGTAATAGCGAAGAGGCCCGCACCGATCG', 57.4, 16, 38], ['R9', 'GCGCAACTGTTGGGAAGGGCGATCGGTGCGGGCCT', 58.31, 19, 35], ['F10', 'CCCTTCCCAACAGTTGCGCAGCCTGAATAATAACGCTGATAGTGC', 57.66, 25, 45], ['R10', 'CCTGGCTCTAGTAGCGATCTACACTAGCACTATCAGCGTTATTATTCAGGC', 57.75, 23, 51], ['F11', 'TGTAGATCGCTACTAGAGCCAGGCATCAAATAAAACGAAAGGCTCAGTCG', 57.71, 26, 50], ['R11', 'CAGATAAAACGAAAGGCCCAGTCTTTCGACTGAGCCTTTCGTTTTATTTGAT', 58.07, 24, 52], ['F12', 'AGACTGGGCCTTTCGTTTTATCTGTTGTTTGTCGGTGAACGCTCTC', 58.17, 22, 46], ['R12', 'AGGTGAGCCAGTGTGACTCTAGTAGAGAGCGTTCACCGACAAACAA', 57.92, 22, 46], ['F13', 'CTAGAGTCACACTGGCTCACCTTCGGGTGGGCCTTTCTGCGT', 58.54, 18, 42], ['R13', 'GTGCCTTAATCTATCTTCAGGAACTGTATAAACGCAGAAAGGCCCACCC', 58.94, 31, 49], ['F14', 'TTATACAGTTCCTGAAGATAGATTAAGGCAC', -1, -1, 31], ['F_Primer', 'TAAGCACCTGTAGGATCGTACA', 54.73, -1, 22], ['R_Primer', 'GTGCCTTAATCTATCTTCAGGAACTGTATAA', 58.94, -1, 31]], 'resInfo': [{'key': 'min', 'value': 56.39}, {'key': 'max', 'value': 59.63}, {'key': 'range', 'value': 3.24}, {'key': 'mean', 'value': 57.99}, {'key': 'std', 'value': 0.78}], 'tail': 'CAGTTCCTGAAGATAGATTAAGGCAC',
        #                    'analyInfoList': [{'key': 'F11,F12', 'value': 9.92911740074282e-09}, {'key': 'F6,R9', 'value': 6.798673356931505e-09}, {'key': 'F12,R13', 'value': 6.085966565061968e-09}, {'key': 'R3,R3', 'value': 2.256725521101852e-09}, {'key': 'F4,R8', 'value': 2.2327214044932395e-09}, {'key': 'R2,R6', 'value': 1.6723188372039826e-09}, {'key': 'R8,R8', 'value': 1.6120679688082714e-09}, {'key': 'F11,F12,R10', 'value': 9.984953284034626e-09}, {'key': 'F11,F12,R12', 'value': 9.927465499273197e-09}, {'key': 'F12,R12,R13', 'value': 6.18041569880846e-09}, {'key': 'F12,F14,R13', 'value': 6.116150845405556e-09}, {'key': 'F4,F9,R8', 'value': 2.524657669197511e-09}]}
        #         print("validation:Yes+res1")
        #     elif data['result'] == 'res2':
        #         context = {'gene_len': 638, 'gene': 'taagcacctgtaggatcgtacaggtttacgcaagaaaatggtttgttatagtcgaataacaccgtgcgtgttgactattttacctctggcggtgatatactagagaaagaggagaaatactagatgaccatgattacgccaagcgcgcaattaaccctcactaaagggaacaaaagctggagctccaccgcggtggcggcagcactagagctagtggatcccccgggctgtagaaattcgatatcaagcttatcgataccgtcgacctcgagggggggcccggtacccaattcgccctatagtgagtcgtattacgcgcgctcactggccgtcgttttacaacgtcgtgactgggaaaaccctggcgttacccaacttaatcgccttgcagcacatccccctttcgccagctggcgtaatagcgaagaggcccgcaccgatcgcccttcccaacagttgcgcagcctgaataataacgctgatagtgctagtgtagatcgctactagagccaggcatcaaataaaacgaaaggctcagtcgaaagactgggcctttcgttttatctgttgtttgtcggtgaacgctctctactagagtcacactggctcaccttcgggtgggcctttctgcgtttata', 'res_type': 'Gap', 'info': [['F0', 'ACGGAATTAGATAGAAGTCCTTGACTAAGCACCTGTAGGATCGTACAGGTTTACG', 59.09, 25, 55], ['R0', 'GTGTTATTCGACTATAACAAACCATTTTCTTGCGTAAACCTGTACGATCCTACAGGT', 58.55, 32, 57], ['F1', 'CAAGAAAATGGTTTGTTATAGTCGAATAACACCGTGCGTGTTGACTATTTTACCTCTG', 59.98, 26, 58], ['R1', 'TTTCTCCTCTTTCTCTAGTATATCACCGCCAGAGGTAAAATAGTCAACACGCACG', 59.72, 29, 55], ['F2', 'GCGGTGATATACTAGAGAAAGAGGAGAAATACTAGATGACCATGATTACGCCAAGC', 60.42, 26, 56], ['R2', 'CCCTTTAGTGAGGGTTAATTGCGCGCTTGGCGTAATCATGGTCATCTAGT', 59.51, 24, 50], ['F3', 'GCGCAATTAACCCTCACTAAAGGGAACAAAAGCTGGAGCTCCACCGC', 59.68, 20, 47], ['R3', 'CTCTAGTGCTGCCGCCACCGCGGTGGAGCTCCAGCTTTT', 59.56, 19, 39], ['F4', 'GGTGGCGGCAGCACTAGAGCTAGTGGATCCCCCGGGCTG', 59.57, 18, 39], ['R4', 'ACGGTATCGATAAGCTTGATATCGAATTTCTACAGCCCGGGGGATCCACT', 59.52, 30, 50], ['F5', 'GAAATTCGATATCAAGCTTATCGATACCGTCGACCTCGAGGGGGGGC', 60.38, 17, 47], ['R5', 'CTATAGGGCGAATTGGGTACCGGGCCCCCCCTCGAGGTCG', 59.78, 23, 40], ['F6', 'CCGGTACCCAATTCGCCCTATAGTGAGTCGTATTACGCGCGCTC', 59.57, 21, 44], ['R6', 'GACGTTGTAAAACGACGGCCAGTGAGCGCGCGTAATACGACTCA', 59.43, 22, 44], ['F7', 'CTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACCCTGGCGT', 60.54, 21, 44], ['R7', 'GCTGCAAGGCGATTAAGTTGGGTAACGCCAGGGTTTTCCCAGTCA', 59.6, 22, 45], ['F8', 'CCCAACTTAATCGCCTTGCAGCACATCCCCCTTTCGCCAGCTG', 60.28, 20, 43], ['R8', 'GCGGGCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATG', 60.39, 21, 42], ['F9', 'CGTAATAGCGAAGAGGCCCGCACCGATCGCCCTTCCCAACA', 60.04, 20, 41], ['R9', 'AGCGTTATTATTCAGGCTGCGCAACTGTTGGGAAGGGCGATCGGT', 59.84, 23, 45], ['F10', 'TGCGCAGCCTGAATAATAACGCTGATAGTGCTAGTGTAGATCGCTACTAGAGC', 59.88, 26, 53], ['R10', 'ACTGAGCCTTTCGTTTTATTTGATGCCTGGCTCTAGTAGCGATCTACACTAGCAC', 60.18, 27, 55], ['F11', 'GGCATCAAATAAAACGAAAGGCTCAGTCGAAAGACTGGGCCTTTCGTTTTATC', 60.27, 26, 53], ['R11', 'GAGAGCGTTCACCGACAAACAACAGATAAAACGAAAGGCCCAGTCTTTCG', 59.7, 23, 50], ['F12', 'GTTGTTTGTCGGTGAACGCTCTCTACTAGAGTCACACTGGCTCACCTT', 59.9, 24, 48], ['R12', 'AAACGCAGAAAGGCCCACCCGAAGGTGAGCCAGTGTGACTCTAGT', 59.94, 20, 45], ['F13', 'GGGTGGGCCTTTCTGCGTTT', -1, -1, 20], ['F_Primer', 'ACGGAATTAGATAGAAGTCCTTGACTAAGC', 60.35, -1, 30], ['R_Primer', 'AAACGCAGAAAGGCCCACCC', 59.94, -1, 20]], 'resInfo': [{'key': 'min', 'value': 58.55}, {'key': 'max', 'value': 60.54}, {'key': 'range', 'value': 1.99}, {'key': 'mean', 'value': 59.82}, {'key': 'std', 'value': 0.44}], 'tail': 'TACTAGAGTCACACTGGCTCACCTTCGGGTGGGCCTTTCTGCGTTT', 'analyInfoList': [{'key': 'R10,R11', 'value': 8.33452998677627e-09}, {'key': 'F9,R5', 'value': 5.1729470192984495e-09}, {'key': 'R3,R3', 'value': 2.1352142800227824e-09}, {'key': 'R8,R8', 'value': 1.5879011962044874e-09}, {'key': 'F10,R10,R11', 'value': 9.541558071902099e-09}, {'key': 'F12,R10,R11', 'value': 7.163895998307081e-09}, {'key': 'F5,F9,R5', 'value': 1.1724603826796238e-09}]}
        #         print("validation:Yes+res2")
        #
        # return JsonResponse(context)

        ion = data.pop('tableData')
        ion = self.get_tableData(ion)
        data.update(ion)
        data['gene'] = data['gene'].replace('\n', '').replace(' ', '').replace('\r', '')
        models.GeneInfo.objects.create(gene=data['gene'], email=data['email'])
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
            'resInfo': tem_res,
            'nextCal': next_cal
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
            # print(context['analyInfoList'])

        # print(context)
        return JsonResponse(context)


class AssemblyPoolsView(View):

    def get_tableData(self, data_list):
        tableData = {}
        for data in data_list:
            tableData[data['name']] = data['data']
        # print(tableData)
        return tableData

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
        print("pools:{0}".format(pools))
        splic = Splicing(data)
        index, tm = splic.cal_for_pool()
        index = [int(i) for i in index]

        print("index_len:{0}, len_tm:{1}".format(len(index), len(tm)))
        # print(index)
        # print(tm)

        # overlap of each pool
        each_pool = int(len(index) / pools)
        each_pool = each_pool + 1 if each_pool % 2 == 0 else each_pool
        print("after pools:{0}".format(each_pool))

        gene = data['gene']
        print("gene:{0}".format(len(gene)))
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
            context = {}
            context = {
                'gene_len': data['remnant'],  # 输入的序列长度
                'gene': data['gene'],  # 输入的序列
                'res_type': data['result_type'],  # 输入的序列
                'info': info.get('result'),
                'resInfo': tem_res,
                'nextCal': next_cal
            }
            # print(context)

            if info.get('tail'):
                context['tail'] = info.get('tail')

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
        analy = Analysis(next_cal[0], next_cal[1][1:], next_cal[2])
        analy_info = analy.analysis_two()

        analy_info.update(analy.analysis_three())
        analy_info_list = []
        context = {}
        for key, value in analy_info.items():
            analy_info_list.append({
                'key': key,
                'value': value,
            })
        context['analyInfoList'] = analy_info_list

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
