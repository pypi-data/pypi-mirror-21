"""Das Modul 'textarbeit' bietet Routinen, um reine Texte (*.txt) zu bearbeiten.

Version: 0.8.0

Folgende Funktionen stellt es zur Verfügung:

Text2Liste(einDatei, ausDatei) - erstellt eine Liste aller Wörter
Text2ListeRein(einDatei, ausDatei): - erstellt eine Liste ohne Sonderzeichen
ListeOhneLeerzeilen(einDatei, ausDatei): entfernt alle Leerzeilen
ListeRein(einDatei, ausDatei) - entfernt Sonderzeichen
ListeSortiert(einDatei, ausDatei): - gibt eine sortierte Liste aus
ListeOhneDuplikate(einDatei, ausDatei) - entfernt alle Duplikate

ListeAnzahlWort(einDatei, ausDatei): gibt eine Liste geordnet nach Anzahl aus
ListeWortAnzahl(einDatei, ausDatei): gibt eine alphabetische Liste mit Anzahl aus
ListeMinus100(einDatei, ausDatei): löscht die 100 häufigsten deutschen Wörter (laut Wikipedia)

ZahlPunktLoeschen(einDatei, ausDatei) - 123. Hallo wird Hallo

Minus3Lz(einDatei, ausDatei) - macht aus 3 Leerzeichen 1
Minus2Lz(einDatei, ausDatei) - macht aus 2 Leerzeichen 1
MinusLzLinks(einDatei, ausDatei) - entfernt Leerzeichen links
MinusLzRechts(einDatei, ausDatei) - entfernt Leerzeichen rechts


Anwendungsbeispiel:
textarbeit.Minus3Lz("/home/beat/texte.txt","/home/beat/texte2.txt")
(es muss der exakte Pfad angegeben werden!)
"""

#**********************Listen*********************************

def Text2Liste(einDatei, ausDatei):
     """Liest einen Text (*.txt-Datei) ein und speichert ihn als Liste
     (ein Wort pro Zeile) wieder ab.
     """
     einText = open(einDatei)
     ausText = open(ausDatei, "w")
     for line in einText:
          Woerter=line.split(" ")
          for Wort in Woerter:
               ausText.write(Wort+"\n")
     ausText.close()
     einText.close()

def Text2ListeRein(einDatei, ausDatei):
     """Liest einen Text (*.txt-Datei) ein und speichert ihn als Liste
     (ein Wort pro Zeile), ohne Sonderzeichen wieder ab.
     """
     liste1 = []
     einText = open(einDatei)
     ausText = open(ausDatei, "w")
     for line in einText:
          Woerter=line.split(" ")
          for Wort in Woerter:
               liste1.append(Wort)
     ZeichenTuple=("»", "«", ">", "<", "*", "^", "'", '"', "“", "”", ",", ".", \
                   ";", ":", "+", "–", "−","—", "±", "-", "_", "!", "?", "=", "@", \
                   "#", "&", "%", " ", "(", ")", "[", "]", "{", "}", "›", "‹", "`", \
                   "‘", "’", "/", "|", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "\t")
     liste2 = []
     for Wort in liste1:
          for zeichen in ZeichenTuple:
               Wort = Wort.replace(zeichen, "")
          liste2.append(Wort)
     for Wort in liste2:
         if Wort != "\n":
             ausText.write(Wort+"\n")
     ausText.close()
     einText.close()

def ListeMinus100(einDatei, ausDatei):
     """ liest eine reine Liste ein, und eliminiert die in der Liste der
     100 häufigsten deutschen Wörter (nach Wikipedia) stehenden. Die
     resultierende Liste wird unter dem 2. Namen gespeichert.
     """
     L1=[]
     L2=['die','der','und','in','zu','den','das','nicht','von','sie','ist',\
     'des','sich','mit','dem','dass','er','es','ein','ich','auf','so',\
     'eine','auch','als','an','nach','wie','im','für','man','aber','aus',\
     'durch','wenn','nur','war','noch','werden','bei','hat','wir','was',\
     'wird','sein','einen','welche','sind','oder','zur','um','haben',\
     'einer','mir','über','ihm','diese','einem','ihr','uns','da','zum',\
     'kann','doch','vor','dieser','mich','ihn','du','hatte','seine','mehr',\
     'am','denn','nun','unter','sehr','selbst','schon','hier','bis','habe',\
     'ihre','dann','ihnen','seiner','alle','wieder','meine','Zeit','gegen',\
     'vom','ganz','einzelnen','wo','muss','ohne','eines','können','sei']
     einText = open(einDatei)
     for wort in einText:
         wort = wort.replace("\n", "")
         if wort != "":
             L1.append(wort)
     einText.close()
     L3 = list(set(L1) - set(L2))
     ausText = open(ausDatei, "w")
     for wort in L3:
          ausText.write(wort+"\n")
     ausText.close()

def ListeOhneLeerzeilen(einDatei, ausDatei):
     """Liest eine Liste ein und entfernt alle Leerzeilen
     """
     einText = open(einDatei)
     ausText = open(ausDatei, "w") 
     liste = []
     for Wort in einText:
          liste.append(Wort)
     for Wort in liste:
         if Wort != "\n": #eliminiert leere Zeile
             ausText.write(Wort)
     ausText.close()
     einText.close()

