import json
import pickle
from model import ciudad
import pandas as pd
import os
import city_grid

class Runner():
    def __init__(self, ruta, city, m, poblacion, area):
        self.densidad = pd.read_excel(ruta,sheet_name="densidad")
        self.edades = pd.read_excel(ruta,sheet_name="edad")
        self.transporte = pd.read_excel(ruta,sheet_name="transporte")
        self.publico = pd.read_excel(ruta,sheet_name="publico")
        self.privado = pd.read_excel(ruta,sheet_name="privado")
        self.salida = pd.read_excel(ruta,sheet_name="probsalida")

        if not os.path.exists("Casillas_zona_"+str(m)+".json"):
            city_grid.create_grid(city=city, cell_size=m)
        with open("Casillas_zona_"+str(m)+".json") as json_file:
            self.Casillas_zona = dict(json.load(json_file))

        for k, v in self.Casillas_zona.items():
            self.Casillas_zona[k] = list(map(tuple, v))

        with open('dim_grida_'+str(m)+'.pickle', 'rb') as h:
            self.Number_in_x, self.Number_in_y = pickle.load(h)

        dens = poblacion / area #densidad por km2
        dens = dens / 1000000 #densidad por m2
        dens = dens * (m**2)

        suma = 0
        for key in self.Casillas_zona.keys():
            suma += len(self.Casillas_zona[key])
        
        n_agentes = round(suma*dens*0.001)
        print(n_agentes)
        
        porcentaje_infectados = 0.999
        dias_cuarentena = 40
        long_paso = 10

        self.acumedad= self.calc_acumedad(self.edades)
        self.transpub = self.calc_transpub(self.transporte)
        self.probasalida = self.calc_probsalida(self.salida)
        self.model = ciudad(
            n_agentes,
            m,
            self.Number_in_x, 
            self.Number_in_y,
            porcentaje_infectados,
            self.densidad, 
            self.acumedad, 
            self.transpub, 
            self.edades, 
            self.transporte, 
            self.Casillas_zona, 
            self.privado, 
            self.publico, 
            self.probasalida, 
            self.salida,
            dias_cuarentena,
            long_paso)

    def calc_acumedad(self, edades):
        acumedad = {}
        for fila in range (len(edades["Zona/Edad"])):
            acumedad[edades["Zona/Edad"][fila]]=[]
            acumedad[edades["Zona/Edad"][fila]].append(edades["0-4"][fila])
            acumedad[edades["Zona/Edad"][fila]].append(edades["0-4"][fila] + edades["5-19"][fila])
            acumedad[edades["Zona/Edad"][fila]].append(edades["0-4"][fila] + edades["5-19"][fila] + edades["20-39"][fila])
            acumedad[edades["Zona/Edad"][fila]].append(edades["0-4"][fila] + edades["5-19"][fila] + edades["20-39"][fila] + edades["40-59"][fila])
            acumedad[edades["Zona/Edad"][fila]].append(edades["0-4"][fila] + edades["5-19"][fila] + edades["20-39"][fila] + edades["40-59"][fila] + edades[">60"][fila])
        return acumedad

    def calc_transpub(self, transporte):
        transpub={}
        for fila in range (len(transporte["Zona/Edad"])):
            transpub[transporte["Zona/Edad"][fila]]={}
            for i in range (1,6):
                transpub[transporte["Zona/Edad"][fila]][transporte.columns[i]]=[]
                transpub[transporte["Zona/Edad"][fila]][transporte.columns[i]].append(transporte[transporte.columns[i]][fila])
        return transpub

    def calc_probsalida(self, salida):
        probasalida={}
        for fila in range (len(salida["Zona/Edad"])):
            probasalida[salida["Zona/Edad"][fila]]={}
            for i in range (1,6):
                probasalida[salida["Zona/Edad"][fila]][salida.columns[i]]=[]
                probasalida[salida["Zona/Edad"][fila]][salida.columns[i]].append(salida[salida.columns[i]][fila])
        return probasalida
    
    def run(self,steps):
        for i in range(steps):
            print(f"empezando step {i}")
            self.model.step()
            print(f"acabo step {i}")
        return self.model.datacollector.get_model_vars_dataframe()
