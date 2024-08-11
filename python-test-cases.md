# Casos de Prueba Python para Analizador Sintáctico

## 1. Programa simple: Hola Mundo ✅

### Código Python:
```python
print("Hola Mundo")
```

### Análisis Sintáctico esperado:
```
program:
  print_statement:
    "Hola Mundo"
```

### Árbol Sintáctico esperado:
```
program
└── print_statement
    └── "Hola Mundo"
```

## 2. Asignación y operación aritmética simple ✅

### Código Python:
```python
x = 5
y = 3
z = x + y
print(z)
```

### Análisis Sintáctico esperado:
```
program:
  assignment:
    x
    5
  assignment:
    y
    3
  assignment:
    z
    +:
      x
      y
  print_statement:
    z
```

### Árbol Sintáctico esperado:
```
program
├── assignment
│   ├── x
│   └── 5
├── assignment
│   ├── y
│   └── 3
├── assignment
│   ├── z
│   └── +
│       ├── x
│       └── y
└── print_statement
    └── z
```

## 3. Condicional simple

### Código Python:
```python
x = 10
if x > 5:
    print("x es mayor que 5")
else:
    print("x es menor o igual a 5")
```

### Análisis Sintáctico esperado:
```
program:
  assignment:
    x
    10
  if-else:
    >:
      x
      5
    block:
      print_statement:
        "x es mayor que 5"
    block:
      print_statement:
        "x es menor o igual a 5"
```

### Árbol Sintáctico esperado:
```
program
├── assignment
│   ├── x
│   └── 10
└── if-else
    ├── >
    │   ├── x
    │   └── 5
    ├── block
    │   └── print_statement
    │       └── "x es mayor que 5"
    └── block
        └── print_statement
            └── "x es menor o igual a 5"
```

## 4. Bucle for simple

### Código Python:
```python
for i in range(5):
    print(i)
```

### Análisis Sintáctico esperado:
```
program:
  for:
    i
    function_call:
      range
      5
    block:
      print_statement:
        i
```

### Árbol Sintáctico esperado:
```
program
└── for
    ├── i
    ├── function_call
    │   ├── range
    │   └── 5
    └── block
        └── print_statement
            └── i
```

## 5. Función simple ✅

### Código Python:
```python
def suma(a, b):
    return a + b

resultado = suma(3, 4)
print(resultado)
```

### Análisis Sintáctico esperado:
```
program:
  function_def:
    suma
    parameter_list:
      a
      b
    block:
      return:
        +:
          a
          b
  assignment:
    resultado
    function_call:
      suma
      3
      4
  print_statement:
    resultado
```

### Árbol Sintáctico esperado:
```
program
├── function_def
│   ├── suma
│   ├── parameter_list
│   │   ├── a
│   │   └── b
│   └── block
│       └── return
│           └── +
│               ├── a
│               └── b
├── assignment
│   ├── resultado
│   └── function_call
│       ├── suma
│       ├── 3
│       └── 4
└── print_statement
    └── resultado
```

## 6. Clase simple ✅

### Código Python:
```python
class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

    def saludar(self):
        print(f"Hola, soy {self.nombre}")

p = Persona("Juan")
p.saludar()
```

### Análisis Sintáctico esperado:
```
program:
  class_def:
    Persona
    block:
      function_def:
        __init__
        parameter_list:
          self
          nombre
        block:
          assignment:
            attribute:
              self
              nombre
            nombre
      function_def:
        saludar
        parameter_list:
          self
        block:
          print_statement:
            fstring:
              text: "Hola, soy "
              expression: self.nombre
  assignment:
    p
    function_call:
      Persona
      "Juan"
  expression_statement:
    method_call:
      p
      saludar
```

### Árbol Sintáctico esperado:
```
program
├── class_def
│   ├── Persona
│   └── block
│       ├── function_def
│       │   ├── __init__
│       │   ├── parameter_list
│       │   │   ├── self
│       │   │   └── nombre
│       │   └── block
│       │       └── assignment
│       │           ├── attribute
│       │           │   ├── self
│       │           │   └── nombre
│       │           └── nombre
│       └── function_def
│           ├── saludar
│           ├── parameter_list
│           │   └── self
│           └── block
│               └── print_statement
│                   └── fstring
│                       ├── text: "Hola, soy "
│                       └── expression: self.nombre
├── assignment
│   ├── p
│   └── function_call
│       ├── Persona
│       └── "Juan"
└── expression_statement
    └── method_call
        ├── p
        └── saludar
```

## 7. Decorador simple

### Código Python:
```python
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
```

### Análisis Sintáctico esperado:
```
program:
  function_def:
    mi_decorador
    parameter_list:
      funcion
    block:
      function_def:
        wrapper
        parameter_list:
        block:
          print_statement:
            "Antes de la función"
          expression_statement:
            function_call:
              funcion
          print_statement:
            "Después de la función"
      return:
        wrapper
  decorated_function:
    decorator:
      mi_decorador
    function_def:
      saludo
      parameter_list:
      block:
        print_statement:
          "¡Hola, mundo!"
  expression_statement:
    function_call:
      saludo
```

### Árbol Sintáctico esperado:
```
program
├── function_def
│   ├── mi_decorador
│   ├── parameter_list
│   │   └── funcion
│   └── block
│       ├── function_def
│       │   ├── wrapper
│       │   ├── parameter_list
│       │   └── block
│       │       ├── print_statement
│       │       │   └── "Antes de la función"
│       │       ├── expression_statement
│       │       │   └── function_call
│       │       │       └── funcion
│       │       └── print_statement
│       │           └── "Después de la función"
│       └── return
│           └── wrapper
├── decorated_function
│   ├── decorator
│   │   └── mi_decorador
│   └── function_def
│       ├── saludo
│       ├── parameter_list
│       └── block
│           └── print_statement
│               └── "¡Hola, mundo!"
└── expression_statement
    └── function_call
        └── saludo
```
