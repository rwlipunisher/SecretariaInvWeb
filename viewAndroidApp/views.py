from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from firebase_admin import db, credentials, initialize_app
from PIL import Image
from io import BytesIO
import base64
import pyrebase
import os
import ast 
import time

config={
  "apiKey": "AIzaSyDam36WYsJhnHPfMwqi5qKKAOW2yvZZdow",
  "authDomain": "secretariainv-6d011.firebaseapp.com",
  "databaseURL": "https://secretariainv-6d011-default-rtdb.firebaseio.com",
  "projectId": "secretariainv-6d011",
  "storageBucket": "secretariainv-6d011.appspot.com",
  "messagingSenderId": "243651555361",
  "appId": "1:243651555361:web:68dacf3138babee7887360"
}
keyFirebase = {
  "type": "service_account",
  "project_id": "secretariainv-6d011",
  "private_key_id": "5a9a24dc851feb902a11864a4c0d586fd42f6e7c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCfWjJt5WTq6i7n\nBaRxpucfztnmxoThUkcW1XPLYwQUkI4F2za1JXmI/TjdB5RWRuBfa6hGjg0dfh0W\nA/t6mGwqPV1zvmJugmjYJDtjEbEH/xQB1/uUY3NGwpxE0iKOrmjJPyRSFZeTTu8h\noKenRzhReb8GV2l7NcIrAvK9noZRAa1GMeIWUFkfoz7JcVHmNVZAmtk9zh1X1WLd\ntjzCVXTpXgnR1R4x9kNHxD5NHgNrAjr6/+v2jZFVbfg0dmXY8BdRGw7JOcfFKmpb\nzMdEAJ4y95cauUqwzW0y6+0GioHXRjbNvMsaHn98H50NHQMWmLZV6PD5I/EBqJai\n9cfWwmy7AgMBAAECggEACPYUDu0PC0znHVPKZx/JMJc71sgEMf2kBMs1K1Nip9tn\nOToWLgKw/nyrBXcHJwDuXj9aI7maUDXG4fWQX1kSACAaUMd8lpVb2wfSlSQqDfaQ\nw/fG7JXZJjoMeqxMiDSTrPmRi9IuB3kxZnU36GbPanmLvgoNYwHnbO7KAtLW39g+\n8kq5WnhnLNzNvhRQGX6UBT2XmIqLHfWIEj0hKUi/4yZBikhK83XQMRebY+bgzVI5\nDuqkia12MyVL26NKWx+DkRA0xTKcW6MhafyzI1V7XISDmkXPR3akomw8Q3nin0MP\nQy2SPC3TPFoM+iVne9xak+yiXjA4uuV7yDLoULuWIQKBgQDhCUX0mZURE+C2o6GT\ndlLcLkrlLRflbmTsO6tF2RcsKJYZohGqHuaQRMvwIQuDFAj/yFF7ne68Wds/RIKg\nTr1AJE83mSDyi/c+7lVodwbEtSlRg9km5OoXe7JgEQ3bIFaVTfAq3Yt5qzJaNaHk\n/jF/w3ElM2gNHlwKOsD3zUKQGwKBgQC1R0JuiHPmVHzJCGQIFFtflafwBvo+ryaf\ns1wIa98lF3V5cIxAB8Fn3GXqqwdxW2Hz4ts1u7UIjOL8HG6Ub8cO18qRLW5WBbrS\n/rymPUlnb5Mm3hRfBy3Bg+bg7E7D4M8EXGuYKWYWTQjQfp0BdXU/pvqkFmg6xqGg\nVG5uDVOf4QKBgQCpXX1U9jIGxFsfmk+E2EzMgdrEWQffGRLD6LSiwRx7k6BEcoGw\n88i7U8vZUkWDxZRwTadlzhtbjpVALKPTWu98Utd8FLeDVGwk5ONK2Coz6dTLENxi\nNW8pdWNugedXwCLqA9p5qHvMelhPJIZP/i/q5IFHakUpemvzFv0cg1NReQKBgEpN\n5jYGanNb6DZC4TXKmlWIs2iYg5SUGKHXU/8DsFi0z+syLdrFEwqudXwGFKvrSDA+\nqZnR0feqQBQU12KymoZD/30YgSRzfsujrNH7Rw5F1qxU1UbKW3/5v/YsBnEVweVI\nuLWLKpQziUxkyZhie+fWWuBNavXEm1VrpkQn5EIhAoGASQ+IYBsx9/RVU8t9d4t1\nU3c9mnJaAV9S1eaKqCCb35SqZtGWwZFZORqTMvwj+OZvSz4Aj7YnScRvfI8azGsg\nGZe/4wI1GJ/8b+Yv+yRD94k9kOmIVMLyfip7jnxC0OI1l7sJhDBtcIz4m5glf3Ww\nHxv3BcA63f/D91ZfoKzYeIw=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-m77tv@secretariainv-6d011.iam.gserviceaccount.com",
  "client_id": "104640566870684044235",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-m77tv%40secretariainv-6d011.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
# Initialising database,auth and firebase for further use
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
# initialize Firebase to getData or SetData in RealTimeDataBase
cred = credentials.Certificate(keyFirebase)
default_app = initialize_app( cred, {'databaseURL':'https://secretariainv-6d011-default-rtdb.firebaseio.com'})

files = open(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/images.txt'))
imgCodes = ast.literal_eval(files.readline())
print(imgCodes)
files.close()

def teste(request):
    return render(request, 'teste.html')

def home(request):
    global imgCodes
    try:
        if request.session['name'] != 'AnonymousUser':
            print(imgCodes)
            return render(request, 'index.html', imgCodes)
        else:
            return redirect(sigIn)
    except:
        return redirect(singIn)

def singIn(request):
    try:
        if request.session['name'] != 'AnonymousUser':
            redirect('home')
        else:
            return render(request, 'login.html')
    except:
        return render(request, 'login.html')
    return render(request, 'login.html')

def postsignIn(request):
    global user
    email=request.POST.get("Email")
    pasw=request.POST.get("Password")
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
        request.session['name'] = user['localId']
        print(str(request.session))
        return redirect(home)
    except Exception as e:
        print(e)
        return render(request, 'login.html', {"message":"Erro! Tente Novamente ou consulte o Administrador do sistema"}) 
    
def savePrincipalImg(request):
    global imgCodes
    if request.method == 'POST':
        imgFromUser = request.FILES['inputModalImgPrincipal'].read()
        imgdata = BytesIO(imgFromUser)
        img = Image.open(imgdata)
        print(str(img.size))
        if img.format == 'PNG' and img.size == (1920, 1080):
            imgbase64 = base64.b64encode(imgFromUser).decode('utf-8')
            db.reference('/ImagensLink/Principal').set(imgbase64)
            os.remove(settings.BASE_DIR + '/viewAndroidApp' + imgCodes['principal'])
            o = str(time.time())
            imgCodes['principal'] = "/static/images/principal"+o+".png"
            newCodes = str(imgCodes)
            img.save(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/principal'+o+'.png'), format='PNG')
            with open(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/images.txt'), "w") as file:
                file.write(newCodes)
            redirect(home)
        else:
            return render(request, 'index.html', {"message":"formato incorreto de Imagem! Tente Novamente"})
    else:
        return (request, 'index.html', {"message":"Erro de Processamento, tente Novamente"})
    return redirect(home)

def saveSecondaryImg(request):
    global imgCodes
    if request.method == 'POST':
        
        try:
            imgCard1 = request.FILES['inputCard1'].read()
            imgCard11 = request.FILES['inputCard11'].read()
        except:
            return render(request,'index.html', {"message":"Sem arquivo Valido, Tente Novamente"})
        
        imgdataCard1 = BytesIO(imgCard1)
        imgdataCard11 = BytesIO(imgCard11)
        imgC1 = Image.open(imgdataCard1)
        imgC11 = Image.open(imgdataCard11)

        if imgC1.format == 'PNG' and imgC1.size == (1080, 1080):
            if imgC11.format == 'PNG' and imgC11.size == (1587, 2245):
                imgbase641 = base64.b64encode(imgCard1).decode('utf-8')
                imgbase6411 = base64.b64encode(imgCard11).decode('utf-8')
                print('Auiiiiidfa   ' + request.POST.get('wcardin'))
                if request.POST.get('wcardin') == 'Col1':
                    db.reference('/ImagensLink/Card1').set(imgbase641)
                    db.reference('/ImagensLink/card1').set(imgbase6411)
                    print(imgCodes['card1'])
                    os.remove(settings.BASE_DIR+'/viewAndroidApp'+imgCodes['card1'])
                    os.remove(settings.BASE_DIR+'/viewAndroidApp'+imgCodes['card11'])
                    o = str(time.time())
                    imgCodes['card1'] = "/static/images/card1"+o+".png"
                    imgCodes['card11'] = "/static/images/card11"+o+".png"
                    imgC1.save(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/card1'+o+'.png'), format='PNG')
                    imgC11.save(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/card11'+o+'.png'), format='PNG')
                    newCodes = str(imgCodes)
                    with open(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/images.txt'), "w") as file:
                        file.write(newCodes)
                    return redirect(home)
                elif request.POST.get('wcardin') == 'Col2':
                    db.reference('/ImagensLink/Card2').set(imgbase641)
                    db.reference('/ImagensLink/card2').set(imgbase6411)
                    os.remove(settings.BASE_DIR+'/viewAndroidApp'+imgCodes['card2'])
                    os.remove(settings.BASE_DIR+'/viewAndroidApp'+imgCodes['card21'])
                    o = str(time.time())
                    imgCodes['card2'] = "/static/images/card2"+o+".png"
                    imgCodes['card21'] = "/static/images/card21"+o+".png"
                    imgC1.save(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/card2'+o+'.png'), format='PNG')
                    imgC11.save(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/card21'+o+'.png'), format='PNG')
                    newCodes = str(imgCodes)
                    with open(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/images.txt'), "w") as file:
                        file.write(newCodes)
                    return redirect(home)
                elif request.POST.get('wcardin') == 'Col3':
                    db.reference('/ImagensLink/Card3').set(imgbase641)
                    db.reference('/ImagensLink/card3').set(imgbase6411)
                    os.remove(settings.BASE_DIR+'/viewAndroidApp'+imgCodes['card3'])
                    os.remove(settings.BASE_DIR+'/viewAndroidApp'+imgCodes['card31'])
                    o = str(time.time())
                    imgCodes['card3'] = "/static/images/card3"+o+".png"
                    imgCodes['card31'] = "/static/images/card31"+o+".png"
                    imgC1.save(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/card3'+o+'.png'), format='PNG')
                    imgC11.save(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/card31'+o+'.png'), format='PNG')
                    newCodes = str(imgCodes)
                    with open(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/images.txt'), "w") as file:
                        file.write(newCodes)
                    return redirect(home)
                elif request.POST.get('wcardin') == 'Col4':
                    db.reference('/ImagensLink/Card4').set(imgbase641)
                    db.reference('/ImagensLink/card4').set(imgbase6411)
                    os.remove(settings.BASE_DIR+'/viewAndroidApp'+imgCodes['card4'])
                    os.remove(settings.BASE_DIR+'/viewAndroidApp'+imgCodes['card41'])
                    o = str(time.time())
                    imgCodes['card4'] = "/static/images/card4"+o+".png"
                    imgCodes['card41'] = "/static/images/card41"+o+".png"
                    imgC1.save(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/card4'+o+'.png'), format='PNG')
                    imgC11.save(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/card41'+o+'.png'), format='PNG')
                    newCodes = str(imgCodes)
                    with open(os.path.join(settings.BASE_DIR, 'viewAndroidApp/static/images/images.txt'), "w") as file:
                        file.write(newCodes)
                    return redirect(home)
                else:
                    return render(request, 'index.html', {"message":"Erro de Sistema Atualize a pagina e tente novamente!"})
            else:
                return render(request, 'index.html', {"message":"Imagem do cartaz em formato errado! Tente Novamente"})
        else:
            return render(request, 'index.html', {"message":"Imagem do Card em formato errado! Tente Novamente"})
        
def logout(request):
    del request.session['name']
    return redirect(home)
