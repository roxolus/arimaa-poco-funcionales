from definiciones import *

#### Algunas funciones ya dadas

def son_posiciones_vecinas(pos1 : Posicion, pos2 : Posicion) -> bool: # pragma: no cover
    return (pos1.fila == pos2.fila and abs(pos1.columna - pos2.columna) == 1) \
        or (pos1.columna == pos2.columna and abs(pos1.fila - pos2.fila) == 1)

def direccion_desde_hasta(pos1 : Posicion, pos2 : Posicion) -> Direccion: # pragma: no cover
    assert son_posiciones_vecinas(pos1, pos2)
    if pos1.fila < pos2.fila:
       return NORTE
    elif pos1.fila > pos2.fila:
       return SUR
    elif pos1.columna < pos2.columna:
       return ESTE
    else:
       return OESTE

def pasar_turno(j : Juego) -> Juego: # pragma: no cover
    return Juego(j.tablero, oponente(j.turno), 0)

tab: Tablero = [[Pieza(CONEJO,DORADO),VACIA,VACIA,VACIA,VACIA,VACIA,VACIA,VACIA],
                [VACIA,VACIA,VACIA,VACIA,VACIA,VACIA,VACIA,VACIA],
                [VACIA,VACIA,VACIA,VACIA,VACIA,VACIA,VACIA,VACIA],
                [Pieza(CAMELLO,PLATEADO),VACIA,VACIA,VACIA,VACIA,VACIA,VACIA,VACIA],                           
                [Pieza(CABALLO,DORADO),Pieza(CONEJO,DORADO),VACIA,VACIA,VACIA,VACIA,VACIA,VACIA],
                [VACIA,VACIA,VACIA,VACIA,VACIA,VACIA,VACIA,VACIA],
                [VACIA,VACIA,VACIA,VACIA,VACIA,VACIA,VACIA,VACIA],
                [VACIA,VACIA,VACIA,VACIA,VACIA,VACIA,VACIA,Pieza(CONEJO,DORADO)],]


def tableroBienFormado (t: Tablero) -> bool:
    columnas_bien: bool = len(t) == ALTO
    filas_bien: bool = len(t[0]) == ANCHO
    return columnas_bien & filas_bien
#print(tablero_bien_formado(tab))

def posiciónEnTablero (pos: Posicion) -> bool:
    fila_valida: bool = 0 <= pos.fila < ALTO
    columna_valida: bool = 0 <= pos.columna < ANCHO
    return fila_valida & columna_valida
#print(posiciónEnTablero(Posicion(8,8)))

def movimientoBienFormado (m: Movimiento) -> bool:
    assert posiciónEnTablero (m.origen)
    pasos_validos: bool = False
    if m.accion == MOVER_A_SECAS:
        pasos_validos = len(m.pasos) == 1
    elif m.accion == ARRASTRAR:
        pasos_validos = len(m.pasos) == 2
    else:
        pasos_validos = len(m.pasos) == 2
    return pasos_validos
#print(movimientoBienFormado(Movimiento(Accion(ARRASTRAR),Posicion(5,5),[NORTE,SUR])))

def juegoBienFormado (j: Juego) -> bool:
    assert tableroBienFormado (j.tablero)
    pasos_usados: bool = 0 <= j.pasos_consumidos < MAX_PASOS
    return pasos_usados

def esPosiciónVecinaHacia (pos: Posicion , d: Direccion , pos2: Posicion | None):
    if d == NORTE:
        pos2 = Posicion(pos.fila + 1, pos.columna)
    elif d == SUR:
        pos2 = Posicion(pos.fila - 1, pos.columna)
    elif d == ESTE:
        pos2 = Posicion(pos.fila, pos.columna + 1)
    else:
        pos2 = Posicion(pos.fila, pos.columna - 1)
    return pos2

def casillaEnPosicion(t : Tablero, p : Posicion) -> Casilla:
    res: Casilla = t[p.fila][p.columna]
    return res
