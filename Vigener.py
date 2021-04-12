from math import sqrt

tabela = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
angleskaFrekv = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.996, 0.153,
                             0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056,
                             2.758, 0.978, 2.360, 0.150, 1.974, 0.074]

def nastaviKljuc(orig, dolzinaBesede):
    if(len(orig)<dolzinaBesede):
        while(len(orig) * 2 <= dolzinaBesede):
            orig += orig
        
        if(len(orig) < dolzinaBesede):
            orig += orig[0:(dolzinaBesede-len(orig))]
    #print(len(orig))
    return orig

def Encrypt(b,k):
    k = nastaviKljuc(k, len(b))
    tabelaBesedila = []
    tabelaKljucev = []
    zakodiranaBeseda = []
    for i in b:
        tabelaBesedila.append(i) #imamo besedilo, ki ga zelimo sifrirati po celicah
    for i in k:
        tabelaKljucev.append(i) #imamo kljuc po celicah
    
    #print(tabelaKljucev, tabelaBesedila)
    for i in range(len(b)):
        indPlain = tabela.index(tabelaBesedila[i])
        #print(indPlain)
        indKey = tabela.index(tabelaKljucev[i])
        #print(indKey)
        tole = (indPlain + indKey)%26
        #print(tole)    
        zakodiranaBeseda.append(tabela[tole])
    #print(zakodiranaBeseda)
    return zakodiranaBeseda
    
def Decrypt(c,k):
    #frekvecnePojav(c)
    k = nastaviKljuc(k, len(c))
    tabelaKode = []
    tabelaKljucev = []
    odkodiranaBeseda = []
    for i in c:
        tabelaKode.append(i) #imamo besedilo, ki ga zelimo desifrirati po celicah
    for i in k:
        tabelaKljucev.append(i) #imamo kljuc po celicah
    
    for i in range(len(c)):
        indCode = tabela.index(tabelaKode[i])
        #print(indPlain)
        indKey = tabela.index(tabelaKljucev[i])
        #print(indKey)
        tole = (indCode - indKey)%26
        #print(tole)    
        odkodiranaBeseda.append(tabela[tole])
    #print(odkodiranaBeseda)

    return odkodiranaBeseda

def frekvecnePojav(besedilo): #dobimo kolikokrat se pojavi crka v kriptogramu
    frekv = [0]*26
    for i in range(len(besedilo)):
        ind = tabela.index(besedilo[i])
        frekv[ind] += 1
        #print('indeks',ind)
    #print('frekv',frekv) 
    return frekv

def poisciPonavljanje(kriptogram):
    slovar = {} #kljuc je podniz, vrednost je razdalja
    for dolzina in range(3,6): #kljuc mora biti saj 3 dolg, pri nas vec kot 5 ne bo
        for start in range(len(kriptogram) - dolzina):
            podniz = kriptogram[start:start+dolzina]
            for i in range(start + dolzina, len(kriptogram) - dolzina):
                if(kriptogram[i:i+dolzina] == podniz):
                    if(podniz not in slovar):
                        slovar[podniz] = []
                    slovar[podniz].append(i-start)

    return slovar

def deljitelji(num):
    factors = [] # the list of factors found
    i = 1
    while(i <= num):
        if(num % i == 0):
            factors.append(i)
        i = i+1
    if 1 in factors:
        factors.remove(1)

    return list(set(factors))
  
def najpogostejsiFaktorji(vsi):
    stevec = {} 
    for podniz in vsi:
        factorList = vsi[podniz]
        for faktor in factorList:
            if faktor not in stevec:
                stevec[faktor] = 0
            stevec[faktor] += 1  #dobimo kolikokrat se ponovi, se v slovar

    slovarFakt = []
    for factor in stevec:
        if factor <= 16: #kljuci ne daljsi od tega
            slovarFakt.append( (factor, stevec[factor]) )
    slovarFakt.sort(key=dobiPrvega, reverse=True)

    return slovarFakt

def dobiPrvega(x):
    return x[1]

def findKeyLenght(c):
    razdalje = poisciPonavljanje(c) #dobis slovar ponavljanih substringov in razdalj

    praFaktorji = {}
    for i in razdalje:
        praFaktorji[i] = []
        for j in razdalje[i]:
            praFaktorji[i].extend(deljitelji(j))

    #print('prafakt',praFaktorji)
    stetje = najpogostejsiFaktorji(praFaktorji)
    #print('stetje',stetje)
    maximal = stetje[1][1]
    indeksNajvecjega = 1
    for i in range(1, len(stetje)):
        element = stetje[i][1]
        if(element > maximal):
            maximal = element
            indeksNajvecjega = i
        #print('tole',maximal, indeksNajvecjega)
    dolzinaKljuca = stetje[indeksNajvecjega][0]
    #print(dolzinaKljuca)

    return dolzinaKljuca

