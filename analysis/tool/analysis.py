import nupack
from nupack import *
from nupack import SetSpec, RawStrand, RawComplex, Strand, Complex, Tube, tube_analysis, \
    Model, complex_analysis, complex_concentrations, Domain, TargetStrand, analysis

def get_strands(gene_list1, gene_list2):
    name = 65
    strands = {}
    for strand in gene_list1:
        strands[Strand(strand, name=chr(name))] = 1e-8
        name += 1
    for strand in gene_list2:
        strands[Strand(strand, name=chr(name))] = 1e-8
        name += 1
    return strands


def get_strands_tube_tow(gene_list1, gene_list2):
    gene_list = gene_list1 + gene_list2
    tubes = []
    count = 1
    for i in range(len(gene_list)):
        for j in range(i, len(gene_list)):
            strands = {}
            strands[Strand(gene_list[i], name="t{0}:L{1}".format(count, i+1))] = 1e-8
            strands[Strand(gene_list[j], name="t{0}:R{1}".format(count, j+1))] = 1e-8  # TODO 每条DNA单链初始浓度
            tubes.append(Tube(strands=strands, complexes=SetSpec(max_size=2),
                              name='t{0}'.format(count)))  # complexes defaults to [A, B]
            count += 1
    return tubes


def verification_two(gene_list, list1):
    # 验证错配的是否有问题
    print(list1)
    set1 = set()
    strands = {}
    for i in range(len(list1)):
        for j in range(len(list1[i])):
            if j == 0:
                set1.add(list1[i][j])
                strands[Strand(gene_list[list1[i][j]-1], name="E:{1}:{0}".format(list1[i][j], i) )] = 2e-8  # TODO 改正浓度

            elif Strand(gene_list[list1[i][j]-1], name=str(list1[i][j])) in strands.keys():
                strands[Strand(gene_list[list1[i][j]-1], name=str(list1[i][j]))] = 2e-8
            else:
                strands[Strand(gene_list[list1[i][j]-1], name=str(list1[i][j]))] = 1e-8

    tube = Tube(strands=strands, complexes=SetSpec(max_size=len(list1)), name="test")
    my_model = Model(material='dna', celsius=37)
    tube_results = tube_analysis(tubes=[tube], model=my_model)
    all_conc = {}
    # print(tube_results)
    # print("____________-")
    for my_complex, conc in tube_results.tubes[tube].complex_concentrations.items():
        all_conc[my_complex.name] = conc
        name = my_complex.name[1:-1]
        # if name.count("E") == 2: #
        if name.count("E") == len(list1) and conc > 1e-14: #
            name_list = name.split("+")
            set_t = set()
            for i in range(len(list1)):
                set_t.add(name_list[i][2])
            if len(set_t) == len(list1) and set_t == set1:  # 只关注错配的那几条
                print(name, conc)
                return False
            # print(name, conc)

    new_conc = sorted(all_conc.items(), key=lambda d: d[1], reverse=True)
    print("-------------------------------")
    # print(new_conc)


def get_tube(index1,len_gene1, len_gene2, len1 ):
    # 找到能与之对应的
    tem_err_list = []

    if index1 < len_gene1:
        if len1 % 2 == 0:  # 边界
            tem_err_list.append([index1, index1 + len_gene1, index1 + len_gene1 + 1])
        else:
            tem_err_list.append([index1, index1 + len_gene1])
    else:
        if index1 == len_gene1 + 1:
            tem_err_list.append([index1, index1 - len_gene1])
        elif index1 == len_gene1 + len_gene2 and len1 % 2 == 0:
            tem_err_list.append([index1, index1 - len_gene1 - 1])
        else:
            tem_err_list.append([index1, index1 - len_gene1 - 1, index1 - len_gene1])
    return tem_err_list


