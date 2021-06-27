import numpy as np
import math

# from cal_util import show_w, get_gene, cal_tm, choose
import analysis.tool.analysis


def choose(tem_list, cou=1):
    """
    根据tm标准差降序排序，返回前count个标准差小的分割方法
    :param tem_list:
    :param cou:
    :return:
    """
    tem_list = np.array(tem_list)
    tem_list = tem_list[np.lexsort(tem_list.T)]
    # count = 10  # 在二维数组中获取前count个tm标准差最小的
    # TODO 获取前cou个、还是前cou种、还是：
    # print(tem_list[:cou])
    # tem_list = np.delete(tem_list, -1, axis=1)  # 删除最后一列
    # print(tem_list[:cou])
    if len(tem_list) > cou:
        return tem_list[:cou]

    return tem_list


def cal_tm1(temp_gene):
    """
    计算一小段基因(temp_gene)的tm
    :param temp_gene:
    :return: 这段基因的tm
    """
    AATT = ATTA = TAAT = CAGT = GTCA = CTGA = GACT = CGGC = GCCG = GGCC = 0
    for i in range(len(temp_gene) - 1):
        if (temp_gene[i:i + 2] == 'AA') | (temp_gene[i:i + 2] == 'TT'):
            AATT += 1
        elif temp_gene[i:i + 2] == 'AT':
            ATTA += 1
        elif temp_gene[i:i + 2] == 'TA':
            TAAT += 1
        elif (temp_gene[i:i + 2] == 'CA') | (temp_gene[i:i + 2] == 'TG'):
            CAGT += 1
        elif (temp_gene[i:i + 2] == 'GT') | (temp_gene[i:i + 2] == 'AC'):
            GTCA += 1
        elif (temp_gene[i:i + 2] == 'CT') | (temp_gene[i:i + 2] == 'AG'):
            CTGA += 1
        elif (temp_gene[i:i + 2] == 'GA') | (temp_gene[i:i + 2] == 'TC'):
            GACT += 1
        elif temp_gene[i:i + 2] == 'CG':
            CGGC += 1
        elif temp_gene[i:i + 2] == 'GC':
            GCCG += 1
        elif (temp_gene[i:i + 2] == 'GG') | (temp_gene[i:i + 2] == 'CC'):
            GGCC += 1

    H = AATT * (-7.9) + ATTA * (-7.2) + TAAT * (-7.2) + CAGT * (-8.5) + GTCA * (-8.4) + CTGA * (-7.8) + GACT * (
        -8.2) + CGGC * (-10.6) + GCCG * (-9.8) + GGCC * (-8) + 0.1 + 2.3
    S = AATT * (-22.2) + ATTA * (-20.4) + TAAT * (-21.3) + CAGT * (-22.7) + GTCA * (-22.4) + CTGA * (-21) + GACT * (
        -22.2) + CGGC * (-27.2) + GCCG * (-24.4) + GGCC * (-19.9) - 2.8 + 4.1 - 1.4
    # TODO 钠离子浓度需要重新设置
    return (H * 1000) / (S + 1.987 * math.log10((10 ** -4) / 4)) - 273.15 + 16.6 * math.log10(1.2)


def cal_gc(tem_gene):
    # 计算一小片段中gc的含量
    return (tem_gene.count("C") + tem_gene.count("G")) / len(tem_gene)


