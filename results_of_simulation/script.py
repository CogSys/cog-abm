# -*- coding: utf-8 -*-

#  data=pd.read_csv("data_no_shift_sim/data_max_max_clos_CSA0.txt", delim_whitespace=True, header=None)

import xlwt
import numpy as np
import cPickle as pickle
t = [[]]
for i in xrange(20):
    f = open("data_no_shift_sim/data_max_max_clos_CSA"+format(i)+".txt")
    lines = []
    for line in f:
        lines.append(line.split()[1:])
    t.append([[float(x) for x in l] for l in lines ])

       
mean = []
for sim in t[1:]:
    mean.append([])
    for iter in sim:
        mean[-1].append(np.mean(iter))

print mean[0]
m_mean = []
for i in xrange(len(mean[1])):
    suma = 0
    for j in xrange(len(mean)):
        suma += mean[j][i]
    m_mean.append(suma/len(mean))
print m_mean




book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Max_Max_Clos mean of mean")
for i in xrange(len(m_mean)):
#    sheet1.write(0,0,"iter")
#    sheet1.write(0,1,"max_max_clos_CSA")
    sheet1.write(i+1,1,m_mean[i])
    sheet1.write(i+1,0,50*i)
f.close()

#book.save("raport.xls")

#m_max_max_clos_CSA=open("m_max_max_clos_CSA", 'wb')
#pickle.dump(t, m_max_max_clos_CSA)


################################################################################
#### MAX VAR CONS

t = [[]]
for i in xrange(20):
    f = open("data_no_shift_sim/data_max_var_cons_CSA"+format(i)+".txt")
    lines = []
    for line in f:
        lines.append(line.split()[1:])
    t.append([[float(x) for x in l] for l in lines ])


mean = []
for sim in t[1:]:
    mean.append([])
    for iter in sim:
        mean[-1].append(np.mean(iter))

print mean[0]
m_mean = []
for i in xrange(len(mean[1])):
    suma = 0
    for j in xrange(len(mean)):
        suma += mean[j][i]
    m_mean.append(suma/len(mean))
print m_mean





for i in xrange(len(m_mean)):

    sheet1.write(i+1,2,m_mean[i])

f.close()


################################################################################
#### MIN AVG BET

t = [[]]
for i in xrange(20):
    f = open("data_no_shift_sim/data_min_avg_bet_CSA"+format(i)+".txt")
    lines = []
    for line in f:
        lines.append(line.split()[1:])
    t.append([[float(x) for x in l] for l in lines ])


mean = []
for sim in t[1:]:
    mean.append([])
    for iter in sim:
        mean[-1].append(np.mean(iter))

print mean[0]
m_mean = []
for i in xrange(len(mean[1])):
    suma = 0
    for j in xrange(len(mean)):
        suma += mean[j][i]
    m_mean.append(suma/len(mean))
print m_mean



for i in xrange(len(m_mean)):
    sheet1.write(i+1,3,m_mean[i])

f.close()


################################################################################
#### MIN AVG CLUST

t = [[]]
for i in xrange(20):
    f = open("data_no_shift_sim/data_min_avg_clust_CSA"+format(i)+".txt")
    lines = []
    for line in f:
        lines.append(line.split()[1:])
    t.append([[float(x) for x in l] for l in lines ])


mean = []
for sim in t[1:]:
    mean.append([])
    for iter in sim:
        mean[-1].append(np.mean(iter))

print mean[0]
m_mean = []
for i in xrange(len(mean[1])):
    suma = 0
    for j in xrange(len(mean)):
        suma += mean[j][i]
    m_mean.append(suma/len(mean))
print m_mean



for i in xrange(len(m_mean)):
    sheet1.write(i+1,4,m_mean[i])

book.save("raportCSA.xls")

f.close()

#tt=open("data_no_shift_sim/data_max_max_clos_CSA0.txt")
#line=tt.readline().split()
#print line
#print "koniec"
#i=0
#for line in tt:
#    edge = line.split()
#    i += 1;
#    print edge
#    if i > 3:
#        break
#
