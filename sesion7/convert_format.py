#!/usr/bin/env python

import argparse

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def get_primal_form(svm):
    count = len(svm['support_vectors'])
    df = svm['decision_functions']
    alphas= df[0]['alpha']
    rho = df[0]['rho']
    var_count=svm['var_count']
    support_vector=[0.0 for i in range(var_count)]
    for r in range(count):
        myalpha = alphas[r]
        vec=svm['support_vectors'][r]
        for j,v in enumerate(vec):
            support_vector[j]+=(-myalpha)*(v)
    support_vector.append(rho)
    return support_vector
        

if __name__ == '__main__':
    p = argparse.ArgumentParser("convert_format.py")
    p.add_argument("model",default="model.svm",
                action="store", help="Original model SVM")
    opts = p.parse_args()

    lines=[]
    for line in  open(opts.model, 'r'):
        line=line.replace(":",": ")
        line=line.replace("!!opencv-ml-svm","")
        line=line.replace("!!opencv-matrix","")
        lines.append(line)
    lines="".join(lines[1:])
    data=load(lines)


    svm_descriptor=get_primal_form(data['my_svm'])
    for line in svm_descriptor:
        print line