def cal_tm(temp_gene):
    """
    计算一小段基因(temp_gene)的tm
    :param temp_gene:
    :return: 这段基因的tm
    """
    AATT = ATTA = TAAT = CAGT = GTCA = CTGA = GACT = CGGC = GCCG = GGCC = 0
    for i in range(len(temp_gene) - 1):
        if (temp_gene[i:i + 2] == 'AA') | (temp_gene[i:i + 2] == 'TT'):
            AATT += 1
        elif temp_gene[i:i + 2] == 'AT':
            ATTA += 1
        elif temp_gene[i:i + 2] == 'TA':
            TAAT += 1
        elif (temp_gene[i:i + 2] == 'CA') | (temp_gene[i:i + 2] == 'TG'):
            CAGT += 1
        elif (temp_gene[i:i + 2] == 'GT') | (temp_gene[i:i + 2] == 'AC'):
            GTCA += 1
        elif (temp_gene[i:i + 2] == 'CT') | (temp_gene[i:i + 2] == 'AG'):
            CTGA += 1
        elif (temp_gene[i:i + 2] == 'GA') | (temp_gene[i:i + 2] == 'TC'):
            GACT += 1
        elif temp_gene[i:i + 2] == 'CG':
            CGGC += 1
        elif temp_gene[i:i + 2] == 'GC':
            GCCG += 1
        elif (temp_gene[i:i + 2] == 'GG') | (temp_gene[i:i + 2] == 'CC'):
            GGCC += 1

    # H = AATT * (-7.9) + ATTA * (-7.2) + TAAT * (-7.2) + CAGT * (-8.5) + GTCA * (-8.4) + CTGA * (-7.8) + GACT * (
    #     -8.2) + CGGC * (-10.6) + GCCG * (-9.8) + GGCC * (-8) + 0.1 + 2.3
    # S = AATT * (-22.2) + ATTA * (-20.4) + TAAT * (-21.3) + CAGT * (-22.7) + GTCA * (-22.4) + CTGA * (-21) + GACT * (
    #     -22.2) + CGGC * (-27.2) + GCCG * (-24.4) + GGCC * (-19.9) - 2.8 + 4.1 - 1.4

    H = AATT * (-7.6) + ATTA * (-7.2) + TAAT * (-7.2) + CAGT * (-8.5) + GTCA * (-8.4) + CTGA * (-7.8) + GACT * (
        -8.2) + CGGC * (-10.6) + GCCG * (-9.8) + GGCC * (-8.0) + 0.2 + 2.2
    S = AATT * (-21.3) + ATTA * (-20.4) + TAAT * (-21.3) + CAGT * (-22.7) + GTCA * (-22.4) + CTGA * (-21.0) + GACT * (
        -22.2) + CGGC * (-27.2) + GCCG * (-24.4) + GGCC * (-19.9) - 5.7 + 6.9 - 1.4

    # TODO 钠离子浓度需要重新设置
    # 当Na+ 浓度不是1 mol / L 时，就需要对其校正，并且C_t / 4
    c_Mon = 0.005  # 输入浓度
    c_Mg = 1.5e-3  #
    c_K = 5.0e-2  # mol / L
    c_Tris = 1.0e-2  # mol / L#
    c_Na = 1e3  #
    c_t = 2e-3  # mmol / L#

    c_dNTP = 8.0e-4  # 脱氧核糖核苷三磷酸
    # c_Mg = c_Mg - c_dNTP

    c_primer = 0  # 引物
    c_oligo = 0 # 寡核苷酸

    kelvins = 273.15

    a = 3.92e-5
    b = -9.11e-6
    c = 6.26e-5
    d = 1.42e-5
    e = -4.82e-4
    f = 5.25e-4
    g = 8.31e-5

    f_GC = cal_gc(temp_gene)
    n_bp = len(temp_gene)

    tm = (H * 1000) / (S + 1.987 * math.log((c_t /1000) / 4)) + 16.6 * math.log(1.02)
    # print(tm-kelvins)
    # print(76.3+kelvins)
    # tm = 76.3+kelvins

    if c_Mon == 0:
        tem = 1 / tm + a + b * math.log(c_Mg) + f_GC * (c + d * math.log(c_Mg)) + (
                e + f * math.log(c_Mg) + g * (math.log(c_Mg) ** 2)) / (2 * (n_bp - 1))
        return 1 / tem - kelvins
    else:
        R = math.sqrt(c_Mg) / c_Mon

        if R < 0.22:
            c_Mon = c_Na + c_K + c_Tris
            tem = 1 / tm + (4.29 * f_GC - 3.95) *10e-5 * math.log(c_Mon) + 9.4e-6*(math.log(c_Mon))**2
            return 1 / tem - kelvins
        elif R < 6.0:

            a = 3.92e-5*(0.843-0.352*math.sqrt(c_Mon) * math.log(c_Mon))
            d = 1.42e-5*(1.279-4.03e-3*math.log(c_Mon)-8.03e-3*(math.log(c_Mon))**2)
            g = 8.31e-5*(0.486-0.258*math.log(c_Mon)+5.25e-3*(math.log(c_Mon))**3)

            tem = 1 / tm + a + b * math.log(c_Mg) + f_GC * (c + d * math.log(c_Mg)) + (
                    e + f * math.log(c_Mg) + g * (math.log(c_Mg) ** 2)) / (2 * (n_bp - 1))
            return 1 / tem - kelvins
        else:

            tem = 1 / tm + a + b * math.log(c_Mg) + f_GC * (c + d * math.log(c_Mg)) + (
                    e + f * math.log(c_Mg) + g * (math.log(c_Mg) ** 2)) / (2 * (n_bp - 1))

            return 1 / tem - kelvins


