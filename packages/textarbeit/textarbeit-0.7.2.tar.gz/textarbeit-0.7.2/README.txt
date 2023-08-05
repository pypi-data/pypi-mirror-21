Titel: textarbeit
Version: 0.7.2
Zweck: Routinen, um reine Texte (*.txt) zu bearbeiten
Pythonversion: Python3
Autor: Batt Bucher
email: batt.bucher.basel@bluewin.ch
---------------------------------------------------------

Das Modul 'textarbeit' bietet Routinen, um reine Texte (*.txt) zu bearbeiten.

ACHTUNG: Es werden nur reine Textdateien verarbeitet 
(Ich arbeite mit Linux!)

Folgende Funktionen stellt es zur Verfügung:

help(textarbeit) - gibt eine eine kurze Hilfe zu jeder Funktion aus

Text2Liste(einDatei, ausDatei) - erstellt eine Liste aller Woerter
Text2ListeRein(einDatei, ausDatei): - erstellt eine Liste ohne Sonderzeichen
ListeOhneLeerzeilen(einDatei, ausDatei): entfernt alle Leerzeilen
ListeRein(einDatei, ausDatei) - entfernt Sonderzeichen
ListeSortiert(einDatei, ausDatei): - gibt eine sortierte Liste aus
ListeOhneDuplikate(einDatei, ausDatei) - entfernt alle Duplikate

ListeAnzahlWort(einDatei, ausDatei): - gibt eine Liste geordnet nach Anzahl aus
ListeWortAnzahl(einDatei, ausDatei): gibt eine alphabetische Liste mit Anzahl aus

ZahlPunktLoeschen(einDatei, ausDatei) - 123. Hallo wird Hallo

Minus3Lz(einDatei, ausDatei) - macht aus 3 Leerzeichen 1
Minus2Lz(einDatei, ausDatei) - macht aus 2 Leerzeichen 1
MinusLzLinks(einDatei, ausDatei) - entfernt Leerzeichen links
MinusLzRechts(einDatei, ausDatei) - entfernt Leerzeichen rechts

Anwendungsbeispiel:
import textarbeit
textarbeit.Minus3Lz("/home/beat/texte.txt","/home/beat/texte2.txt")
textarbeit.Text2Liste("/home/beat/texte.txt","/home/beat/texte2.lst")

