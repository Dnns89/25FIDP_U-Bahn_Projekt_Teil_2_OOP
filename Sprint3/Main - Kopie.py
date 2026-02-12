from datetime import datetime
from haltestellen import stationen
from Ubahn import LinieU1
from Preislogik import PreisLogik


def main():
    u1 = LinieU1(stationen)
    preislogik = PreisLogik()

    # ----------------------------
    # Benutzereingaben
    # ----------------------------
    start = input("Start-Haltestelle: ")
    ziel = input("Ziel-Haltestelle: ")
    zeit = input("Früheste Abfahrtszeit (HH:MM): ")

    ermaessigung = input("Ermäßigung (Ja/Nein): ")
    barzahlung = input("Barzahlung (Ja/Nein): ")
    einzelfahrt = input("Einzelfahrt (Ja/Nein): ")

    try:
        # ----------------------------
        # Nächste Abfahrt (liefert Minuten seit 00:00)
        # ----------------------------
        abfahrt_min = u1.naechste_abfahrt(start, ziel, zeit)

        # ----------------------------
        # Ankunft berechnen (liefert Minuten seit 00:00)
        # ----------------------------
        ankunft_min = u1.ankunftszeit(start, ziel, abfahrt_min)

        # ----------------------------
        # Formatieren in HH:MM
        # ----------------------------
        abfahrt_str = f"{int(abfahrt_min // 60):02d}:{int(abfahrt_min % 60):02d}"
        ankunft_str = f"{int(ankunft_min // 60):02d}:{int(ankunft_min % 60):02d}"

        # ----------------------------
        # Ticket & Preis berechnen
        # ----------------------------
        ticket = preislogik.ticket_typ(start, ziel, stationen)
        preis = preislogik.berechne_preis(ticket, ermaessigung, barzahlung, einzelfahrt)

        # ----------------------------
        # Zeitstempel
        # ----------------------------
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # ----------------------------
        # Ausgabe
        # ----------------------------
        print("\n--- Verbindung ---")
        print(f"Zeitstempel: {timestamp}")
        print(f"Abfahrt:  {abfahrt_str}")
        print(f"Ankunft:  {ankunft_str}")
        print(f"Ticket:   {ticket}")
        print(f"Preis:    {preis:.2f} €")

    except ValueError as e:
        print("Fehler:", e)


if __name__ == "__main__":
    main()