from pathlib import Path
import csv
import os

# PATH DONDE ESTAN LOS ARCHIVOS
individuos_path = Path("data/individuos")
hogares_path = Path("data/hogares")

# PATH A LA CARPETA DE SALIDA
procesados_path = Path("data/procesados")

def unir_archivos(origen_path, salida_path):
    """Crea un archivo unificado con todos los archivos contenidos en la ruta origen
    y lo guarda en la ruta de salida"""

    # se obtienen todos los nombres de archivos que hay en la carpeta origen
    archivos = os.listdir(origen_path)

    # se utiliza para asegurarse de escribir los encabezados una sola vez
    encabezado_escrito = False  
    
    with open(salida_path, 'w', encoding='utf-8') as salida:
        writer = None

        # se recorren todos los archivos de la carpeta origen
        for archivo in archivos:

            with open(origen_path / archivo, 'r', encoding='utf-8') as entrada:
                reader = csv.reader(entrada, delimiter=';')

                # se obtiene la primera fila (encabezado) del archivo
                encabezado = next(reader)

                # se escribe el encabezado una sola vez en el archivo final
                if not encabezado_escrito:
                    writer = csv.writer(salida, delimiter=';')
                    writer.writerow(encabezado)
                    encabezado_escrito = True

                for fila in reader:
                    writer.writerow(fila)

# ------------- FUNCIONES GENERALES INDIVIDUOS ------------------

def agregar_CH04 (row):
    """ Traduce 1 y 2 a Varon y Mujer en nueva columna respectivamente """

    if row['CH04'] == '1':
        row['CH04_str'] = 'Varon'
    else:
        row['CH04_str'] = 'Mujer'
    return row

def agregar_nivel_ED(row):
    """ Traduce valores numericos a una nueva columna en cadena """

    if row['NIVEL_ED'] == '1':
        row['NIVEL_ED_str'] = 'Primario incompleto'
    elif row['NIVEL_ED'] == '2':
        row['NIVEL_ED_str'] = 'Primario completo'
    elif row['NIVEL_ED'] == '3':
        row['NIVEL_ED_str'] = 'Secundario incompleto'    
    elif row['NIVEL_ED'] == '4':
        row['NIVEL_ED_str'] = 'Secundario completo'    
    elif row['NIVEL_ED'] == '5' or row['NIVEL_ED'] == '6' :
        row['NIVEL_ED_str'] = 'Primario incompleto'
    elif row['NIVEL_ED'] == '7' or row['NIVEL_ED'] == '9' :
        row['NIVEL_ED_str'] = 'Sin informacion'
    return row

def agregar_condicion_laboral(row):
    """ Dependiendo la condicion laboral se traduce en una nueva columna """

    valorEstado = row['ESTADO']
    valorCategoria = row['CAT_OCUP']

    if valorEstado == '1' and valorCategoria in ['1', '2']:
        row['CONDICION_LABORAL'] = 'Ocupado autonomo'
    elif valorEstado == '1' and valorCategoria in ['3', '4', '9']:
        row['CONDICION_LABORAL'] = 'Ocupado dependiente'
    elif valorEstado == '2':
        row['CONDICION_LABORAL'] = 'Desocupado'
    elif valorEstado == '3':
        row['CONDICION_LABORAL'] = 'Inactivo'
    else:
        row['CONDICION_LABORAL'] = 'Fuera de categoria/sin informacion'
    
    return row

def agregar_universitario(row):
    """ Revisa si es mayor de edad y si termino la universidad o no, traduciendolo a una nueva columna """

    if row['CH06'] >= '18':
        if row['NIVEL_ED'] == '6':
            row['UNIVERSITARIO'] = '1'
        else:
            row['UNIVERSITARIO'] = '0'
    else:
        row['UNIVERSITARIO'] = '2'

    return row


# ------------- FUNCIONES GENERALES HOGARES ------------------

def agregar_tipo_hogar(row):
    """ Revisa la cantidad de habitantes que tiene el hogar, traduciendolo a una nueva columna """

    habitantes = row['IX_TOT']
    if habitantes == '1':
        row['TIPO_HOGAR'] = 'Unipersonal'
    elif '2' <= habitantes <= '4':
        row['TIPO_HOGAR'] = 'Nuclear'
    else:
        row['TIPO_HOGAR'] = 'Extendido'

    return row


