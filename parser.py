import sqlite3
from collections import Counter, defaultdict
from functools import lru_cache
from copy import deepcopy

db = sqlite3.connect('data.sql')
cur = db.cursor()

cur.execute('select * from tokenInfo')
tok = cur.fetchall()
adr = {i[0]:i[4].lower() for i in tok}
decimals = {i[0]:int(i[3]) for i in tok if i[3]}

cur.execute('select * from pancakeFactory')
rawPancake = cur.fetchall()
rawPancake = [list(i) for i in rawPancake if i[3] and i[5] and i[2] in decimals and i[4] in decimals]
for i in rawPancake:
    i[3] = int(i[3])/10**decimals[i[2]]
    i[5] = int(i[5])/10**decimals[i[4]]
rawPancake = [i for i in rawPancake if i[3] and i[5]]

priceEstimator = {'0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c':1}

rawPancake2 = rawPancake
rawPancake = deepcopy(rawPancake)

while rawPancake:
    print(len(rawPancake), len(priceEstimator))
    n_raw = []
    for i in rawPancake:
        if i[2] in priceEstimator:
            if i[4] not in priceEstimator:
                priceEstimator[i[4]] = i[3] * priceEstimator[i[2]] / i[5] 
                
        elif i[4] in priceEstimator:
            priceEstimator[i[4]] = i[5] * priceEstimator[i[4]] / i[3]
        else:
            n_raw.append(i)

    if len(n_raw) == len(rawPancake):
        break
    else:
        rawPancake = n_raw

panPairs = [ [i[2], i[4], i[3]*priceEstimator[i[2]]+i[5]*priceEstimator[i[4]]] for i in rawPancake2
             if i[2] in adr and i[4] in adr and i[2] in priceEstimator and i[4] in priceEstimator]
panPairs.sort(reverse=True, key = lambda x: x[2])
panPairs = [ tuple(i[:2]) for i in panPairs]
print('len pan', len(panPairs))

counters = Counter()
for a,b in panPairs:
    counters[a] += 1
    counters[b] += 1

sym = defaultdict(list)
for i in adr:
    sym[adr[i]].append([counters[i], i])
for i in sym:
    sym[i].sort()

allowed = set()
for i in sorted(sym):
    sym[i].sort()
    if len(sym[i]) == 1 or (sym[i][-1][0] and sym[i][-1][0] > sym[i][-2][0] * 2):
        allowed.add(sym[i][-1][1])
        sym[i] = sym[i][-1][1]
    else:
        del sym[i]

        
adr = {i:adr[i] for i in adr if i in allowed}
    
 
panPairs = [ (adr[i[0]], adr[i[1]]) for i in panPairs if i[0] in adr and i[1] in adr]

cur.execute('select * from binancePairs')
bn = cur.fetchall()
foB = set([ (i[0].lower(), i[1].lower()) for i in bn if i[0]])
reB = set([ (i[1].lower(), i[0].lower()) for i in bn if i[0]])

cur.execute('select * from kucoinPairs')
ku = cur.fetchall()
foK = set([ (i[0].lower(), i[1].lower()) for i in ku if i[0]])
reK = set([ (i[1].lower(), i[0].lower()) for i in ku if i[0]])

foKB = foK&foB
reKB = foK&reB

foB = [i for i in panPairs if i in foB and sym[i[0]] and sym[i[1]]]
reB = [i for i in panPairs if i in reB and sym[i[0]] and sym[i[1]]]

foK = [i for i in panPairs if i in foK and sym[i[0]] and sym[i[1]]]
reK = [i for i in panPairs if i in reK and sym[i[0]] and sym[i[1]]]

tokens = set()
cA = 30
for i,j in foB[:cA]:
    tokens.add(i)
    tokens.add(j)
    print('forward PB', i, j)
print('PB >', len(foB))

for i,j in reB[:cA]:
    tokens.add(i)
    tokens.add(j)
    print('re PB', i, j)
print('PB <', len(reB))
 
for i,j in foK:
    tokens.add(i)
    tokens.add(j)
    print('forward Pk', i, j)
print('PK >', len(foK))

for i,j in reK:
    tokens.add(i)
    tokens.add(j)
    print('re Pk', i, j)
print('PK <', len(reK))

syms = set()

foKB = list(foKB)
reKB = list(reKB)

for i,j in foKB[:cA]:
    syms.add(i)
    syms.add(j)
    print('forward BK', i, j)
print('KB >', len(foKB))
for i,j in reKB[:cA]:
    syms.add(i)
    syms.add(j)
    print('re BK', i, j)
print('KB <', len(reKB))



print('Token addresses from')
for i in tokens:
    print(i, sym[i])
    #cur.execute('insert or ignore into tokenInGame values ("'+sym[i]+'");')


            
   
    
print()
print()
print('Syms')
for i in syms-tokens:
    #cur.execute('insert or ignore into symbolsInGame values ("'+i.upper()+'");')
    print(i)


db.commit()


db.close()
