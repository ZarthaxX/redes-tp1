#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
import math

def getSymbolInformation(symbolProbability):
    return -math.log(symbolProbability, 2.0)

def getNullSourceEntropy(S):
    N = sum(S.values())
    symbolsProbability = map(lambda x: x/N, S.values())
    symbolsInformation = map(lambda s : getSymbolInformation(s)*s, symbolsProbability)
    entropy = sum(symbolsInformation)
    return entropy

#• Cantidad de información de cada símbolo comparado con la entropía de la red.

def probabilityOfDir(index, dir, S):
    total = 0
    for d,v in S.items():
        if d[index] == dir:
            total += v
    N = sum(S.values())
    return total/N

def generateAddressTable(S1History):
    cols = ["BROADCAST","UNICAST"]
    rows = [[probabilityOfDir(0,'BROADCAST',S),probabilityOfDir(0,'UNICAST',S)] for S in S1History]
    dfTable = pd.DataFrame(rows, columns=cols)
    dfTable.to_csv("..\\results\\addressProbabilityTable.csv", index=False, header=True)

def generateEntropyTable(S1History):
    cols = ["ENTROPY"]
    rows = [[getNullSourceEntropy(S)] for S in S1History]
    dfTable = pd.DataFrame(rows, columns=cols)
    dfTable.to_csv("..\\results\\entropyTable.csv", index=False, header=True)

def generateProtocolProbabilityTable(S1History):
    cols = set([p for k,p in S1History[-1].keys()])
    rows = [[probabilityOfDir(1, p, S) for p in cols] for S in S1History]
    dfTable = pd.DataFrame(rows, columns=cols)
    dfTable.to_csv("..\\results\\protocolProbabilityTable.csv", index=False, header=True)

def generateSymbolInformationTable(S1History):
    protos = S1History[-1].keys()
    cols = [ f"{d}-{p}" for d,p in S1History[-1].keys()]
    rows = [[ getSymbolInformation(S[s]/sum(S.values())) if (s in S) else None for s in protos] for S in S1History]
    dfTable = pd.DataFrame(rows, columns=cols)
    dfTable.to_csv("..\\results\\symbolInformationTable.csv", index=False, header=True)

def generateHostSrcTable(S2History):
    cols = S2History[-1].keys()
    rows = [[S2[ip] if ip in S2 else 0 for ip in cols] for S2 in S2History]
    dfTable = pd.DataFrame(rows, columns=cols)
    dfTable.to_csv("..\\results\\hostSrcTable.csv", index=False, header=True)

def generateHostDstTable(S3History):
    cols = S3History[-1].keys()
    rows = [[S3[ip] if ip in S3 else 0 for ip in cols] for S3 in S3History]
    dfTable = pd.DataFrame(rows, columns=cols)
    dfTable.to_csv("..\\results\\hostDstTable.csv", index=False, header=True)

def generateAllTables(S1History,S2History,S3History):
    Path("..\\results").mkdir(parents=True, exist_ok=True)
    generateAddressTable(S1History)
    generateEntropyTable(S1History)
    generateProtocolProbabilityTable(S1History)
    generateSymbolInformationTable(S1History)
    generateHostSrcTable(S2History)
    generateHostDstTable(S3History)