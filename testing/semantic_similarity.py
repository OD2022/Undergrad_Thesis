from scipy.spatial import distance
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
 

kg_file = ""
with open("kgfile.txt", "r") as file:
    kg_file = file.read().replace("\n", " ")
    #print(kg_file)

vd_file = ""
with open("vdfile.txt", "r") as file:
    vd_file = file.read().replace("\n", " ")
    #print(vd_file)


test_vec = model.encode([vd_file])[0]
similarity_score = 1-distance.cosine(test_vec, model.encode([kg_file])[0])
print(f'\nFor kg_llm and vd_llm\nSimilarity Score = {similarity_score} ')