def ListeRein(einDatei, ausDatei):
     """liest eine Liste (*.txt-Datei) ein, entfernt alle Sonderzeichen
     der deutschen Sprache und speichert die Liste unter dem 2. Namen 
     Wort für Wort ab.
     """
     einText = open(einDatei)
     ausText = open(ausDatei, "w")
     ZeichenTuple=("»", "«", ">", "<", "*", "^", "'", '"', "“", "”", ",", ".", \
                   ";", ":", "+", "–", "−","—", "±", "-", "_", "!", "?", "=", "@", \
                   "#", "&", "%", " ", "(", ")", "[", "]", "{", "}", "›", "‹", "`", \
                   "‘", "’", "/", "|", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "\t")
     liste = []
     for Wort in einText:
          for zeichen in ZeichenTuple:
               Wort = Wort.replace(zeichen, "")
          liste.append(Wort)
     for Wort in liste:
           if Wort != "\n": #eliminiert leere Zeile
                ausText.write(Wort)
     ausText.close()
     einText.close()

def ListeAnzahlWort(einDatei, ausDatei):
     """liest eine gereinigte Liste (*.txt-Datei) ein, zählt die Anzahl 
     verschiedener Wörter und gibt eine Liste sortiert nach Häufigkeit
     in der Form Anzahl Wort aus:
     0212 da
     0122 hier
     """
     einText = open(einDatei, "r")
     ausText = open(ausDatei, "w")
     Anzahl = dict()
     liste = []
     for Wort in einText:
          Wort = Wort.replace("\n", "")
          if Wort not in Anzahl:
               Anzahl[Wort] = 1
          else:
               Anzahl[Wort] += 1
     for key in Anzahl:
          AnzahlundWort = ("{0:04d}".format(Anzahl[key])+" "+key)
          liste.append(AnzahlundWort)
     liste.sort(key=str.lower, reverse=True)
     for Wort in liste:
          ausText.write(Wort+"\n")
     einText.close()
     ausText.close()

def ListeWortAnzahl(einDatei, ausDatei):
     """liest eine gereinigte Liste (*.txt-Datei) ein, zählt die Anzahl 
     verschiedener Wörter und gibt eine Liste sortiert nach Häufigkeit
     in der Form Wort Anzahl aus:
     da 22
     hier 21
     """
     einText = open(einDatei, "r")
     ausText = open(ausDatei, "w")
     Anzahl = dict()
     liste = []
     for Wort in einText:
          Wort = Wort.replace("\n", "")
          if Wort not in Anzahl:
               Anzahl[Wort] = 1
          else:
               Anzahl[Wort] += 1
     for key in Anzahl:
          WortundAnzahl = (key+" "+"{0:04d}".format(Anzahl[key]))
          liste.append(WortundAnzahl)
     liste.sort(key=str.lower)
     for Wort in liste:
          ausText.write(Wort+"\n")
     einText.close()
     ausText.close()

def ListeSortiert(einDatei, ausDatei):
     """ liest eine Liste (*.txt-Datei) ein, sortiert sie (lowercase) und speichert
     die sortierte Liste unter dem zweiten Namen ab.
     Es ist zu empfehlen, diese Liste zuerst durch die Funktion
     Liste_rein(einDatei, ausDatei) von Sonderzeichen zu reinigen.
     """
     einText = open(einDatei)
     ausText = open(ausDatei, "w") 
     liste = []
     for Wort in einText:
          liste.append(Wort)
     liste.sort(key=str.lower)
     for Wort in liste:
          ausText.write(Wort)
     ausText.close()
     einText.close()

def ListeOhneDuplikate(einDatei, ausDatei):
     """ liest eine Liste (*.txt-Datei) ein, wandelt sie in ein Set (ungeordnete
     Unikate) und anschliessend wieder in eine Liste um. Die neue Liste wird
     unter dem angegebenen 2. Namen gespeichert.
     """
     Liste = []
     einText = open(einDatei)
     ausText = open(ausDatei, "w")
     for wort in einText:
          Liste.append(wort)
     Liste = list(set(Liste))
     Liste.sort()
     for wort in Liste:
          ausText.write(wort)
     einText.close()
     ausText.close()

def ZahlPunktLoeschen(einDatei, ausDatei):
     """ liest eine Textdatei ein und schreibt alle Wörter
     zeilenweise in die Ausgabedatei ohne die jeweils ersten Zeichen
     (Trenner ist ". ")
     123. Hallo   wird zu:   Hallo
     """
     einText = open(einDatei)
     ausText = open(ausDatei, "w")
     for line in einText:
          Wort = line.split(". ")
          ausText.write(Wort[1])
     einText.close()
     ausText.close()

#******************Leerzeichen eliminieren************************************

def Minus3Lz(einDatei, ausDatei):
    """Liest eine Textdatei ein, ersetzt 3 Leerzeichen 
    durch 1 Leerzeichen.
    """
    einText = open(einDatei)
    ausText = open(ausDatei, "w")
    for line in einText:
        Woerter=line.split("   ")
        for Wort in Woerter:
            ausText.write(" "+Wort)
    ausText.close()
    einText.close()

def Minus2Lz(einDatei, ausDatei):
    """Liest eine Textdatei ein, ersetzt 2 Leerzeichen 
    durch 1 Leerzeichen.
    """
    einText = open(einDatei)
    ausText = open(ausDatei, "w")
    for line in einText:
        Woerter=line.split("  ")
        for Wort in Woerter:
            ausText.write(" "+Wort)
    ausText.close()
    einText.close()    

def MinusLzLinks(einDatei, ausDatei):
    """Liest eine Textdatei ein und löscht alle Leerzeichen links.
    """
    einText = open(einDatei)
    ausText = open(ausDatei, "w")
    for line in einText:
        ausText.write(line.lstrip())
    einText.close()

def MinusLzRechts(einDatei, ausDatei):
    """Liest eine Textdatei ein und löscht alle Leerzeichen rechts.
    """
    einText = open(einDatei)
    ausText = open(ausDatei, "w")
    for line in einText:
        ausText.write(line.rstrip())
    einText.close()
