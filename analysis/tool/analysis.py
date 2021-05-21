import nupack
from nupack import *


def analysis_all(gene_list1, gene_list2):
    count = len(gene_list1) + len(gene_list2)
    name = 65
    dict = {}
    for strand in gene_list1:
        dict[Strand(strand, name=chr(name))] = 1e-8
        name+=1

    for strand in gene_list2:
        dict[Strand(strand, name=chr(name))] = 1e-8
        name+=1


    # print(dict)

    my_model = Model(material='dna', celsius=37)
    # A = Strand('TGAGATTTAGTTCAACGGATATGCAATACCAAAAGATGCTATTTGCTGCTATTC', name='A')
    # B = Strand('TTTGTGCATTAAGTTCGAAGAAGATCTCAATCTATAATGAAGAAATGATAGTAGCTGGTTGTTTTATAGGCT', name='B')
    # C = Strand('AGATTGAGATCTTCTTCGAACTTAATGCACAAATAAATAGAATAGCAGCAAATAGCATCTTTTGGT', name='C')
    # D = Strand('ACCTAAACTCTTCCGACTGAATATGAGAAAGCCTATAAAACAACCAGCTACTATCATTTCTTC', name='D')

    # t1 = Tube(strands={a: 1e-8, b: 1e-9, c: 1e-8, d: 1e-9}, complexes=SetSpec(max_size=4), name='t1')
    # tube_results = tube_analysis(tubes=[t1, t2], model=model1)

    t1 = Tube(strands=dict, complexes=SetSpec(max_size=count), name='t1')  # complexes defaults to [A, B]
    # print(t1.complexes)

    tube_results = tube_analysis(tubes=[t1], model=my_model)
    #
    print(tube_results)

    pass

