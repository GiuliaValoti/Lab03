import csv
from operator import attrgetter

class Strumento:
    def __init__(self, id_strumento, tipo, marca, anno_acquisto, valore):
        self.id = id_strumento
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = int(anno_acquisto)
        self.valore = float(valore)

    def __str__(self):
        return f"[{self.id}] {self.tipo} - {self.marca} ({self.anno_acquisto}) - €{self.valore:.2f}"

    def __repr__(self):
        return self.__str__()


class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"[{self.id_prestito}] Data: {self.data} | Strumento: {self.id_strumento} | Allievo: {self.cognome_allievo}"

    def __repr__(self):
        return self.__str__()


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = []
        self.prestiti = []
        self.contatore_prestiti = 1

    def carica_file_strumenti(self, file_path):
        try:
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for riga in reader:
                    if riga:
                        id_s, tipo, marca, anno, valore = [x.strip() for x in riga]
                        s = Strumento(id_s, tipo, marca, anno, valore)
                        if not any(item.id == id_s for item in self.strumenti):
                            self.strumenti.append(s)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} non trovato.")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        max_num = 0
        for s in self.strumenti:
            if s.id.startswith("S"):
                try:
                    num = int(s.id[1:])
                    if num > max_num:
                        max_num = num
                except ValueError:
                    pass

        nuovo_id = f"S{max_num + 1}"
        nuovo_s = Strumento(nuovo_id, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(nuovo_s)
        return nuovo_s

    def strumenti_ordinati_per_marca(self):
        return sorted(self.strumenti, key=attrgetter("marca"))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        if not any(s.id == id_strumento for s in self.strumenti):
            raise Exception(f"Strumento {id_strumento} non presente.")

        if any(p.id_strumento == id_strumento for p in self.prestiti):
            raise Exception(f"Strumento {id_strumento} già in prestito.")

        id_prestito = f"P{self.contatore_prestiti}"
        self.contatore_prestiti += 1

        prestito = Prestito(id_prestito, data, id_strumento, cognome_allievo)
        self.prestiti.append(prestito)
        return prestito

    def termina_prestito(self, id_prestito):
        for p in self.prestiti:
            if p.id_prestito == id_prestito:
                self.prestiti.remove(p)
                return
        raise Exception(f"Prestito {id_prestito} non trovato.")