def agregar_material_techumbre(row):
    """ Se fija el tipo de material que tiene el hogar, traduciendolo a una nueva columna """

    # MATERIAL (IV4 EN EL ARCHIVO), QUITO ESPACIOS INNECESARIOS DEL DATO DEL ARCHIVO
    material = row['IV4'].strip()

    if '1' <= material <= '4':
        row['MATERIAL_TECHUMBRE'] = 'Material durable'
    elif '5' <= material <= '7':
        row['MATERIAL_TECHUMBRE'] = 'Material precario'
    elif material == '9':
        row['MATERIAL_TECHUMBRE'] = 'No Aplica'            

    return row

def agregar_densidad_hogar(row):
    """ Revisa columnas de total de personas y habitaciones, obtiene la densidad diviendolos y traduce el resultado
        a una nueva columna """
    
    # HAY QUE DIVIDIR PERSONAS/HABITACIONES
    # iv2 TIENE EL TOTAL DE HABITACIONES y ix_tot EL DE PERSONAS, PASO AMBOS A INT
    total = int(row['IX_TOT'])
    rooms = int(row['IV2'])
    densidad = total/rooms

    if densidad < 1:
        row['DENSIDAD_HOGAR'] = 'Bajo'
    elif 1 <= densidad <= 2:
        row['DENSIDAD_HOGAR'] = 'Medio'
    elif densidad > 2:
        row['DENSIDAD_HOGAR'] ='Alto'
         
    return row

# ------ LECTURA DEL ARCHIVO ORIGINAL, APLICACION DE FUNCIONES PARA GENERAR LISTA DE HILERAS CON INFORMACION MODIFICADA, REESCRITURA EN ARCHIVO .CSV ------

def reemplazar(file_path,funciones,cadenas):
    """ Obtiene el path del archivo , lista de funciones y lista de encabezados por parametros.
        Ambas listas deben coincidir en orden ya que son 1-1 
        Agrega todos los encabezados y aplica cada funcion especifica a las hileras. 
        Genera una lista de hileras con informacion modificada que luego se escribe en el archivo, modificando el original """
    
    with file_path.open('r') as file:
        reader = csv.DictReader(file, delimiter=';')
        # AGREGO TODOS LOS NUEVOS ENCABEZADOS
        fieldnames = reader.fieldnames + cadenas

        # POR CADA FILA, APLICO FUNCION DE LA LISTA DE FUNCIONES Y AGREGO EL NUEVO CONTENIDO EN FILAS_NUEVAS
        filas_nuevas = []
        for row in reader:
            for funcion in funciones:
                row = funcion(row)
            filas_nuevas.append(row)

    with file_path.open('w') as procesados_file:
        writer = csv.DictWriter(procesados_file,fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(filas_nuevas)

# UNO LOS ARCHIVOS DE INDIVIDUOS Y HOGARES EN .CSV RESPECTIVAMENTE
unir_archivos(individuos_path, procesados_path / "individuos.csv")
unir_archivos(hogares_path, procesados_path / "hogares.csv")

# CREO LISTA DE FUNCIONES Y DE ENCABEZADOS PARA MODIFICAR ARCHIVO DE INDIVIDUOS/HOGARES
funciones_individuos = [agregar_CH04,agregar_nivel_ED,agregar_condicion_laboral,agregar_universitario]
nombres_individuos =["CH04_str","NIVEL_ED_str", "CONDICION_LABORAL","UNIVERSITARIO"]

funciones_hogares = [agregar_tipo_hogar,agregar_material_techumbre,agregar_densidad_hogar]
nombres_hogares =["TIPO_HOGAR","MATERIAL_TECHUMBRE", "DENSIDAD_HOGAR"]

reemplazar(procesados_path / "individuos.csv", funciones_individuos, nombres_individuos)
reemplazar(procesados_path / "hogares.csv", funciones_hogares, nombres_hogares)