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


# ------ LECTURA DEL ARCHIVO, GENERACION DE LISTA CON INFORMACION A AGREGAR Y REEMPLAZO EN ARCHIVO CSV ------
def leerYmodificar(file_path, funcion, string):
    """ Obtiene el path, tipo de funcion y nombre nuevo a agregar en el encabezado por parametros, agrega el encabezad
        y, leyendo el archivo y aplicandole la funcion especifica, genera una lista de hileras con informacion modificada. Luego retorna por
        separado la lista de hileras y el encabezado en dos variables """
    
    with file_path.open('r') as file:
        reader = csv.DictReader(file, delimiter=";")
        # AGREGO NUEVO CAMPO EN COLUMNA
        fieldnames = reader.fieldnames + [string]

        # CREO UNA LISTA VACIA CON TODAS LAS ROWS MODIFICADAS
        filas_nuevas = []
        for row in reader:
            fila = funcion(row)
            filas_nuevas.append(fila)
        
    return filas_nuevas, fieldnames

def reemplazar(file_path,funcion,string):
    """ Obtiene el path, tipo de funcion y nombre nuevo a agregar en el encabezado por parametros, llama a una funcion y obtiene la informacion
     de hileras y encabezado modificadas y las escribe en el archivo respectivamente """
    
    filas_modificadas, fieldnames = leerYmodificar(file_path, funcion, string)
    with file_path.open('w') as procesados_file:
        writer = csv.DictWriter(procesados_file, fieldnames= fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(filas_modificadas)


# UNO LOS ARCHIVOS DE INDIVIDUOS Y HOGARES EN .CSV RESPECTIVAMENTE
unir_archivos(individuos_path, procesados_path / "individuos.csv")
unir_archivos(hogares_path, procesados_path / "hogares.csv")

# AGREGAR Y REEMPLAZAR COLUMNAS A LOS ARCHIVOS INDIVIDUOS
reemplazar(procesados_path / "individuos.csv",agregar_CH04,"CH04_str")
reemplazar(procesados_path / "individuos.csv",agregar_nivel_ED,"NIVEL_ED_str")
reemplazar(procesados_path / "individuos.csv",agregar_condicion_laboral,"CONDICION_LABORAL")
reemplazar(procesados_path / "individuos.csv",agregar_universitario,"UNIVERSITARIO")


# AGREGAR Y REEMPLAZAR COLUMNAS A LOS ARCHIVOS HOGARES
reemplazar(procesados_path / "hogares.csv",agregar_tipo_hogar,"TIPO_HOGAR")
reemplazar(procesados_path / "hogares.csv",agregar_material_techumbre,"MATERIAL_TECHUMBRE")
reemplazar(procesados_path / "hogares.csv",agregar_densidad_hogar,"DENSIDAD_HOGAR")