from pathlib import Path
import csv

# PATH DONDE ESTAN LOS ARCHIVOS
individuos_path = Path("data/individuos")
hogares_path = Path("data/hogares")
# PATH A LA CARPETA DE SALIDA
procesados_path = Path("data/procesados/individuos_procesados.csv")



# PROCESADOS_FILE = NOMBRE DEL ARCHIVO FINAL
# ARCHIVO = ITERADOR SOBRE LOS TRIMESTRES DENTRO DE INDIVIDUAL_PATH
# FILE = NOMBRE DEL ARCHIVO QUE ABRIS
writer = None
with procesados_path.open('w') as procesados_file:
    for archivo in individuos_path.glob("*.txt"):
        with archivo.open('r') as file:
            reader = csv.DictReader(file, delimiter = ";")

            # SI WRITER NO TIENE NADA, ESCRIBE EL HEADER
            if writer is None:
                writer = csv.DictWriter(procesados_file, fieldnames= reader.fieldnames, delimiter= ';')
                writer.writeheader()
            
            # ESCRIBE TODAS LAS ROWS
            for row in reader:
                writer.writerow(row)


def nivel_ED(row):
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

def agregar_fila_CH04 (row):
    if row['CH04'] == '1':
        row['CH04_str'] = 'Varon'
    else:
        row['CH04_str'] = 'Mujer'
    return row

def leerYmodificar(file_path, funcion, string):
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
    filas_modificadas, fieldnames = leerYmodificar(file_path, funcion, string)
    with file_path.open('w') as procesados_file:
        writer = csv.DictWriter(procesados_file, fieldnames= fieldnames, delimiter=';')
        writer.writeheader()
        # ESCRIBO EN EL ARCHIVO LA NUEVA COLUMNA CON LOS DATOS QUE AGREGUE
        writer.writerows(filas_modificadas)

reemplazar(procesados_path,agregar_fila_CH04,"CH04_str")
reemplazar(procesados_path,nivel_ED,"NIVEL_ED_str")