def cal_all_tm(arr):
    """
    求这种切割位点的tm的标准差
    :param arr: 整个基因片段的切割位点
    :return: np.std(tm_list)：标准差， tm_list：每段的tm组成的list
    """
    tm_list = []
    arr = arr.astype(int)
    for i in range(1, len(arr)):
        tm_t = cal_tm(gene[arr[i - 1]: arr[i]])
        tm_list.append(tm_t)
    return np.std(tm_list), tm_list


def cal_first_tm():
    """
    计算第一段与第二段的tm值并且计算其标准差
    :return:
    """
    tem_res = []
    for i in range(max_len - min_len):
        mid_cut = min_len + i
        fir_tm = cal_tm(gene[:mid_cut])
        for j in range(max_len - min_len):
            end_cut = mid_cut + min_len + j
            sec_tm = cal_tm(gene[mid_cut:end_cut])
            tem_res.append([mid_cut, fir_tm, end_cut, sec_tm, np.std([fir_tm, sec_tm])])
    return tem_res


def cal_first_tm2(tm_mean):
    tem_res = []
    for i in range(max_len - min_len):
        fir_tm = cal_tm(gene[0:min_len + i])
        tem_res.append([min_len + i, fir_tm, np.std([tm_mean, fir_tm])])
    return tem_res


def cal_next_tm(tm_mea=0.):
    """
    计算第三段到最后的切割位点
    :return:
    """
    if tm_mea == 0.:
        result = cal_first_tm()
    else:
        result = cal_first_tm2(tm_mea)

    result = choose(result, count)
    result = np.delete(result, -1, axis=1)  # 删除最后一列

    fir_ans_tem = []  # 初步切割结果
    answer1_tem = []
    # 尝试控制answer不为0
    while len(fir_ans_tem) == 0:
        tem_res = []
        for i in range(len(result)):  # 遍历上一轮选择到的最优的
            fir_cut = int(result[i, -2])  # 这段gene开始
            for j in range(max_len - min_len):  #
                sec_cut = fir_cut + min_len + j  # 这段gene结束
                if sec_cut > len(gene) - 1:
                    sec_cut = len(gene) - 1
                tem_tm = cal_tm(gene[fir_cut: sec_cut])  # 计算这段gene的tm
                bef_tm = result[i, 1::2]  # 取出前面所有tm
                bef_tm = np.append(bef_tm, tem_tm)  # 将这段gene的tm添加到之前中
                tm_std = np.std(bef_tm)  # 计算标准差
                bef_arr = result[i, :]  # 获取数组，转化为列表
                bef_arr = bef_arr.tolist()
                tem_gene_tm = [sec_cut, tem_tm, tm_std]
                tem_list = bef_arr + tem_gene_tm

                if fir_cut + min_len > len(gene) - 1:
                    answer1_tem.append(tem_list)  # TODO最后一段是独立好还是分开好
                    break
                elif sec_cut == len(gene) - 1:
                    fir_ans_tem.append(tem_list)
                    break
                else:
                    tem_res.append(tem_list)
        # 可能刚刚好处理完
        if len(tem_res) != 0:
            tem_res = choose(tem_res, count)
            result = np.delete(tem_res, -1, axis=1)  # 删除最后一列
    # 挑选结果
    fir_ans_tem = choose(fir_ans_tem)
    if len(answer1_tem) > 0 and len(answer1_tem[0]) == len(answer1_tem[-1]):
        answer1_tem = choose(answer1_tem)
        if fir_ans_tem[0, -1] > answer1_tem[0, -1]:
            fir_ans_tem = answer1_tem
    index111 = np.array(fir_ans_tem[0][:-1:2])
    tm111 = np.array(fir_ans_tem[0][1::2])

    # show_w(index111, tm111, "init")

    return index111, tm111


