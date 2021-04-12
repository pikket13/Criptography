import numpy
tabela = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
angleskaFrekv = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.996, 0.153,
                             0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056,
                             2.758, 0.978, 2.360, 0.150, 1.974, 0.074]

dekriptiraj = True
MIN_SUM = 100000

def Encrypt(b,k):
    b = preveri(b,k)
    rezultat = []
    b = matrikaBesedila(b)
    k = matrikaKljuca(k)
    #print('kluc tak', k)
    zmnozek = mnozenjeMatrik(k,b)  
    #print(len(zmnozek[1]), len(zmnozek), len(zmnozek[0]))
    col = len(zmnozek[1])
    row = len(zmnozek)
    for i in range(col):
        for j in range(row):
            rezultat.append(tabela[zmnozek[j][i]])
    #print('rez',rezultat)
    return rezultat


def Decrypt(c,k):
    c = preveri(c,k)
    odkrip = []
    c = matrikaBesedila(c)
    k = matrikaKljuca(k)
    k = inverz(k)
    produkt = mnozenjeMatrik(k,c)
    for i in range(len(produkt[0])):
        for j in range(len(produkt)):
            odkrip.append(tabela[produkt[j][i]])
    #print('odk',odkrip)
    return odkrip


def preveri(besedilo, kljuc):
    if((len(kljuc) % len(besedilo)) != 0):
        besedilo += "X"
    return besedilo

def mnozenjeMatrik(a,b):
    #print('dolzinaB', len(b))
    result = [[0 for x in range(len(b[1]))] for y in range(2)] #tukaj len(b[1]), ce ni samo vektor
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k]*b[k][j]
            result[i][j] = result[i][j] % 26
    #print(result)
    return result

def inverz(a):
    det = (a[0][0]*a[1][1] - a[0][1]*a[1][0])%26
    det = inverzDeter(det)
    #zamenjamo a in d
    a[0][0], a[1][1] = a[1][1], a[0][0]
    a[0][1] *= -1
    a[1][0] *= -1
    for i in range(len(a)):
        for j in range(len(a)):
            a[i][j] *= det
            a[i][j] = a[i][j] %26
    #print(a)
    return a

def inverzDeter(det):
    for i in range(26):
        if(((det*i)%26) == 1):
            return i 
    return -1

def matrikaKljuca(k): #tukaj se visino in sirino, ce dimenzija > 2
    ind = 0
    matrika = [[0 for x in range(2)] for y in range(2)]
    for i in range(2):
        for j in range(2):
            matrika[j][i] = tabela.index(k[ind])
            ind += 1
    #print(matrika)
    return matrika

def matrikaBesedila(bes):
    stolpci = len(bes)/2
    matrikaB = [[0 for x in range(stolpci)] for y in range(2)]
    idx = 0
    for i in range(stolpci):
        for j in range(2):
            matrikaB[j][i]= tabela.index(bes[idx])
            idx += 1
            if(idx > len(bes)):
                break

    #print('vector',matrikaB)
    return matrikaB

def frekvence(c):
    f = []
    for i in range(26):
        #inx = tabela.index(c[i])
        f[c[i]] += 1
    for i in range(26):
        f[i] = (f[i]/len(c))*100
    return f

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

def prestej(slovar):
    stevec = 0
    count = {}
    for i in range(len(slovar)):
        stevec = 0
        count[i] = [] 
        for j in range(len(slovar.values()[i])):
            if(slovar.values()[i][j] == 1):
                stevec += 1
        count[i].append(stevec+1)
    #print('tole', len(count))
    #print(slovar.keys()[0], count[0])
    tabel = [[0 for x in range(2)] for y in range(len(count))]
    for i in range(len(count)):
        tabel[i][0] = slovar.keys()[i]
        tabel[i][1] = count[i]
    #print(tabel)
    return tabel


def najveckratPojavi(tabela):
    max1 = 0
    max2 = 0
    ind1 = 0
    ind2 = 0
    for i in range(len(tabela)):
        if(tabela[i][1] > max1):
            max2 = max1
            max1 = tabela[i][1]
            ind1 = i
        elif(tabela[i][1] > max2):
            max2 = tabela[i][1]
            ind2 = i
    #print('tole', max1, max2, ind1, ind2) #mjbi kle odstejes

    tabelaPrvihDveh = [[0 for x in range(2)] for y in range(2)]

    tabelaPrvihDveh[0] = ind1    
    tabelaPrvihDveh[1] = ind2

    return tabelaPrvihDveh

