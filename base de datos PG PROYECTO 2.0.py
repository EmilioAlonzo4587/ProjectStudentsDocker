#Proyecto Final Progrmacion II

import psycopg2
from psycopg2 import sql
from colorama import Fore, Style, init

# Usamos colorama para darle color a la consola
init()

# Conexión a la base de datos PostgreSQL
def conectar():
    return psycopg2.connect(
        dbname="bdestudiantes",
        user="user",
        password="5033",
        host="localhost",
        port="5432"
    )

# **Definición de Clases**
class Estudiante:
    def __init__(self, carnet, carrera, nombre):
        self.carnet = carnet
        self.carrera = carrera
        self.nombre = nombre

    def mostrar_informacion(self):
        print(f'{self.carnet} - {self.carrera} - {self.nombre}')

class Curso:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

    def mostrar_informacion(self):
        print(f'{self.codigo} - {self.nombre}')

class Nota:
    def __init__(self, id_estudiante, id_curso, nota_parcial1, nota_parcial2, examen_final):
        self.id_estudiante = id_estudiante
        self.id_curso = id_curso
        self.nota_parcial1 = nota_parcial1
        self.nota_parcial2 = nota_parcial2
        self.examen_final = examen_final

# --- Funciones para la Base de Datos ---
def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            carnet VARCHAR(20) PRIMARY KEY,
            carrera VARCHAR(50) NOT NULL,
            nombre VARCHAR(50) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS cursos (
            codigo VARCHAR(20) PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS notas (
            id SERIAL PRIMARY KEY,
            id_estudiante VARCHAR(20) NOT NULL,
            id_curso VARCHAR(20) NOT NULL,
            nota_parcial1 NUMERIC,
            nota_parcial2 NUMERIC,
            examen_final NUMERIC,
            FOREIGN KEY (id_estudiante) REFERENCES estudiantes (carnet),
            FOREIGN KEY (id_curso) REFERENCES cursos (codigo)
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# --- CRUD Funciones para Estudiantes ---
def crear_estudiante(estudiante):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO estudiantes (carnet, carrera, nombre)
        VALUES (%s, %s, %s)
    ''', (estudiante.carnet, estudiante.carrera, estudiante.nombre))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_estudiantes():
    """Obtiene la lista de todos los estudiantes."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM estudiantes')
    estudiantes = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Estudiante(*e) for e in estudiantes]

def buscar_estudiante_por_carnet(carnet):
    """Busca un estudiante por su carnet."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM estudiantes WHERE carnet = %s', (carnet,))
    estudiante = cursor.fetchone()
    cursor.close()
    conn.close()
    return Estudiante(*estudiante) if estudiante else None



def editar_estudiante(carnet, nueva_carrera, nuevo_nombre):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE estudiantes
        SET carrera = %s, nombre = %s
        WHERE carnet = %s
    ''', (nueva_carrera, nuevo_nombre, carnet))
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_estudiante(carnet):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM estudiantes WHERE carnet = %s', (carnet,))
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_estudiante_por_nombre(nombre):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM estudiantes WHERE nombre = %s', (nombre,))
    conn.commit()
    cursor.close()
    conn.close()


def buscar_estudiante_por_nombre(nombre):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM estudiantes WHERE nombre ILIKE %s', (f'%{nombre}%',))
    estudiantes = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Estudiante(*e) for e in estudiantes]

# --- CRUD Funciones para Cursos ---
def crear_curso(curso):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cursos (codigo, nombre)
        VALUES (%s, %s)
    ''', (curso.codigo, curso.nombre))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_cursos():
    """Obtiene la lista de todos los cursos."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cursos')
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Curso(*c) for c in cursos]


def editar_curso(codigo, nuevo_nombre):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE cursos
        SET nombre = %s
        WHERE codigo = %s
    ''', (nuevo_nombre, codigo))
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_curso(codigo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cursos WHERE codigo = %s', (codigo,))
    conn.commit()
    cursor.close()
    conn.close()

def buscar_curso_por_nombre(nombre):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cursos WHERE nombre ILIKE %s', (f'%{nombre}%',))
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Curso(*c) for c in cursos]

