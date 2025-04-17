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


def traducir_nivel_ed(fila):
    valor = fila['NIVEL_ED']
    if valor == '1':
        return "Primario incompleto"
    elif valor == '2':
        return "Primario completo"
    elif valor == '3':
        return "Secundario incompleto"
    elif valor == '4':
        return "Secundario completo"
    elif valor in ['5', '6']:
        return "Superior o universitario"
    else:
        return "Sin informacion"

def agregar_universitario(row):
    if row['CH06'] >= '18':
        if row['NIVEL_ED'] == '6':
            row['UNIVERSITARIO'] = '1 '
        else:
            row['UNIVERSITARIO'] = '0'
    else:
        row['UNIVERSITARIO'] = '2'
    return row

def traducir_ch04 (fila):
    if fila['CH04'] == '1':
        return 'Masculino'
    else:
        return'Femenino'

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

reemplazar(procesados_path,traducir_ch04,"CH04_str")
reemplazar(procesados_path,traducir_nivel_ed,"NIVEL_ED_str")