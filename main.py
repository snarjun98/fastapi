from data import model_data
from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# from firebase import Database, firebase
app = FastAPI()
cred = credentials.Certificate('./firebase.json')
default_app = firebase_admin.initialize_app(cred) 
db = firestore.client()

import pickle
activity_mod=pickle.load(open("activity_mod.pkl","rb"))
health_mod=pickle.load(open("health_mod.pkl","rb"))
@app.post("/sensor")
def read_root(data:model_data):
    data=data.dict()
    doc_ref=db.collection(u'sensors').document(data['id'])
    activity_out=activity_mod.predict([[data['x'],data['y'],data['z']]])
    if(activity_out[0]=='STANDING'):
        a=1
    if(activity_out[0]=='WALKING'):
        a=2
    if(activity_out[0]=='FEEDING'):
        a=0
    health_out=health_mod.predict([[data['temp'],data['pulse'],a]])
    doc_ref.update({'temp':data['temp'],'activity':activity_out[0],'pulse':data['pulse'],'lat':data['lat'],'lon':data['lon'],'status':health_out[0]})
    return health_out[0]
