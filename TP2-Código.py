dic_colores={"rojo": "255 0 0", "azul": "0 0 255", "verde": "0 255 0", "negro": "0 0 0", "blanco": "255 255 255", "amarillo": "255 255 0", "violeta": "255 0 255", "celeste": "0 255 255"}
tamaño_celda_v_predet=10
tamaño_celda_h_predet=10
espejado_v_predet=1
espejado_h_predet=1
dic_colores_predet={0:dic_colores["negro"], 1:dic_colores["rojo"], 2:dic_colores["verde"], 3:dic_colores["azul"]}
condicion="*"


def pedir_tamanio_fractal():
    """Pide el tamaño del fractal. Devuelve el tamaño en forma de tupla. """
    
    tamaño_h=input("Tamaño horizontal del fractal: ")
    tamaño_v=input("Tamaño vertical del fractal: ")
    
    return(int(tamaño_h), int(tamaño_v))

def pedir_coordenadas():
    """Pide coordenadas y se las asigna como clave a un diccionario, con cantidad de arena como valor. Devuelve el diccionario. """
    
    pedir_coord="Coordenada (Ej: 3,6). " + condicion + " para terminar: "
    
    dic_coords={}
    coordenada=input(pedir_coord)
    
    while coordenada!=condicion:
        coordx, coordy=coordenada.split(",")
        coord=(int(coordx), int(coordy))
        arena=input("Cantidad de arena: ")
        dic_coords[coord]=int(arena)
        coordenada=input(pedir_coord)
    
    return dic_coords
    
def pedir_tamanio_celdas():
    """Pide el tamaño de las celdas. Devuelve el tamaño deseado como tupla."""
    
    tamaño_celdas=input("Tamaño de las celdas (Ej: 10x10): ")
    if tamaño_celdas!=condicion:
        tamaño_celda_h, tamaño_celda_v=tamaño_celdas.split("x")
    else:
        tamaño_celda_h=tamaño_celda_h_predet
        tamaño_celda_v=tamaño_celda_v_predet
        
    return(int(tamaño_celda_h), int(tamaño_celda_v))
    
def pedir_espejado():
    """Pide el espejado deseado. Devuelve una tupla con el mismo."""
    
    espejado=input("Espejado (Ej: 2x2): ")
    if espejado!=condicion:
        espejado_h, espejado_v=espejado.split("x")
    else:
        espejado_h=espejado_h_predet
        espejado_v=espejado_v_predet
        
    return(int(espejado_h), int(espejado_v))
    
def pedir_colores():
    """Pide 4 colores al usuario. Devuelve una lista con estos."""
    dic_colores_usuario={}
    print("Ingrese  colores (rojo, azul, verde, negro, blanco, amarillo, violeta, celeste o en RGB): ")
    for n in range(4):
        color=input("Color " + str(n+1) + " : ")
        if color!=condicion:
            if " " not in color:
                dic_colores_usuario[n]=dic_colores[color.lower()]
            else:
                dic_colores_usuario[n]=color
        else:
            return(dic_colores_predet)
    return(dic_colores_usuario)
        

def pedir_datos_obligatorios():
    """Pide al usuario por pantalla parámetros opcionales. Devuelve estos parámetros."""

    print("Complete la siguiente información: ")
    
    tamaño_fractal=pedir_tamanio_fractal()
    dic_coords=pedir_coordenadas()
    nombre_salida=input("Nombre de salida del archivo: ")
    
    return (dic_coords, tamaño_fractal, nombre_salida)
    
def pedir_datos_opcionales():
    """Pide datos opcionales al uruario. Devuelve estos datos. En caso de ingresar "*", devuelve valores por defecto según el campo. """
    
    print("Para los siguientes, ingrese " + condicion + " si desea usar una configuración por defecto:")
    tamaño_celdas=pedir_tamanio_celdas()
    espejado=pedir_espejado()
    colores=pedir_colores()
    
    
    return (tamaño_celdas, espejado, colores)

def celdas_adyacentes(celda, tamaño_fractal):
    """Recive una celda y el tamaño del fractal donde se encuentra y devuelve las coordenadas de las celdas adyacentes. """
    
    tamaño_mapa_h, tamaño_mapa_v= tamaño_fractal
    x,y=celda
    adys=[]
    for n in [-1,1]:
        if tamaño_mapa_h>x+n>-1:
            ady1=(x+n,y)
            adys.append(ady1)
        if tamaño_mapa_v>y+n>-1:
            ady2=(x,y+n)
            adys.append(ady2)
    return adys
    
