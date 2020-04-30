from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents import personas
import random

class ciudad(Model):
    "Inicialización del modelo"
    "Se necesita incluir la base de datos, suponiendo que tendremos varias ciudades para que la inicialización sea genérica"
    def __init__(self,n,width,height,porcentaje_infectados, densidad, acumedad, transpub, edades, transporte, Casillas_zona, privado, publico, probasalida, salida):
        self.total_agentes = n #número de agentes a iniciar
        self.schedule = RandomActivation(self) #inicialización en paralelo de todos los agentes
        self.grid = MultiGrid(width,height,True) #creación de la grilla genérica
        
        "Creación de cada agente"
        for i in range(self.total_agentes):
            n_id = random.random()
            estado = (2 if n_id > porcentaje_infectados else 1)
            tcontagio = (5 if estado == 2 else 0)
            nuevo = personas(i,self,estado,tcontagio, densidad, acumedad, transpub, edades, transporte, Casillas_zona, privado, publico, probasalida, salida) #asignación del id
            self.schedule.add(nuevo) #creación del agente en el sistema
        
        "Configurar el recolector de datos"
        self.datacollector = DataCollector(
            model_reporters = {"Susceptibles": susceptibles,"Total infectados": total_infectados,"Graves": infectados_graves,
                             "Críticos": infectados_criticos,"Leves": infectados_leves,"Recuperados":recuperados,"Rt": rt, "CO": recuento_co,
                              "CE": recuento_ce,"NOR": recuento_nor,"NOC": recuento_noc,"SO": recuento_so,
                              "S": recuento_s,"0-4": recuento_ge1,"5-19": recuento_ge2,"20-39": recuento_ge3,
                              "40-59": recuento_ge4,">60": recuento_ge5,"En_cuarentena":en_cuarentena,"Vivos":agentes_vivos,
                              "Día":dia,"Max_movs": max_pos,"Min_movs": min_pos,"Contactos_prom":prom_contactos}
        )
    
    "Avanzar el modelo"
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        
#Cálculos por grupos de edad
import numpy as np
def min_pos (model):
    iniciales = [agent.posin for agent in model.schedule.agents]
    finales = [agent.posf for agent in model.schedule.agents]
    l = []
    for i in range(len(iniciales)):
        posi = iniciales[i]
        posfn = finales[i]
        diff = abs(posi[0]-posfn[0])+abs(posi[1]-posfn[1])
        l.append(diff)
        
    return min(l)

def max_pos (model):
    iniciales = [agent.posin for agent in model.schedule.agents]
    finales = [agent.posf for agent in model.schedule.agents]
    l = []
    for i in range(len(iniciales)):
        posi = iniciales[i]
        posfn = finales[i]
        diff = abs(posi[0]-posfn[0])+abs(posi[1]-posfn[1])
        l.append(diff)
        
    return max(l)

def recuento_ge1 (model): #grupo de 0-4
    estado = [agent.estado for agent in model.schedule.agents]
    ledad= [agent.edad for agent in model.schedule.agents]
    k = [1,2,3,4,5]
    l = []
    for i in k:
        suma = 0
        for j in range(len(estado)):
            if (ledad[j]<5 and estado[j]==i):
                suma +=1
        l.append(suma)
    return l
def recuento_ge2 (model): #grupo de 5-19
    estado = [agent.estado for agent in model.schedule.agents]
    ledad= [agent.edad for agent in model.schedule.agents]
    k = [1,2,3,4,5]
    l = []
    for i in k:
        suma = 0
        for j in range(len(estado)):
            if (ledad[j]<20 and ledad[j]>=5 and estado[j]==i):
                suma +=1
        l.append(suma)
    return l
def recuento_ge3 (model): #grupo de 20-39
    estado = [agent.estado for agent in model.schedule.agents]
    ledad= [agent.edad for agent in model.schedule.agents]
    k = [1,2,3,4,5]
    l = []
    for i in k:
        suma = 0
        for j in range(len(estado)):
            if (ledad[j]<40 and ledad[j]>=20 and estado[j]==i):
                suma +=1
        l.append(suma)
    return l
def recuento_ge4 (model): #grupo de 40-59
    estado = [agent.estado for agent in model.schedule.agents]
    ledad= [agent.edad for agent in model.schedule.agents]
    k = [1,2,3,4,5]
    l = []
    for i in k:
        suma = 0
        for j in range(len(estado)):
            if (ledad[j]<60 and ledad[j]>=40 and estado[j]==i):
                suma +=1
        l.append(suma)
    return l
def recuento_ge5 (model): #grupo >=60
    estado = [agent.estado for agent in model.schedule.agents]
    ledad= [agent.edad for agent in model.schedule.agents]
    k = [1,2,3,4,5]
    l = []
    for i in k:
        suma = 0
        for j in range(len(estado)):
            if (ledad[j]>=60 and estado[j]==i):
                suma +=1
        l.append(suma)
    return l

