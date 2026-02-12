class PreisLogik:
    PREISE = {
        "Kurzstrecke": 1.50,
        "Mittelstrecke": 2.00,
        "Langstrecke": 10.00
    }

    def __init__(self):
        pass  # keine Liste mehr nötig

    def ticket_typ(self, start, ziel, stationen):
        indices = {s.name: i for i, s in enumerate(stationen)}

        if start not in indices or ziel not in indices:
            raise ValueError("Unbekannte Station (Preislogik)")

        distanz = abs(indices[ziel] - indices[start])

        if distanz <= 3:
            return "Kurzstrecke"
        elif distanz <= 6:
            return "Mittelstrecke"
        else:
            return "Langstrecke"

    def berechne_preis(self, ticket_typ, ermaessigung="Nein", barzahlung="Nein", einzelfahrt="Nein"):
        """Berechnet den endgültigen Preis für die gewählte Kombination"""
        grundpreis = self.PREISE[ticket_typ]

        rabatt_prozent = 0
        aufpreis_prozent = 0

        if ermaessigung == "Ja":
            rabatt_prozent += 20
        if barzahlung == "Ja":
            aufpreis_prozent += 10
        if einzelfahrt == "Ja":
            aufpreis_prozent += 5

        endpreis = grundpreis * (1 - rabatt_prozent / 100) * (1 + aufpreis_prozent / 100)
        return round(endpreis, 2)