# --- CRUD Funciones para Notas ---
def registrar_notas(nota):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO notas (id_estudiante, id_curso, nota_parcial1, nota_parcial2, examen_final)
        VALUES (%s, %s, %s, %s, %s)
    ''', (nota.id_estudiante, nota.id_curso, nota.nota_parcial1, nota.nota_parcial2, nota.examen_final))
    conn.commit()
    cursor.close()
    conn.close()

def imprimir_todas_las_notas():
    """Imprime todas las notas de todos los estudiantes, incluyendo el ID de cada registro."""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT n.id, e.carnet, e.nombre, c.nombre AS curso, n.nota_parcial1, n.nota_parcial2, n.examen_final
        FROM notas n
        JOIN estudiantes e ON n.id_estudiante = e.carnet
        JOIN cursos c ON n.id_curso = c.codigo
    ''')
    
    notas = cursor.fetchall()
    cursor.close()
    conn.close()

    if notas:
        print(Fore.CYAN + "\nNotas de todos los estudiantes:" + Style.RESET_ALL)
        for nota in notas:
            print(f"ID: {nota[0]}, Estudiante: {nota[1]} - {nota[2]}, Curso: {nota[3]}, Parcial 1: {nota[4]}, Parcial 2: {nota[5]}, Examen Final: {nota[6]}")
    else:
        print(Fore.RED + "No se encontraron notas registradas." + Style.RESET_ALL)


def buscar_notas_por_estudiante(carnet):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_curso, nota_parcial1, nota_parcial2, examen_final
        FROM notas
        WHERE id_estudiante = %s
    ''', (carnet,))
    notas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Convertir los resultados en una lista de instancias de Nota
    return [Nota(id_estudiante=carnet, id_curso=nota[0], nota_parcial1=nota[1], nota_parcial2=nota[2], examen_final=nota[3]) for nota in notas]

def eliminar_notas(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notas WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

# Menus para interaccion con el usurio... #
def submenu_estudiantes():
    while True:
        print('\n*** Gestión de Estudiantes ***')
        print('1. Registrar Estudiante')
        print('2. Imprimir lista de estudiantes')
        print('3. Editar Estudiante')
        print('4. Eliminar Estudiante')
        print('5. Buscar Estudiante')
        print('6. Reportes')
        print('9. Regresar al Menú Principal')

        opcion = input('Seleccione una opción: ')

        match opcion:
            case '1':
                carnet = input('Ingrese el carnet: ')
                carrera = input('Ingrese la carrera: ')
                nombre = input('Ingrese el nombre: ')
                estudiante = Estudiante(carnet, carrera, nombre)
                crear_estudiante(estudiante)
                print(Fore.GREEN + 'Estudiante registrado con éxito.' + Style.RESET_ALL)

            case '2':
                estudiantes = obtener_estudiantes()
                if estudiantes:
                    for e in estudiantes:
                        e.mostrar_informacion()
                else:
                    print(Fore.RED + 'No hay estudiantes registrados.' + Style.RESET_ALL)

            case '3':
                carnet = input('Ingrese el carnet del estudiante a editar: ')
                nueva_carrera = input('Ingrese la nueva carrera: ')
                nuevo_nombre = input('Ingrese el nuevo nombre: ')
                editar_estudiante(carnet, nueva_carrera, nuevo_nombre)
                print(Fore.GREEN + 'Estudiante editado con éxito.' + Style.RESET_ALL)

            case '4':
                carnet = input('Ingrese el carnet del estudiante a eliminar: ')
                eliminar_estudiante(carnet)
                print(Fore.GREEN + 'Estudiante eliminado con éxito.' + Style.RESET_ALL)

            case '5':
                nombre = input('Ingrese el nombre del estudiante a buscar: ')
                estudiantes = buscar_estudiante_por_nombre(nombre)
                if estudiantes:
                    for e in estudiantes:
                        e.mostrar_informacion()
                else:
                    print(Fore.RED + 'No se encontraron estudiantes.' + Style.RESET_ALL)

            case '6':
                submenu_reportes()

            case '9':
                break

            case _:
                print(Fore.RED + 'Opción no válida. Intente de nuevo.' + Style.RESET_ALL)

# --- Submenú de Reportes ---
def submenu_reportes():
    while True:
        print('\n*** Reportes de Estudiantes ***')
        print('1. Estudiantes con mejores y peores calificaciones')
        print('2. Promedio de notas por curso y por estudiante')
        print('3. Estudiantes sin notas')
        print('9. Regresar al menú de Estudiantes')

        opcion = input('Seleccione una opción: ')

        match opcion:
            case '1':
                obtener_estudiantes_mejores_y_peores()
            case '2':
                calcular_promedio_por_curso_y_estudiante()
            case '3':
                obtener_estudiantes_sin_notas()
            case '9':
                break
            case _:
                print(Fore.RED + 'Opción no válida. Intente de nuevo.' + Style.RESET_ALL)

# --- Funciones de Reportes ---
def obtener_estudiantes_mejores_y_peores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.carnet, e.nombre, AVG((n.nota_parcial1 + n.nota_parcial2 + n.examen_final) / 3) AS promedio
        FROM estudiantes e
        JOIN notas n ON e.carnet = n.id_estudiante
        GROUP BY e.carnet, e.nombre
        ORDER BY promedio DESC
        LIMIT 5;
    ''')
    mejores = cursor.fetchall()

    cursor.execute('''
        SELECT e.carnet, e.nombre, AVG((n.nota_parcial1 + n.nota_parcial2 + n.examen_final) / 3) AS promedio
        FROM estudiantes e
        JOIN notas n ON e.carnet = n.id_estudiante
        GROUP BY e.carnet, e.nombre
        ORDER BY promedio ASC
        LIMIT 5;
    ''')
    peores = cursor.fetchall()

    cursor.close()
    conn.close()

    print(Fore.CYAN + "\nTop 5 Estudiantes con mejores calificaciones:" + Style.RESET_ALL)
    for est in mejores:
        print(f'{est[0]} - {est[1]} - Promedio: {est[2]:.2f}')

    print(Fore.CYAN + "\nTop 5 Estudiantes con peores calificaciones:" + Style.RESET_ALL)
    for est in peores:
        print(f'{est[0]} - {est[1]} - Promedio: {est[2]:.2f}')