def iteration(index_list, tm_list):  # 全局迭代，从左到右
    """
    全局迭代，
    :param index_list:上次得到最好的剪切位置
    :param tm_list:每个剪切片段的tm
    :return:
    """
    flag = [-1, -2, -3]  # 提前停止遍历的终止判断
    tem_max_len = max_len + 5
    tem_min_len = min_len - 5
    bias_len = 5
    while flag[-1] != flag[-3]:
        for i in range(len(tm_list)):  # 对于整条
            left = index_list[i]
            right = index_list[i + 1]
            # 遍历
            tem_result = []
            for j in range(1 - bias_len, bias_len):  # 对于每个片段,
                tem_left = left + j  # 左边新的切割位点
                if tem_left < 0:
                    # 当第一个位点小于0时，舍弃该情况
                    continue
                # 左边移动后前一个片段的长度判断：
                if i >= 1 and (
                        tem_left - index_list[i - 1] < tem_min_len or tem_left - index_list[i - 1] > tem_max_len):
                    # 当左边位点移动导致左边片段过长或者过短时，舍弃该情况
                    continue

                for k in range(1 - bias_len, bias_len):
                    tem_right = right + k  # 右边新的切割位点
                    if tem_right >= len(gene):
                        # 右边切割位点超越右边界
                        continue
                    # 右节点移动后下一个片段长度判断
                    if i + 1 < len(tm_list) and (
                            index_list[i + 2] - tem_right > tem_max_len or index_list[i + 2] - tem_right < tem_min_len):
                        # 当右边位点移动导致右边片段过长或者过短时，舍弃该情况
                        continue
                    # 当前片段长度是否正确
                    if tem_min_len > (tem_right - tem_left) or (tem_right - tem_left) > tem_max_len:
                        # 当前片段过长或者过短时
                        continue

                    tem_index_list = index_list.copy()
                    tem_index_list[i] = tem_left
                    tem_index_list[i + 1] = tem_right
                    tem_std, _ = cal_all_tm(tem_index_list)
                    tem_result.append([tem_left, tem_right, tem_std])

            tem_result = choose(tem_result, cou=1)
            index_list[i] = tem_result[0, 0]
            index_list[i + 1] = tem_result[0, 1]
            best_std, tm_list = cal_all_tm(index_list)  # 本次迭代得到最好的std和tm_list

        flag.append(best_std)
        # show_w(index_list[1:], tm_list, "d")

    return index_list, tm_list


