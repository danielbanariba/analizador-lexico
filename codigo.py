# Ejemplo 1: Funciones y condicionales
def es_par(numero):
    if numero % 2 == 0:
        return True
    else:
        return False

print(es_par(4))
print(es_par(7))

# Ejemplo 2: Bucles y listas
numeros = [1, 2, 3, 4, 5]
for num in numeros:
    print(num * 2)

# Ejemplo 3: Comprensión de listas
cuadrados = [x**2 for x in range(10)]
print(cuadrados)

# Ejemplo 4: Manejo de excepciones
try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("Error: División por cero")

# Ejemplo 5: Clases y objetos
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
    
    def saludar(self):
        print(f"Hola, soy {self.nombre} y tengo {self.edad} años.")

persona1 = Persona("Ana", 30)
persona1.saludar()

# Ejemplo 6: Funciones lambda y map
numeros = [1, 2, 3, 4, 5]
duplicados = list(map(lambda x: x * 2, numeros))
print(duplicados)


################################################## No lo reconoce el analizador lexico ##################################################
# Ejemplo 7: Diccionarios
frutas = {"manzana": 2, "banana": 3, "naranja": 1}
for fruta, cantidad in frutas.items():
    print(f"Tengo {cantidad} {fruta}(s)")

##########################################################################################################################################



################################################## No lo reconoce el analizador lexico ##################################################
# Ejemplo 8: Decoradores
def mi_decorador(funcion):
    def wrapper():
        print("Antes de la función")
        funcion()
        print("Después de la función")
    return wrapper

@mi_decorador
def saludo():
    print("¡Hola, mundo!")

saludo()
##########################################################################################################################################


# Ejemplo 9: Generadores
def contador(max):
    n = 0
    while n < max:
        yield n
        n += 1

for num in contador(5):
    print(num)


################################################## No lo reconoce el analizador lexico ##################################################
# Ejemplo 10: f-strings y métodos de cadenas
nombre = "python"
version = 3.9
print(f"{nombre.capitalize()} versión {version}")
##########################################################################################################################################