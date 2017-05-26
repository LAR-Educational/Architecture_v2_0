import dialogue
import codecs

file = codecs.open('perguntas.txt', 'r+', encoding="utf-8")

for line in file:
	line = line.decode('utf-8')
	dialogue.run(line)