import textstat

with open("vdfile.txt", "r") as file:
    kg_file = file.read().replace("\n", " ")
    index = textstat.flesch_reading_ease(kg_file)
    print(index)
