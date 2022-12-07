from vutil.comparitors import intersection


#l1 = ['a', 'b', 'c', 'c', 'c', 'b', 'c']
#l2 = ['a', 'b', 'c', 'b','e']
#l1 = ['a','a','b','b','b','c']
#l2 = ['a','c','b','b','b','a']
l1 = ['WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'APPMEM128CPU4', 'APPMEM128CPU4', 'APPMEM64CPU1', 'APPMEM128CPU4', 'DBMEM512CPU8', 'DBMEM512CPU8']
l2 = ['WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'WEBMEM256CPU2', 'APPMEM128CPU4', 'APPMEM128CPU4', 'APPMEM128CPU4', 'APPMEM128CPU4', 'DBMEM128CPU2']


from collections import Counter

c1 = Counter(l1)
c2 = Counter(l2)

print("c1",c1)
print("c2:",c2)

diff1 = c1-c2
diff2 = c2-c1
print("diff:",diff1)
print("diff2",diff2)

print("l1:",l1)
print("l2:",l2)
diffc = list(diff1.elements())
diffd = list(diff2.elements())
diffe = diffc + diffd + intersection(l1,l2)
print("ORED:",diffe)
print("ANDED:",intersection(l1,l2))
simil = len(intersection(l1,l2))/len(diffe)
print(simil)