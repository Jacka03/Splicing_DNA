import nupack
from nupack import *


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

def get_strands1(gene_list1, gene_list2):
    count_tem = 1
    strands = {}
    for strand in gene_list1:
        strands[Strand(strand, name="R" + str(count_tem))] = 1e-8
        count_tem += 1
    count_tem = 1
    for strand in gene_list2:
        strands[Strand(strand, name="L" + str(count_tem))] = 1e-8
        count_tem += 1
    return strands


def get_strands_tube(gene_list1, gene_list2):
    gene_list = gene_list1 + gene_list2
    name = 64
    tubes = []
    count = 1
    for i in range(len(gene_list)):
        name += 1
        name1 = name
        for j in range(i, len(gene_list)):

            strands = {}
            strands[Strand(gene_list[j], name=chr(name1))] = 1e-8
            strands[Strand(gene_list[i], name=chr(name))] = 1e-8
            name1 += 1
            tubes.append(Tube(strands=strands, complexes=SetSpec(max_size=2),
                              name='t{0}'.format(count)))  # complexes defaults to [A, B]
            count += 1

    return tubes


def analysis_two(gene_list1, gene_list2):
    my_model = Model(material='dna', celsius=37)
    tubes = get_strands_tube(gene_list1, gene_list2)
    # print(tubes)

    tube_results = tube_analysis(tubes=tubes, model=my_model)

    print(tube_results)
    print('---------------')
    cou = 2 * (len(gene_list1) + len(gene_list2)) - 1
    all_conc = {}
    for t in tubes:
        for my_complex, conc in tube_results.tubes[t].complex_concentrations.items():
            # print('The equilibrium concentration of %s is %.2e M' % (my_complex.name, conc))
            # if my_complex.name not in all_conc:
            all_conc[my_complex.name] = conc

    new_conc = sorted(all_conc.items(), key=lambda d: d[1], reverse=True)
    i = 0
    k_cou = 0
    all_cou = 0
    for k, v in new_conc:
        all_cou += 1
        print(k, v)
        if len(k) == 3:
            k_cou += 1

        i += 1
        if i == cou:
            print('-----------')
            print('单链总数{0}'.format(k_cou))
            print('单链总数{0}(预估值）'.format(len(gene_list1) + len(gene_list2)))
    # print(new_conc)
    print('总数'.format(all_cou))


def analysis_all(gene_list1, gene_list2):
    count = len(gene_list1) + len(gene_list2)
    strands = get_strands(gene_list1, gene_list2)

    my_model = Model(material='dna', celsius=37)
    t1 = Tube(strands=strands, complexes=SetSpec(max_size=count), name='t1')  # complexes defaults to [A, B]
    tube_results = tube_analysis(tubes=[t1], model=my_model)

    print(tube_results)
    # filename = 'write_data1.txt'
    # with open(filename, 'w') as f:
    #     f.write(tube_results)

