# diferenta.py - ce SUID a aparut fata de un sistem curat
import os

from arsenal.privesc.enum import citeste_linii, nume, GTFO

START = os.path.join(os.path.dirname(__file__), "start")


def cai(fisier):
    """MULTIMEA cailor din fisier."""
    return set(citeste_linii(fisier))


def main():
    baza = cai(os.path.join(START, "baza_suid.txt"))
    acum = cai(os.path.join(START, "suid.txt"))
    print("baza:", len(baza), " acum:", len(acum))

    # diferenta de multimi: ce e in "acum" si nu e in "baza"
    noi = acum - baza
    print(len(noi), "SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)

    # dictionar nume -> risc, pentru cele noi
    risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
    print("risc:", dict(sorted(risc.items())))

    # filtrul final: doar cele periculoase
    periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
    print("periculoase NOI:", periculoase)


if __name__ == "__main__":
    main()