def overlap(index_list, tm_list):
    index_list = index_list.astype(int)
    gene_list = []
    for i in range(len(tm_list)):  # 将gene截取出来存放在一个二维list中
        # 【原来第一个切割位点，修改后第一个切割位点，原来第二个切割位点，修改后第二个切割位点，修改后片段tm】
        gene_list.append([index_list[i], index_list[i], index_list[i + 1], index_list[i + 1], tm_list[i]])

    over_size = 6
    temp_avg_tm = [0, 1]  # flag 结束迭代的标志

    tem_max_op = 10  # 相邻两个片段间隔最大值

    tem_min_len = min_len - 10  # 切割后每个片段最小值
    x = 0
    while temp_avg_tm[-1] != temp_avg_tm[-2]:  # 迭代，终止条件

        for i in range(len(gene_list)):
            new_tm_list = tm_list.copy()
            tem_result = []
            for j in range(over_size):
                for k in range(over_size):
                    left = gene_list[i][1] + j
                    right = gene_list[i][2] - k

                    if right - left < tem_min_len:  # 长度小于限定值
                        continue
                    if (i == 0 and gene_list[i][1] - 0 > tem_max_op) or (
                            i > 0 and left - gene_list[i - 1][2] > tem_max_op):  # 这段与前一段的距离
                        continue
                    if (i + 1 == len(gene_list) and len(gene) - gene_list[i][2] - 1 > tem_max_op) or (
                            i + 1 < len(gene_list) and gene_list[i + 1][1] - right > tem_max_op):
                        continue

                    tem_tm = cal_tm(gene[left: right])
                    new_tm_list[i] = tem_tm
                    tm_std = np.std(new_tm_list)
                    tem_result.append([left, right, tem_tm, tm_std])
            if len(tem_result) == 0:
                continue
            tem_result = choose(tem_result, 1)
            gene_list[i][1] = int(tem_result[0, 0])
            gene_list[i][2] = int(tem_result[0, 1])
            tm_list[i] = tem_result[0, 2]
            temp_avg_tm.append(tem_result[0, 3])
        x = x + 1
        # show_w(index_list[1:], tm_list, x)

    a = np.argsort(tm_list)

    # 经过剪切后，在迭代一次，进行扩展
    for i in range(len(a)):
        if a[i] < 1 or a[i] + 2 > len(a):  # 先不管第一段和最后一段
            continue
        test_tm_list = tm_list.copy()
        test_result = []
        for j in range(int(gene_list[a[i]][1] - gene_list[a[i] - 1][2])):
            # print(gene_list[a[i] + 1][1], gene_list[a[i]][2], gene_list[a[i] + 1][1] - gene_list[a[i]][2])
            for k in range(int(gene_list[a[i] + 1][1] - gene_list[a[i]][2])):
                # print(gene_list[a[i]][1], gene_list[a[i]][1] - j)
                # print(gene_list[a[i]][2], gene_list[a[i]][2] + k)
                test_gene = gene[gene_list[a[i]][1] - j: gene_list[a[i]][2] + k]
                test_tm = cal_tm(test_gene)
                # print(test_tm, gene_list[a[i]][4])
                test_tm_list[a[i]] = test_tm
                test_std = np.std(test_tm_list)
                test_result.append([gene_list[a[i]][1] - j, gene_list[a[i]][2] + k, test_tm, test_std])
        if len(test_result) == 0:
            continue
        # 下表从0开始
        test_result = choose(test_result, 1)
        gene_list[a[i]][1] = test_result[0, 0]
        gene_list[a[i]][2] = test_result[0, 1]
        gene_list[a[i]][4] = test_result[0, 2]
        tm_list[a[i]] = test_result[0, 2]
    # show_w(index_list[1:], tm_list, "end")

    # for i in range(len(gene_list)):
    #     print("原来+{0}，更改{1}".format(gene_list[i][3] - gene_list[i][0], gene_list[i][2] - gene_list[i][1]))
    # print("每个间隙的长度:", end=" ")
    # for i in range(len(gene_list) - 1):
    #     print(gene_list[i+1][1] - gene_list[i][2], end=" ")
    # print()
    return gene_list


