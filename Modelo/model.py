from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents import personas
import random

class Ciudad(Model):
    "Inicialización del modelo"
    "Se necesita incluir la base de datos, suponiendo que tendremos varias ciudades para que la inicialización sea genérica"
    def __init__(self, n, width, height, densidad, acumedad, transpub, edades, transporte, Casillas_zona, transportepiv, transportepub, probasalida, salida):
        self.total_agentes = n #número de agentes a iniciar
        self.schedule = RandomActivation(self) #inicialización en paralelo de todos los agentes
        self.grid = MultiGrid(width,height,True) #creación de la grilla genérica
        
        "Creación de cada agente"
        n_id = random.randint(0,self.total_agentes)
        for i in range(self.total_agentes):
            estado = (1 if i != n_id else 2)
            nuevo = personas(i, self, estado, densidad, acumedad, transpub, edades, transporte, Casillas_zona, transportepiv, transportepub, probasalida, salida) #asignación del id
            self.schedule.add(nuevo) #creación del agente en el sistema
        
        "Configurar el recolector de datos"
        self.datacollector = DataCollector(
            model_reporters = {"Susceptibles":susceptibles,"Total infectados": total_infectados,"Graves": infectados_graves,
                             "Críticos":infectados_criticos,"Leves":infectados_leves,"Rt":rt},
            agent_reporters = {"Estado": "estado"}
        )
    
    "Avanzar el modelo"
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

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

def rt(model):
    infectados = [agent.infectados for agent in model.schedule.agents]
    estado = [agent.estado for agent in model.schedule.agents]
    cuenta = 0
    suma = 0
    res = 0
    for i in range(len(infectados)):
        if(estado[i]!=1 and estado[i]!=5):
            cuenta+=1
            suma+=infectados[i]
            res = (0 if cuenta == 0 else suma/cuenta)
    return res

def recuento_por_zona (model,zona):
    estado = [agent.estado for agent in model.schedule.agents]
    zonas = [agent.zona for agent in model.schedule.agents]
    cuenta = 0
    for i in range(len(zonas)):
        if(zonas[i]==zona):
            if(estado[i]!=1 and estado[i]!=5):
                cuenta+=1
    return cuenta