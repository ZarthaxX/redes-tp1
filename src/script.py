#!/usr/bin/env python3
from scapy.all import *
import atexit
from tableGeneration import *

S1History = []
S2History = []
S3History = []
S1 = {}
S2 = {}
S3 = {}
totalPackets = 0
startTime = time.asctime( time.localtime(time.time()) )
lastSnapshot = 0.0
SECONDS_SNAPSHOT = 10

def mostrar_fuente(S):
    print(f"Time: {startTime}")
    print(f"totalPackets: {totalPackets}")
    print(f"entropy: {getNullSourceEntropy(S)}")
    N = sum(S.values())
    simbolos = sorted(S.items(), key=lambda x: -x[1])
    print("symbol\t\t\tprobability\tinformation")
    print(
        "\n".join(
            [f"{d[0],hex(d[1])}\t{(k/N):.5f}\t\t{getSymbolInformation(k/N):.5f}" for d,k in simbolos ]
        )
    )
    print(f"BROADCAST % {probabilityOfDir(0,'BROADCAST',S):5f}")
    print(f"UNICAST % {probabilityOfDir(0,'UNICAST',S):5f}")
    protos = set([p for d,p in S])
    for proto in protos:
        print(f"{hex(proto)} % {probabilityOfDir(1, proto, S):5f}")
    print()

def callback(pkt):
    global totalPackets
    global lastSnapshot

    if pkt.haslayer(Ether):
        dire = "BROADCAST" if pkt[Ether].dst=="ff:ff:ff:ff:ff:ff" else "UNICAST"
        proto = pkt[Ether].type # El campo type del frame tiene el protocolo
        s_i = (dire, proto) # Aca se define el simbolo de la fuente
        if s_i not in S1:
            S1[s_i] = 0.0
        S1[s_i] += 1.0

        totalPackets += 1

        if proto == 0x806:
            src = pkt[ARP].psrc
            if src not in S2:
                S2[src] = 0.0
            S2[src] += 1.0
            dst = pkt[ARP].pdst
            if dst not in S3:
                S3[dst] = 0.0
            S3[dst] += 1.0
            
    deltaTime = (time.time()-lastSnapshot)
    if deltaTime > SECONDS_SNAPSHOT:
        mostrar_fuente(S1)
        print("OPCIONAL")
        print("Src")
        print(''.join([f"ARP from src {ip}: {S2[ip]}\n" for ip in S2]))
        print("Dst")
        print(''.join([f"ARP to dst {ip}: {S3[ip]}\n" for ip in S3]))
        S1History.append(S1.copy())
        S2History.append(S2.copy())
        S3History.append(S3.copy())
        lastSnapshot = time.time()
sniff(prn=callback)

def exit_handler():
    generateAllTables(S1History,S2History,S3History)

atexit.register(exit_handler)