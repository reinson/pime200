import unicodedata
import re
import os
import webapp2
import jinja2
from google.appengine.ext import db

def umardaja(nr):
    #?mardab viiega jaguvaks
    jaak = nr - nr/5*5
    if jaak <3:
        return nr - jaak
    else:
        return nr - jaak + 5

def tihide_arvestaja(tihid):
    #v?tab sisse dictionary m?ngijate tihidest
    #kontrollib, kas tihid on ?igesti sisestatud
    #leiab sisestamata j?etud tihide v??rtused
    #annab v?lja ?mardatud tihide v??rtused k?igile m?nijatele
    #annab v?lja errori, mis on "" kui k?ik on ?ige
    tihide_summa=0
    tihide_arv=0
    error=""
    for i in tihid:
        if isinstance(tihid[i],int):
            tihide_summa+=tihid[i]
        if tihid[i]!="":
            tihide_arv+=1
        if tihid[i]<0:
            error="Tihide punktid negatiivsed"
            return tihid,error
        if tihid[i]>120 and isinstance(tihid[i],int):
            error="Tihide punktid ule 120"
            return tihid[i],error
        if not isinstance(tihid[i], int) and tihid[i]!="":
            error="Tihid pole numbrid"
            return tihid,error

    if tihide_summa>120:
        return tihid,"Tihide summa on " + str(tihide_summa)

    if tihide_summa==120:
        if tihide_arv==1:
            for i in tihid:
                if tihid[i]=="":
                    tihid[i]=0
        if tihide_arv==2:
            for i in tihid:
                if tihid[i]=="":
                    tihid[i]=0
    if tihide_summa<120:
        if tihide_arv==3:
            error="Tihide summa on "+str(tihide_summa)
        if tihide_arv==2:
            for i in tihid:
                if tihid[i]=="":
                    tihid[i]=120-tihide_summa
        if tihide_arv<2:
            error="Sisesta vahemalt kahe mangija tihide punktid"

    if error=="":
        result={}
        for i in tihid:
            result[i]=umardaja(tihid[i])
        return result,error

    return tihid,error,

def boonus(pime,neli9,pakkumine,pakkuja,tais):
    #leiab boonus punktide summa k?igi m?ngijate jaoks
    dict={"pl1":0,"pl2":0,"pl3":0}
    if neli9:
        dict[neli9]+=100
    if pime:
        if tais:
            dict[pime]+=pakkumine[pakkuja]
        else:
            dict[pime]-=pakkumine[pakkuja]
    return dict


def convert_to_number1(number):
    if number:
        return int(number)
    else:
        return ""
def convert_to_number2(number):
    if number:
        return int(number)
    else:
        return 0

def pmst(tihid,trumbid):
    #punkte m?ngust (pmst)
    #lisab tihide punktidele trumpidest saadud punktid
    dict={"risti":100,"poti":80,"artu":60,"ruutu":40}
    result={}
    for i in tihid:
        result[i]=tihid[i]
    for i in trumbid:
        if trumbid[i]:
            result[trumbid[i]]+=dict[i]
    return result

def pakkumise_arvestaja(pakkumine):
    #v?tab sisse dictionary pakkumiste lahtritest
    #kontrollib kas pakkumine on ?igesti sisestatud
    #annab v?lja pakkuja nime ja errori (mis on "" kui k?ik on ?ige)
    pakkumiste_arv=0
    pakkuja=""
    for i in pakkumine:
        if isinstance(pakkumine[i],int) and pakkumine[i]!=0:
            pakkumiste_arv+=1
            pakkuja=i
    if pakkumiste_arv!=1:
        return pakkuja, "pakkumisi on sisestatud " + str(pakkumiste_arv)
    if pakkumine[pakkuja]<-59:
        return pakkuja, "maha"
    if pakkumine[pakkuja]<60 and pakkumine[pakkuja]>0:
        return pakkuja, "alla 60 ei saa pakkuda"
    if pakkumine[pakkuja]>300:
        return pakkuja, "ule 300 ei saa pakkuda"
    if pakkumine[pakkuja]/5*5!=pakkumine[pakkuja]:
        return pakkuja, "sisesta viiega jaguv pakkumine"

    return pakkuja, ""


