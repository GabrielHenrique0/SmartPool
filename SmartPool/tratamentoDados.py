import math
import statistics
import time

import numpy as np
import pylab as p
import matplotlib.pyplot as plt
import firebase_admin
from firebase_admin import credentials, db
from scipy.stats import kurtosis
from scipy.stats import skew
import pandas as pd
import seaborn as sb
import openpyxl
import json
import requests

# Fetch the service account key JSON file contents
cred = credentials.Certificate('chave.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://smartpool-57e1d-default-rtdb.firebaseio.com/"
})

vet = []
vet2 = []
contador = 0

ref = db.reference('/Usuario1/Piscina1/PH'.format(contador))
ref2 = db.reference('/Usuario1/Piscina1/Historico')

while True:
    contador += 1
    vet = [ref.get((ref.set(ref.get())))] # puxar os dados do path ph do firebase
    vet2 = vet2 + vet
    ref2.set(vet2)
    # vet = vet.replace("{", "")

    print(vet2)

    time.sleep(4.8)

    # vet2 = [2,5,7,4,1,9,5,9,2,6,7,9,4,3,9,5,7]
    ordenados = sorted(vet2)

    pastilhas = 120
    pastilhasUsadas = 30

    media = statistics.mean(vet2)
    print("\nMédia aritmética: ", media)

    moda = statistics.mode(vet2)
    print("Moda: ", moda)

    mediana = statistics.median(vet2)
    print("Mediana: ", mediana)

    desvioPadrao = np.std(vet2)
    print("Desvio padrão: ", desvioPadrao)

    desvioPadrao = "{:.2f}".format(desvioPadrao)

    # correlacao = statistics.correlation(vet2)
    # print(correlacao)

    # vet2 = sb.load_dataset('tips')
    # sb.regplot(x = "total_bill", y = "tip", data = vet2)
    # plt.show()

    porcen_pas = pastilhasUsadas/pastilhas*100

    print("Porcentagem de pastilhas utilizadas: ", porcen_pas)

    assimetria = skew(vet2, axis=0, bias=True)
    
    print("Assimetria:", assimetria)

    assimetria = "{:.2f}".format(assimetria)
      
    # plt.plot(vet2, y1, '*')
    
    curtose = kurtosis(vet2, axis=0, bias=True)

    print("Curtose: ", curtose, "\n")
    
    curtose = "{:.2f}".format(curtose)
    
    # print('Kurtosis for normal distribution:',  
    #       kurtosis(vet2, fisher = False)) 
    
    # print('Kurtosis for normal distribution:',  
    #       kurtosis(vet2, fisher = True))
 
    # kurtosis(vet2, fisher = True))

    # df = pd.DataFrame(vet2,columns=['Media'],dtype=float)
    # print (df)

    # vet3 = [media, moda, mediana, desvioPadrao, assimetria, curtose]

    # activity = ["media", "moda", "mediana", "dp", "assimetria", "curtose"]
    # fig = ax = plt.subplot()
    # ax.plot(activity, vet3, label="cat")

    # vet2 = pd.DataFrame(vet2)
    # vet4 = vet2.to_json()
    # print(vet4)
    # vet4.to_excel('./TesteExcel.xlsx')
    menorPH = min(vet2)
    maiorPH = max(vet2)
    print("Menor PH: ", menorPH)
    print("Maior PH:", maiorPH)

    requests.post('https://api.powerbi.com/beta/cf72e2bd-7a2b-4783-bdeb-39d57b07f76f/datasets/ec527141-925f-4a25-9ee3-3df864909ebd/rows?key=2vLBzVElbF2cF%2F9YAjEbYvIY20LFJPOO0HpMXqjrV9U%2Fqh8lvY7Fo13LAH8H4TkEEPBU0NAHq%2BMIoni2AdpmQQ%3D%3D', json={
        "PH": vet2[-1],
        "Media": media,
        "Moda": moda,
        "Mediana": mediana,
        "Desvio Padrão": desvioPadrao,
        "Assimetria": assimetria,
        "Curtose": curtose,
        "Menor PH": menorPH,
        "Maior PH": maiorPH,
        "Porcentagem de Pastilhas Usadas": porcen_pas
    })
