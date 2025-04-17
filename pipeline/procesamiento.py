from pathlib import Path
import csv

# PATH DONDE ESTAN LOS ARCHIVOS
individuos_path = Path("data/individuos")
hogares_path = Path("data/hogares")
# PATH A LA CARPETA DE SALIDA
procesados_path = Path("data/procesados/individuos_procesados.csv")

def unir_archivos(origen_path, salida_path):
    """crea un archivo unificado con todos los archivos contenidos en la ruta origen
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

# unir los archivos de individuos y hogares en archivos csv unificados
unir_archivos(individuos_path, procesados_path / "individuos.csv")
unir_archivos(hogares_path, procesados_path / "hogares.csv")


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