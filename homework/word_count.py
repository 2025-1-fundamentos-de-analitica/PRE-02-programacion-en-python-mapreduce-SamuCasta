"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os.path
import time
from itertools import groupby
import string


#
# Escriba la funcion que  genere n copias de los archivos de texto en la
# carpeta files/raw en la carpeta files/input. El nombre de los archivos
# generados debe ser el mismo que el de los archivos originales, pero con
# un sufijo que indique el número de copia. Por ejemplo, si el archivo
# original se llama text0.txt, el archivo generado se llamará text0_1.txt,
# text0_2.txt, etc.
#
def copy_raw_files_to_input_folder(n):
    """Funcion copy_files"""

    # Verifica si la carpeta "files/input" existe, si no, la crea
    if not os.path.exists("files/input"):
        os.makedirs("files/input")

    # Itera sobre todos los archivos en la carpeta "files/raw"
    for file in glob.glob("files/raw/*"):
        # Para cada archivo, genera 'n' copias
        for i in range(1, n + 1):
            # Abre el archivo original en modo lectura con codificación UTF-8
            with open(file, "r", encoding="utf-8") as f:
                # Crea un nuevo archivo en la carpeta "files/input" con un sufijo que indica el número de copia
                with open(
                    f"files/input/{os.path.basename(file).split('.')[0]}_{i}.txt",
                    "w",
                    encoding="utf-8",
                ) as f2:
                    # Escribe el contenido del archivo original en el nuevo archivo
                    f2.write(f.read())


#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo. La función convierte a tuplas
# todas las lineas de cada uno de los archivos. La función es genérica y debe
# leer todos los archivos de folder entregado como parámetro.
#
# Por ejemplo:
#   [
#     ('text0'.txt', 'Analytics is the discovery, inter ...'),
#     ('text0'.txt', 'in data. Especially valuable in ar...').
#     ...
#     ('text2.txt'. 'hypotheses.')
#   ]
#
def load_input(input_directory):
    """Funcion load_input"""

    # Inicializa una lista vacía para almacenar las tuplas (nombre_archivo, línea)
    sequence = []
    
    # Obtiene una lista de todos los archivos en el directorio especificado
    files = glob.glob(f"{input_directory}/*")
    
    # Usa fileinput para leer todos los archivos secuencialmente como si fueran uno solo
    with fileinput.input(files=files) as f:
        # Itera sobre cada línea de todos los archivos
        for line in f:
            # Añade una tupla con el nombre del archivo actual y la línea leída a la lista sequence
            sequence.append((fileinput.filename(), line))
    
    # Retorna la lista de tuplas (nombre_archivo, línea)
    return sequence


#
# Escriba la función line_preprocessing que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). Esta función
# realiza el preprocesamiento de las líneas de texto,
#
def line_preprocessing(sequence):
    """Line Preprocessing"""
    # Itera sobre cada tupla (clave, valor) en la lista de entrada 'sequence'
    sequence = [
        # Para cada tupla, elimina los signos de puntuación del valor (línea de texto)
        # y convierte el texto a minúsculas
        (
            key,  # Mantiene la clave (nombre del archivo)
            value.translate(str.maketrans("", "", string.punctuation))  # Elimina puntuación
            .lower()  # Convierte el texto a minúsculas
        )
        for key, value in sequence  # Desempaqueta cada tupla en clave y valor
    ]
    # Retorna la lista procesada de tuplas (clave, valor)
    return sequence


#
# Escriba una función llamada maper que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). En este caso,
# la clave es cada palabra y el valor es 1, puesto que se está realizando un
# conteo.
#
#   [
#     ('Analytics', 1),
#     ('is', 1),
#     ...
#   ]
#
def mapper(sequence):
    """Mapper"""
    # Retorna una lista de tuplas (palabra, 1)
    # Para cada tupla (clave, valor) en la lista de entrada 'sequence':
    #   - Se ignora la clave (nombre del archivo) con '_'
    #   - Se toma el valor (línea de texto) y se divide en palabras usando split()
    #   - Para cada palabra, se crea una tupla donde la palabra es la clave y el valor es 1
    return [(word, 1) for _, value in sequence for word in value.split()]



#
# Escriba la función shuffle_and_sort que recibe la lista de tuplas entregada
# por el mapper, y retorna una lista con el mismo contenido ordenado por la
# clave.
#
#   [
#     ('Analytics', 1),
#     ('Analytics', 1),
#     ...
#   ]
#
def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    # Ordena la lista de tuplas basada en la clave (primer elemento de cada tupla)
    # Utiliza la función sorted() con una función lambda que especifica que la clave
    # para la ordenación es el primer elemento de cada tupla (x[0]).
    # Esto asegura que todas las tuplas con la misma clave queden juntas en la lista.
    return sorted(sequence, key=lambda x: x[0])


