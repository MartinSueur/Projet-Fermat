
dicoPartis = {}
def calcule_partis(score,arret):
            if score[0] == arret:
                dicoPartis[score] = (100,0)
                return (100,0)
            elif score[1] == arret:
                dicoPartis[score] = (0,100)
                return (0,100)
            else:
                res0 = calcule_partis((score[0]+1,score[1]),arret)
                res1 = calcule_partis((score[0],score[1]+1),arret)
                res = (res0[0]+res1[0])/2,(res0[1]+res1[1])/2
                dicoPartis[score] = res
                return res
print(calcule_partis((8,0),10))