def calcular_promedio_por_curso_y_estudiante():
    conn = conectar()
    cursor = conn.cursor()
    
    # Promedio por curso
    cursor.execute('''
        SELECT c.codigo, c.nombre, AVG((n.nota_parcial1 + n.nota_parcial2 + n.examen_final) / 3) AS promedio_curso
        FROM cursos c
        JOIN notas n ON c.codigo = n.id_curso
        GROUP BY c.codigo, c.nombre;
    ''')
    cursos = cursor.fetchall()
    print(Fore.CYAN + "\nPromedio de notas por curso:" + Style.RESET_ALL)
    for curso in cursos:
        print(f'{curso[0]} - {curso[1]} - Promedio: {curso[2]:.2f}')

    # Promedio por estudiante
    cursor.execute('''
        SELECT e.carnet, e.nombre, AVG((n.nota_parcial1 + n.nota_parcial2 + n.examen_final) / 3) AS promedio_estudiante
        FROM estudiantes e
        JOIN notas n ON e.carnet = n.id_estudiante
        GROUP BY e.carnet, e.nombre;
    ''')
    estudiantes = cursor.fetchall()
    print(Fore.CYAN + "\nPromedio de notas por estudiante:" + Style.RESET_ALL)
    for est in estudiantes:
        print(f'{est[0]} - {est[1]} - Promedio: {est[2]:.2f}')

    cursor.close()
    conn.close()

    
