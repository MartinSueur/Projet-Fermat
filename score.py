from manim import *

class Score(Scene):
    def construct(self):
        def create_score(p1,p2,x=0,y=0,z=0,taille=1,strk_width=4):
            carre1 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x-0.5*taille,y,z])
            carre2 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+0.5*taille,y,z])
            i1 = Integer(number=p1,color=WHITE).move_to([x-0.5*taille,y,z]).scale(1.5*taille)
            i2 = Integer(number=p2,color=WHITE).move_to([x+0.5*taille,y,z]).scale(1.5*taille)
            return VGroup(carre1,carre2,i1,i2)
        
        
        j1 = ImageMobject("joueur-de-tennis-avec-raquette.png").shift(LEFT*2).scale(0.7)
        j2 = ImageMobject("joueur-de-tennis-avec-raquette2.png").shift(RIGHT*2).scale(0.7)
        p1 = ImageMobject("pluie.png").shift(UP*3+RIGHT*6).scale(0.7)
        p2 = ImageMobject("pluie.png").shift(UP*3+LEFT*6).scale(0.7)
        Ferdi = Text("Ferdinand").next_to(j1,UP).scale(0.5)
        Phili = Text("Philippe").next_to(j2,UP).scale(0.5)
        listeScore = [(1,0),(2,0),(2,1),(3,1)]
        
        xs1 = Integer(number=0).shift(DOWN*2.5+LEFT)
        xs2 = Integer(number=0).next_to(xs1,DOWN/2)
        f = Text("F:").next_to(xs1,LEFT/2).scale(0.7)
        p = Text("P:").next_to(xs2,LEFT/2).scale(0.7)
        match = Text("Match en 5 points").shift(UP*3).scale(0.8)
        finpartie = Text("On ne peut pas continuer la partie...").shift(DOWN*1.8).scale(0.5)
        mises = Text("Mises").shift(UP).scale(0.7)
        cent = Integer(number=100)
        
        listeInt = [xs1,xs2,f,p]
        mise1 = Integer(number=50).shift(LEFT/2)
        mise2 = Integer(number=50).shift(RIGHT/2)
        group = VGroup(mise1,mise2)

        self.play(AnimationGroup(FadeIn(j1),FadeIn(j2)))
        self.play(AnimationGroup(Write(Ferdi),Write(Phili)))
        self.play(Write(match))

        self.play(Write(mises))
        self.play(AnimationGroup(FadeIn(mise1,shift=RIGHT),FadeIn(mise2,shift=LEFT)))
        self.play(Transform(group,cent))

        self.play(AnimationGroup(
            Write(f),
            Write(p),
            Write(xs1),
            Write(xs2)
        ))

        for sc1,sc2 in listeScore:
            sco1 = Integer(number=sc1).next_to(xs1,RIGHT)
            sco2 = Integer(number=sc2).next_to(sco1,DOWN/2)
            if sc1 > xs1.get_value():
                self.play(AnimationGroup(Indicate(Ferdi),AnimationGroup(Write(sco1),Write(sco2)),lag_ratio=0.5))
            else:
                self.play(AnimationGroup(Indicate(Phili),AnimationGroup(Write(sco1),Write(sco2)),lag_ratio=0.5))
            listeInt+=[sco1,sco2]
            xs1 = sco1
            xs2 = sco2
        
        x1 = Text("X").scale(0.6).next_to(xs1,RIGHT)
        x2 = Text("X").scale(0.6).next_to(xs2,RIGHT)
        listeInt+=[x1,x2]

        self.play(AnimationGroup(FadeIn(p1,shift=LEFT),FadeIn(p2,shift=RIGHT)))
        self.play(AnimationGroup(Indicate(p1),Indicate(p2)))
        self.play(AnimationGroup(Write(x1),Write(x2)))
        self.play(Write(finpartie))

        self.play(AnimationGroup(
            AnimationGroup(*[FadeOut(Int,shift=DOWN*2) for Int in listeInt]),
            FadeOut(match,shift=UP*2),
            AnimationGroup(Unwrite(Ferdi),Unwrite(Phili)),
            AnimationGroup(FadeOut(j1,shift=LEFT*4),FadeOut(j2,shift=RIGHT*4)),
            Unwrite(finpartie),
            AnimationGroup(FadeOut(p1,shift=RIGHT),FadeOut(p2,shift=LEFT)),
        ))
        
        egal = Text("=").move_to([-5.125,3.5,0]).scale(0.7)
        self.remove(group)
        self.play(AnimationGroup(mises.animate.move_to([-6,3.5,0]),cent.animate.move_to([-4.5,3.5,0]),Write(egal),lag_ratio=0.5))
        comment = Text("Comment répartir les mises entre les deux joueurs ?").shift(UP*2.5+LEFT*1.75).scale(0.7)
        self.play(Write(comment))
        theo = Text("Théorème des partis")
        under = Underline(theo)
        self.play(Write(theo),Write(under))
        
        self.play(
            AnimationGroup(
                FadeOut(theo,shift=UP*3),
                FadeOut(mises,shift=UP),
                FadeOut(cent,shift=UP),
                FadeOut(egal,shift=UP),
                FadeOut(under,shift=UP*3),
                FadeOut(comment,shift=UP*2)
            ))
        
        titre = Title("Théorème des partis")
        self.play(Write(titre))
        recap = Text("Récapitulons la partie sous forme d'arbre :").scale(0.7).next_to(titre,DOWN)
        self.play(Write(recap))

        def suiteScore(score):
            a,b = score
            return [(a+1,b),(a,b+1)]

        def createArbreScores(scores,arret,hauteur=-1,bord=-5,taille=0.2,strk_w=4,renvoieExt=False):
            h = hauteur
            x = bord
            ex = (0,0)
            c=0
            espx = 2.5*taille
            espy = espx/1.75
            extremites = []
            listMobj = [create_score(ex[0],ex[1],(bord+0.6)*espx+taille,(hauteur+(ex[0]-ex[1]))*espy,0,taille,strk_width=strk_w)]
            for a,b in scores:
                c+=1
                if a > ex[0]:
                    listMobj.append(Line([(bord+c)*espx+taille,(hauteur+(ex[0]-ex[1]))*espy+taille/2,0],[(bord+1+c)*espx-taille,(hauteur+(a-b))*espy-taille/2,0],stroke_width=strk_w))
                    h+=espy
                    x+=espx
                elif b > ex[1]:
                    listMobj.append(Line([(bord+c)*espx+taille,(hauteur+(ex[0]-ex[1]))*espy-taille/2,0],[(bord+1+c)*espx-taille,(hauteur+(a-b))*espy+taille/2,0],stroke_width=strk_w))
                    h-=espy
                    x+=espx
                else:
                    print("erreur")
                listMobj.append(create_score(a,b,espx*(c+bord+1),(hauteur+(a-b))*espy,0,taille,strk_width=strk_w))
                ex = (a,b)
            pileScore = suiteScore(ex)
            for i in range((len(scores)+1),arret*2):
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
                    j = score[0]-score[1]
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
                            listMobj.append(create_score(score[0],score[1],espx*(i+bord+1),(hauteur+j)*espy,0,taille,strk_width=strk_w))
                        else:
                            listMobj.append(Line([(i+bord)*espx+taille,(hauteur+j+1)*espy-taille/2,0],[espx*(i+bord+1)-taille,(hauteur+j)*espy+taille/2,0],stroke_width=strk_w))
                            listMobj.append(create_score(score[0],score[1],espx*(i+bord+1),(hauteur+j)*espy,0,taille,strk_width=strk_w))
                        p+=1
                        memoire.append(score)
                pileScore=bloc
            if renvoieExt:
                return extremites
            return listMobj
                

        arbre = createArbreScores(listeScore,5,-2,-5.5,0.5)
        extremites = createArbreScores(listeScore,5,-2,-5.5,0.5,4,True)

        self.play(AnimationGroup(*[FadeIn(arbre[i]) if i%2==0 else Write(arbre[i]) for i in range(len(arbre))]))

        pourcents = []
        i=0
        for e in extremites:
            if i in [0,1,2,4]:
                pourcents+= [Integer(number=100,color=GREEN).scale(0.4).next_to(e,RIGHT/2).shift(UP*0.15),Integer(number=0,color=BLUE).scale(0.4).next_to(e,RIGHT/2).shift(UP*-0.15)]
            else:
                pourcents+= [Integer(number=0,color=GREEN).scale(0.4).next_to(e,RIGHT/2).shift(UP*0.15),Integer(number=100,color=BLUE).scale(0.4).next_to(e,RIGHT/2).shift(UP*-0.15)]
            i+=1
        self.play(AnimationGroup(*[Write(pour) for pour in pourcents]))
        
        score44 = [Integer(number=50,color=GREEN).scale(0.4).next_to(arbre[34],RIGHT/2).shift(UP*0.15),Integer(number=50,color=BLUE).scale(0.4).next_to(arbre[34],RIGHT/2).shift(UP*-0.15)]
        self.play(AnimationGroup(*[Write(s) for s in score44]))
        score3443 = [Integer(number=75,color=GREEN).scale(0.4).next_to(arbre[26],RIGHT/2).shift(UP*0.15),Integer(number=25,color=BLUE).scale(0.4).next_to(arbre[26],RIGHT/2).shift(UP*-0.15)]+[Integer(number=25,color=GREEN).scale(0.4).next_to(arbre[28],RIGHT/2).shift(UP*0.15),Integer(number=75,color=BLUE).scale(0.4).next_to(arbre[28],RIGHT/2).shift(UP*-0.15)]
        self.play(AnimationGroup(*[Write(s) for s in score3443]))
        score4233 = [Integer(number=87.5,num_decimal_places=1,color=GREEN).scale(0.4).next_to(arbre[18],RIGHT/2).shift(UP*0.15),Integer(number=12.5,color=BLUE,num_decimal_places=1).scale(0.4).next_to(arbre[18],RIGHT/2).shift(UP*-0.15)]+[Integer(number=50,color=GREEN).scale(0.4).next_to(arbre[20],RIGHT/2).shift(UP*0.15),Integer(number=50,color=BLUE).scale(0.4).next_to(arbre[20],RIGHT/2).shift(UP*-0.15)]
        self.play(AnimationGroup(*[Write(s) for s in score4233]))
        score4233 = [Integer(number=93.75,num_decimal_places=2,color=GREEN).scale(0.4).next_to(arbre[10],RIGHT/2).shift(UP*0.15),Integer(number=6.25,color=BLUE,num_decimal_places=2).scale(0.4).next_to(arbre[10],RIGHT/2).shift(UP*-0.15)]+[Integer(number=62.5,color=GREEN,num_decimal_places=1).scale(0.4).next_to(arbre[12],RIGHT/2).shift(UP*0.15),Integer(number=37.5,color=BLUE,num_decimal_places=1).scale(0.4).next_to(arbre[12],RIGHT/2).shift(UP*-0.15)]
        self.play(AnimationGroup(*[Write(s) for s in score4233]))
        score4233 = [Integer(number=78.125,num_decimal_places=3,color=GREEN).scale(0.4).next_to(arbre[8],RIGHT/2).shift(UP*0.15),Integer(number=21.875,color=BLUE,num_decimal_places=3).scale(0.4).next_to(arbre[8],RIGHT/2).shift(UP*-0.15)]
        self.play(AnimationGroup(*[Write(s) for s in score4233]))