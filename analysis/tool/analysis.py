import time

import nupack
from nupack import *
from nupack import SetSpec, RawStrand, RawComplex, Strand, Complex, Tube, tube_analysis, \
    Model, complex_analysis, complex_concentrations, Domain, TargetStrand, analysis


class Analysis:

    def __init__(self, list_g1, list_g2, len1, temp, conc):
        self.list_g1 = list_g1  # 上面的基因片段
        self.list_g2 = list_g2  # 下面的基因片段
        self.gene_list = list_g1 + list_g2

        self.len_g1 = len(list_g1)  # 上面的基因片段数量
        self.len_g2 = len(list_g2)  # 下面的基因片段数量
        self.len_gene = self.len_g1 + self.len_g2

        self.len1 = len1  # 拼接前的基因片段数

        self.c_gene = conc  # 检验的时候反应的基因序列的浓度

        self.first_check = conc / 10  # 第一次验证时的浓度
        self.second_check = 1e-14  # 第二次验证时的浓度
        self.temp = temp  # 验证 时的温度

    def get_strands_tube_tow(self):
        # 获取试管中只有两条基因片段的所有情况
        tubes = []
        count = 1
        for i in range(self.len_gene):
            for j in range(i, self.len_gene):
                strands = {Strand(self.gene_list[i], name="t{0}:L{1}".format(count, i)): self.c_gene,
                           Strand(self.gene_list[j], name="t{0}:R{1}".format(count, j)): self.c_gene}
                tubes.append(Tube(strands=strands, complexes=SetSpec(max_size=2), name='t{0}'.format(count)))
                count += 1
        return tubes

    def get_tube(self, index1):
        # 找到能与之对应的 index
        if index1 < self.len_g1:
            if self.len1 % 2 == 0:  # 边界
                tem_err_list = [index1, index1 + self.len_g1, index1 + self.len_g1 + 1]
            else:
                tem_err_list = [index1, index1 + self.len_g1]
        else:
            if index1 == self.len_g1 + 1:
                tem_err_list = [index1, index1 - self.len_g1]
            elif index1 == self.len_g1 + self.len_g2 and self.len1 % 2 == 0:
                tem_err_list = [index1, index1 - self.len_g1 - 1]
            else:
                tem_err_list = [index1, index1 - self.len_g1 - 1, index1 - self.len_g1]
        return tem_err_list

    def analysis_two(self):
        my_model = Model(material='dna', celsius=self.temp)  # 温度
        tubes = self.get_strands_tube_tow()  # 得到每个试管中都有两条DNA单链
        tube_results = tube_analysis(tubes=tubes, model=my_model)
        all_conc = {}
        for t in tubes:
            for my_complex, conc in tube_results.tubes[t].complex_concentrations.items():
                all_conc[my_complex.name] = conc  # 反应后每个试管中DNA的浓度

        all_conc = sorted(all_conc.items(), key=lambda d: d[1], reverse=True)  # 排序

        error = {}  # 怀疑是错配的
        # 验证
        for k, v in all_conc:
            if k.count("+") == 1 and v > self.first_check:  # 将浓度换成输入的浓度
                # 根据：分割k， 然后根据名字具有顺序关系，然后确定是不是正确的配对
                tem_split = k.split('+')
                t1 = int(tem_split[0].split(':')[1][1:])  # 单链序号
                t2 = int(tem_split[1].split(':')[1][1:-1])
                if t1 > t2:
                    t1, t2 = t2, t1

                if t2 - t1 - self.len_g1 not in [-1, 0]:  # 错配
                    ste = '{0},{1}'.format(t1, t2)
                    if ste in error and v < error[ste]:
                        continue
                    else:
                        error[ste] = v
            elif v < self.first_check:  #
                break

        # 找出那两个的相邻的放到一起，然后反应，看下最后的结果
        # error_end = []  # 经过校验后还是错配的
        # for enu in error:
        #     str = enu.split(',')
        #     tem_err_list = [self.get_tube(int(str[0])), self.get_tube(int(str[1]))]
        #     if self.verification_two(tem_err_list):
        #         error_end.append(enu)

        tem_info = {}
        for key, val in error.items():
            arr = key.split(',')
            arr = [int(i) for i in arr]

            if arr[0] >= self.len_g1:
                str1 = 'R{0}'.format(arr[0] - self.len_g1)
            else:
                str1 = 'F{0}'.format(arr[0])

            if arr[1] >= self.len_g1:
                str2 = 'R{0}'.format(arr[1] - self.len_g1)
            else:
                str2 = 'F{0}'.format(arr[1])
            tem_info[str1 + ',' + str2] = val
        # print(len(tem_info), tem_info)

        # print("目标{0},list1:{1},list2:{2}".format(self.len1, self.len_g1, self.len_g2))
        # print("出错的{0},{1}".format(len(error), error))
        # print("最终检测还是出错的{0}".format(error_end))
        # print('总数{0}'.format(len(all_conc)))
        return tem_info

    def verification_two(self, list1):
        # 验证错配的是否有问题
        set1 = set()
        strands = {}
        for i in range(len(list1)):
            for j in range(len(list1[i])):
                if j == 0:
                    set1.add(list1[i][j])
                    strands[Strand(self.gene_list[list1[i][j] - 1],
                                   name="E:{1}:{0}".format(list1[i][j], i))] = self.c_gene * 2  # 改正浓度
                elif Strand(self.gene_list[list1[i][j] - 1], name=str(list1[i][j])) in strands.keys():
                    strands[Strand(self.gene_list[list1[i][j] - 1], name=str(list1[i][j]))] = self.c_gene * 2
                else:
                    strands[Strand(self.gene_list[list1[i][j] - 1], name=str(list1[i][j]))] = self.c_gene

        tube = Tube(strands=strands, complexes=SetSpec(max_size=len(list1)), name="test")
        my_model = Model(material='dna', celsius=self.temp)
        tube_results = tube_analysis(tubes=[tube], model=my_model)
        all_conc = {}
        # print(tube_results)
        # print("____________-")
        for my_complex, conc in tube_results.tubes[tube].complex_concentrations.items():
            all_conc[my_complex.name] = conc
            name = my_complex.name[1:-1]
            # if name.count("E") == 2: #
            if name.count("E") == len(list1) and conc > self.second_check:  #
                name_list = name.split("+")
                set_t = set()
                for i in range(len(list1)):
                    set_t.add(name_list[i][2])
                if len(set_t) == len(list1) and set_t == set1:  # 只关注错配的那几条
                    # print(name, conc)
                    return False
                # print(name, conc)

        new_conc = sorted(all_conc.items(), key=lambda d: d[1], reverse=True)
        # print("-------------------------------")
        # print(new_conc)

    def get_strands_tube_three(self):
        tubes = []
        count = 1  # 记录试管数目
        for i in range(self.len_gene):
            for j in range(i, self.len_gene):
                for k in range(j, self.len_gene):
                    strands = {Strand(self.gene_list[i], name="t{0}:L{1}".format(count, i)): self.c_gene,
                               Strand(self.gene_list[j], name="t{0}:M{1}".format(count, j)): self.c_gene,
                               Strand(self.gene_list[k], name="t{0}:R{1}".format(count, k)): self.c_gene}
                    tubes.append(Tube(strands=strands, complexes=SetSpec(max_size=3),  # max_size,使用变量代替？
                                      name='t{0}'.format(count)))  # complexes defaults to [A, B]
                    count += 1
        return tubes

    def analysis_three(self):
        my_model = Model(material='dna', celsius=self.temp)
        tubes = self.get_strands_tube_three()  # 得到每个试管中都有两条DNA单链
        start = time.time()
        tube_results = tube_analysis(tubes=tubes, model=my_model)
        print("analysis time:{0}".format(time.time() - start))
        all_conc = {}  # 记录结果
        for t in tubes:
            for my_complex, conc in tube_results.tubes[t].complex_concentrations.items():
                all_conc[my_complex.name] = conc  # 反应后每个试管中DNA的浓度
        all_conc = sorted(all_conc.items(), key=lambda d: d[1], reverse=True)  # 排序

        error = {}  # 怀疑是错配的
        k_cou = 0  # 记录浓度大于某个值的

        for k, v in all_conc:
            if k.count("+") == 2 and v > self.first_check:  # 将浓度换成输入的浓度
                k_cou += 1
                # 根据：分割k， 然后根据名字具有顺序关系，然后确定是不是正确的配对
                tem_split = k.split('+')
                t1 = int(tem_split[0].split(':')[1][1:])
                t2 = int(tem_split[1].split(':')[1][1:])
                t3 = int(tem_split[2].split(':')[1][1:-1])
                set_t = {abs(t1 - t2), abs(t1 - t3), abs(t2 - t3)}

                if set_t != {1, self.len_g1, self.len_g1 - 1}:
                    tem_arr = [t1, t2, t3]
                    tem_arr.sort()
                    key = ''
                    for i in tem_arr:
                        if i >= self.len_g1:
                            key = key + 'R{0},'.format(i - self.len_g1)
                        else:
                            key = key + 'F{0},'.format(i)
                    key = key[:-1]
                    if key in error and v < error[key]:
                        continue
                    else:
                        error[key] = v

            elif v < self.first_check:  #
                break

        # second check
        error_end = []  # 经过校验后还是错配的

        # 添加验证
        # print("验证:{0},{1},{2}".format(t1, t2, t3))
        # tem_err_list = self.get_tube(t1)
        # tem_err_list.extend(self.get_tube(t2))
        # tem_err_list.extend(self.get_tube(t3))
        # if self.verification_two(tem_err_list):
        #     error_end.append(k)

        # print("目标:{0},list1:{1},list2:{2}".format(int(self.len1 / 2), self.len_g1, self.len_g2))
        print("出错的:{0},{1}".format(len(error), error))
        # print("最终检测还是出错的{0}".format(error_end))
        # print("浓度大于1e-9数:{0}".format(k_cou))
        # print('总数:{0}'.format(len(all_conc)))
        return error

    def get_strands(self):
        name = 65
        strands = {}
        for strand in self.list_g1:
            strands[Strand(strand, name=chr(name))] = self.c_gene
            name += 1
        for strand in self.list_g2:
            strands[Strand(strand, name=chr(name))] = self.c_gene
            name += 1
        return strands

    def analysis_all(self):
        count = self.len_g1 + self.len_g2
        strands = self.get_strands()
        my_model = Model(material='dna', celsius=self.temp)
        t1 = Tube(strands=strands, complexes=SetSpec(max_size=count), name='t1')  # complexes defaults to [A, B]
        tube_results = tube_analysis(tubes=[t1], model=my_model)
        # print(tube_results)
