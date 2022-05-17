from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime 
from DB import DB
import sys
 
def baglantikur():
    global uri,user,password,db_neo
    uri = "neo4j+s://7255dd1c.databases.neo4j.io:7687"
    user = "neo4j"
    password = "<Your password>"
    db_neo = DB(uri, user, password)

def baglantisonlandir():
    db_neo.close()


app= Flask(__name__)


@app.route("/vis/<name>",methods=["GET","POST"])
def vis(name):
    
    baglantikur()
    every_result = []
    yayin_result = db_neo.find_Arastirmaci_wrote_yayin(name)
    for re in yayin_result:
        sonuc = re["YayinAdi"]
        result = db_neo.find_Yayin_to_everything(sonuc)
        every_result =every_result+result
    
    
    unique_arastirmacilar = []
    for row in every_result:
        if len(unique_arastirmacilar)>0:
            val=0
            for ad in unique_arastirmacilar:
                if ad == row["ArastirmaciAdi"]:
                    val+=1
            if val==0:
                unique_arastirmacilar.append(row["ArastirmaciAdi"])
        else :
            unique_arastirmacilar.append( row["ArastirmaciAdi"])
    


    nodes = []
    id = 0
    for ad in  unique_arastirmacilar:
        veri={
            "id":"",
            "label":""
        }
        veri.update({"id":id,"label":ad})
        id+=1
        nodes.append(veri)


    unique_yayin= []
    for row in every_result:
        if len(unique_yayin)>0:
            val=0
            for yayin in unique_yayin:
                if yayin == row["YayinAdi"]:
                    val+=1
            if val==0:
                unique_yayin.append(row["YayinAdi"])
        else :
            unique_yayin.append( row["YayinAdi"])
    

    for yayin in  unique_yayin:
        veri1={
            "id":"",
            "label":""
        }
        veri1.update({"id":id,"label":yayin})
        id+=1
        nodes.append(veri1)


    unique_tur= []
    for row in every_result:
        if len(unique_tur)>0:
            val=0
            for tur in unique_tur:
                if tur == row["YayinYeri"]:
                    val+=1
            if val==0:
                unique_tur.append(row["YayinYeri"])
        else :
            unique_tur.append( row["YayinYeri"])
    

    for tur in  unique_tur:
        veri2={
            "id":"",
            "label":""
        }
        veri2.update({"id":id,"label":tur})
        id+=1
        nodes.append(veri2)
    


    connection=[]
    for row in every_result:
        
        if len(connection)>0:
            for one in nodes:
                for two in nodes:
                    for tree in nodes:
                        if one["label"]==row["ArastirmaciAdi"] and two["label"]==row["YayinAdi"]and tree["label"]==row["YayinYeri"]:
                            key1=0
                            for deger in connection:
                                if deger["one"]==one["id"] and deger["two"]==two["id"]:
                                    key1=1
                            con3={
                                "one":"",
                                "two":""
                            }
                            con3.update({"one":one["id"],"two":two["id"]})
                            if key1==0:
                                connection.append(con3)


                            key2=0
                            for deger in connection:
                                if deger["one"]==two["id"] and deger["two"]==tree["id"]:
                                    key2=1
                            con4={
                                "one":"",
                                "two":""
                            }
                            con4.update({"one":two["id"],"two":tree["id"]})
                            if key2==0:
                                connection.append(con4)
        else:
            
            for one in nodes:
                for two in nodes:
                    for tree in nodes:
                        if one["label"]==row["ArastirmaciAdi"] and two["label"]==row["YayinAdi"]and tree["label"]==row["YayinYeri"]:
                            
                            con1={
                                "one":"",
                                "two":""
                            }
                            con1.update({"one":one["id"],"two":two["id"]})
                            connection.append(con1)
                            con2={
                                "one":"",
                                "two":""
                            }
                            con2.update({"one":two["id"],"two":tree["id"]})
                            connection.append(con2)

    baglantisonlandir()
    return render_template("vis.html",data=nodes,connection=connection)

@app.route("/",methods=["GET","POST"])
def home():
    
    if request.method=="POST":
        
        sec=request.form.get("sec")
        fname=request.form.get("fname")
        veriler = []
        baglantikur()

        result = db_neo.search(sec, fname)
        baglantisonlandir()
        
        return render_template('home.html', veriler=result)
    return render_template("home.html")

@app.route("/adminhome",methods=["GET","POST"])
def adminhome():
    if request.method=="POST":
        baglantikur()
        YayinYeri=db_neo.find_YayinYeri()
        YayinAdi=db_neo.find_YayinAdi()
        ArastirmaciAdi=db_neo.find_ArastirmaciAdi()
        return render_template('createBaglanti.html',YayinYeri=YayinYeri,YayinAdi=YayinAdi,ArastirmaciAdi=ArastirmaciAdi)
        baglantisonlandir()

    return render_template("adminhome.html")