def naKateremZacnemo(kripto, start, n):
    val = ''
    for i in range(0,len(kripto)):
        if(i%n == start):
            val = val + kripto[i]
        #print('val',val)
    return val

def frekvecneCrk(besedilo):
    k =0
    for i in range(0, len(tabela)):
        #print('besedilo',besedilo)
        #print('element', tabela[i])
        pojavitev = (besedilo.count(tabela[i])*1.0)/len(besedilo)
        #print('stPojavitev', pojavitev)
        k = k + pow(pojavitev - angleskaFrekv[i], 2)
        #print('k',k)
    return k

def caesar(c, shift):
    celotnaNova = ''
    for i in range(len(c)):
        inx = tabela.index(c[i])
        shifted = (inx + shift)%26
        #print('shifted',shifted)
        #dati shifted v abecedo
        crka = tabela[shifted]
        #print('crka',crka)
        celotnaNova += crka
    #print(celotnaNova)
    return celotnaNova

def findKey(c, keyLen):
    hipotetiKljuc =''
    #dolzinaKjuca = FindKeyLenght(c)
    #print('dolzinaKljucaaa', dolzinaKjuca)
    for i in range(0, keyLen):
        t = naKateremZacnemo(c, i, keyLen)
        min = -1
        zamik = 0
        for j in range(0,len(tabela)): #cez crke abecede
            #naredimo za vsako cezarjevo
            cezar = caesar(t, -j) #mogoce kle -j
            frekve = frekvecneCrk(cezar) #mogoce kle frekvence crk v abecedi
            if min == -1:
                min = frekve
            if frekve < min:
                zamik = j
                min = frekve
        hipotetiKljuc = hipotetiKljuc + tabela[zamik]
    #print(hipotetiKljuc)
    return hipotetiKljuc

print("enkriptira ATTACKATDOWN s kljucem LEMON", Encrypt('ATTACKATDOWN', 'LEMON'))
print('dekriptira LXFOPVEFRBHR s kljucem LEMON', Decrypt('LXFOPVEFRBHR', 'LEMON'))
dolzina = findKeyLenght('UTAHELHUSBXLZAZYMVXXGELAUOGDTEMOQRTUKGHCQRGTQNMUATMVASMYANZMARMOQLBIQRMPQSHMUTLWQOISQCTUNELADOGNQNHBSHMVYABUFABUUTLLJILAQNVLUNZYQAMLYEKNQNVPQSHUFHBZBOBUFTALBRXZQNMYQBXSXIHUNRHBSHMVGRKLBUUSUCMVMSXCQRXAQSMHZDMOQPKLEIWLZTBHXEELOTBVZOVJGRKPZGBUDEZBXAKJAUKZQDNYUNZATEKLNEESUOGHPDXKZOMHXIMAXEMVFHXZFRTPZTALETKPREHMFHXLXEVAUOGPEBNATUFHZNTAGRXWDAVAUCTSXYTWBLBLPTHATEYHOTLPZTALOALL')
print("Dolzina kljuca v danem besedilu", dolzina)
kljuc = findKey('UTAHELHUSBXLZAZYMVXXGELAUOGDTEMOQRTUKGHCQRGTQNMUATMVASMYANZMARMOQLBIQRMPQSHMUTLWQOISQCTUNELADOGNQNHBSHMVYABUFABUUTLLJILAQNVLUNZYQAMLYEKNQNVPQSHUFHBZBOBUFTALBRXZQNMYQBXSXIHUNRHBSHMVGRKLBUUSUCMVMSXCQRXAQSMHZDMOQPKLEIWLZTBHXEELOTBVZOVJGRKPZGBUDEZBXAKJAUKZQDNYUNZATEKLNEESUOGHPDXKZOMHXIMAXEMVFHXZFRTPZTALETKPREHMFHXLXEVAUOGPEBNATUFHZNTAGRXWDAVAUCTSXYTWBLBLPTHATEYHOTLPZTALOALL', dolzina)
print("Najdem kljuc", kljuc)
dekriptirano = Decrypt('UTAHELHUSBXLZAZYMVXXGELAUOGDTEMOQRTUKGHCQRGTQNMUATMVASMYANZMARMOQLBIQRMPQSHMUTLWQOISQCTUNELADOGNQNHBSHMVYABUFABUUTLLJILAQNVLUNZYQAMLYEKNQNVPQSHUFHBZBOBUFTALBRXZQNMYQBXSXIHUNRHBSHMVGRKLBUUSUCMVMSXCQRXAQSMHZDMOQPKLEIWLZTBHXEELOTBVZOVJGRKPZGBUDEZBXAKJAUKZQDNYUNZATEKLNEESUOGHPDXKZOMHXIMAXEMVFHXZFRTPZTALETKPREHMFHXLXEVAUOGPEBNATUFHZNTAGRXWDAVAUCTSXYTWBLBLPTHATEYHOTLPZTALOALL', kljuc)
print("Dekriptirano besedilo z najdenim kljucem", dekriptirano)