def get_gene_list(index_list):
    # 将每个片段返回
    res_index1 = []
    res_index2 = []

    dnaTable = {
        "A": "T", "T": "A", "C": "G", "G": "C"
    }

    gene_complement = ""
    for ele in gene:
        gene_complement += dnaTable[ele]

    # print(gene)
    # print(gene_complement)
    coun = 0
    for i in range(0, len(index_list), 2):
        if i + 1 < len(index_list):
            coun += 1
            res_index1.append(gene[int(index_list[i][1]): int(index_list[i + 1][2])])

    if len(index_list) % 2 != 0:  # 最后一片
        coun += 1
        res_index1.append(gene[int(index_list[-1][1]): int(index_list[-1][2])])

    # 第一片
    gene_tem = gene_complement[int(index_list[0][1]):int(index_list[1][2])]
    # print(gene_tem[::-1])
    res_index2.append(gene_tem[::-1])

    for i in range(1, len(index_list), 2):
        if i + 1 < len(index_list):
            coun += 1
            gene_tem = gene_complement[int(index_list[i][1]):int(index_list[i + 1][2])]
            res_index2.append(gene_tem[::-1])

    if len(index_list) % 2 == 0:  # 最后一片
        coun += 1
        gene_tem = gene_complement[int(index_list[-1][1]):int(index_list[-1][2])]
        res_index2.append(gene_tem[::-1])
    # print(coun)
    return res_index1, res_index2



def get_dict(gene_list1, gene_list2):
    tem_dic1 = {}
    for i in range(1, len(gene_list1) + 1):
        tem_dic1['+str'.format(i)] = gene_list1[i - 1]
    tem_dic2 = {}
    for i in range(1, len(gene_list2) + 1):
        tem_dic2['-str'.format(i)] = gene_list2[i - 1]
    return tem_dic1, tem_dic2


def cal(gene_t):
    global gene, min_len, max_len, count
    gene = gene_t
    # gene = get_gene('test_gene/test_gene3.txt')
    # print("基因长度:{0}".format(len(gene)))
    min_len, max_len = 15, 35
    count = 20  # 每一代取标准差最小的前count个
    # 初步贪心得到的结果
    index, tm = cal_next_tm()
    # show_w(index, tm, "f")
    # 初步贪心得到的结果，将tm取均值，然后当做起点
    index, tm = cal_next_tm(float(np.mean(tm)))
    # 对整体遍历
    index = np.insert(index, 0, [0])

    index, tm = iteration(index, tm)
    cut_of_index = overlap(index, tm)
    res1, res2 = get_gene_list(cut_of_index)

    print("拼接前基因片段个数:{0}".format(len(cut_of_index)))
    return res1, res2, len(cut_of_index)


# if __name__ == '__main__':
#     import time
#     start = time.time()
#     gen = "CGTTTTAAAGGGCCCGCGCGTTGCCGCCCCCTCGGCCCGCCATGCTGCTATCCGTGCCGCTGCTGCTCGGCCTCCTCGGCCTGGCCGTCGCCGAGCCTGCCGTCTACTTCAAGGAGCAGTTTCTGGACGGAGACGGGTGGACTTCCCGCTGGATCGAATCCAAACACAAGTCAGATTTTGGCAAATTCGTTCTCAGTTCCGGCAAGTTCTACGGTGACGAGGAGAAAGATAAAGGTTTGCAGACAAGCCAGGATGCACGCTTTTATGCTCTGTCGGCCAGTTTCGAGCCTTTCAGCAACAAAGGCCAGACGCTGGTGGTGCAGTTCACGGTGAAACATGAGCAGAACATCGACTGTGGGGGCGGCTATGTGAAGCTGTTTCCTAATAGTTTGGACCAGACAGACATGCACGGAGACTCAGAATACAACATCATGTTTGGTCCCGACATCTGTGGCCCTGGCACCAAGAAGGTTCATGTCATCTTCAACTACAAGGGCAAGAACGTGCTGATCAACAAGGACATCCGTTGCAAGGATGATGAGTTTACACACCTGTACACACTGATTGTGCGGCCAGACAACACCTATGAGGTGAAGATTGACAACAGCCAGGTGGAGTCCGGCTCCTTGGAAGACGATTGGGACTTCCTGCCACC";
#     r1, r2 = cal(gen)
#     analysis.tool.analysis.analysis_all(r1, r2)
#     end = time.time()
#
#     print('Running time: {0}}s Seconds'.format(end - start))
#     filename = 'write_data.txt'
#     with open(filename, 'w') as f:
#         f.write('Running time: {0}}s Seconds\n'.format(end - start))
