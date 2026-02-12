from datetime import datetime
from haltestellen import stationen
from Ubahn import LinieU1
from Preislogik import PreisLogik

def main():
    u1 = LinieU1(stationen)
    preislogik = PreisLogik()

    start = input("Start-Haltestelle: ")
    ziel = input("Ziel-Haltestelle: ")
    zeit = input("Früheste Abfahrtszeit (HH:MM): ")

    ermaessigung = input("Ermäßigung (Ja/Nein): ")
    barzahlung = input("Barzahlung (Ja/Nein): ")
    einzelfahrt = input("Einzelfahrt (Ja/Nein): ")

    try:
        abfahrt_min = u1.naechste_abfahrt(start, ziel, zeit)
        ankunft_min = u1.ankunftszeit(start, ziel, abfahrt_min)

        # Abfahrt / Ankunft HH:MM
        abfahrt_str = f"{int(abfahrt_min // 60):02d}:{int(round(abfahrt_min % 60)):02d}"
        ankunft_str = f"{int(ankunft_min // 60):02d}:{int(round(ankunft_min % 60)):02d}"

        ticket = preislogik.ticket_typ(start, ziel, stationen)
        preis = preislogik.berechne_preis(
            ticket_typ=ticket,
            ermaessigung=ermaessigung,
            barzahlung=barzahlung,
            einzelfahrt=einzelfahrt
        )

        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

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