def poisciBesedo(kriptogram):
    stevecdva = 0
    #print(len(kriptogram))
    slovar = {} #kljuc je podniz, vrednost je razdalja
    dolzina = 2 #kljuc mora biti saj 3 dolg, pri nas vec kot 5 ne bo
    for start in range(len(kriptogram)-dolzina): #kle je len(kriptogram) - dolzina
        podniz = kriptogram[start:start+2]
        stevecdva = 0
        for i in range(start+dolzina, len(kriptogram)-dolzina): #kle start+dolzina, len(kriptogram)-dolzina
            #print(podniz, kriptogram[i:i+dolzina])
            if(kriptogram[i:i+dolzina] == podniz):
                stevecdva += 1
                if(podniz not in slovar):
                    slovar[podniz] = []
                #slovar[podniz].append(stevecdva)
                slovar[podniz].append(stevecdva)
    
    tabelaPojavitev = prestej(slovar)
    #print('tabela',tabelaPojavitev[137])
    tabelaa = najveckratPojavi(tabelaPojavitev) #tabela[0] je prvi max in tabela[1] je drugi max
    prvaBeseda = tabelaPojavitev[tabelaa[0]][0] + (tabelaPojavitev[tabelaa[1]][0])
    #print(prvaBeseda)
    return prvaBeseda

def vBesedo(matrika):
    beseda = ''
    for i in range(2):
        for j in range(2):
            beseda += tabela[matrika[j][i]]
    #print(beseda)
    return beseda
            

def findKey(c):
    prvaBeseda = poisciBesedo(c)
    matrx = matrikaKljuca(prvaBeseda)
    #print(matrx)

    najpogostejsiPar = 'THHE'
    najpog = matrikaKljuca(najpogostejsiPar)
    najpog = inverz(najpog)
    koncenKljuc = mnozenjeMatrik(matrx, najpog)
    #print(koncenKljuc)
    koncenKljuc = vBesedo(koncenKljuc)
    print("najden kljuc", koncenKljuc)
    
    return koncenKljuc



print('Funckija Encrypt za besedo MIZA s kljuCem FTRW', Encrypt('MIZA', 'FTRW'))
print('Funkcija Decrypt za besedo OOVH s kljucem FTRW', Decrypt('OOVH', 'FTRW'))
kljucNajden = findKey('STSQALWTCJMIJMTHNFEBWZTVJWMRNNHPMFICJFNWSZSXGWPFHHAJFBNTWZTVTHIRMRCGVRJTAFXBWDIVMFWSNSTVLXIRACANWLYSIYVPJQMQNFLNMRPXSBHMWNJTIYNSZNHPHPIMNZDRWBPPNSHMSBUJMUHZXJHMWPSQHHJBMHHMWMJTAFXBWDICVETVLXIRANXFVETVUDWUHBWHEBMBSXHMWEEEHMANWUJUWWHAWWSNWZMLJXVXHWTVJTZZICACHHJTNWWTZRHWWTIYJSSUWSNSTVLWWWWHHPNSTVSNWWIYNSSOPFHMWEWHMHHMWNJTIYNSXPCQJTOQYFPBQKHMWEWHMHHMWNACHRNWHMWBSZWSIOGIICVETVLWWWWHHXANZRVZYWXUMVWZHDJHXAANHRUQZZOUNBTZTJFNSBUUMBVZSTTLHZXNWDTZELTVPPAJWTICVETVNNHPMFVZYWXUTVXBAJSQIUWWMHHMWNACHTGCTJIRGFCGVGSBYAPQITSDWISVPPNNZMWCIRMSFRSXHMWZEENFGDVBMHSYOYJHPBHLANXNNZVOSUSANTCVTVUMPSIATHYFAHEGCSPBWKNZMFWUYFIKXBMHHMWAAZWGJJAHSSWKVJANANXFVMAFSENLHMWBLZNDHMSBUJMNALWUFRSXWDMFWSVBTHLLJTYOSQWHYAGJHDJTXNNSTVMXTVJH')
print('reseno', Decrypt('STSQALWTCJMIJMTHNFEBWZTVJWMRNNHPMFICJFNWSZSXGWPFHHAJFBNTWZTVTHIRMRCGVRJTAFXBWDIVMFWSNSTVLXIRACANWLYSIYVPJQMQNFLNMRPXSBHMWNJTIYNSZNHPHPIMNZDRWBPPNSHMSBUJMUHZXJHMWPSQHHJBMHHMWMJTAFXBWDICVETVLXIRANXFVETVUDWUHBWHEBMBSXHMWEEEHMANWUJUWWHAWWSNWZMLJXVXHWTVJTZZICACHHJTNWWTZRHWWTIYJSSUWSNSTVLWWWWHHPNSTVSNWWIYNSSOPFHMWEWHMHHMWNJTIYNSXPCQJTOQYFPBQKHMWEWHMHHMWNACHRNWHMWBSZWSIOGIICVETVLWWWWHHXANZRVZYWXUMVWZHDJHXAANHRUQZZOUNBTZTJFNSBUUMBVZSTTLHZXNWDTZELTVPPAJWTICVETVNNHPMFVZYWXUTVXBAJSQIUWWMHHMWNACHTGCTJIRGFCGVGSBYAPQITSDWISVPPNNZMWCIRMSFRSXHMWZEENFGDVBMHSYOYJHPBHLANXNNZVOSUSANTCVTVUMPSIATHYFAHEGCSPBWKNZMFWUYFIKXBMHHMWAAZWGJJAHSSWKVJANANXFVMAFSENLHMWBLZNDHMSBUJMNALWUFRSXWDMFWSVBTHLLJTYOSQWHYAGJHDJTXNNSTVMXTVJH', kljucNajden))