from itertools import combinations
from collections import Counter
from vutil.db import metricWriter

def calcSim(url,dc,doc):
# A very simple way to calculate the similarity among two lists of objects is finding the distinct elements 
# and also common elements and computing it’s quotient. 
# The result is then multiplied by 100, to get the percentage.

    print(" .      Calculating site similarity for url:",url[0])
    print(" .      Datacenters ",dc[0],dc[1])
 
   # initialize lists
    l1 = list(doc[0].split(" "))
    l2 = list(doc[1].split(" "))
    L3 = ['WEB','APP','DB','MAINFRAME',"SLB"]

    for func in L3:
        #print(func)
        l3 = []
        l4 = []
        for dce in l1:
            if dce.startswith(func):
                l3.append(dce)
        for dce in l2:
            if dce.startswith(func):
                l4.append(dce)

        #Following code is basically is AND'ing and OR'ing two lists with duplicate elements (un-normalized)
        c1 = Counter(l3)
        c2 = Counter(l4)
        diff1 = c1-c2
        diff2 = c2-c1
        #print("diff:",diff1)
        #print("diff2",diff2)

        #print("l3:",l4)
        #print("l3:",l4)
        ss = False
        diffc = list(diff1.elements())
        diffd = list(diff2.elements())
        diffe = diffc + diffd + intersection(l3,l4)
        #print("ORED:"diffe)
        #print("ANDED:",intersection(l3,l4))
        alen = len(intersection(l3,l4))
        olen = len(diffe)
        #print(alen,olen)
        if (olen>0):
            if (alen==0 and olen>0):
                ss = True
            res = alen/olen * 100

            # (Using sets (normalized data) - Percentage similarity of lists using "|" operator + "&" operator + set()
            #res = len(set(l1) & set(l2)) / float(len(set(l1) | set(l2))) * 100
            
            #print("l3:",l3)
            #print("l4:",l4)
            #print("set1:",set(l3))
            #print("set2:",set(l4))
            #print("AND",len(set(l3) & set(l4)))
            #print("OR",float(len(set(l3) | set(l4))))
            #print("++++++")
            
            # Write Metrics
            sitepair = dc[0] + ' ' + dc[1]
            metricWriter("PERCENT SIMILAR",url[0],dc[0],dc[1],sitepair,func,res,' ' . join(str(element) for element in l3),' ' . join(str(element) for element in l4))
            # printing result
            sss = ""
            if ss == True:
                sss = "  Single site function for this deployment environment pair."      
            print(" .         Percentage similarity " + func + " is " + str(res) + sss)
    
    return

def calcLocalHA(url,dc,doc):
# A very simple way to calculate HA - basic assumption is >1 is good to go.

    print(" .      Calculating local HA for url:",url)
    print(" .      Datacenter ",dc)
 
   # initialize lists
    l1 = list(doc.split(" "))
    L3 = ['WEB','APP','DB','MAINFRAME',"SLB"]

    for func in L3:
        #print(func)
        l3 = []
        for dce in l1:
            if dce.startswith(func):
                l3.append(dce)

        if len(l3) >0:
            c1 = Counter(l3)
            lha = 0
            for key,value in c1.items():
                if value >  1:
                    lha=1
            
    
            # Write Metrics
            sitepair = ''
            metricWriter("LOCAL HA",url,dc,'',sitepair,func,lha,' ' . join(str(element) for element in l1),'')
            print(" .         Local HA " + func + " is " + str(lha))

    return

def intersection(A,B):
    c_a=Counter(A)
    c_b=Counter(B)
    duplicates=[]
    for c in c_a:
        duplicates+=[c]*min(c_a[c],c_b[c])
    return duplicates


def cosineSim(url,dc,doc):
# This needs work, wonky results
# Cosine similarity.
    print("Calculating similarity for url:",url[0])
    print("Datacenters ",dc[0],dc[1])
    # Document Vectorization
    #nlp = en_core_web_sm.load()
    #doc1, doc2 = nlp(doc[0]).vector, nlp(doc[1]).vector
    ## Cosine Similarity
    #result = 1 - spatial.distance.cosine(doc1, doc2)
    #print(result)
    return

def rSubset(arr):
    # Find the combinations of deployment environments
    return list(combinations(arr, 2))
