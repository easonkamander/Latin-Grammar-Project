import re
import mysql.connector as mariadb
wordNI = 0
file = open('words.txt', 'r', encoding="utf8")
lines = file.readlines()
rawList = []


class rawWord:
    def __init__(self, word):
        self.type = re.search('  [\w\s\;\,\.\-\=\>\!\"\~\|\(\)\[\]\/]+?   ', word).group()[2:-3]
        self.latinRAW = re.search('#[\w\s\;\,\.\-\=\>\!\"\~\|\(\)\[\]\/]+?  ', word).group()[1:-2].lower()
        self.englishRAW = re.search(' \:\: [\w\s\;\,\.\-\=\>\!\"\~\|\(\)\[\]\/]+', word).group()[4:-2].lower()
        self.latin = re.split('\,\s', self.latinRAW)
        self.english = re.split('\;\s', self.englishRAW)
        for meaning in self.english:
            if len(meaning) > 2 and ((meaning[0] == '[' and meaning[-1] == ']') or (meaning[0] == '(' and meaning[-1] == ')')):
                self.english.remove(meaning)


allValues = []
for line in lines:
    rawLine = rawWord(line)
    values = []
    if len(rawLine.type) >= 6 and rawLine.type[0:6] == 'PREP  ':
        values = [
            (wordNI, '! Part Of Speech', 'Preposition'),
            (wordNI, 'Name', rawLine.latin[0])
        ]
        if len(rawLine.type) >= 9 and rawLine.type[6:9] == 'ABL':
            values.append((wordNI, '! Governed Case', 'Ablative'))
        else:
            values.append((wordNI, '! Governed Case', 'Accusative'))
    elif len(rawLine.type) >= 6 and rawLine.type[0:6] == 'INTERJ':
        values = [
            (wordNI, '! Part Of Speech', 'Interjection'),
            (wordNI, 'Name', rawLine.latin[0])
        ]
    elif len(rawLine.type) >= 4 and rawLine.type[0:4] == 'CONJ':
        values = [
            (wordNI, '! Part Of Speech', 'Conjunction'),
            (wordNI, 'Name', rawLine.latin[0])
        ]
    elif len(rawLine.type) >= 3 and rawLine.type[0:3] == 'ADV':
        values = [
            (wordNI, '! Part Of Speech', 'Adverb'),
            (wordNI, 'Positive', rawLine.latin[0])
        ]
        if len(rawLine.latin) > 1:
            if rawLine.latin[1] != '-':
                values.append((wordNI, 'Comparative', rawLine.latin[1]))
            if len(rawLine.latin) > 2:
                values.append((wordNI, 'Superlative', rawLine.latin[2]))
    elif len(rawLine.type) >= 2 and rawLine.type[0:2] == 'N ':
        values = [
            (wordNI, '! Part Of Speech', 'Noun'),
            (wordNI, 'Nominative Singular', rawLine.latin[0])
        ]
        if len(rawLine.latin) >= 2 and rawLine.latin[1] != 'undeclined':
            values.append((wordNI, 'Genetive Singular', rawLine.latin[1]))
            if rawLine.type[3:4] == '1':
                values.extend([
                    (wordNI, '! Declension', '1st'),
                    (wordNI, 'Dative Singular', rawLine.latin[1]),
                    (wordNI, 'Accusative Singular', rawLine.latin[1][:-2]+'am'),
                    (wordNI, 'Ablative Singular', rawLine.latin[0]),
                    (wordNI, 'Vocative Singular', rawLine.latin[0]),
                    (wordNI, 'Locative Singular', rawLine.latin[1]),
                    (wordNI, 'Nominative Plural', rawLine.latin[1]),
                    (wordNI, 'Genetive Plural', rawLine.latin[1][:-2]+'arum'),
                    (wordNI, 'Dative Plural', rawLine.latin[1][:-2]+'is'),
                    (wordNI, 'Accusative Plural', rawLine.latin[1][:-2]+'as'),
                    (wordNI, 'Ablative Plural', rawLine.latin[1][:-2]+'is'),
                    (wordNI, 'Vocative Plural', rawLine.latin[1]),
                    (wordNI, 'Locative Plural', rawLine.latin[1][:-2]+'is')
                ])
            elif rawLine.type[3:4] == '2':
                values.extend([
                    (wordNI, '! Declension', '2nd'),
                    (wordNI, 'Dative Singular', rawLine.latin[1][:-1]+'o'),
                    (wordNI, 'Accusative Singular', rawLine.latin[1][:-1]+'um'),
                    (wordNI, 'Ablative Singular', rawLine.latin[1][:-1]+'o'),
                    (wordNI, 'Locative Singular', rawLine.latin[1]),
                    (wordNI, 'Genetive Plural', rawLine.latin[1][:-1]+'orum'),
                    (wordNI, 'Dative Plural', rawLine.latin[1][:-1]+'is'),
                    (wordNI, 'Ablative Plural', rawLine.latin[1][:-1]+'is'),
                    (wordNI, 'Vocative Plural', rawLine.latin[1]),
                    (wordNI, 'Locative Plural', rawLine.latin[1][:-1]+'is')
                ])
                if rawLine.type[-2] == ' N':
                    values.extend([
                        (wordNI, 'Nominative Plural', rawLine.latin[1][:-1]+'a'),
                        (wordNI, 'Accusative Plural', rawLine.latin[1][:-1]+'a')
                    ])
                else:
                    values.extend([
                        (wordNI, 'Nominative Plural', rawLine.latin[1]),
                        (wordNI, 'Accusative Plural', rawLine.latin[1][:-1]+'os')
                    ])
                if rawLine.latin[0][:-3] == 'ius':
                    values.append((wordNI, 'Vocative Singular', rawLine.latin[1][:-1]))
                elif rawLine.latin[0][:-2] == 'us':
                    values.append((wordNI, 'Vocative Singular', rawLine.latin[1][:-1]+'e'))
                else:
                    values.append((wordNI, 'Vocative Singular', rawLine.latin[0]))
            elif rawLine.type[3:4] == '3':
                values.extend([
                    (wordNI, '! Declension', '3rd'),
                    (wordNI, 'Dative Singular', rawLine.latin[1][:-2]+'i'),
                    (wordNI, 'Ablative Singular', rawLine.latin[1][:-2]+'e'),
                    (wordNI, 'Locative Singular', rawLine.latin[1][:-2]+'i'),
                    (wordNI, 'Locative Singular', rawLine.latin[1][:-2]+'e'),
                    (wordNI, 'Vocative Singular', rawLine.latin[0]),
                    (wordNI, 'Dative Plural', rawLine.latin[1][:-2]+'ibus'),
                    (wordNI, 'Ablative Plural', rawLine.latin[1][:-2]+'ibus'),
                    (wordNI, 'Locative Plural', rawLine.latin[1][:-2]+'ibus')
                ])
                if rawLine.latin[0] == rawLine.latin[1] or (len(rawLine.latin[1])-len(rawLine.latin[0]) == 2 and rawLine.latin[1][-3:-2] not in ['a', 'e', 'i', 'o', 'u'] and rawLine.latin[1][-4:-3] not in ['a', 'e', 'i', 'o', 'u']):
                    values.append((wordNI, 'Genetive Plural', rawLine.latin[1][:-2]+'ium'))
                else:
                    values.append((wordNI, 'Genetive Plural', rawLine.latin[1][:-2]+'um'))
                if rawLine.type[-2] == ' N':
                    values.append((wordNI, 'Accusative Singular', rawLine.latin[0]))
                    if rawLine.latin[0] == rawLine.latin[1] or (len(rawLine.latin[1])-len(rawLine.latin[0]) == 2 and rawLine.latin[1][-3:-2] not in ['a', 'e', 'i', 'o', 'u'] and rawLine.latin[1][-4:-3] not in ['a', 'e', 'i', 'o', 'u']):
                        values.extend([
                            (wordNI, 'Nominative Plural', rawLine.latin[1][:-2]+'ia'),
                            (wordNI, 'Accusative Plural', rawLine.latin[1][:-2]+'ia'),
                            (wordNI, 'Vocative Plural', rawLine.latin[1][:-2]+'ia')
                        ])
                    else:
                        values.extend([
                            (wordNI, 'Nominative Plural', rawLine.latin[1][:-2]+'a'),
                            (wordNI, 'Accusative Plural', rawLine.latin[1][:-2]+'a'),
                            (wordNI, 'Vocative Plural', rawLine.latin[1][:-2]+'a')
                        ])
                else:
                    values.extend([
                        (wordNI, 'Accusative Singular', rawLine.latin[1][:-2]+'em'),
                        (wordNI, 'Nominative Plural', rawLine.latin[1][:-2]+'es'),
                        (wordNI, 'Accusative Plural', rawLine.latin[1][:-2]+'es'),
                        (wordNI, 'Vocative Plural', rawLine.latin[1][:-2]+'es')
                    ])
            elif rawLine.type[3:4] == '4':
                values.extend([
                    (wordNI, 'Ablative Singular', rawLine.latin[1][:-2]+'u'),
                    (wordNI, 'Vocative Singular', rawLine.latin[0]),
                    (wordNI, 'Genetive Plural', rawLine.latin[1][:-2]+'uum'),
                    (wordNI, 'Dative Plural', rawLine.latin[1][:-2]+'ibus'),
                    (wordNI, 'Ablative Plural', rawLine.latin[1][:-2]+'ibus')
                ])
                if rawLine.type[-2] == ' N':
                    values.extend([
                        (wordNI, 'Dative Singular', rawLine.latin[1][:-2]+'u'),
                        (wordNI, 'Accusative Singular', rawLine.latin[1][:-2]+'u'),
                        (wordNI, 'Nominative Plural', rawLine.latin[1][:-2]+'ua'),
                        (wordNI, 'Accusative Plural', rawLine.latin[1][:-2]+'ua'),
                        (wordNI, 'Vocative Plural', rawLine.latin[1][:-2]+'ua')
                    ])
                else:
                    values.extend([
                        (wordNI, 'Dative Singular', rawLine.latin[1][:-2]+'ui'),
                        (wordNI, 'Accusative Singular', rawLine.latin[1][:-2]+'um'),
                        (wordNI, 'Nominative Plural', rawLine.latin[1]),
                        (wordNI, 'Accusative Plural', rawLine.latin[1]),
                        (wordNI, 'Vocative Plural', rawLine.latin[1])
                    ])
            elif rawLine.type[3:4] == '5':
                values.extend([
                    (wordNI, 'Dative Singular', rawLine.latin[1]),
                    (wordNI, 'Accusative Singular', rawLine.latin[1][:-2]+'em'),
                    (wordNI, 'Ablative Singular', rawLine.latin[1][:-2]+'e'),
                    (wordNI, 'Locative Singular', rawLine.latin[1][:-2]+'e'),
                    (wordNI, 'Vocative Singular', rawLine.latin[0]),
                    (wordNI, 'Nominative Plural', rawLine.latin[0]),
                    (wordNI, 'Genetive Plural', rawLine.latin[1][:-2]+'erum'),
                    (wordNI, 'Dative Plural', rawLine.latin[1][:-2]+'ebus'),
                    (wordNI, 'Accusative Plural', rawLine.latin[0]),
                    (wordNI, 'Ablative Plural', rawLine.latin[1][:-2]+'ebus'),
                    (wordNI, 'Locative Plural', rawLine.latin[1][:-2]+'ebus'),
                    (wordNI, 'Vocative Plural', rawLine.latin[0])
                ])
            if rawLine.type[-2] == ' F':
                values.append((wordNI, '! Gender', 'Feminine'))
            if rawLine.type[-2] == ' M':
                values.append((wordNI, '! Gender', 'Masculine'))
            if rawLine.type[-2] == ' N':
                values.append((wordNI, '! Gender', 'Neuter'))
            if rawLine.type[-2] == ' C':
                values.append((wordNI, '! Gender', 'Feminine'))
                values.append((wordNI, '! Gender', 'Masculine'))
    elif len(rawLine.type) >= 3 and rawLine.type[0:3] == 'ADJ':
        values = [
            (wordNI, '! Part Of Speech', 'Adjective')
        ]
        if len(rawLine.latin) == 3:
            if rawLine.latin[0][:-2] == rawLine.latin[1][:-1] == rawLine.latin[2][:-2] and rawLine.latin[0][-2:] == 'us' and rawLine.latin[1][-1:] == 'a' and rawLine.latin[2][-2:] == 'um':
                pass
            elif rawLine.latin[0][:-2] == rawLine.latin[1][:-1] == rawLine.latin[2][:-13] and rawLine.latin[0][-2:] == 'us' and rawLine.latin[1][-1:] == 'a' and rawLine.latin[2][-13:] == 'um (gen -ius)':
                pass
            elif rawLine.latin[0][:-2] == rawLine.latin[1][:-2] == rawLine.latin[2][:-3] and rawLine.latin[0][-1:] == 'r' and rawLine.latin[1][-2:] == 'ra' and rawLine.latin[2][-3:] == 'rum':
                pass
            elif rawLine.latin[0][:-2] == rawLine.latin[1][:-3] == rawLine.latin[2][:-4] and rawLine.latin[0][-2:] == 'er' and rawLine.latin[1][-3:] == 'era' and rawLine.latin[2][-4:] == 'erum':
                pass
            elif rawLine.latin[0][:-2] == rawLine.latin[1][:-2] == rawLine.latin[2][:-1] and rawLine.latin[0][-2:] == 'is' and rawLine.latin[1][-2:] == 'is' and rawLine.latin[2][-1:] == 'e':
                pass
            elif rawLine.latin[0][:-2] == rawLine.latin[1][:-2] == rawLine.latin[2][:-2] and rawLine.latin[0][-2:] == 'es' and rawLine.latin[1][-2:] == 'es' and rawLine.latin[2][-2:] == 'es':
                pass
            elif rawLine.latin[0][:-2] == rawLine.latin[1][:-2] == rawLine.latin[2][:-2] and rawLine.latin[0][-2:] == 'os' and rawLine.latin[1][-2:] == 'os' and rawLine.latin[2][-2:] == 'on':
                pass
            elif rawLine.latin[1] == '(gen.)' and rawLine.latin[2][-2:] == 'is':
                pass
            elif rawLine.latin[1] == '(gen.)' and rawLine.latin[2][-2:] == 'os':
                pass
            else:
                print(rawLine.latin)
    if len(values) == 0 and rawLine.type[0:1] != 'V' and rawLine.type[0:3] != 'ADJ' and rawLine.type[0:3] != 'NUM' and rawLine.type[0:4] != 'PRON' and rawLine.type[0:4] != 'PACK' and rawLine.type != ' ':
        print("'"+rawLine.type+"'")
    for meaning in rawLine.english:
        values.append((wordNI, 'Meaning', meaning))
    allValues.extend(values)
    wordNI += 1
latindb = mariadb.connect(
    host='localhost',
    user='root',
    passwd=,
    database='latindb'
)
cursor = latindb.cursor()
cursor.execute('DELETE FROM words')
cursor.executemany('INSERT INTO words (word, name, value) VALUES (%s, %s, %s)', allValues)
latindb.commit()
