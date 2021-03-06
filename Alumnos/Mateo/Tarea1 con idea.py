import math                                 ##
from controller import Robot                ##
from controller import Motor                ##
from controller import PositionSensor       ##
###############################################################################################################################################
robot = Robot() # Crear el objeto robot                                                     ##
timeStep = 32   # timeStep = numero de milisegundos entre actualizaciones mundiales         ##
angulo_actual = 0                                                                           ##
###############################################################################################################################################
# Motor                                                 ##
ruedaIzquierda = robot.getDevice("wheel1 motor")        ##
ruedaDerecha = robot.getDevice("wheel2 motor")          ##
ruedaIzquierda.setPosition(float('inf'))                ##
ruedaDerecha.setPosition(float('inf'))                  ##
###############################################################################################################################################
'# Gyrosocopo'                      ##
gyro = robot.getDevice("gyro")      ##
gyro.enable(timeStep)               ##
###############################################################################################################################################
'# Gps'                                                                 ##
gps = robot.getDevice("gps")                                            ##
gps.enable(timeStep)                                                    ##
tilesize = 0.06                                                         ##
robot.step(timeStep) # Actualizo los valores de los sensores            ##
startX = gps.getValues()[0]/tilesize # Cargo La posicion inicial        ##
startY = gps.getValues()[2]/tilesize                                    ##
###############################################################################################################################################
'# Funciones'                                                    ##
def avanzar(vel):
    ruedaIzquierda.setVelocity(vel)
    ruedaDerecha.setVelocity(vel)
def girar(vel):
    ruedaIzquierda.setVelocity(-vel)
    ruedaDerecha.setVelocity(vel)
def rotar(angulo):
    global angulo_actual
    tiempo_anterior = 0
    #  iniciar_rotacion
    girar(1.2)  
    # Mientras no llego al angulo solicitado sigo girando  
    while (abs(angulo - angulo_actual) > 1):
        tiempo_actual = robot.getTime()
        # print("Inicio rotacion angulo", angulo, "Angulo actual:",angulo_actual)
        tiempo_transcurrido = tiempo_actual - tiempo_anterior  # tiempo que paso en cada timestep
        radsIntimestep = abs(gyro.getValues()[1]) * tiempo_transcurrido   # rad/seg * mseg * 1000
        degsIntimestep = radsIntimestep * 180 / math.pi
        print("rads: " + str(radsIntimestep) + " | degs: " + str(degsIntimestep))
        angulo_actual += degsIntimestep
        # Si se pasa de 360 grados se ajusta la rotacion empezando desde 0 grados
        angulo_actual = angulo_actual % 360
        # Si es mas bajo que 0 grados, le resta ese valor a 360
        if angulo_actual < 0:
            angulo_actual += 360
        tiempo_anterior = tiempo_actual
        robot.step(timeStep) 
    print("Rotacion finalizada pa")
    angulo_actual = 0
    return True
def MovimientoPa(angulo, vel, coordX, coordY):
    global x
    global y
    if rotar(angulo):
        print("Rotacion de 90 terminada, me detengo pa")
        avanzar(0)
    while not ((coordX - 0.15 <= x <= coordX + 0.15) and (coordY - 0.15 <= y <= coordY + 0.15)):
        x = gps.getValues()[0]/tilesize
        y = gps.getValues()[2]/tilesize
        print("Avanzamos, pa")
        avanzar(vel)
        robot.step(timeStep) 
        print("x:",round(x,2), "y:",round(y,2))
    print("Llegamos pa")
################################################################################################################################################
'# Codigo Real'
while robot.step(timeStep) != -1:
    x = gps.getValues()[0]/tilesize
    y = gps.getValues()[2]/tilesize

# Movimiento 1:
    MovimientoPa(90, 6, -5, -1)
# Movimiento 2:
    MovimientoPa(87, 6, -5, 3)
# Movimiento 3:
    MovimientoPa(270, 6, 5, 3)
# Movimiento 4:
    MovimientoPa(270, 6, 5, 1)
# Movimiento 5:
    MovimientoPa(270, 6, 3, 1)
# Movimiento 6:
    MovimientoPa(86, 6, 3, -1)
# Movimiento 7:
    MovimientoPa(90, 6, -5, -1)
# Salida del loop:
    break
###############################################################################################################################################