def siguiente_estado_celdas(dic_coordenadas, tamaño_fractal):
    """Recibe el diccionario de coordenadas de un fractal y devuelve el estado que sigue."""
    tamaño_mapa_h, tamaño_mapa_v= tamaño_fractal
    nuevo_estado={}
    for celda in dic_coordenadas:
        arena=dic_coordenadas[celda]
        nueva_arena=nuevo_estado.get(celda,0)
        nuevo_estado[celda]=nueva_arena+arena
        if arena>=4:
            adyacentes=celdas_adyacentes(celda, tamaño_fractal)
            for ady in adyacentes:
                arena_ady=nuevo_estado.get(ady,0)
                nuevo_estado[ady]=arena_ady+arena//4
            nuevo_estado[celda]+=arena%4-arena
            if nuevo_estado[celda]==0:
                nuevo_estado.pop(celda)
    return nuevo_estado

def sandpile(dic_celdas, tamaño_fractal):
    """Recibe un diccionario de números y el tamaño del fractal al que pertenecen, y reparte sus números según el método de 'sandpiles'. Devuelve la lista de listas al momento de no tener números mayores a 3."""
    
    siguiente=siguiente_estado_celdas(dic_celdas,tamaño_fractal)
    anterior=dic_celdas.copy()
    while siguiente!=anterior:
        anterior=siguiente.copy()
        siguiente=siguiente_estado_celdas(siguiente, tamaño_fractal)
    return siguiente
    
def pasar_a_archivo_espejado(dic_coordenadas, espejado, nombre_salida, tamaño_fractal, tamaño_celdas, dic_colores_usuario):
    """Recive un diccionario con coordenadas, un espejado en forma de tupla, el nombre de salida del archivo, el tamaño de fractas deseado, en forma de tupla, y un diccionario con colores como valores. Guarda el archivo con el fractal espejado."""
    espejado_h, espejado_v=espejado
    tamaño_fractal_h, tamaño_fractal_v=tamaño_fractal
    tamaño_celda_h, tamaño_celda_v=tamaño_celdas
    tamañox=tamaño_fractal_h*tamaño_celda_h*(2**(espejado_h-1))
    tamañoy=tamaño_fractal_v*tamaño_celda_v*(2**(espejado_v-1))
    i=1
    filas_arch=[]
    with open(nombre_salida+".ppm", "w+") as file:
        file.write("P3 " + str(tamañox) + " " + str(tamañoy) + " " + "255 \n ")
        for y in range(tamaño_fractal_v):
            fila=[]
            for x in range(tamaño_fractal_h):
                if (x, y) in dic_coordenadas:
                    pixel=str(dic_colores_usuario[dic_coordenadas[(x, y)]]+" ")*tamaño_celda_h
                else:
                    pixel=(dic_colores_usuario[0]+" ")*tamaño_celda_h
                fila.append(pixel)
            filas_arch.append(fila)
            fila_espejada=espejar_fila(fila, espejado_h)
            file.write((fila_espejada * tamaño_celda_v)+ "\n ")
            
        
        espejar_columnas(filas_arch, espejado_v, espejado_h, file, tamaño_celda_v)

def espejar_fila(fila, espejado_h):
    """Recive una lista con cadena y la muta, agregandole el espejado. Devuelve esta lista en forma de cadena."""
    
    for nro in range(1,espejado_h):
        for elem in fila[::-1]:
            fila.append(elem)
    return (" ".join(fila))

def espejar_columnas(filas, espejado_v, espejado_h, file, tamaño_celda_v):
    """Recibe las filas que se desean espejar verticalmete, el espejado requerido, el archivo donde se guardará y el tamaño en vertical de las celdas. Guarda el archivo espejado en el archivo."""
    
    for nro in range(1,espejado_v):
        filas_arch=filas[:]
        for fila in filas_arch[::-1]:
            file.write(((str(" ".join(fila))+"\n ")*tamaño_celda_v)+"\n ")
            filas.append(fila)

def main():
    """Pide al usuario la información necesaria para armar un fractal, como su tamaño y colores.
    Guarda el archivo en formato ppm del fractal. """
    
    
    dic_coords, tamaño_fractal, nombre_salida=pedir_datos_obligatorios()
    
    tamaño_celdas, espejado, colores=pedir_datos_opcionales()
    
    dic_coordenadas=sandpile(dic_coords, tamaño_fractal)
    
    pasar_a_archivo_espejado(dic_coordenadas, espejado, nombre_salida, tamaño_fractal, tamaño_celdas, colores)
    
main()
    
