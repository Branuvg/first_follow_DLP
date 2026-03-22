# FIRST y FOLLOW — Calculador de Conjuntos

Un programa en Python que lee gramáticas desde archivos de texto y calcula los conjuntos FIRST y FOLLOW, además de verificar si una gramática es LL(1).

## Descripción

Este programa implementa los algoritmos para calcular los conjuntos **FIRST** y **FOLLOW** de una gramática libre de contexto, junto con la detección de conflictos LL(1). Es una herramienta útil para el análisis de compiladores y procesadores de lenguaje.

### Características

- Cálculo automático de conjuntos FIRST y FOLLOW
- Detección de conflictos LL(1)
- Soporte para múltiples archivos de gramática
- Manejo de epsilon (ε)
- Formato flexible de entrada
- Reportes detallados de resultados

## Instalación y Requisitos

### Requisitos Previos

- Python 3.6 o superior
- No se requieren dependencias externas (solo librerías estándar)

### Instalación

1. Clona o descarga este repositorio
2. Asegúrate de tener Python instalado
3. No se necesita instalación adicional

## Estructura del Proyecto

```
pruebas_hm/
├── first_follow.py                    # Programa principal
├── gramatica_clase.txt               # Gramática de ejemplo (clase)
├── gramatica_aritmetica_ambigua.txt  # Gramática ambigua (conflictos)
├── gramatica_lenguaje_simple.txt     # Gramática de lenguaje simple
└── README.md                         # Este archivo
```

## Formato del Archivo de Gramática

Los archivos de gramática deben seguir este formato:

### Sintaxis Básica

```
# Líneas que comienzan con # son comentarios
START <simbolo_inicial>              # Define el símbolo inicial

<NoTerminal> -> <simbolo1> <simbolo2> | <alternativa2> | <alternativa3>
```

### Reglas Importantes

1. **Símbolo Inicial**: Use `START <nombre>` para definir el símbolo inicial
2. **Comentarios**: Las líneas que comienzan con `#` son ignoradas
3. **Epsilon**: Use `eps`, `epsilon` o `ε` para representar epsilon
4. **No Terminales con Prima**: Use comilla simple (ej: `E'`)
5. **Separadores**: Use `->` para las producciones y `|` para alternativas
6. **Espacios**: Use espacios para separar símbolos

### Ejemplo Completo

```txt
# Gramática de expresiones aritméticas
START E

E  -> T E'
E' -> + T E' | eps
T  -> F T'
T' -> * F T' | eps
F  -> ( E ) | id
```

## Cómo Usar el Programa

### Ejecución Básica

```bash
# Especificar un archivo de gramática personalizado
python first_follow.py mi_gramatica.txt
```

### Tips para Buenas Gramáticas

- Define siempre un símbolo inicial con `START`
- Usa nombres descriptivos para no terminales
- Documenta con comentarios
- Verifica que no haya recursión izquierda directa
- Prueba con diferentes entradas