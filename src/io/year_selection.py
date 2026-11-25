#Jahresabfrage
def year_selection() -> tuple[int, int]:
    a = int(input("Startjahr: ").strip())
    b = int(input("Endjahr: ").strip())
    return (a,b) if a<=b else (b,a) 