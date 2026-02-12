class PreisLogik:
    PREISE_EINZEL = {
        "Kurzstrecke": 1.50,
        "Mittelstrecke": 2.00,
        "Langstrecke": 3.00
    }
    PREISE_MEHRFAHRT = {
        "Kurzstrecke": 5.00,
        "Mittelstrecke": 7.00,
        "Langstrecke": 10.00
    }

    def __init__(self):
        pass

    def ticket_typ(self, start, ziel, stationen):
        indices = {s.name: i for i, s in enumerate(stationen)}

        if start not in indices or ziel not in indices:
            raise ValueError("Unbekannte Station (Preislogik)")

        distanz = abs(indices[ziel] - indices[start])


        if distanz <= 3:
            return "Kurzstrecke"
        elif distanz <= 8:
            return "Mittelstrecke"
        else:
            return "Langstrecke"

    def berechne_preis(self, ticket_typ, ermaessigung="Nein", barzahlung="Nein", einzelfahrt="Nein"):
        """Berechnet den endgültigen Preis basierend auf der Wahl"""

        # Wahl der Preisliste
        if einzelfahrt == "Ja":
            grundpreis = self.PREISE_EINZEL[ticket_typ]
        else:
            grundpreis = self.PREISE_MEHRFAHRT[ticket_typ]

        prozent_summe = 0

        if ermaessigung == "Ja":
            prozent_summe -= 20
        if barzahlung == "Ja":
            prozent_summe += 15
        if einzelfahrt == "Ja":
            prozent_summe += 10

        # Anwendung der Summe auf den Grundpreis
        endpreis = grundpreis * (1 + prozent_summe / 100)
        return round(endpreis, 2)