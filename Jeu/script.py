#script de l'animation pour le musee Fermat
import os

listeScores=[]
for i in range(0,11):
    for j in range(0,11):
        if i+j>=7 and max(i,j) <= 8 and i!=j:
            listeScores.append((i,j))

for i in range(48):
    x = listeScores[i]
    os.rename(f"videos/Graphe_{i:04d}.mp4",f"{x[0]}_{x[1]}.mp4")