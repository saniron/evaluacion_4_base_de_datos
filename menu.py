from math import e
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
            print("2---insertar libro---")
            print("3---insertar varios libros---")
            print("3---actualizar libro---")
            print("4---eliminar libros---")
            print("5---Salir")
            
            elececion=input("Ingrese elecion: ")
            if elececion == "1": 
             libros =conexion.db.libros.find() 
             for libro in libros:
                  ordenarlibro = pd.DataFrame(libro)
                  
                  print(ordenarlibro)
            elif elececion == "2":
                titulo = input("Ingrese el título del libro a buscar: ")
                resultado = conexion.db.libros.find({"titulo": titulo})

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
                if not resultado:
                    print("No se encontró ningún libro con ese título.")
                    
                        
                   
              
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
                    

            elif elececion == "5":
                print("Saliendo del programa...")
                break   
 
           
                

       

            


            



Menu()
