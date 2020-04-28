from mesa import Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import numpy as np
import random
import math

class personas(Agent):
        "Inicialización de los atributos del agente"
        #Sexo: hombre o mujer (check)
        #Edad: se asigna de acuerdo con la distribución de la edad de la localidad a la que pertenece el agente. (check)
        #Mododetransporte: publico o privado (check)
        #Síntomas?: true si es sintomático, false dlc (check)
        #Estado: Tipo de contagio que toma los siguientes valores: no contagiado [1], contagio leve asintomático o sintomático[2], 
        #contagio grave [3], contagio crítico [4], recuperado [5]
        #Estado (check)
        #TiempoRecuperacion: Tiempo de recuperación del paciente (días) (check)
        #TiempoContagiado: tiempo que lleva contagiado el agente (check)
        #Posición inicial: posición inicial del agente (check)
        #Posición final: posición final del agente (check)
        #zona: zona a la que pertenece (check)
        #Sale?: parametro de verificación si la persona se mueve afuera de su localidad (check)
        #def _init_(self,n_id, modelo , sexo, edad, modtrans, sintomas, estado, trecuperacion = 0, tcontagio = 0, posin, posf, localidad, sale):
        #propMujer = 0.522 #proporcion de mujeres en la ciudad
        
        #Se inicializa el estado de todos los agentes. #no contagiado [1], contagio leve asintomático o sintomático[2], 
        #contagio grave [3], contagio crítico [4], recuperado [5]
        #Al principio todos están no contagiados
    
        def __init__(self, n_id, modelo, n_estado, densidad, acumedad, transpub, edades, transporte, Casillas_zona, transportepiv, transportepub, probasalida, salida):
            super().__init__(n_id,modelo)
            
            self.estado = n_estado
            #Hay que pedirle a solo un agente de una zona determinada que se contagie en estado = 2
            #Se definen los parámetros de la infección
            self.infectados = 0
            self.trecuperacion =0
            self.tcontagio = 0 
            self.cuarentena = 0 #parámetro de la cuarentena. 1 hay cuarentena, 0 no hay cuarentena
            self.tcuarentena = 0 #tiempo en cuarentena
            #Se asigna el sexo: 1 - hombre, 2 - mujer
            numsex = random.random()
            propMujer = 0.522
            if numsex <= propMujer:
                self.sexo = 2 
            else:
                self.sexo = 1
            
            #Se asigna la zona de acuerdo a la densidad poblacional

            self.set_zona(densidad)
                              
            #Se asigna la edad

            #Ahora, para cada agente, dependiendo de la zona se asigna la edad

            self.set_edad(acumedad, edades)
            
            #Ahora, dependiendo de la zona y edad se asigna el transporte: #1 - público, 2 - privado
            self.set_transporte(transpub, edades)
            
            
            #Se define si es asintomático o no #1 - sintomático (20%) , 2 - asintomático (80%)
            self.set_sintomas()
            
            #Se define la posición inicial y final de acuerdo con la localidad FALTA ESTO
            self.posin = random.choice(Casillas_zona[self.zona])
            self.pos = self.posin

            self.model.grid._place_agent(self.pos,self)

            self.set_posf(transportepiv, transportepub, Casillas_zona)

            self.set_salida(probasalida, salida)

        def set_zona(self, densidad):
            numdens = random.random()
            acum = []
            for fila in range(len(densidad["Zona"])):
                if fila == 0:
                    acum.append(densidad["Densidad"][fila])
                    if numdens >= 0 and numdens < densidad["Densidad"][fila]:
                        self.zona = densidad["Zona"][fila]
                else:
                    suma=densidad["Densidad"][fila]+ acum[fila-1]
                    acum.append(suma)
                    if numdens >= suma-float(acum[fila-1]) and numdens <= suma:
                        self.zona = densidad["Zona"][fila] 

        def set_posf(self, transportepiv, transportepub, Casillas_zona):
            trans = transportepiv["Zona"]
            ledad = ["5-19","20-39","40-50",">60"]
            
            if self.modtrans == 1: #público
                if (self.edad > 4 and self.edad < 20):
                    l = acum_trans(trans,transportepub,"5-19",self.zona, transportepiv)
                    n = random.random()
                    for i in range(len(l)):
                        if(i>0):
                            if n < l[i] and n>= l[i-1]:
                                self.posf = random.choice(Casillas_zona[trans[i]])   
                        else:
                            if n < l[i]:
                                self.posf = random.choice(Casillas_zona[trans[i]])   
                elif(self.edad > 19 and self.edad < 40):
                    l = acum_trans(trans,transportepub,"20-39",self.zona, transportepiv)
                    n = random.random()
                    for i in range(len(l)):
                        if(i>0):
                            if n < l[i] and n>= l[i-1]:
                                self.posf = random.choice(Casillas_zona[trans[i]])   
                        else:
                            if n < l[i]:
                                self.posf = random.choice(Casillas_zona[trans[i]]) 
                elif(self.edad > 39 and self.edad < 60):
                    l = acum_trans(trans,transportepub,"40-59",self.zona, transportepiv)
                    n = random.random()
                    for i in range(len(l)):
                        if(i>0):
                            if n < l[i] and n>= l[i-1]:
                                self.posf = random.choice(Casillas_zona[trans[i]])   
                        else:
                            if n < l[i]:
                                self.posf = random.choice(Casillas_zona[trans[i]]) 
                elif(self.edad > 60):
                    l = acum_trans(trans,transportepub,">60",self.zona, transportepiv)
                    n = random.random()
                    for i in range(len(l)):
                        if(i>0):
                            if n < l[i] and n>= l[i-1]:
                                self.posf = random.choice(Casillas_zona[trans[i]])   
                        else:
                            if n < l[i]:
                                self.posf = random.choice(Casillas_zona[trans[i]]) 
                else:
                    self.posf = random.choice(Casillas_zona[self.zona])
                    
            else: #privado
                if (self.edad >4 and self.edad <20):
                    l = acum_trans(trans,transportepiv,"5-19",self.zona, transportepiv)
                    n = random.random()
                    for i in range(len(l)):
                        if(i>0):
                            if n < l[i] and n>= l[i-1]:
                                self.posf = random.choice(Casillas_zona[trans[i]])   
                        else:
                            if n < l[i]:
                                self.posf = random.choice(Casillas_zona[trans[i]])   
                elif(self.edad > 19 and self.edad < 40):
                    l = acum_trans(trans,transportepiv,"20-39",self.zona, transportepiv)
                    n = random.random()
                    for i in range(len(l)):
                        if(i>0):
                            if n < l[i] and n>= l[i-1]:
                                self.posf = random.choice(Casillas_zona[trans[i]])   
                        else:
                            if n < l[i]:
                                self.posf = random.choice(Casillas_zona[trans[i]]) 
                elif(self.edad > 39 and self.edad < 60):
                    l = acum_trans(trans,transportepub,"40-59",self.zona, transportepiv)
                    n = random.random()
                    for i in range(len(l)):
                        if(i>0):
                            if n < l[i] and n>= l[i-1]:
                                self.posf = random.choice(Casillas_zona[trans[i]])   
                        else:
                            if n < l[i]:
                                self.posf = random.choice(Casillas_zona[trans[i]]) 
                elif(self.edad > 60):
                    l = acum_trans(trans,transportepiv,">60",self.zona, transportepiv)
                    n = random.random()
                    for i in range(len(l)):
                        if(i>0):
                            if n < l[i] and n>= l[i-1]:
                                self.posf = random.choice(Casillas_zona[trans[i]])   
                        else:
                            if n < l[i]:
                                self.posf = random.choice(Casillas_zona[trans[i]]) 
                else:
                    self.posf = random.choice(Casillas_zona[self.zona])

        def set_salida(self, probasalida, salida):
            numsalida = random.random()
            for fila in range(len(salida["Zona/Edad"])):
                #Si el agente pertenece a la zona validada entonces se revisa la edad
                
                if self.zona == salida["Zona/Edad"][fila]: 
                    if self.edad >= 0 and self.edad <= 4: #Entre 0 y 4 años
                        if numsalida <= probasalida[self.zona]["0-4"][0]:
                            self.sale = 1 #sale 
                        else:
                            self.sale = 2 #no sale
                    if self.edad > 4 and self.edad <= 19: #Entre 5 y 19
                        if numsalida <= probasalida[self.zona]["5-19"][0]:
                            self.sale = 1
                        else:
                            self.sale = 2
                    if self.edad > 19 and self.edad <= 29: #Entre 20 y 39
                        if numsalida <= probasalida[self.zona]["20-39"][0]:
                            self.sale = 1
                        else:
                            self.sale = 2                         
                    if self.edad > 39 and self.edad <= 59: #Entre 40 y 59
                        if numsalida <= probasalida[self.zona]["40-59"][0]:
                            self.sale = 1
                        else:
                            self.sale = 2                                                
                    if self.edad > 59 and self.edad <= 99: #Más de 60
                        if numsalida <= probasalida[self.zona][">60"][0]:
                            self.sale = 1
                        else:
                            self.sale = 2 

        "Método para asignar el tipo de sintomas"
        def set_sintomas(self):
            numsint = random.random() 
            
            if numsint <= 0.2:
                self.sintomas = 1
            else:
                self.sintomas = 2

        "Método para asignar el tipo de transporte dependiendo de la edad"
        def set_transporte(self, transpub, edades):
            #Primero la zona
            numtrans = random.random()
            for fila in range(len(edades["Zona/Edad"])):
                #Si el agente pertenece a la zona validada entonces se revisa la edad
                if self.zona == edades["Zona/Edad"][fila]: 
                    if self.edad >= 0 and self.edad <= 4: #Entre 0 y 4 años
                        if numtrans <= transpub[self.zona]["pub-0-4"][0]:
                            self.modtrans = 1
                        else:
                            self.modtrans = 2
                    if self.edad > 4 and self.edad <= 19: #Entre 5 y 19
                        if numtrans <= transpub[self.zona]["pub-5-19"][0]:
                            self.modtrans = 1
                        else:
                            self.modtrans = 2
                            
                    if self.edad > 19 and self.edad <= 39: #Entre 20 y 39
                        if numtrans <= transpub[self.zona]["pub-20-39"][0]:
                            self.modtrans = 1
                        else:
                            self.modtrans = 2
                                                        
                    if self.edad > 39 and self.edad <= 59: #Entre 40 y 59
                        if numtrans <= transpub[self.zona]["pub-40-59"][0]:
                            self.modtrans = 1
                        else:
                            self.modtrans = 2
                                                                                    
                    if self.edad > 59: #Más de 60
                        if numtrans <= transpub[self.zona]["pub->60"][0]:
                            self.modtrans = 1
                        else:
                            self.modtrans = 2
        
        "Método para asignar la edad dependiendo de la zona"
        def set_edad(self, acumedad, edades):
            numedad = random.random()
            for fila in range(len(edades["Zona/Edad"])):
                #Si la localidad corresponde a la que se está recorriendo
                if self.zona == edades["Zona/Edad"][fila]:
                    acumulada = acumedad[self.zona] #Corresponde a la acumulada de esa zona
                    for columna in range(0,6): #Siempre se van a manejar estos valores porque los rangos no cambian
                        if columna == 0:
                            if numedad >= 0 and numedad < acumulada[columna]:
                                self.edad = random.randrange(0,5)
                        if columna == 1:
                            if numedad >= acumulada[columna-1] and numedad < acumulada[columna]:
                                self.edad = random.randrange(5,20)
                        if columna == 2:
                            if numedad >= acumulada[columna-1] and numedad < acumulada[columna]:
                                self.edad = random.randrange(20,40)
                        if columna == 3:
                            if numedad >= acumulada[columna-1] and numedad < acumulada[columna]:
                                self.edad = random.randrange(40,60)
                        if columna == 4:
                            if numedad >= acumulada[columna-1] and numedad < acumulada[columna]:
                                self.edad = random.randrange(60,100)


        "Método actualización de estados"
        def actualizar_tiempos_estados(self, tiempo_cuarentena):
            if self.estado == 2 and self.tcontagio >= 5: #cambia de leve a grave o crítico
                s1 = random.random()
                s2 = random.random()
                if self.edad <= 9: #rango de edad de 0-9
                    self.estado = (2 if s1 > 0.001 else 3 if s2 > 0.05 else 4)
                if self.edad > 9 and self.edad <= 19: #rango de edad de 10-19
                    self.estado = (2 if s1 > 0.003 else 3 if s2 > 0.05 else 4)
                elif self.edad > 19 and self.edad <= 29: #rango de edad de 20-29
                    self.estado = (2 if s1 > 0.012 else 3 if s2 > 0.05 else 4)
                elif self.edad > 29 and self.edad <= 39: #rango de edad de 30-39
                    self.estado = (2 if s1 > 0.032 else 3 if s2 > 0.05 else 4)
                elif self.edad > 39 and self.edad <= 49: #rango de edad de 40-49
                    self.estado = (2 if s1 > 0.049 else 3 if s2 > 0.05 else 4)
                elif self.edad > 49 and self.edad <= 59: #rango de edad de 50-59
                    self.estado = (2 if s1 > 0.102 else 3 if s2 > 0.122 else 4)
                elif self.edad > 59 and self.edad <= 69: #rango de edad de 60-69
                    self.estado = (2 if s1 > 0.166 else 3 if s2 > 0.274 else 4)
                elif self.edad > 69 and self.edad <= 79: #rango de edad de 70-79
                    self.estado = (2 if s1 > 0.243 else 3 if s2 > 0.432 else 4)
                else: #rango de edad de 6más de 80
                    self.estado = (2 if s1 > 0.273 else 3 if s2 > 0.709 else 4)
                     
            #Actualizar tiempos de recuperación
            if self.estado == 3 | self.estado == 4:
                self.trecuperacion = 21 + random.randint(0,22)    
            else:
                self.trecuperacion = 14
                
            #Validar continuación de la cuarentena  
            if self.tcuarentena == tiempo_cuarentena:
                self.cuarentena = 0
                self.tcuarentena = 0
            
            #Actualizar tiempo en cuarentena si la hay
            if self.cuarentena == 1:
                self.tcuarentena += 1
            
             
            #matar a los agentes. Pendiente de trabajo futuro es tener modelado la hospitalización
            if self.estado == 3 | self.estado == 4: 
                s1 = random.random()
                if self.edad <= 9: #rango de edad de 0-9
                    if s1 < 0.00002:
                        self.model.grid._remove_agent(self.pos,self)
                        self.model.schedule.remove(self)
                if self.edad > 9 and self.edad <= 19: #rango de edad de 10-19
                    if s1 < 0.00004:
                        self.model.grid._remove_agent(self.pos,self)
                        self.model.schedule.remove(self)
                elif self.edad > 19 and self.edad <= 29: #rango de edad de 20-29
                    if s1 < 0.0003:
                        self.model.grid._remove_agent(self.pos,self)
                        self.model.schedule.remove(self)
                elif self.edad > 29 and self.edad <= 39: #rango de edad de 30-39
                    if s1 < 0.0008:
                        self.model.grid._remove_agent(self.pos,self)
                        self.model.schedule.remove(self)
                elif self.edad > 39 and self.edad <= 49: #rango de edad de 40-49
                    if s1 < 0.0015:
                        self.model.grid._remove_agent(self.pos,self)
                        self.model.schedule.remove(self)
                elif self.edad > 49 and self.edad <= 59: #rango de edad de 50-59
                    if s1 < 0.006:
                        self.model.grid._remove_agent(self.pos,self)
                        self.model.schedule.remove(self)
                elif self.edad > 59 and self.edad <= 69: #rango de edad de 60-69
                    if s1 < 0.022:
                        self.model.grid._remove_agent(self.pos,self)
                        self.model.schedule.remove(self)
                elif self.edad > 69 and self.edad <= 79: #rango de edad de 70-79
                    if s1 < 0.051:
                        self.model.grid._remove_agent(sel.pos,self)
                        self.model.schedule.remove(self)
                else: #rango de edad de 6más de 80
                    if s1 < 0.093:
                        self.model.grid._remove_agent(self.pos,self)
                        self.model.schedule.remove(self)
            
            if self.estado != 1 and self.estado != 5  and self.tcontagio == self.trecuperacion: #recupera a los infectados
                self.tcontagio = 0
                self.estado = 5
            if self.estado != 1 and self.estado != 5  and self.tcontagio < self.trecuperacion: #actualiza los tiempos de contagio
                self.tcontagio += 1
                
        
        "Método step general"
        def step(self):
            tviaje = (120 if self.modtrans == 1 else 60)
            self.activar_cuarentena(False,0)
            self.mtrabajo(tviaje,60)
            n_posx =int( self.pos[0] + round(random.uniform(-5,5)))
            n_posy =int( self.pos[1] + round(random.uniform(-5,5)))
            self.mzona(360,60,[n_posx,n_posy])
            self.mcasa(tviaje,60)
            self.actualizar_tiempos_estados(0)
            
        "Organizar la cuarentena de un porcentaje de la población"
        def activar_cuarentena(self, activar_cuarentena, porcentaje_en_cuarentena):
            if activar_cuarentena == True:
                r = random.random()
                if(r<porcentaje_en_cuarentena): #a un porcentaje de la población les restringe la movilidad
                    self.cuarentena = 1
            
        "Construcción del método de infectar"
        def infectar(self):
            if self.estado == 2 and self.tcontagio >= 5:
                agentes = self.model.grid.get_cell_list_contents([self.posin])
                if (len(agentes) > 1):
                    for i in range(len(agentes)):
                        agente = agentes[i]
                        if agente.estado == 1:
                            s = random.random()
                            if(self.sintomas == 1):
                                # caso de infección por sintomático
                                if (s <= 0.09):
                                    agente.estado = 2
                                    self.infectados +=1
                            else:
                                # caso de infección por asintomático
                                if (s <= 0.09 * 0.5):
                                    agente.estado = 2
                                    self.infectados +=1
        
        "Construcción del método de mover en zona"
        def mzona(self, tiempo, intervalo, poszona):
            if self.estado != 3 and self.estado != 4 and self.cuarentena == 0:
                count = 0
                movs = tiempo// intervalo
                mv1 = round(euc_dist(self.pos,poszona)/(tiempo/intervalo))
                #print("t: ",tiempo, " - inter: ",intervalo)
                while movs > 0 or self.pos != poszona:
                    n_pasos_req = abs(self.pos[0]-poszona[0])+abs(self.pos[1]-poszona[1])
                    mv2 = round(euc_dist(self.pos,poszona)/(movs))
                    #print("Pos: ",self.pos," - posf: ",poszona)
                    #print("Iteración: ", count," pasos_req: ",n_pasos_req)
                    #print("movs: ",movs)
                    if movs == 1:
                        paso = n_pasos_req
                        #print("paso_f: ",paso)
                        n_pos = tuple(moverxy([self.pos[0],self.pos[1]], [poszona[0],poszona[1]],paso))
                        self.model.grid.move_agent(self,n_pos)
                        self.infectar()
                        break
                    else:
                        paso =  (min(mv1,mv2) if (mv1!=0 and mv2!=0) else n_pasos_req)
                        if paso == 0:
                            break
                        else:
                            #print("paso_f: ",paso)
                            n_pos = tuple(moverxy([self.pos[0],self.pos[1]], [poszona[0],poszona[1]],paso))
                            self.model.grid.move_agent(self,n_pos)
                            self.infectar()
                            count += 1
                            movs -= 1
        
        #Construcción del método de regresar a casa
        def mcasa(self, tiempo, intervalo):
            if self.estado != 3 and self.estado != 4 :
                count = 0
                movs = tiempo // intervalo
                mv1 = round(euc_dist(self.pos,self.posin)/(tiempo/intervalo))
                #print("t: ",tiempo, " - inter: ",intervalo)
                while movs > 0 or self.pos != self.posin:
                    n_pasos_req = abs(self.pos[0]-self.posin[0])+abs(self.pos[1]-self.posin[1])
                    mv2 = round(euc_dist(self.pos,self.posin)/(movs))
                    #print("Pos: ",self.pos,"- posin: ",self.posin," - posf: ",self.posf)
                    #print("Iteración: ", count," pasos_req: ",n_pasos_req)
                    #print("movs: ",movs)
                    if movs == 1:
                        paso = n_pasos_req
                        #print("paso_f: ",paso)
                        n_pos = tuple(moverxy([self.pos[0],self.pos[1]], [self.posin[0],self.posin[1]],paso))
                        self.model.grid.move_agent(self,n_pos)
                        self.infectar()
                        break
                    else:
                        paso =  (min(mv1,mv2) if (mv1!=0 and mv2!=0) else n_pasos_req)
                        if paso == 0:
                            break
                        else:
                            #print("paso_f: ",paso)
                            n_pos = tuple(moverxy([self.pos[0],self.pos[1]], [self.posin[0],self.posin[1]],paso))
                            self.model.grid.move_agent(self,n_pos)
                            self.infectar()
                            count += 1
                            movs -= 1
        
        #Construcción del método de mover a trabajo
        def mtrabajo(self, tiempo, intervalo) : 
            #tiempo en minutos, intervalo es la longitud del paso en minutos
            if self.estado != 3 and self.estado != 4 and self.cuarentena == 0:
                count = 0
                movs = tiempo// intervalo
                mv1 = round(euc_dist(self.pos,self.posf)/(tiempo/intervalo))
                #print("t: ",tiempo, " - inter: ",intervalo)
                while movs > 0 or self.pos != self.posf:
                    n_pasos_req = abs(self.pos[0]-self.posf[0])+abs(self.pos[1]-self.posf[1])
                    mv2 = round(euc_dist(self.pos,self.posf)/(movs))
                    #print("Pos: ",self.pos,"- posin: ",self.posin," - posf: ",self.posf)
                    #print("Iteración: ", count," pasos_req: ",n_pasos_req)
                    #print("movs: ",movs)
                    if movs == 1:
                        paso = n_pasos_req
                        #print("paso_f: ",paso)
                        n_pos = tuple(moverxy([self.pos[0],self.pos[1]], [self.posf[0],self.posf[1]],paso))
                        self.model.grid.move_agent(self,n_pos)
                        self.infectar()
                        break
                    else:
                        paso = (min(mv1,mv2) if (mv1!=0 and mv2!=0) else n_pasos_req)
                        if paso ==0:
                            break
                        else:
                            #print("paso_f: ",paso)
                            n_pos = tuple(moverxy([self.pos[0],self.pos[1]], [self.posf[0],self.posf[1]],paso))
                            self.model.grid.move_agent(self,n_pos)
                            self.infectar()
                            count += 1
                            movs -= 1

