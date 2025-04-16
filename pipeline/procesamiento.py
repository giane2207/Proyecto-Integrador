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

def agregar_fila_CH04 (row):
    if row['CH04'] == '1':
        row['CH04_str'] = 'Varon'
    else:
        row['CH04_str'] = 'Mujer'
    return row

with procesados_path.open('r') as procesados_file:
    reader = csv.DictReader(procesados_file, delimiter=";")
    # AGREGO NUEVO CAMPO EN COLUMNA
    fieldnames = reader.fieldnames + ['CH04_str']

    # CREO UNA LISTA VACIA CON TODAS LAS ROWS MODIFICADAS
    filas_nuevas = []
    for row in reader:
        fila = agregar_fila_CH04(row)
        filas_nuevas.append(fila)


with procesados_path.open('w') as procesados_file:
    writer = csv.DictWriter(procesados_file, fieldnames= fieldnames, delimiter=';')
    writer.writeheader()
    # ESCRIBO EN EL ARCHIVO LA NUEVA COLUMNA CON LOS DATOS QUE AGREGUE
    writer.writerows(filas_nuevas)