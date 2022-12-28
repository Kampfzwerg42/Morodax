# coding: utf-8
Ws=[4,6,8,10,12,20,100]

outfilePrints=['>=']

outcomes=[-2,-1,0,1]
def PWx(outcome,W):
    if outcome<=0:
        return 1/W
    #if outcome==1:
    #    return 1/W
    return (W-3)/W
def ErgSuccess(Ereigniss,x):
    sumOf=0
    for i in range(len(Ereigniss)):
        erg=outcomes[i]
        num=Ereigniss[i]
        sumOf+=num*erg
    return sumOf>=x

maxNum=6

#werteXAchse=range(-maxNum*2,maxNum*2+1)
werteXAchse=[-12,-7,-6,-1,0,1,2,3,4,5,6,7,8]
plotDim=(maxNum,6)
n=3
def WListForPlot(w1,i):
    WList=[]
    for _ in Ws:
        WList.append(0)
    
    WList[w1]=i+n
    return WList,f'{i+n}w{Ws[w1]}({(i+n)*(w1-1)})'

    WList[w1+1]=i
    WList[w1]=maxNum-i
    a=f"{maxNum-i}*{Ws[w1]:2}+{i}*{Ws[w1+1]:2}: "
    if i==0:
        return WList,f"{maxNum-i}w{Ws[w1]}"
    if i==maxNum:
        return WList,f"{i}w{Ws[w1+1]}"
    return WList,f"{maxNum-i}w{Ws[w1]} + {i}w{Ws[w1+1]}"


import sys,math
from tqdm import tqdm
import matplotlib.pyplot as plt

def PxTimesYOrMore(Px, y, overallAmount,cache={}):
    asStr=f"{Px} {y} {overallAmount}"
    if cache.get(asStr):
        return cache.get(asStr)
    if y<=0:
        return 1
    if overallAmount<=0:
        return 0
    return Px*PxTimesYOrMore(Px, y-1, overallAmount-1)+(1-Px)*PxTimesYOrMore(Px, y, overallAmount-1)
def PxTimesY(Px, y, overallAmount):
    return PxTimesYOrMore(Px, y, overallAmount)-PxTimesYOrMore(Px, y+1, overallAmount)

#Erg 
def PErg(WList,cache={}):
    asStr=f"{WList}"
    if cache.get(asStr):
        return cache.get(asStr)
    #print(f"NoMatch{cache}")
    if(sum(WList)==0):
        erg=[]
        for wert in outcomes:
            erg.append(0)
        return {tuple(erg):1}
    result={}
    for wertNr in range(len(outcomes)):
        wert=outcomes[wertNr]
        for i in range(len(WList)):
            if WList[i]:
                WList[i]-=1
                for resT,p in PErg(WList).items():
                    res=list(resT)
                    res[wertNr]+=1
                    result.setdefault(tuple(res),0)
                    result[tuple(res)]+=p*PWx(wert,Ws[i])
                WList[i]+=1
                break
    cache[asStr]=result
    #print(WList,result)
    return result


#P(X>=x)
def PX(x, WList,Ergebnisse={},cache={}):
    asStr=f"{x}{WList}{Ergebnisse}"
    if cache.get(asStr):
        return cache.get(asStr)
    pGes=0.0
    #print(f"NoMatch{cache}")
    for ereigniss,p in PErg(WList).items():
        if ErgSuccess(ereigniss,x):
            pGes+=p
    cache[asStr]=pGes
    return pGes

#P(X>x)
def PGeX(x, WList):
    return PX(x+0.01,WList)
#P(X<=x)
def PLEqX(x, WList):
    return 1-PGeX(x,WList)
#P(X<x)
def PLoX(x, WList):
    return 1-PX(x,WList)
#P(X==x)
def PEqX(x, WList):
    return PX(x,WList)-PGeX(x,WList)

from tqdm import tqdm
import time
from joblib import Parallel, delayed

fig,ax = plt.subplots(plotDim[0],plotDim[1],sharex=True,sharey=True)
maxLenTitle=0
for x in tqdm(range(plotDim[0])):
    for y in range(plotDim[1]):
        maxLenTitle=max(maxLenTitle,len(WListForPlot(x,y)[1]))
with open("out.txt","w") as f:
    for x in tqdm(range(plotDim[0])):
        for y in range(plotDim[1]):
            WList,title=WListForPlot(x,y)

            outLine=f'{title:{maxLenTitle}}'
            ydata = []
            xdata = []
            if PLoX(werteXAchse[0],WList)>0.0000000000001:
                xdata.append(f'<{werteXAchse[0]}')
                ydata.append(PLoX(werteXAchse[0],WList)*100)
            for j in range(len(werteXAchse)):
                wert=werteXAchse[j]

                if '>=' in outfilePrints:
                    outLine+=f">={wert}={PX(wert,WList)*100:5.1f}%; "
                if '>' in outfilePrints:
                    outLine+=f">{j}={PGeX(wert,WList)*100:5.1f}%; "
                if '=' in outfilePrints:
                    outLine+=f"=={wert}={PEqX(wert,WList)*100:5.1f}%; "
                if '<=' in outfilePrints:
                    outLine+=f"<={wert}={PLEqX(wert,WList)*100:5.1f}%; "
                if '<' in outfilePrints:
                    outLine+=f"<{wert}={PLoX(wert,WList)*100:5.1f}%; "

                if j+1!=len(werteXAchse) and wert-werteXAchse[j+1]!=-1:
                    continue
                if j==0 or wert-werteXAchse[j-1]==1:
                    xdata.append(f'{wert}')
                    ydata.append(PEqX(wert,WList)*100)
                else:
                    prevWert=werteXAchse[j-1]
                    xdata.append(f'[{prevWert};{wert}]')
                    ydata.append((PX(prevWert,WList)-PGeX(wert,WList))*100)
            if PGeX(wert,WList)>0.0000000000001:
                xdata.append(f'>{wert}')
                ydata.append(PGeX(wert,WList)*100)
            outLine+="\n"
            f.write(outLine)
            ax[x,y].barh(xdata, ydata)
            ax[x,y].set_title(title)
            ax[plotDim[0]-1,y].set_xlabel("Prozent(%)")
            ax[x,plotDim[1]-1].set_ylabel("")
plt.show()
            
            
            