#print(casilla_en_posicion(tab, Posicion(4,0)))

def hayCasillaVacía (t : Tablero , pos : Posicion ) -> bool:
    esVacia: bool = casillaEnPosicion(t,pos) == VACIA
    return esVacia


def hayFiguraDeColor (t: Tablero , pos: Posicion , f: Figura , col: Color ) -> bool:
    hayFig: bool = False
    casilla_actual = casillaEnPosicion (t,pos)
    if  casilla_actual.figura == f:
        if casilla_actual.color == col:
            hayFig = True
    return hayFig
#print(hayFiguraDeColor(tab,Posicion(4,0),CABALLO,PLATEADO))

def hayPiezaDeColor (t : Tablero , pos : Posicion , col : Color ) -> bool:
    res: bool = False
    c: Casilla = casillaEnPosicion(t,pos)
    if c != VACIA:
        f:Figura = c.figura
        res: bool = hayFiguraDeColor (t,pos,f,col)
    return res

def hayCasillaVacíaHacia (t : Tablero , pos : Posicion , d : Direccion ) -> bool:
    pos2:Posicion = esPosiciónVecinaHacia(pos,d,None)
    print(pos2)
    casilla_vacia: bool = False
    if posiciónEnTablero(pos2):
        casilla_vacia = hayCasillaVacía (t,pos2)
    return casilla_vacia

def hayPiezaAmigaHacia (t : Tablero , pos : Posicion , d : Direccion ):
    pos_amigo: Posicion = esPosiciónVecinaHacia(pos,d,None)
    col: Color = casillaEnPosicion(t,pos).color
    es_amigo: bool = False
    if posiciónEnTablero (pos_amigo):
        es_amigo = hayPiezaDeColor(t,pos_amigo,col)
    return es_amigo

def hayPiezaAmigaVecina (t : Tablero , pos : Posicion ) -> bool:
    amigo_adyacente: bool = False
    for d in Direccion:
        if not amigo_adyacente:
            amigo_adyacente = hayPiezaAmigaHacia (t,pos,d)
    return amigo_adyacente
#print(hayPiezaAmigaVecina(tab,Posicion(4,0)))

def hayPiezaEnemigaMásDébilHacia (t : Tablero , pos : Posicion , d : Direccion ) -> bool:
    col_amigo: Color = casillaEnPosicion(t,pos).color
    col_enemigo: Color = oponente(col_amigo)
    pos_enemigo: Posicion = esPosiciónVecinaHacia(pos,d,None)
    piezaDebil: bool = False

    if posiciónEnTablero(pos_enemigo):
        if hayPiezaDeColor (t,pos_enemigo,col_enemigo):
            fuerza_amigo = fuerza((casillaEnPosicion(t,pos).figura))
            fuerza_enemigo = fuerza((casillaEnPosicion(t,pos_enemigo).figura))
            piezaDebil = fuerza_amigo > fuerza_enemigo
    return piezaDebil

def hayPiezaEnemigaMásFuerteHacia (t : Tablero , pos : Posicion , d : Direccion ):
    col_amigo: Color = casillaEnPosicion(t,pos).color
    col_enemigo: Color = oponente(col_amigo)
    pos_enemigo: Posicion = esPosiciónVecinaHacia(pos,d,None)
    piezaFuerte: bool = False

    if posiciónEnTablero(pos_enemigo):
        if hayPiezaDeColor (t,pos_enemigo,col_enemigo):
            fuerza_amigo = fuerza((casillaEnPosicion(t,pos).figura))
            fuerza_enemigo = fuerza((casillaEnPosicion(t,pos_enemigo).figura))
            piezaFuerte = fuerza_amigo < fuerza_enemigo
    return piezaFuerte
#print(hayPiezaEnemigaMásFuerteHacia(tab,Posicion(4,0),ESTE))