@app.route("/admingiris",methods=["GET","POST"])
def admingiris():
    if request.method=="POST":
        baglantikur()
        kullaniciAdi =request.form.get('kullaniciAdi')
        password=request.form.get('password')
        if kullaniciAdi=="Admin" and password=="1234":
            return redirect(url_for('adminhome'))
        baglantisonlandir() 
    return render_template("admingiris.html")

@app.route("/createBaglanti",methods=["GET","POST"])
def createBaglanti():
    new_YayinYeri = []
    new_YayinAdi = []
    new_YayinTuru = []
    new_ArastırmaciAdi = []
    baglantikur()

    YayinYeri=db_neo.find_YayinYeri()

    for yayinyeri in YayinYeri:
        if yayinyeri != None:
            yayinyeri = yayinyeri.replace(" ","_")
            new_YayinYeri.append(yayinyeri)

    YayinAdi=db_neo.find_YayinAdi()

    for yayinadi in YayinAdi:
        if yayinadi != None:
            yayinadi = yayinadi.replace(" ","_")
            new_YayinAdi.append(yayinadi)

    YayinTuru=db_neo.find_YayinTuru()

    for yayinturu in YayinTuru:
        if yayinturu != None:
            yayinturu = yayinturu.replace(" ","_")
            new_YayinTuru.append(yayinturu)
            

    ArastirmaciAdi=db_neo.find_ArastirmaciAdi()

    for arastirmaciadi in ArastirmaciAdi:
        if arastirmaciadi != None:
            arastirmaciadi = arastirmaciadi.replace(" ","_")
            new_ArastırmaciAdi.append(arastirmaciadi)

    baglantisonlandir()
    if request.method=="POST":
        YayinYeri=request.form.get("YayinYeri")
        YayinAdi=request.form.get("YayinAdi")
        YayinTuru=request.form.get("YayinTuru")
        ArastirmaciAdi=request.form.get("ArastirmaciAdi")   
        ArastirmaciAdi=ArastirmaciAdi.replace("_"," ")
        YayinAdi=YayinAdi.replace("_"," ")
        YayinTuru=YayinTuru.replace("_"," ")
        YayinYeri=YayinYeri.replace("_"," ")

        
        baglantikur()
        if YayinYeri !='' and YayinAdi !='' and ArastirmaciAdi !='' :
            if  db_neo.y_t_c_sorgu(YayinAdi, YayinYeri, YayinTuru):
                db_neo.create_yayin_to_tur_connection(YayinAdi,YayinYeri,YayinTuru)#yayinID --- turID
                
            if  db_neo.a_y_c_sorgu(ArastirmaciAdi, YayinAdi):
                db_neo.create_arastirmacilar_to_yayin_connection(ArastirmaciAdi ,YayinAdi)#
                
        baglantisonlandir()

    return render_template("createBaglanti.html",YayinTuru=new_YayinTuru,YayinYeri=new_YayinYeri,YayinAdi=new_YayinAdi,ArastirmaciAdi=new_ArastırmaciAdi)



@app.route("/createTur",methods=["GET","POST"])
def createTur():
    if request.method=="POST": 
        YayinTuru=request.form.get("YayinTuru")
        YayinYeri=request.form.get("YayinYeri")
        baglantikur()
        if db_neo.tur_sorgu(YayinTuru, YayinYeri):
            db_neo.create_tur(YayinTuru,YayinYeri)
        baglantisonlandir()
        return redirect(url_for('adminhome'))
    return render_template("createTur.html")


@app.route("/createArastirmaci",methods=["GET","POST"])
def createArastirmaci():     
    if request.method=="POST":
        ArastirmaciAdi=request.form.get("ArastirmaciAdi")
        ArastirmaciSoyadi=request.form.get("ArastirmaciSoyadi")
        baglantikur()
        if db_neo.arastirmaci_sorgu(ArastirmaciAdi, ArastirmaciSoyadi):
            db_neo.create_arastirmaci(ArastirmaciAdi, ArastirmaciSoyadi)
        baglantisonlandir()
        return redirect(url_for('adminhome'))
    return render_template("createArastirmaci.html")


@app.route("/createYayin",methods=["GET","POST"])
def createYayin():  
    if request.method=="POST":
        YayinAdi=request.form.get("YayinAdi")
        YayinYili=request.form.get("YayinYili")
        baglantikur()
        if db_neo.yayin_sorgu(YayinAdi, YayinYili):
            db_neo.create_yayin(YayinAdi, YayinYili)
        baglantisonlandir()
        return redirect(url_for('adminhome'))
    return render_template("createYayin.html")


if __name__ =="__main__":
    app.debug=True
    app.run()
