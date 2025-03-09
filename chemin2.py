from manim import *

class Arbre2(Scene):
    def construct(self):
        def create_score(p1,p2,x=0,y=0,z=0,taille=1,strk_width=4):
            carre1 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x-0.5*taille,y,z])
            carre2 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+0.5*taille,y,z])
            i1 = Integer(number=p1,color=WHITE).move_to([x-0.5*taille,y,z]).scale(1.5*taille)
            i2 = Integer(number=p2,color=WHITE).move_to([x+0.5*taille,y,z]).scale(1.5*taille)
            return VGroup(carre1,carre2,i1,i2)

        def suiteScore(score):
            a,b = score
            return [(a+1,b),(a,b+1)]

        def createArbreScores(scores,arret,hauteur=-1,bord=-5,taille=0.2,strk_w=4):
            h = hauteur
            x = bord
            ex = (0,0)
            c=0
            espx = 2.5*taille
            espy = espx/1.75
            listMobj = [create_score(ex[0],ex[1],(bord+0.6)*espx+taille,(hauteur+(ex[0]-ex[1]))*espy,0,taille,strk_width=strk_w)]
            for a,b in scores:
                c+=1
                listMobj.append(Line([(bord+c)*espx+taille,(hauteur+(ex[0]-ex[1]))*espy+taille/2,0],[(bord+1+c)*espx-taille,(hauteur+(a-b))*espy-taille/2,0],stroke_width=strk_w))
                h+=espy
                x+=espx
                listMobj.append(Line([(bord+c)*espx+taille,(hauteur+(ex[0]-ex[1]))*espy-taille/2,0],[(bord+1+c)*espx-taille,(hauteur+(a-b))*espy+taille/2,0],stroke_width=strk_w))
                h-=espy
                x+=espx
                listMobj.append(create_score(a,b,espx*(c+bord+1),(hauteur+(a-b))*espy,0,taille,strk_width=strk_w))
                ex = (a,b)
            return listMobj
        
        listeScore = [(0,1),(0,2),(0,3),(1,3),(2,3),(3,3)]

        arbre = createArbreScores(listeScore,15,hauteur=0,bord=-15.5,taille=0.19,strk_w=2)

        self.add(VGroup(*arbre))