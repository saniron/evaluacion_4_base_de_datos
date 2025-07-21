
from wsgiref.validate import validator
import pymongo
import pymongo.errors
import pandas as pd

class Conexion:
    def __init__(self, uri="mongodb://localhost:27017", db_name="LibreriaDB"):
        try:
            self.client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[db_name]
            # Forzar verificación de conexión
            self.client.server_info()
            self.estado = True
        except pymongo.errors.ServerSelectionTimeoutError as error:
            print("Error de conexión:", error)
            self.estado = False

# Usar la clase y verificar el estado
conexion = Conexion("mongodb+srv://seba:Cx9484chxj.@cluster0.sn3zuqv.mongodb.net/", "Libreria")

if conexion.estado:
    print("✅ Conexión exitosa a la base de datos MongoDB Atlas")
else:
    print("❌ Error al conectar a la base de datos MongoDB")
class Menu:
    def __init__(self):    
        while True:
            print("1---Listado de libros...")
            print("2---buscar libro---")
            print("3---insertar libro---")
            print("4---insertar varios libros---")
            print("6---actualizar libro---")
            print("5---actualizar varios libros---")
            print("7---eliminar libros---")
            print("8---eliminar varios libros---")
            print("9---Salir")
            
            elececion=input("Ingrese elecion: ")
            if elececion == "1": 
             libros =conexion.db.libros.find() 
             for libro in libros:
                  ordenarlibro = pd.DataFrame(libro)
                  
                  print(ordenarlibro)
            elif elececion == "2":
                campo = input("Ingrese el campo a buscar (titulo, autor, genero, editorial): ").strip().lower()
                valor = input(f"Ingrese el {campo} a buscar: ")
                resultado = conexion.db.libros.find({campo: {"$regex": f"^{valor}$", "$options": "i"}})
                encontrado = False
                for libro in resultado:
                    print("📘 Libro encontrado:")
                    print(f"Título: {libro['titulo']}")
                    print(f"Autor: {libro['autor']['nombre']} {libro['autor']['apellido']}")
                    print(f"Año: {libro['año_publicacion']}")
                    print(f"Género: {libro['genero']}")
                    print(f"Editorial: {libro['editorial']}")
                    print(f"Stock: {libro['stock']} unidades")
                    print(f"Precio: ${libro['precio']}")
                    encontrado = True

                if not encontrado:
                    print("❌ No se encontró ningún libro con ese título.")
       
                    
                        
                   
              
            elif elececion == "3":
                print("Ingrese datos del libro")
                titulo = input("Ingrese el título del libro: ")
                año_publicacion = int(input("Año de publicación: "))
                genero = input("Género: ")
                editorial = input("Editorial: ")
                stock = int(input("Stock disponible: "))
                precio = int(input("Precio del libro (sin $): "))
                formato = input("Formato (ej: Tapa blanda): ")
    
                print("--- Datos del autor ---")
                nombre_autor = input("Nombre del autor: ")
                apellido_autor = input("Apellido del autor: ")
                nacionalidad = input("Nacionalidad: ")
                fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")



                libro = {
                    
                    "titulo": titulo,
                    "autor": {
                        "nombre": nombre_autor,
                        "apellido": apellido_autor,
                        "nacionalidad": nacionalidad,
                        "fecha_nacimiento": fecha_nacimiento
                    },
                    "año_publicacion": año_publicacion,
                    "genero": genero,
                    "editorial": editorial,
                    "stock": stock,
                    "precio": precio,
                    "formato": formato
                }
                conexion.db.libros.insert_one(libro)
                print("✅ Libro insertado exitosamente.")
            elif elececion == "4":
                print("cuantos libros desea insertar?")
                cantidad = int(input("Ingrese la cantidad de libros a insertar: "))
                libros = []
                if cantidad <= 0:
                    print("❌ La cantidad debe ser mayor a 0.")
                    continue
                for i in range(cantidad):
                    print(f"--- Libro {i + 1} ---")
                    print("Ingrese los datos del libro (deje el título vacío para terminar):")
                    titulo = input("Título del libro: ")
                    if not titulo:
                        break
                    año_publicacion = int(input("Año de publicación: "))
                    genero = input("Género: ")
                    editorial = input("Editorial: ")
                    stock = int(input("Stock disponible: "))
                    precio = int(input("Precio del libro (sin $): "))
                    formato = input("Formato (ej: Tapa blanda): ")

                    print("--- Datos del autor ---")
                    nombre_autor = input("Nombre del autor: ")
                    apellido_autor = input("Apellido del autor: ")
                    nacionalidad = input("Nacionalidad: ")
                    fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")

                    libro = {
                        "titulo": titulo,
                        "autor": {
                            "nombre": nombre_autor,
                            "apellido": apellido_autor,
                            "nacionalidad": nacionalidad,
                            "fecha_nacimiento": fecha_nacimiento
                        },
                        "año_publicacion": año_publicacion,
                        "genero": genero,
                        "editorial": editorial,
                        "stock": stock,
                        "precio": precio,
                        "formato": formato
                    }
                    libros.append(libro)

                if libros:
                    conexion.db.libros.insert_many(libros)
                    print(f"✅ Se han insertado {len(libros)} libros exitosamente.")
                else:
                    print("❌ No se han insertado libros.")
            elif elececion == "5":
                titulo = input("Ingrese el título del libro a actualizar: ")
                libro = conexion.db.libros.find_one({"titulo": {"$regex": f"^{titulo}$", "$options": "i"}})
                if libro:
                    print("Libro encontrado:")
                    print(f"Título: {libro['titulo']}")
                    print(f"Autor: {libro['autor']['nombre']} {libro['autor']['apellido']}")
                    print(f"Año: {libro['año_publicacion']}")
                    print(f"Género: {libro['genero']}")
                    print(f"Editorial: {libro['editorial']}")
                    print(f"Stock: {libro['stock']} unidades")
                    print(f"Precio: ${libro['precio']}")

                    nuevo_titulo = input("Nuevo título (dejar vacío para no cambiar): ")
                    nuevo_año = input("Nuevo año de publicación (dejar vacío para no cambiar): ")
                    nuevo_genero = input("Nuevo género (dejar vacío para no cambiar): ")
                    nueva_editorial = input("Nueva editorial (dejar vacío para no cambiar): ")
                    nuevo_stock = input("Nuevo stock (dejar vacío para no cambiar): ")
                    nuevo_precio = input("Nuevo precio (dejar vacío para no cambiar): ")

                    actualizaciones = {}
                    if nuevo_titulo:
                        actualizaciones["titulo"] = nuevo_titulo
                    if nuevo_año:
                        actualizaciones["año_publicacion"] = int(nuevo_año)
                    if nuevo_genero:
                        actualizaciones["genero"] = nuevo_genero
                    if nueva_editorial:
                        actualizaciones["editorial"] = nueva_editorial
                    if nuevo_stock:
                        actualizaciones["stock"] = int(nuevo_stock)
                    if nuevo_precio:
                        actualizaciones["precio"] = int(nuevo_precio)

                    if actualizaciones:
                        conexion.db.libros.update_one({"_id": libro["_id"]}, {"$set": actualizaciones})
                        print("✅ Libro actualizado exitosamente.")
                    else:
                        print("❌ No se realizaron cambios.")
                else:
                    print("❌ No se encontró ningún libro con ese título.")
            elif elececion == "7":
                campo = input("Ingrese el campo a buscar (titulo, autor, genero, editorial): ").strip().lower()
                valor = input(f"Ingrese el {campo} a buscar: ")
                resultado = conexion.db.libros.find({campo: {"$regex": f"^{valor}$", "$options": "i"}})
                encontrado = False
                for libro in resultado:
                    print("📘 Libro encontrado:")
                    print(f"Título: {libro['titulo']}")
                    print(f"Autor: {libro['autor']['nombre']} {libro['autor']['apellido']}")
                    print(f"Año: {libro['año_publicacion']}")
                    print(f"Género: {libro['genero']}")
                    print(f"Editorial: {libro['editorial']}")
                    print(f"Stock: {libro['stock']} unidades")
                    print(f"Precio: ${libro['precio']}")
                    encontrado = True

                if not encontrado:
                    print("❌ No se encontró ningún libro con ese título.")
                else:
                    confirmacion = input("¿Desea eliminar este libro? (s/n): ").strip().lower()
                    if confirmacion == 's':
                        conexion.db.libros.delete_one({"_id": libro["_id"]})
                        print("✅ Libro eliminado exitosamente.")   
            elif elececion == "9":
                print("Saliendo del programa...")
                break   
 
           
                

       

            


            



Menu()