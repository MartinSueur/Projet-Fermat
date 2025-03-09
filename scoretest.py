from manim import *
from math import floor

class Score(Scene):
    def construct(self):
        def create_score(p1,p2,x=0,y=0,z=0,taille=1,strk_width=4):
            carre1 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x-0.5*taille,y,z])
            carre2 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+0.5*taille,y,z])
            i1 = Integer(number=p1,color=WHITE).move_to([x-0.5*taille,y,z]).scale(1.5*taille)
            i2 = Integer(number=p2,color=WHITE).move_to([x+0.5*taille,y,z]).scale(1.5*taille)
            return VGroup(carre1,carre2,i1,i2)
        
        def partis1(score,x,taille=1):
            x = round(x,2)
            return [Integer(number=x,color=RED,num_decimal_places=min(numDec(x),2)).scale(taille).next_to(score,taille*RIGHT).shift(UP*(taille/2.5)),Integer(number=100-x,color=PURPLE,num_decimal_places=min(numDec(100-x),2)).scale(taille).next_to(score,taille*RIGHT).shift(UP*-(taille/2.5))]


        def get_calcul(x=0,y=0,z=0,taille=1,strk_width=4):
            carre1 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x-0.5*taille,y,z])
            carre2 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+0.5*taille,y,z])
            i1 = MathTex("n",color=RED).move_to([x-0.5*taille,y,z]).scale(taille*0.75)
            i2 = MathTex("m",color=PURPLE).move_to([x+0.5*taille,y,z]).scale(taille*0.75)
            l1 = Line([taille,taille/2,0],[3*taille/2,taille,0],stroke_width=strk_width)
            l2 = Line([taille,-taille/2,0],[3*taille/2,-taille,0],stroke_width=strk_width)
            carre3 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+2*taille,y+1.5,z])
            carre4 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+3*taille,y+1.5,z])
            i3 = MathTex("n+1",color=RED).move_to([x+2*taille,y+1.5,z]).scale(taille*0.75)
            i4 = MathTex("m",color=PURPLE).move_to([x+3*taille,y+1.5,z]).scale(taille*0.75)
            carre5 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+2*taille,y-1.5,z])
            carre6 = Square(taille,color=WHITE,stroke_width=strk_width).move_to([x+3*taille,y-1.5,z])
            i5 = MathTex("n",color=RED).move_to([x+2*taille,y-1.5,z]).scale(taille*0.75)
            i6 = MathTex("m+1",color=PURPLE).move_to([x+3*taille,y-1.5,z]).scale(taille*0.75)
            p1 = MathTex(r"\frac{a+c}{2}",color=RED).next_to(carre2,taille*0.5*RIGHT).shift(UP*(taille/2.5)).scale(taille*0.5)
            p2 = MathTex(r"\frac{b+d}{2}",color=PURPLE).next_to(carre2,taille*0.5*RIGHT).shift(DOWN*(taille/2.5)).scale(taille*0.5)
            p3 = MathTex("a",color=RED).next_to(carre4,taille*0.75*RIGHT).shift(UP*(taille/2.5)).scale(taille*0.75)
            p4 = MathTex("b",color=PURPLE).next_to(carre4,taille*0.75*RIGHT).shift(DOWN*(taille/2.5)).scale(taille*0.75)
            p5 = MathTex("c",color=RED).next_to(carre6,taille*0.75*RIGHT).shift(UP*(taille/2.5)).scale(taille*0.75)
            p6 = MathTex("d",color=PURPLE).next_to(carre6,taille*0.75*RIGHT).shift(DOWN*(taille/2.5)).scale(taille*0.75)

            return VGroup(carre1,carre2,i1,i2,l1,l2,carre3,carre4,i3,i4,carre5,carre6,i5,i6,p1,p2,p3,p4,p5,p6)

        def numDec(x):
            i=0
            while x-floor(x)>0:
                x*=10
                i+=1
            return i

        def partis1(score,x,taille=1):
            return [Integer(number=x,color=GREEN,num_decimal_places=numDec(x)).scale(taille).next_to(score,RIGHT/2).shift(UP*(taille/2.5)),Integer(number=100-x,color=BLUE,num_decimal_places=numDec(100-x)).scale(taille).next_to(score,RIGHT/2).shift(UP*-(taille/2.5))]
        def partis2(score,x,taille=1):
            return Tex(r"("+str(x)+r","+str(100-x)+r")").scale(taille).next_to(score,RIGHT/2)
        
        calcul = get_calcul(strk_width=2).shift(RIGHT*4.2).scale(0.5)
        self.add(calcul)