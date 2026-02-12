class Station:
    def __init__(self, name, fahrzeit_zur_naechsten):
        self.name = name
        self.fahrzeit_zur_naechsten = fahrzeit_zur_naechsten  # Minuten


class LinieU1:
    def __init__(self, stationen, takt=10):
        self.stationen = stationen
        self.takt = takt  # Minuten
        self.startzeit = 5 * 60      # 05:00
        self.endzeit = 23 * 60       # 23:00

        self.hauptknoten = {"Plärrer", "Hauptbahnhof"}
        self.endstationen = {stationen[0].name, stationen[-1].name}

    # ----------------------------
    # Haltezeit (nach Ankunft!)
    # ----------------------------
    def haltezeit(self, station):
        if station.name in self.hauptknoten:
            return 1.0
        if station.name in self.endstationen:
            return 1.0  # 60 Sekunden an Endhaltestellen
        return 0.5      # 30 Sekunden sonst

    # ----------------------------
    # Fahrplan generieren
    # ----------------------------
    def generiere_fahrplan(self):
        fahrplan = {s.name: [] for s in self.stationen}

        for zugstart in range(self.startzeit, self.endzeit + 1, self.takt):

            # ============================
            # Hinfahrt (+1)
            # ============================
            zeit = zugstart

            for i, station in enumerate(self.stationen):
                # Abfahrt (keine Haltezeit an Abfahrtshaltestelle!)
                fahrplan[station.name].append((zeit, +1))

                # Haltezeit NUR wenn nicht Abfahrtshaltestelle
                if i != 0:
                    zeit += self.haltezeit(station)

                # Fahrzeit zur nächsten Station
                if i < len(self.stationen) - 1:
                    zeit += station.fahrzeit_zur_naechsten

            # ============================
            # Rückfahrt (-1)
            # ============================
            for i in range(len(self.stationen) - 1, -1, -1):
                station = self.stationen[i]

                fahrplan[station.name].append((zeit, -1))

                # Haltezeit NUR wenn nicht Abfahrtshaltestelle der Rückfahrt
                if i != len(self.stationen) - 1:
                    zeit += self.haltezeit(station)

                if i > 0:
                    zeit += self.stationen[i - 1].fahrzeit_zur_naechsten

        return fahrplan

    # ----------------------------
    # Nächste Abfahrt berechnen
    # ----------------------------
    def naechste_abfahrt(self, start, ziel, uhrzeit):
        stunden, minuten = map(int, uhrzeit.split(":"))
        wunschzeit = stunden * 60 + minuten

        fahrplan = self.generiere_fahrplan()

        if start not in fahrplan or ziel not in fahrplan:
            raise ValueError("Unbekannte Station.")

        indices = {s.name: i for i, s in enumerate(self.stationen)}

        if indices[start] == indices[ziel]:
            raise ValueError("Start und Ziel sind identisch.")

        # Richtung bestimmen
        richtung = 1 if indices[ziel] > indices[start] else -1

        # Abfahrten heute
        kandidaten_heute = [
            zeit for zeit, r in fahrplan[start]
            if r == richtung and zeit >= wunschzeit
        ]

        if kandidaten_heute:
            beste = min(kandidaten_heute)
        else:
            # nächster Betriebstag
            kandidaten_morgen = [
                zeit for zeit, r in fahrplan[start]
                if r == richtung and zeit >= self.startzeit
            ]
            if not kandidaten_morgen:
                raise ValueError("Keine Bahn verfügbar.")
            beste = min(kandidaten_morgen)

        return beste  # Minuten seit 00:00

    # ----------------------------
    # Ankunftszeit berechnen
    # ----------------------------
    def ankunftszeit(self, start, ziel, abfahrtszeit):
        indices = {s.name: i for i, s in enumerate(self.stationen)}

        start_i = indices[start]
        ziel_i = indices[ziel]

        zeit = abfahrtszeit

        schritt = 1 if ziel_i > start_i else -1
        i = start_i

        while i != ziel_i:
            naechste = i + schritt

            # Fahrzeit
            if schritt == 1:
                zeit += self.stationen[i].fahrzeit_zur_naechsten
            else:
                zeit += self.stationen[naechste].fahrzeit_zur_naechsten

            # Haltezeit an Ziel-Zwischenstationen
            zeit += self.haltezeit(self.stationen[naechste])

            i = naechste

        return zeit