#Cálculos globales
import statistics as st
def prom_contactos(model):
    contactos = [agent.contactos for agent in model.schedule.agents]
    return st.mean(contactos)
    
def total_infectados(model):
    return infectados_leves(model) + infectados_graves(model) + infectados_criticos(model)

def susceptibles(model):
    infectados = [agent.estado for agent in model.schedule.agents]
    cuenta = 0
    for i in infectados:
        if i==1:
            cuenta+=1
    return cuenta

def infectados_leves(model):
    infectados = [agent.estado for agent in model.schedule.agents]
    cuenta = 0
    for i in infectados:
        if i==2:
            cuenta+=1
    return cuenta

def infectados_graves(model):
    infectados = [agent.estado for agent in model.schedule.agents]
    cuenta = 0
    for i in infectados:
        if i==3: 
            cuenta+=1
    return cuenta

def infectados_criticos(model):
    infectados = [agent.estado for agent in model.schedule.agents]
    cuenta = 0
    for i in infectados:
        if i==4:
            cuenta+=1
    return cuenta

def recuperados(model):
    infectados = [agent.estado for agent in model.schedule.agents]
    cuenta = 0
    for i in infectados:
        if i==5:
            cuenta+=1
    return cuenta

def agentes_vivos(model):
    return model.schedule.get_agent_count()

def dia(model):
    return model.schedule.time

def en_cuarentena(model):
    estado = [agent.estado for agent in model.schedule.agents]
    cuarentena = [agent.cuarentena for agent in model.schedule.agents]
    k = [1,2,3,4,5]
    l = []
    for i in k:
        suma = 0
        for j in range(len(cuarentena)):
            if (cuarentena[j]==1 and estado[j]==i):
                suma +=1
        l.append(suma)
    return l

def rt(model):
    infectados = [agent.infectados for agent in model.schedule.agents]
    estado = [agent.estado for agent in model.schedule.agents]
    tiempo = [agent.tcontagio for agent in model.schedule.agents]
    cuenta = 0
    suma = 0
    res = 0
    for i in range(len(infectados)):
        if(estado[i]==2 or estado[i]==3 or estado[4] and tiempo[i]>=5):
            cuenta+=1
            suma+=infectados[i]
            res = (0 if cuenta == 0 else suma/cuenta)
    return res

def recuento_co (model):
    estado = [agent.estado for agent in model.schedule.agents]
    zonas = [agent.zona for agent in model.schedule.agents]
    k = [1,2,3,4,5]
    l = []
    for i in k:
        suma = 0
        for j in range(len(zonas)):
            if (zonas[j] == "CO" and estado[j]==i):
                suma +=1
        l.append(suma)
    return l

def recuento_ce (model):
    estado = [agent.estado for agent in model.schedule.agents]
    zonas = [agent.zona for agent in model.schedule.agents]
    k = [1,2,3,4,5]
    l = []
    for i in k:
        suma = 0
        for j in range(len(zonas)):
            if (zonas[j] == "CE" and estado[j]==i):
                suma +=1
        l.append(suma)
    return l

def recuento_nor (model):
    estado = [agent.estado for agent in model.schedule.agents]
    zonas = [agent.zona for agent in model.schedule.agents]
    k = [1,2,3,4,5]
    l = []
    for i in k:
        suma = 0
        for j in range(len(zonas)):
            if (zonas[j] == "NOR" and estado[j]==i):
                suma +=1
        l.append(suma)
    return l

def recuento_noc (model):
    estado = [agent.estado for agent in model.schedule.agents]
    zonas = [agent.zona for agent in model.schedule.agents]
    k = [1,2,3,4,5]
    l = []
    for i in k:
        suma = 0
        for j in range(len(zonas)):
            if (zonas[j] == "NOC" and estado[j]==i):
                suma +=1
        l.append(suma)
    return l

def recuento_so (model):
    estado = [agent.estado for agent in model.schedule.agents]
    zonas = [agent.zona for agent in model.schedule.agents]
    k = [1,2,3,4,5]
    l = []
    for i in k:
        suma = 0
        for j in range(len(zonas)):
            if (zonas[j] == "SO" and estado[j]==i):
                suma +=1
        l.append(suma)
    return l

def recuento_s (model):
    estado = [agent.estado for agent in model.schedule.agents]
    zonas = [agent.zona for agent in model.schedule.agents]
    k = [1,2,3,4,5]
    l = []
    for i in k:
        suma = 0
        for j in range(len(zonas)):
            if (zonas[j] == "S" and estado[j]==i):
                suma +=1
        l.append(suma)
    return l
