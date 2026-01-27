import math

class Haltestelle:
    def __init__(self, name, fahrzeit_ab_a):
        self.name = name
        self.fahrzeit_ab_a = fahrzeit_ab_a  # Minuten ab Start der Linie

class Linie:
    def __init__(self, name, intervall, startzeit, endzeit):
        self.name = name
        self.intervall = intervall  # Minuten zwischen Zügen
        self.startzeit = startzeit  # Minuten ab Mitternacht
        self.endzeit = endzeit      # Minuten ab Mitternacht
        self.haltestellen = []

    def add_haltestelle(self, haltestelle):
        self.haltestellen.append(haltestelle)

    def naechster_zug(self, haltestellen_name, gewünschte_uhrzeit):
        # Uhrzeit HH:MM → Minuten seit Mitternacht
        stunden, minuten = map(int, gewünschte_uhrzeit.split(":"))
        gewünschte_zeit = stunden * 60 + minuten

        # Haltestelle suchen
        haltestelle = next(
            (h for h in self.haltestellen if h.name == haltestellen_name.upper()),
            None
        )
        if haltestelle is None:
            raise ValueError(f"Haltestelle {haltestellen_name} existiert nicht.")

        offset = haltestelle.fahrzeit_ab_a

        # Erste mögliche Abfahrt an dieser Haltestelle
        erste_abfahrt = self.startzeit + offset
        letzte_abfahrt = self.endzeit + offset

        # Wenn gewünschte Zeit vor Betriebsbeginn liegt
        if gewünschte_zeit <= erste_abfahrt:
            naechster_zug = erste_abfahrt
        else:
            n = math.ceil((gewünschte_zeit - erste_abfahrt) / self.intervall)
            naechster_zug = erste_abfahrt + n * self.intervall

        # Prüfen, ob noch Betrieb ist
        if naechster_zug > letzte_abfahrt:
            raise ValueError("Zu dieser Uhrzeit fährt keine Bahn mehr.")

        # Rückgabe als HH:MM
        stunden_out = naechster_zug // 60
        minuten_out = naechster_zug % 60
        return f"{stunden_out:02d}:{minuten_out:02d}"

# Linie erstellen (05:00–23:00)
linie1 = Linie("Linie 1", intervall=10, startzeit=5*60, endzeit=23*60)

# Haltestellen hinzufügen
linie1.add_haltestelle(Haltestelle("A", 0))
linie1.add_haltestelle(Haltestelle("B", 2))
linie1.add_haltestelle(Haltestelle("C", 5))
linie1.add_haltestelle(Haltestelle("D", 6))

# Benutzerabfrage
haltestelle = input("Haltestelle eingeben (A, B, C oder D): ")
uhrzeit = input("Gewünschte Uhrzeit eingeben (HH:MM): ")

try:
    nächste_abfahrt = linie1.naechster_zug(haltestelle, uhrzeit)
    print(f"Nächster Zug an Haltestelle {haltestelle.upper()}: {nächste_abfahrt} Uhr")
except ValueError as e:
    print(e)