def hayPiezaEnemigaMásFuerteVecina (t : Tablero , pos : Posicion ) -> bool:
    enemigo_fuerte: bool = False
    for d in Direccion:
        if not enemigo_fuerte:
            enemigo_fuerte = hayPiezaEnemigaMásFuerteHacia (t,pos,d)
    return enemigo_fuerte

def hayPiezaCongelada (t : Tablero , pos : Posicion ):
    enemigo_fuerte: bool = hayPiezaEnemigaMásFuerteVecina (t,pos)
    amigo:bool = hayPiezaAmigaVecina (t,pos)
    congelado: bool = enemigo_fuerte & (not amigo)
    return congelado
    


        
#### Ejercicio 1

def tablero_bien_formado(t : Tablero) -> bool:
    return tableroBienFormado(t)
    raise Exception("No implementado")

def posicion_en_tablero(pos : Posicion) -> bool:
    return posiciónEnTablero(pos)
    raise Exception("No implementado")

def movimiento_bien_formado(m : Movimiento) -> bool:
    return movimientoBienFormado(m)
    raise Exception("No implementado")

def juego_bien_formado(j : Juego) -> bool:
    juegoBienFormado(j)
    raise Exception("No implementado")

#### Ejercicio 2

def posicion_vecina_hacia(pos : Posicion, d : Direccion) -> Posicion:
    res = esPosiciónVecinaHacia(pos,d,None)
    return res
    raise Exception("No implementado")
#print(posicion_vecina_hacia(Posicion(6,5),SUR))

def casilla_en_posicion(t : Tablero, pos : Posicion) -> Casilla:
    return casillaEnPosicion(t,pos)
    raise Exception("No implementado")


def hay_casilla_vacia(t : Tablero, pos : Posicion) -> bool:
    return hayCasillaVacía (t,pos)
    raise Exception("No implementado")
#print(hayCasillaVacía(tab,Posicion(4,0)))

def hay_pieza_de_color(t : Tablero, pos : Posicion, col : Color) -> bool:
    return hayPiezaDeColor(t,pos,col)
    raise Exception("No implementado")
#print(hay_pieza_de_color(tab,Posicion(4,0),DORADO))

#### Ejercicio 3

def hay_casilla_vacia_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    return hayCasillaVacíaHacia (t,pos,d)
    raise Exception("No implementado")
#print(hay_casilla_vacia_hacia(tab,Posicion(3,1),NORTE))

def hay_pieza_amiga_vecina(t : Tablero, pos : Posicion) -> bool:
    return hayPiezaAmigaVecina(t,pos)
    raise Exception("No implementado")

def hay_pieza_enemiga_mas_debil_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    return hayPiezaEnemigaMásDébilHacia (t,pos,d)
    raise Exception("No implementado")
#print(hay_pieza_enemiga_mas_debil_hacia(tab,Posicion(4,0),ESTE))


def hay_pieza_enemiga_mas_fuerte_vecina(t : Tablero, pos : Posicion) -> bool:
    return hayPiezaEnemigaMásFuerteVecina (t,pos)
    raise Exception("No implementado")
print(hay_pieza_enemiga_mas_fuerte_vecina(tab,Posicion(0,0)))

def hay_pieza_congelada(t : Tablero, pos : Posicion) -> bool:
    return hayPiezaCongelada (t,pos)
    raise Exception("No implementado")
#print(hay_pieza_congelada(tab, Posicion(3,0)))

#### Ejercicio 4

def puede_realizar_movimiento(j : Juego, m : Movimiento) -> bool:
    raise Exception("No implementado")

#### Ejercicio 5

def activar_trampas(t : Tablero) -> Tablero:
    raise Exception("No implementado")

#### Ejercicio 6

def realizar_movimiento(j : Juego, m : Movimiento) -> Juego:
    raise Exception("No implementado")

#### Ejercicio 7

def hay_ganador_determinado(j : Juego) -> bool:
    raise Exception("No implementado")

def ganador_del_juego(j : Juego) -> Color:
    raise Exception("No implementado")

