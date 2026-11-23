# enum.py - enumerare spre root: SUID, sudo, cron -> raport JSON
import argparse
import json
import os

# Binare cunoscute ca "scapari" spre root (stil GTFOBins)
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}


def citeste_linii(cale):
    """Lista liniilor curate: fara spatii in jur, fara goluri, fara comentarii."""
    with open(cale, encoding="utf-8") as f:
        return [ln.strip() for ln in f
                if ln.strip() and not ln.strip().startswith("#")]


def nume(cale):
    """Numele fisierului: ce e dupa ultimul '/'."""
    return cale.rsplit("/", 1)[-1]


def suid_constatari(cale):
    """Lista de dictionare, sortata, fara dubluri, pentru fisierele SUID."""
    cai = citeste_linii(cale)
    return [
        {"cale": c,
         "nume": nume(c),
         "risc": "mare" if nume(c) in GTFO else "normal"}
        for c in sorted(set(cai))
    ]


def sudo_constatari(cale):
    """O linie 'user : drept' devine un dictionar."""
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)  # despachetare in tuplu
        out.append({"user": user.strip(),
                    "drept": drept.strip(),
                    "risc": "mare" if "NOPASSWD" in drept else "normal"})
    return out


def cron_constatari(cale):
    """Sase campuri de program, apoi userul si comanda."""
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        user = campuri[5]
        comanda = " ".join(campuri[6:])
        out.append({"user": user, "comanda": comanda})
    return out


def enumereaza(d):
    """Grupeaza totul intr-un dictionar: o cheie pe categorie."""
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    raport = enumereaza(a.capturi)

    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")

    # utilizatorii implicati = userii din sudo REUNITI cu cei din cron
    useri = ({c["user"] for c in raport["sudo"]}
             | {c["user"] for c in raport["cron"]})
    print("utilizatori implicati:", ", ".join(sorted(useri)))

    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")


if __name__ == "__main__":
    main()
