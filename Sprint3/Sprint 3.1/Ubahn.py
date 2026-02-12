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

    def haltezeit(self, station):
        if station.name in self.hauptknoten:
            return 1.0
        if station.name in self.endstationen:
            return 1.0
        return 0.5

    def generiere_fahrplan(self):
        fahrplan = {s.name: [] for s in self.stationen}
        for zugstart in range(self.startzeit, self.endzeit + 1, self.takt):
            # --- Hinfahrt ---
            zeit = float(zugstart)
            for i in range(len(self.stationen)):
                station = self.stationen[i]
                # Wir speichern die Zeit, zu der der Zug an der Station ABFÄHRT
                fahrplan[station.name].append((zeit, +1))

                # Wenn nicht Endstation: Fahrzeit + Haltezeit an der NÄCHSTEN Station
                if i < len(self.stationen) - 1:
                    zeit += station.fahrzeit_zur_naechsten
                    zeit += self.haltezeit(self.stationen[i + 1])

            # --- Rückfahrt ---
            # Startzeit der Rückfahrt ist Ankunft Hinfahrt + Wendezeit (z.B. 1 Min)
            zeit += 1.0
            for i in range(len(self.stationen) - 1, -1, -1):
                station = self.stationen[i]
                fahrplan[station.name].append((zeit, -1))

                if i > 0:
                    zeit += self.stationen[i - 1].fahrzeit_zur_naechsten
                    zeit += self.haltezeit(self.stationen[i - 1])
        return fahrplan

    def naechste_abfahrt(self, start, ziel, uhrzeit):
        stunden, minuten = map(int, uhrzeit.split(":"))
        wunschzeit = stunden * 60 + minuten

        fahrplan = self.generiere_fahrplan()

        if start not in fahrplan or ziel not in fahrplan:
            raise ValueError("Unbekannte Station.")

        indices = {s.name: i for i, s in enumerate(self.stationen)}
        if indices[start] == indices[ziel]:
            raise ValueError("Start und Ziel sind identisch.")

        richtung = 1 if indices[ziel] > indices[start] else -1

        kandidaten = [zeit for zeit, r in fahrplan[start] if r == richtung and zeit >= wunschzeit]
        if not kandidaten:
            kandidaten = [zeit for zeit, r in fahrplan[start] if r == richtung and zeit >= self.startzeit]
            if not kandidaten:
                raise ValueError("Keine Bahn verfügbar.")

        return float(min(kandidaten))

    def ankunftszeit(self, start, ziel, abfahrtszeit):
        indices = {s.name: i for i, s in enumerate(self.stationen)}
        start_i = indices[start]
        ziel_i = indices[ziel]

        zeit = float(abfahrtszeit)
        schritt = 1 if ziel_i > start_i else -1
        i = start_i

        # Keine Haltezeit an Startstation
        while i != ziel_i:
            naechste = i + schritt
            if schritt == 1:
                zeit += self.stationen[i].fahrzeit_zur_naechsten
            else:
                zeit += self.stationen[naechste].fahrzeit_zur_naechsten

            # Haltezeit an der Ziel-Zwischenstation
            zeit += self.haltezeit(self.stationen[naechste])
            i = naechste

        return float(zeit)
