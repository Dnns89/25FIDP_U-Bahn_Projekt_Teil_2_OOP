class Station:
    def __init__(self, name, fahrzeit_zur_naechsten):
        self.name = name
        self.fahrzeit_zur_naechsten = fahrzeit_zur_naechsten  # Minuten


# ----------------------------
# U1 Daten
# ----------------------------

u1_daten = [
    ("Langwasser Süd", 3),
    ("Gemeinschaftshaus", 2),
    ("Langwasser Mitte", 2),
    ("Scharfreiterring", 3),
    ("Langwasser Nord", 2),
    ("Messe", 3),
    ("Bauernfeindstraße", 2),
    ("Hasenbuck", 2),
    ("Frankenstraße", 2),
    ("Maffeiplatz", 1),
    ("Aufseßplatz", 2),
    ("Hauptbahnhof", 2),
    ("Lorenzkirche", 3),
    ("Weißer Turm", 2),
    ("Plärrer", 2),
    ("Gostenhof", 1),
    ("Bärenschanze", 2),
    ("Maximilianstraße", 2),
    ("Eberhardshof", 2),
    ("Muggenhof", 3),
    ("Stadtgrenze", 2),
    ("Jakobinenstraße", 3),
    ("Fürth Hbf.", 0)
]

stationen = [Station(name, zeit) for name, zeit in u1_daten]