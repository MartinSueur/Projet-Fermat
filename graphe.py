from manim import *
from math import floor

class Graphe(Scene):
    def construct(self):


        def create_score(p1,p2,x=0,y=0,z=0,taille=1,strk_width=4):
            carre1 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x-0.5*taille,y,z])
            carre2 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+0.5*taille,y,z])
            i1 = Integer(number=p1,color=PURPLE).move_to([x-0.5*taille,y,z]).scale(1.5*taille)
            i2 = Integer(number=p2,color=RED).move_to([x+0.5*taille,y,z]).scale(1.5*taille)
            return VGroup(carre1,carre2,i1,i2)
        
        def get_calcul(x=0,y=0,z=0,taille=1,strk_width=4):
            carre1 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x-0.5*taille,y,z])
            carre2 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+0.5*taille,y,z])
            i1 = MathTex("n",color=PURPLE).move_to([x-0.5*taille,y,z]).scale(taille*0.75)
            i2 = MathTex("m",color=RED).move_to([x+0.5*taille,y,z]).scale(taille*0.75)
            l1 = Line([taille,taille/2,0],[3*taille/2,taille,0],stroke_width=strk_width)
            l2 = Line([taille,-taille/2,0],[3*taille/2,-taille,0],stroke_width=strk_width)
            carre3 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+2*taille,y+1.5,z])
            carre4 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+3*taille,y+1.5,z])
            i3 = MathTex("n+1",color=PURPLE).move_to([x+2*taille,y+1.5,z]).scale(taille*0.75)
            i4 = MathTex("m",color=RED).move_to([x+3*taille,y+1.5,z]).scale(taille*0.75)
            carre5 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+2*taille,y-1.5,z])
            carre6 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+3*taille,y-1.5,z])
            i5 = MathTex("n",color=PURPLE).move_to([x+2*taille,y-1.5,z]).scale(taille*0.75)
            i6 = MathTex("m+1",color=RED).move_to([x+3*taille,y-1.5,z]).scale(taille*0.75)
            p1 = MathTex(r"\frac{a+c}{2}",color=PURPLE).next_to(carre2,taille*0.5*RIGHT).shift(UP*(taille/2.5)).scale(taille*0.5)
            p2 = MathTex(r"\frac{b+d}{2}",color=RED).next_to(carre2,taille*0.5*RIGHT).shift(DOWN*(taille/2.5)).scale(taille*0.5)
            p3 = MathTex("a",color=PURPLE).next_to(carre4,taille*0.75*RIGHT).shift(UP*(taille/2.5)).scale(taille*0.75)
            p4 = MathTex("b",color=RED).next_to(carre4,taille*0.75*RIGHT).shift(DOWN*(taille/2.5)).scale(taille*0.75)
            p5 = MathTex("c",color=PURPLE).next_to(carre6,taille*0.75*RIGHT).shift(UP*(taille/2.5)).scale(taille*0.75)
            p6 = MathTex("d",color=RED).next_to(carre6,taille*0.75*RIGHT).shift(DOWN*(taille/2.5)).scale(taille*0.75)
            return VGroup(carre1,carre2,i1,i2,l1,l2,carre3,carre4,i3,i4,carre5,carre6,i5,i6,p1,p2,p3,p4,p5,p6)

        def suiteScore(score):
            a,b = score
            return [(a+1,b),(a,b+1)]

        def createArbreScores(a,b,arret,hauteur=-1,bord=-5,taille=0.2,strk_w=4,renvoieExt=False):
            h = hauteur
            x = bord
            ex = (0,0)
            c = 0
            dico = {}
            espx = 2.5*taille
            espy = espx/1.75
            extremites = []
            obj = create_score(a,b,espx*(bord),(hauteur)*espy,0,taille,strk_width=strk_w)
            listMobj = [obj]
            ex = (a,b)
            dico[ex] = obj
            pileScore = suiteScore(ex)
            for i in range(0,arret*2):
                bloc = []
                memoire = []
                p = 0
                for score in pileScore:
                    extremite = False
                    if score[0] < arret and score[1] < arret and score not in memoire:
                        bloc += suiteScore(score)
                    else:
                        if score not in memoire:
                            extremite = True
                    j = (score[0]-score[1])-(a-b)
                    if extremite and renvoieExt:
                        if p%2==0:
                            extremites.append(create_score(score[0],score[1],espx*(i+bord+1),(hauteur+j)*espy,0,taille,strk_width=strk_w))
                        else:
                            extremites.append(create_score(score[0],score[1],espx*(i+bord+1),(hauteur+j)*espy,0,taille,strk_width=strk_w))
                        p+=1
                        memoire.append(score)
                    else:
                        if p%2==0:
                            listMobj.append(Line([(i+bord)*espx+taille,(hauteur+j-1)*espy+taille/2,0],[espx*(i+bord+1)-taille,(hauteur+j)*espy-taille/2,0],stroke_width=strk_w))
                            obj = create_score(score[0],score[1],espx*(i+bord+1),(hauteur+j)*espy,0,taille,strk_width=strk_w)
                            listMobj.append(obj)
                            dico[score] = obj
                        else:
                            listMobj.append(Line([(i+bord)*espx+taille,(hauteur+j+1)*espy-taille/2,0],[espx*(i+bord+1)-taille,(hauteur+j)*espy+taille/2,0],stroke_width=strk_w))
                            obj = create_score(score[0],score[1],espx*(i+bord+1),(hauteur+j)*espy,0,taille,strk_width=strk_w)
                            listMobj.append(obj)
                            dico[score] = obj
                        p+=1
                        memoire.append(score)
                pileScore=bloc
            if renvoieExt:
                return extremites
            return listMobj,dico
        
        def numDec(x):
            i=0
            while x-floor(x)>0:
                x*=10
                i+=1
            return i

        def partis1(score,x,taille=1):
            x = round(x,2)
            return [Integer(number=x,color=PURPLE,num_decimal_places=min(numDec(x),2)).scale(taille).next_to(score,taille*RIGHT).shift(UP*(taille/2.5)),Integer(number=100-x,color=RED,num_decimal_places=min(numDec(100-x),2)).scale(taille).next_to(score,taille*RIGHT).shift(UP*-(taille/2.5))]
        
        def calcule_partis(score,arret):
            if score[0] == arret:
                dicoPartis[score] = (100,0)
                return (100,0)
            elif score[1] == arret:
                dicoPartis[score] = (0,100)
                return (0,100)
            else:
                res0 = calcule_partis((score[0]+1,score[1]),arret)
                res1 = calcule_partis((score[0],score[1]+1),arret)
                res = (res0[0]+res1[0])/2,(res0[1]+res1[1])/2
                dicoPartis[score] = res
                return res
        
        listeScores = [(0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 5), (2, 6), (2, 7), (2, 8), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (4, 3), (4, 5), (4, 6), (4, 7), (4, 8), (5, 2), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 7), (6, 8), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 8), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7)]

        t1 = Text("Voici la méthode de Pascal :").shift(UP*3).scale(0.5)
        t2 = Text("Il faut d'abord représenter tous les scores possibles si le jeu s'était poursuivi :").shift(UP*3).scale(0.5)
        t5 = Text("Avec un point de plus, on obtient deux scores possibles :").shift(UP*3).scale(0.5)
        t6 = Text("En itérant...").shift(UP*3).scale(0.5)
        t7 = Text("Le joueur qui arrive à 10 remporte l'intégralité des mises.").shift(UP*3).scale(0.5)
        t8 = Text("En suivant le principe du calcul, on remonte pas à pas jusqu'au score à l'arrêt du jeu :").shift(UP*3).scale(0.5)

        calcul = get_calcul(strk_width=2).shift(RIGHT*4.2).scale(0.5)

        for couple_scores in listeScores:
            scorej1 = couple_scores[0]
            scorej2 = couple_scores[1]

            arbre,dico = createArbreScores(scorej1,scorej2,10,hauteur=(scorej1-scorej2)/2-1.25,bord=-8,taille=0.3,strk_w=2)
            dicoPartis = {}
            terminaux = []

            calcule_partis((scorej1,scorej2),10)
            partis = []
            for score in dico.keys():
                if score[0]==10 or score[1] == 10:
                    terminaux.append(dico[score])
                    #arbre.remove(dico[score])
                partis+=partis1(dico[score],dicoPartis[score][0],0.3)
            partis.reverse()

            
            
            self.play(
                AnimationGroup(
                Write(t1),
                FadeIn(arbre[0]),
                lag_ratio=0.7)
            )
            self.wait(3)
            self.play(
                AnimationGroup(
                FadeOut(t1,shift=UP),
                Write(t2),
                lag_ratio=0.7)
            )
            self.wait(3)
            self.play(
                AnimationGroup(
                FadeOut(t2,shift=UP),
                Write(t5),
                AnimationGroup(FadeIn(arbre[1]),FadeIn(arbre[2])),
                AnimationGroup(FadeIn(arbre[3]),FadeIn(arbre[4])),
                lag_ratio=0.7)
            )
            self.wait(2)
            self.play(
                AnimationGroup(
                FadeOut(t5,shift=UP),
                Write(t6),
                AnimationGroup(*[FadeIn(arb) for arb in arbre[5:]],lag_ratio=0.1),
                lag_ratio=0.7))
            self.wait(3)
            self.play(
                AnimationGroup(
                FadeOut(t6,shift=UP),
                Write(t7),
                FadeIn(partis[0],partis[1],partis[2],partis[3]),
                lag_ratio=0.7))
            self.wait(3)
            self.play(
                AnimationGroup(
                FadeOut(t7,shift=UP),
                Write(t8),
                FadeIn(calcul),
                AnimationGroup(*[FadeIn(par) for par in partis[4:10]],lag_ratio=0.1),
                lag_ratio=0.7))
            self.wait(3)
            self.play(
                AnimationGroup(*[FadeIn(par) for par in partis[10:]],lag_ratio=0.1),
                lag_ratio=0.7)
            self.play(AnimationGroup(*[Indicate(par) for par in [partis[-1],partis[-2]]]))
            self.clear()
            self.next_section(f"{scorej1}-{scorej2}")
        