def acum_trans(l1,lbase,ledad,lzona, transportepiv):
            #l1 es la base de nombres de las zonas
            #lbase es la base de datos para calcular la acumulada
            #ledad es el rango de edad en string. P.ej: "5-19"
            #lzona es la zona del agente
            trans = transportepiv["Zona"]
            matching = [s for s in lbase if ledad in s]
            l = []
            for t in range(len(l1)):
                if (trans[t]==lzona):
                    for j in range(len(matching)):
                        if(j==0):
                            l.append(lbase[matching[j]][t])
                        else:
                            suma = lbase[matching[j]][t] + l[j-1]
                            l.append(suma)
            return l

def euc_dist(a,b): #Calcula la distancia eucliadiana entre dos puntos. a y b son dos tuplas con las posicioanes iniciales (a) y finnales(b)
    return math.sqrt(((a[0]-b[0])**2)+((a[1]-b[1])**2))

def nueva_pos(posinicial,width,height): #Método para asignar la posicón final de manera recursiva
    x = random.randrange(width)
    y = random.randrange(height)
    posnueva = [x,y]
    if (posinicial != posnueva):
        return posnueva
    else:
        return nueva_pos(posinicial)

def movery(posi,posf,paso): #Método para calcular la mejor ruta entre dos puntos
    dist = euc_dist(posi,posf) #calcula la distancia     
    #revisa si el movimiento debe ser en y
    if (posf[1]<posi[1] and abs(posf[1]-posi[1])< paso):
        correccion = posi[1] - int(paso)
        n_pos = [posi[0],correccion]
        dist2 = euc_dist(n_pos,posf)
        if (dist2 < dist):
            return n_pos
        else:
            return moverx(posi,posf,paso)
    elif (posf[1]>posi[1] and abs(posf[1]-posi[1])< paso):
        correccion = posi[1] + int(paso)
        n_pos = [posi[0],correccion]
        dist2 = euc_dist(n_pos,posf)
        if (dist2 < dist):
            return n_pos
        else:
            return moverx(posi,posf,paso)
    else:
        return moverx(posi,posf,paso)