def obtener_estudiantes_sin_notas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.carnet, e.nombre
        FROM estudiantes e
        LEFT JOIN notas n ON e.carnet = n.id_estudiante
        WHERE n.id_estudiante IS NULL
    ''')
    estudiantes_sin_notas = cursor.fetchall()
    cursor.close()
    conn.close()

    if estudiantes_sin_notas:
        print(Fore.CYAN + "\nEstudiantes sin notas registradas:" + Style.RESET_ALL)
        for est in estudiantes_sin_notas:
            print(f'{est[0]} - {est[1]}')
    else:
        print(Fore.RED + "No hay estudiantes sin notas registradas." + Style.RESET_ALL)


def submenu_cursos():
    while True:
        print('\n*** Gestión de Cursos ***')
        print('1. Registrar Curso')
        print('2. imprimir cursos')
        print('3. Editar Curso')
        print('4. Eliminar Curso')
        print('5. Buscar Curso')
        print('9. Regresar al Menú Principal')

        opcion = input('Seleccione una opción: ')

        match opcion:
            case '1':
                codigo = input('Ingrese el código del curso: ')
                nombre = input('Ingrese el nombre del curso: ')
                curso = Curso(codigo, nombre)
                crear_curso(curso)
                print(Fore.GREEN + 'Curso registrado con éxito.' + Style.RESET_ALL)
            case '2':
                cursos = obtener_cursos()
                if cursos:
                    for c in cursos:
                        c.mostrar_informacion()
                else:
                    print(Fore.RED + 'No hay cursos registrados.' + Style.RESET_ALL)

            case '3':
                codigo = input('Ingrese el código del curso a editar: ')
                nuevo_nombre = input('Ingrese el nuevo nombre del curso: ')
                editar_curso(codigo, nuevo_nombre)
                print(Fore.GREEN + 'Curso editado con éxito.' + Style.RESET_ALL)
            case '4':
                codigo = input('Ingrese el código del curso a eliminar: ')
                eliminar_curso(codigo)
                print(Fore.GREEN + 'Curso eliminado con éxito.' + Style.RESET_ALL)
            case '5':
                nombre = input('Ingrese el nombre del curso a buscar: ')
                cursos = buscar_curso_por_nombre(nombre)
                if cursos:
                    for c in cursos:
                        c.mostrar_informacion()
                else:
                    print(Fore.RED + 'No se encontraron cursos.' + Style.RESET_ALL)
            case '9':
                break
            case _:
                print(Fore.RED + 'Opción no válida. Intente de nuevo.' + Style.RESET_ALL)

def submenu_notas():
    while True:
        print('\n*** Registro de Notas ***')
        print('1. Registrar Notas')
        print('2. imprimir Notas')
        print('3. Eliminar Notas')
        print('4. Buscar Notas por Estudiante')
        print('9. Regresar al Menú Principal')

        opcion = input('Seleccione una opción: ')

        match opcion:
            case '1':
                id_estudiante = input('Ingrese el carnet del estudiante: ')
                id_curso = input('Ingrese el código del curso: ')
                nota_parcial1 = float(input('Ingrese la nota del primer parcial: '))
                nota_parcial2 = float(input('Ingrese la nota del segundo parcial: '))
                examen_final = float(input('Ingrese la nota del examen final: '))
                nota = Nota(id_estudiante, id_curso, nota_parcial1, nota_parcial2, examen_final)
                registrar_notas(nota)
                print(Fore.GREEN + 'Notas registradas con éxito.' + Style.RESET_ALL)

            case '2':
                imprimir_todas_las_notas()
            case '3':
                id = input('Ingrese el ID de las notas a eliminar: ')
                eliminar_notas(id)
                print(Fore.GREEN + 'Notas eliminadas con éxito.' + Style.RESET_ALL)
            case '4':
                carnet = input('Ingrese el carnet del estudiante: ')
                notas = buscar_notas_por_estudiante(carnet)
                if notas:
                    for n in notas:
                        print(f'Curso: {n.id_curso}, Parcial 1: {n.nota_parcial1}, Parcial 2: {n.nota_parcial2}, Examen Final: {n.examen_final}')
                else:
                    print(Fore.RED + 'No se encontraron notas para el estudiante.' + Style.RESET_ALL)
            case '9':
                break
            case _:
                print(Fore.RED + 'Opción no válida. Intente de nuevo.' + Style.RESET_ALL)

# --- Menú Principal ---
def menu_principal():
    while True:
        print('\n*** Menú Principal ***')
        print('1. Gestión de Estudiantes')
        print('2. Gestión de Cursos')
        print('3. Registro de Notas')
        print('9. Salir')
        
        opcion = input('Seleccione una opción: ')
        
        match opcion:
            case '1':
                submenu_estudiantes()
            case '2':
                submenu_cursos()
            case '3':
                submenu_notas()
            case '9':
                print('Saliendo del programa...')
                break
            case _:
                print(Fore.RED + 'Opción no válida. Intente de nuevo.' + Style.RESET_ALL)

if __name__ == '__main__':
    crear_tablas()
    menu_principal()