def ptsse(punkte_mangust,pakkumised):
    #punkte tabelisse (ptsse)
    #kontrollib kas pakkumine saadi t?is
    #v?ljastab palju iga m?ngija punkte saab selles voorus
    #v?ljastab pakkuja nime ja selle kas pakkumine saadi t?is
    pakkuja=""
    tais=True
    for i in pakkumised:
        if pakkumised[i]!=0:
            pakkuja=i
    if punkte_mangust[pakkuja]<pakkumised[pakkuja]:
        punkte_mangust[pakkuja]=-pakkumised[pakkuja]
        tais=False
    else:
        punkte_mangust[pakkuja]=pakkumised[pakkuja]
    return punkte_mangust, pakkuja, tais


template_dir=os.path.join(os.path.dirname(__file__),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)

    def render_str(self, template,**params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
         self.write(self.render_str(template,**kw))


class Punktid(db.Model):

    mangija1 = db.StringProperty()
    mangija2 = db.StringProperty()
    mangija3 = db.StringProperty()

    tihid1 = db.IntegerProperty()
    tihid2 = db.IntegerProperty()
    tihid3 = db.IntegerProperty()

    punkte_mangust1 = db.IntegerProperty()
    punkte_mangust2 = db.IntegerProperty()
    punkte_mangust3 = db.IntegerProperty()

    punktid_tabelisse1 = db.IntegerProperty()
    punktid_tabelisse2 = db.IntegerProperty()
    punktid_tabelisse3 = db.IntegerProperty()

    punktid_tabelis1 = db.IntegerProperty()
    punktid_tabelis2 = db.IntegerProperty()
    punktid_tabelis3 = db.IntegerProperty()

    pakkuja = db.StringProperty()
    pakkumine = db.IntegerProperty()
    pakkumine_tais = db.BooleanProperty()

    risti = db.StringProperty()
    poti = db.StringProperty()
    artu = db.StringProperty()
    ruutu = db.StringProperty()
    pime = db.StringProperty()
    neli9 = db.StringProperty()

    created = db.DateTimeProperty(auto_now_add = True)
    game_id = db.IntegerProperty()


class Permalink(Handler):
    def render_front(self, id, error="",Player1="",Player2="",Player3=""):
        seis = db.GqlQuery("SELECT * FROM Punktid WHERE game_id = "+id+" ORDER BY created DESC")

        self.render("front.html",Player1=seis[0].mangija1,Player2=seis[0].mangija2,
                          Player3=seis[0].mangija3, seis=seis, error=error)

    def get(self, id):
        seis = db.GqlQuery("SELECT * FROM Punktid WHERE game_id = "+id+" ORDER BY created DESC")
        self.render("front.html",Player1=seis[0].mangija1,Player2=seis[0].mangija2,
                          Player3=seis[0].mangija3, seis=seis)

    def post(self,g_id):
        tihid={}
        pakkumine={}
        trumbid={}
        tihid["pl1"]=convert_to_number1(self.request.get("tihid1"))
        tihid["pl2"]=convert_to_number1(self.request.get("tihid2"))
        tihid["pl3"]=convert_to_number1(self.request.get("tihid3"))
        pakkumine["pl1"]=convert_to_number2(self.request.get("pakkumine1"))
        pakkumine["pl2"]=convert_to_number2(self.request.get("pakkumine2"))
        pakkumine["pl3"]=convert_to_number2(self.request.get("pakkumine3"))

        for i in ["risti","poti","artu","ruutu"]:
            trumbid[i]=self.request.get(i)

        pime=self.request.get("pime")
        neli9=self.request.get("neli9")

        pakkuja, error2=pakkumise_arvestaja(pakkumine)

        error=""
        if error2!="maha":
            tihid,error=tihide_arvestaja(tihid)

        else:
            hetke_seis={}
            seis=db.GqlQuery("SELECT * FROM Punktid WHERE game_id = "+g_id+" ORDER BY created DESC")
            hetke_seis["pl1"]=seis[0].punktid_tabelis1
            hetke_seis["pl2"]=seis[0].punktid_tabelis2
            hetke_seis["pl3"]=seis[0].punktid_tabelis3
            m1=seis[0].mangija1
            m2=seis[0].mangija2
            m3=seis[0].mangija3
            mangijad={"pl1":m1,"pl2":m2,"pl3":m3,"":""}

            punkte_mangust={}
            uus_seis={}
            for i in ["pl1","pl2","pl3"]:
                if pakkumine[i]==0:
                    uus_seis[i]=hetke_seis[i]+25

                else:
                    if pime:
                        uus_seis[i]=hetke_seis[i]+(pakkumine[pakkuja]*2)
                    else:
                        uus_seis[i]=hetke_seis[i]+pakkumine[pakkuja]

            for i in ["pl1","pl2","pl3"]:
                if neli9==i:
                    uus_seis[i]+=100



            b = Punktid(
            pakkuja=mangijad[pakkuja], pakkumine=-pakkumine[pakkuja],pakkumine_tais=False,
            punktid_tabelis1 = uus_seis["pl1"], punktid_tabelis2 = uus_seis["pl2"], punktid_tabelis3 = uus_seis["pl3"],
            mangija1=m1, mangija2=m2, mangija3=m3,game_id=int(g_id),
            risti = mangijad[trumbid["risti"]],poti = mangijad[trumbid["poti"]], artu= mangijad[trumbid["artu"]],
            ruutu = mangijad[trumbid["ruutu"]], pime = mangijad[pime] , neli9 = mangijad[neli9]
            )
            b.put()





        if error=="" and error2=="":
            punkte_mangust={}
            punkte_mangust=pmst(tihid,trumbid)

            pakkuja=""
            tais=None
            punkte_tabelisse,pakkuja,tais=ptsse(punkte_mangust,pakkumine)


            hetke_seis={}
            seis=db.GqlQuery("SELECT * FROM Punktid WHERE game_id = "+g_id+" ORDER BY created DESC")
            hetke_seis["pl1"]=seis[0].punktid_tabelis1
            hetke_seis["pl2"]=seis[0].punktid_tabelis2
            hetke_seis["pl3"]=seis[0].punktid_tabelis3
            m1=seis[0].mangija1
            m2=seis[0].mangija2
            m3=seis[0].mangija3
            mangijad={"pl1":m1,"pl2":m2,"pl3":m3,"":""}

            lisa_punktid=boonus(pime,neli9,pakkumine,pakkuja,tais)
            uus_seis={}
            for i in ["pl1","pl2","pl3"]:
                uus_seis[i]=hetke_seis[i]+punkte_mangust[i]+lisa_punktid[i]

            b = Punktid(tihid1 = tihid["pl1"], tihid2 = tihid["pl2"], tihid3 = tihid["pl3"],
            punktid_tabelisse1 = punkte_tabelisse["pl1"], punktid_tabelisse2 = punkte_tabelisse["pl2"],
            punktid_tabelisse3 = punkte_tabelisse["pl3"], pakkuja=mangijad[pakkuja], pakkumine=pakkumine[pakkuja],pakkumine_tais=tais,
            punktid_tabelis1 = uus_seis["pl1"], punktid_tabelis2 = uus_seis["pl2"], punktid_tabelis3 = uus_seis["pl3"],
            punkte_mangust1 = punkte_mangust["pl1"], punkte_mangust2 = punkte_mangust["pl2"], punkte_mangust3 = punkte_mangust["pl3"],
            mangija1=m1, mangija2=m2, mangija3=m3,game_id=int(g_id),
            risti = mangijad[trumbid["risti"]],poti = mangijad[trumbid["poti"]], artu= mangijad[trumbid["artu"]],
            ruutu = mangijad[trumbid["ruutu"]], pime = mangijad[pime] , neli9 = mangijad[neli9]
            )
            b.put()

        self.render_front(id=g_id, error=error+" //"+error2)


class MainPage(Handler):

    def get(self):
        m = db.GqlQuery("SELECT * FROM Punktid ORDER BY created DESC")
        mangud = []
        printimiseks = []
        for i in m:

            if i.game_id not in mangud:

                mangud = mangud + [i.game_id]
                printimiseks = printimiseks + [i]

        self.render("frontpage.html", seis=printimiseks)

class NewGame(Handler):

    def render_front(self,error=""):

        self.render("newgame2.html")

    def get(self):
        self.render_front()

    def post(self):
        pl1=self.request.get("pl1")
        pl2=self.request.get("pl2")
        pl3=self.request.get("pl3")

        try:
            seis = db.GqlQuery("SELECT * FROM Punktid ORDER BY game_id DESC")
            uus_id = seis[0].game_id+1
        except:
            uus_id=1

        d = Punktid (punktid_tabelis1 = 0, punktid_tabelis2= 0, punktid_tabelis3 =0,mangija1 = pl1, mangija2 = pl2, mangija3 = pl3,
        game_id=uus_id)
        d.put()
        self.redirect("/%d" % uus_id)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newgame', NewGame),
    ('/(\d+)', Permalink)
    ], debug=True)