def analysis_two(gene_list1, gene_list2, len1):
    my_model = Model(material='dna', celsius=37)
    tubes = get_strands_tube_tow(gene_list1, gene_list2)  # 得到每个试管中都有两条DNA单链
    tube_results = tube_analysis(tubes=tubes, model=my_model)
    gene_list = gene_list1+gene_list2
    # print(tube_results)
    all_conc = {}
    for t in tubes:
        for my_complex, conc in tube_results.tubes[t].complex_concentrations.items():
            # print('The equilibrium concentration of %s is %.2e M' % (my_complex.name, conc))
            # if my_complex.name not in all_conc:
            all_conc[my_complex.name] = conc  # 反应后每个试管中DNA的浓度

    new_conc = sorted(all_conc.items(), key=lambda d: d[1], reverse=True)

    error = []  # 怀疑是错配的
    k_cou = 0  # 记录浓度大于某个值的

    # 验证
    # 找出那两个的相邻的放到一起，然后反应，看下最后的结果
    error_end = []  # 经过校验后还是错配的

    for k, v in new_conc:
        if k.count("+") == 1 and v > 2e-9:  # TODO 将浓度换成输入的浓度
            # print(k, v)
            k_cou += 1
            # 根据：分割k， 然后根据名字具有顺序关系，然后确定是不是正确的配对
            tem_split = k.split('+')
            t1 = int(tem_split[0].split(':')[1][1:])  # 单链序号
            t2 = int(tem_split[1].split(':')[1][1:-1])

            if abs(t1 - t2) - len(gene_list1) not in [0,1]:  # 错配
                error.append(k)
                # TODO 添加验证
                print("验证:{0},{1}".format(t1, t2))
                tem_err_list = get_tube(t1, len(gene_list1), len(gene_list2), len1)
                tem_err_list = tem_err_list + get_tube(t2, len(gene_list1), len(gene_list2), len1)
                # tem_err_list.append([t2, t2 - len(gene_list1) - 1, t2 - len(gene_list1)])

                if verification_two(gene_list, tem_err_list):
                    error_end.append(k)
    # if len(error_end):
    #     return False
    print("目标{0},list1:{1},list2:{2}".format(len1, len(gene_list1), len(gene_list2)))
    print("出错的{0}".format(error))
    print("浓度大于1e-9数{0}".format(k_cou))
    print('总数{0}'.format(len(new_conc)))


def get_strands_tube_three(gene_list1, gene_list2):
    gene_list = gene_list1 + gene_list2
    tubes = []
    count = 1  # 记录试管数目

    for i in range(len(gene_list)):
        for j in range(i, len(gene_list)):
            for k in range(j, len(gene_list)):
                strands = {}
                strands[Strand(gene_list[i], name="t{0}:L{1}".format(count, i+1))] = 1e-8
                strands[Strand(gene_list[j], name="t{0}:M{1}".format(count, j+1))] = 1e-8  # TODO 每条DNA单链初始浓度
                strands[Strand(gene_list[k], name="t{0}:R{1}".format(count, k+1))] = 1e-8  # TODO 每条DNA单链初始浓度
                tubes.append(Tube(strands=strands, complexes=SetSpec(max_size=3),  # TODO max_size,使用变量代替？
                                  name='t{0}'.format(count)))  # complexes defaults to [A, B]
                count += 1
    return tubes


def analysis_three(gene_list1, gene_list2, len1):
    gene_list = gene_list1+gene_list2

    my_model = Model(material='dna', celsius=37)
    tubes = get_strands_tube_three(gene_list1, gene_list2)  # 得到每个试管中都有两条DNA单链
    tube_results = tube_analysis(tubes=tubes, model=my_model)
    # print(tube_results.complexes)
    all_conc = {}  # 记录结果
    for t in tubes:
        for my_complex, conc in tube_results.tubes[t].complex_concentrations.items():
            all_conc[my_complex.name] = conc  # 反应后每个试管中DNA的浓度

    new_conc = sorted(all_conc.items(), key=lambda d: d[1], reverse=True)  # 排序

    error = []  # 怀疑是错配的
    k_cou = 0  # 记录浓度大于某个值的
    error_end = []  # 经过校验后还是错配的

    for k, v in new_conc:
        if k.count("+") == 2 and v > 1e-9:  # TODO 将浓度换成输入的浓度
            # print(k, v)
            k_cou += 1
            # 根据：分割k， 然后根据名字具有顺序关系，然后确定是不是正确的配对
            tem_split = k.split('+')

            t1 = int(tem_split[0].split(':')[1][1:])
            t2 = int(tem_split[1].split(':')[1][1:])
            t3 = int(tem_split[2].split(':')[1][1:-1])
            set_t = {abs(t1-t2), abs(t1-t3), abs(t2-t3)}

            if set_t != {1, len(gene_list1)+1, len(gene_list1)+2}:
                error.append(k)
                # 添加验证
                print("验证:{0},{1},{2}".format(t1, t2, t3))
                tem_err_list = get_tube(t1, len(gene_list1), len(gene_list2), len1)
                tem_err_list = tem_err_list + get_tube(t2, len(gene_list1), len(gene_list2), len1)
                tem_err_list = tem_err_list + get_tube(t3, len(gene_list1), len(gene_list2), len1)

                verification_two(gene_list, tem_err_list)

    print("目标:{0},list1:{1},list2:{2}".format(int(len1/2), len(gene_list1), len(gene_list2)))
    print("出错的:{0},{1}".format(len(error), error))
    print("浓度大于1e-9数:{0}".format(k_cou))
    print('总数:{0}'.format(len(new_conc)))


def analysis_all(gene_list1, gene_list2):
    count = len(gene_list1) + len(gene_list2)
    strands = get_strands(gene_list1, gene_list2)
    my_model = Model(material='dna', celsius=37)
    t1 = Tube(strands=strands, complexes=SetSpec(max_size=count), name='t1')  # complexes defaults to [A, B]
    tube_results = tube_analysis(tubes=[t1], model=my_model)
    print(tube_results)