#
# Escriba la función reducer, la cual recibe el resultado de shuffle_and_sort y
# reduce los valores asociados a cada clave sumandolos. Como resultado, por
# ejemplo, la reducción indica cuantas veces aparece la palabra analytics en el
# texto.
#
def reducer(sequence):
    """Reducer"""
    # Inicializa una lista vacía para almacenar los resultados finales
    result = []
    
    # Agrupa las tuplas en la secuencia por la clave (primer elemento de cada tupla)
    # groupby requiere que la secuencia esté ordenada previamente por la clave
    for key, group in groupby(sequence, lambda x: x[0]):
        # Calcula la suma de los valores (segundo elemento de cada tupla) para cada grupo
        # group es un iterador que contiene todas las tuplas con la misma clave
        result.append((key, sum(value for _, value in group)))
    
    # Retorna la lista de tuplas (clave, suma de valores), donde cada clave es única
    return result


#
# Escriba la función create_ouptput_directory que recibe un nombre de
# directorio y lo crea. Si el directorio existe, lo borra
#
def create_ouptput_directory(output_directory):
    """Create Output Directory"""

    # Verifica si el directorio de salida ya existe
    if os.path.exists(output_directory):
        # Si existe, elimina todos los archivos dentro del directorio
        for file in glob.glob(f"{output_directory}/*"):
            os.remove(file)
        # Luego elimina el directorio vacío
        os.rmdir(output_directory)
    
    # Crea un nuevo directorio con el nombre especificado
    os.makedirs(output_directory)


#
# Escriba la función save_output, la cual almacena en un archivo de texto
# llamado part-00000 el resultado del reducer. El archivo debe ser guardado en
# el directorio entregado como parámetro, y que se creo en el paso anterior.
# Adicionalmente, el archivo debe contener una tupla por línea, donde el primer
# elemento es la clave y el segundo el valor. Los elementos de la tupla están
# separados por un tabulador.
#
def save_output(output_directory, sequence):
    """Save Output"""
    # Abre un archivo llamado 'part-00000' en el directorio de salida en modo escritura
    # Si el archivo no existe, se crea automáticamente
    with open(f"{output_directory}/part-00000", "w", encoding="utf-8") as f:
        # Itera sobre cada tupla (clave, valor) en la secuencia proporcionada
        for key, value in sequence:
            # Escribe cada tupla en el archivo como una línea de texto
            # Los elementos de la tupla están separados por un tabulador (\t)
            f.write(f"{key}\t{value}\n")
    # Al finalizar el bloque 'with', el archivo se cierra automáticamente


#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory):
    """Create Marker"""
    # Abre (o crea si no existe) un archivo llamado '_SUCCESS' en el directorio de salida
    # El archivo se abre en modo escritura ('w') con codificación UTF-8
    with open(f"{output_directory}/_SUCCESS", "w", encoding="utf-8") as f:
        # Escribe una cadena vacía en el archivo. Esto crea el archivo como un marcador
        # para indicar que el trabajo se completó correctamente
        f.write("")
    # Al salir del bloque 'with', el archivo se cierra automáticamente


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run_job(input_directory, output_directory):
    """Job"""

    # Carga las líneas de texto de los archivos en el directorio de entrada
    # y las convierte en una lista de tuplas (nombre_archivo, línea)
    sequence = load_input(input_directory)

    # Realiza el preprocesamiento de las líneas de texto, eliminando signos
    # de puntuación y convirtiendo el texto a minúsculas
    sequence = line_preprocessing(sequence)

    # Mapea las líneas de texto a una lista de tuplas (palabra, 1),
    # donde cada palabra es una clave y el valor es 1
    sequence = mapper(sequence)

    # Ordena las tuplas por clave (palabra) para agrupar palabras iguales
    sequence = shuffle_and_sort(sequence)

    # Reduce las tuplas agrupadas sumando los valores asociados a cada clave
    # para obtener el conteo total de cada palabra
    sequence = reducer(sequence)

    # Crea el directorio de salida. Si ya existe, lo elimina y lo vuelve a crear
    create_ouptput_directory(output_directory)

    # Guarda el resultado del reducer en un archivo de texto llamado part-00000
    # dentro del directorio de salida
    save_output(output_directory, sequence)

    # Crea un archivo llamado _SUCCESS en el directorio de salida para indicar
    # que el trabajo se completó correctamente
    create_marker(output_directory)



if __name__ == "__main__":

    copy_raw_files_to_input_folder(n=1000)

    start_time = time.time()

    run_job(
        "files/input",
        "files/output",
    )

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
