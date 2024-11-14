# coding: utf-8
Ws=[4,6,8,10,12,20,100]

outfilePrints=['>=']

outcomes=[-1,-1,0,1]
def PWx(outcome,W):
    if outcome<=0:
        return 1/W
    #if outcome==1:
    #    return 1/W
    return (W-3)/W
def ErgSuccess(Ereigniss,x):
    sumOf=0
    hasSucc=0
    for i in range(len(Ereigniss)):
        erg=outcomes[i]
        num=Ereigniss[i]
        if(i>1 and num>0):
            hasSucc=1
        sumOf+=num*erg
    if(x<=-12):
        return hasSucc==1
    return hasSucc==1 and sumOf>=x
def ErgMultiSuccess(newX,gesX,amount):
    if(gesX<=-12):
        if(newX<=-12):
            return 1,-12
        return 0,-12
    if(newX<-12):
        return -1,0
    #<-6 -> auto lost
    diff=max(-6,gesX-newX)
    penality=2
    oriAmount=amount
    while(amount>=penality):
        amount-=penality
        diff+=1
    if(diff>(7*(oriAmount-1))):
        #<-7 -> vorher verloren
        return -1,0
    return 0,diff

maxNum=6

#werteXAchse=range(-maxNum*2,maxNum*2+1)
werteXAchse=[-12,-7,-6,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
werteXAchseMulti=[-100,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7]
plotDim=(7,maxNum)
n=1
def WListForPlot(w1,i):
    WList=[]
    for _ in Ws:
        WList.append(0)
    
    #WList[w1]=6
    #amount=n*i+1
    #return WList,amount,f'{i+n}w{Ws[w1]}({(i+n)*(w1-1)})({amount} times)'

    #System Attr=würfel, Spez=güte v1
    spez=(w1-2)*4
    attr=5#i+n
    amount=1+i
    #tiefenaufbau
    #att=attr
    #spe=spez
    #while (att>0):
    #    if(spe>5):
    #        spe-=5
    #        att-=1
    #        WList[5]+=1
    #    else:
    #        WList[spe]+=1
    #        spe=0
    #        att-=1
    #return WList,amount,f'Attr:{attr};Spez:{spez}({WList[0]}w{Ws[0]},{WList[1]}w{Ws[1]},{WList[2]}w{Ws[2]},{WList[3]}w{Ws[3]},{WList[4]}w{Ws[4]},{WList[5]}w{Ws[5]})'
    #breitenaufbau
    wr1=int(abs(spez)/attr)
    wa2=spez%attr
    if wr1>=4:
        wr1=4
        wa2=min(0,attr,int((spez-attr*4)/3))
    if spez<0:
        wr1=-wr1
    else:
        wr1+=1
    if wr1<0:
        wr1=0
        wa2=0
    WList[wr1+0]=attr-wa2
    WList[wr1+1]=wa2
    return WList,amount,f'{amount}xAttr:{attr};Spez:{spez}({WList[wr1+0]}w{Ws[wr1+0]},{WList[wr1+1]}w{Ws[wr1+1]})'

    #WList[w1]=i+n
    #amount=1
    #return WList,amount,f'{WList[w1]}w{Ws[w1]}'

    WList[w1+1]=i
    WList[w1]=maxNum-i
    a=f"{maxNum-i}*{Ws[w1]:2}+{i}*{Ws[w1+1]:2}: "
    if i==0:
        return WList,1,f"{maxNum-i}w{Ws[w1]}"
    if i==maxNum:
        return WList,1,f"{i}w{Ws[w1+1]}"
    return WList,1,f"{maxNum-i}w{Ws[w1]} + {i}w{Ws[w1+1]}"


import sys,math

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
def PXN(amount, x, WList, cache={}):
    asStr=f"{amount} {x} {WList}"
    if cache.get(asStr):
        return cache.get(asStr)
    if(amount==0):
        return 1
    if(amount==1):
        return PX(x,WList)
    pGes=0
    for j in werteXAchseMulti:
        posi,res=ErgMultiSuccess(j,x,amount)
        if(posi==0):
            pGes+=PEqX(j,WList)*PXN(amount-1,res,WList)
        if(posi==1):
            pGes+=PEqX(j,WList)
    #print(asStr)
    #for^amount
    cache[asStr]=pGes
    return pGes

#P(X>x)
def PGeX(x, WList):
    return PX(x+0.01,WList)
def PGeXN(amount,x, WList):
    return PXN(amount,x+0.01,WList)
#P(X<=x)
def PLEqX(x, WList):
    return 1-PGeX(x,WList)
def PLEqXN(amount,x, WList):
    return 1-PGeXN(amount,x,WList)
#P(X<x)
def PLoX(x, WList):
    return 1-PX(x,WList)
def PLoXN(amount,x, WList):
    return 1-PXN(amount,x,WList)
#P(X==x)
def PEqX(x, WList):
    return PX(x,WList)-PGeX(x,WList)
def PEqXN(amount,x, WList):
    return PXN(amount,x,WList)-PGeXN(amount,x,WList)

import time
import matplotlib.pyplot as plt

fig,ax = plt.subplots(plotDim[0],plotDim[1],sharex=True,sharey=True)
maxLenTitle=0
for x in range(plotDim[0]):
    for y in range(plotDim[1]):
        maxLenTitle=max(maxLenTitle,len(WListForPlot(x,y)[2]))
with open("out.txt","w") as f:
    for x in (range(plotDim[0])):
        for y in range(plotDim[1]):
            WList,amount,title=WListForPlot(x,y)

            outLine=f'{title:{maxLenTitle}}'
            outLine2=outLine
            ydata = []
            xdata = []
            if PLoXN(amount,werteXAchse[0],WList)>0.0000000000001:
                xdata.append(f'<{werteXAchse[0]}')
                ydata.append(PLoXN(amount,werteXAchse[0],WList)*100)
            for j in range(len(werteXAchse)):
                wert=werteXAchse[j]

                if '>=' in outfilePrints:
                    outLine+=f">={wert}={PXN(amount,wert,WList)*100:5.1f}%; "
                if '>' in outfilePrints:
                    outLine+=f">{j}={PGeXN(amount,wert,WList)*100:5.1f}%; "
                if '=' in outfilePrints:
                    outLine+=f"=={wert}={PEqXN(amount,wert,WList)*100:5.1f}%; "
                if '<=' in outfilePrints:
                    outLine+=f"<={wert}={PLEqXN(amount,wert,WList)*100:5.1f}%; "
                if '<' in outfilePrints:
                    outLine+=f"<{wert}={PLoXN(amount,wert,WList)*100:5.1f}%; "

                if j+1!=len(werteXAchse) and wert-werteXAchse[j+1]!=-1:
                    continue
                if j==0 or wert-werteXAchse[j-1]==1:
                    xdata.append(f'{wert}')
                    ydata.append(PEqXN(amount,wert,WList)*100)
                else:
                    prevWert=werteXAchse[j-1]
                    xdata.append(f'[{prevWert};{wert}]')
                    ydata.append((PXN(amount,prevWert,WList)-PGeXN(amount,wert,WList))*100)
            if PGeXN(amount,wert,WList)>0.0000000000001:
                xdata.append(f'>{wert}')
                ydata.append(PGeXN(amount,wert,WList)*100)
            outLine+="\n"
            outLine2+="\n"
            f.write(outLine)
            #f.write(outLine2)
            ax[x,y].barh(xdata, ydata)
            ax[x,y].set_title(title)
            ax[plotDim[0]-1,y].set_xlabel("Prozent(%)")
            ax[x,plotDim[1]-1].set_ylabel("")
        f.write("\n")
plt.show()
            
            
            