def moverxy(posi,posf,paso): #Método para calcular la mejor ruta entre dos puntos
    dist = euc_dist(posi,posf) #calcula la distancia
    l = []
    count = -paso
    while count < paso + 1:
        l.append(count)
        count +=1
    dists = []
    coords = []
    #mira x
    for i in range(len(l)):
        for j in range(len(l)):
            suma = abs(l[i])+abs(l[j])
            if suma == paso:
                n_posx = int(posi[0]+l[i])
                n_posy = int(posi[1]+l[j])
                dist2 = euc_dist([n_posx,n_posy],posf)
                coords.append([n_posx,n_posy])
                dists.append(dist2)
    
    for i in range(len(l)):
        for j in range(len(l)):
            suma = abs(l[i])+abs(l[j])
            if suma == paso:
                n_posy = int(posi[1]+l[i])
                n_posx = int(posi[0]+l[j])
                dist2 = euc_dist([n_posx,n_posy],posf)
                coords.append([n_posx,n_posy])
                dists.append(dist2)
    index_min = np.argmin(dists)
    return coords[index_min]

def movery2(posi,posf,paso): #Método para calcular la mejor ruta entre dos puntos
    dist = euc_dist(posi,posf) #calcula la distancia
    l = []
    count = -paso
    while count < paso + 1:
        l.append(count)
        count +=1
    dists = []
    coords = []
    for i in range(len(l)):
        if posf[0]<posi[0]:
            n_posx = int(posi[0]+l[i])
            n_posy = int(posi[1]-(paso-abs(l[i])))
            dist2 = euc_dist([n_posx,n_posy],posf)
            coords.append([n_posx,n_posy])
            dists.append(dist2)
        elif posf[0]>posi[0]:
            n_posx = int(posi[0]+l[i])
            n_posy = int(posi[1]+(paso-abs(l[i])))
            dist2 = euc_dist([n_posx,n_posy],posf)
            coords.append([n_posx,n_posy])
            dists.append(dist2)
        else:
            return moverx2(posi,posf,paso)
    if(len(dists)==0):
        return moverx2(posi,posf,paso)
    else:
        index_min = np.argmin(dists)
        if(dists[index_min]<dist):
            return coords[index_min]
        else:
            return moverx2(posi,posf,paso)

def moverx2(posi,posf,paso): #Método para calcular la mejor ruta entre dos puntos
    dist = euc_dist(posi,posf) #calcula la distancia
    l = []
    count = -paso
    while count < paso + 1:
        l.append(count)
        count +=1
    dists = []
    coords = []
    for i in range(len(l)):
        if posf[1]<posi[1]:
            n_posy = int(posi[1]+l[i])
            n_posx = int(posi[0]-(paso-abs(l[i])))
            dist2 = euc_dist([n_posx,n_posy],posf)
            coords.append([n_posx,n_posy])
            dists.append(dist2)
        elif posf[1]>posi[1]:
            n_posy = int(posi[1]+l[i])
            n_posx = int(posi[0]+(paso-abs(l[i])))
            dist2 = euc_dist([n_posx,n_posy],posf)
            coords.append([n_posx,n_posy])
            dists.append(dist2)
        else:
            return movery2(posi,posf,paso)
    if(len(dists)==0):
        return movery2(posi,posf,paso)
    else:
        index_min = int(np.argmin(dists))
        if(dists[index_min]<dist):
            return coords[index_min]
        else:
            return movery2(posi,posf,paso)