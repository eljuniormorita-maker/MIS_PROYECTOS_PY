"""
problema 2: Se gestionan los precios de un menu de restaurante.
El menu se representa como una matriz: [Nombre del producto, Categoria, Precio base].

Requisitos de Desarrollo:
-Matriz: Crear una matriz con al menos 6 productos de diversas categorias.
-Modulos: Se requiere un modulo (funcion) para calcular el precio final de un producto.
-Logica de Negocio: Aplicar un 15% de descuento si el producto cumple con la categoria 
objetivo especifico y su precio base es mayor a un umbral definido.
Mantener el precio base si no se cumplen las condiciones.
-Salida: Mostrar cada producto, su precio base y el precio final con la promocion aplicada.
"""

menu = [
    ["Bandeja Paisa", "Almuerzo",20000],
    ["jugo de Mora", "Bebida", 7000],
    ["Empanada", "Entrada", 3000],
    ["Cafe con Leche", "Bebida", 4500],
    ["Porcion de Torta", "Postre", 8000],
    ["Michelada", "Bebida con Alcohol",7500] 
]
CATEGORIA_OBJETIVO = "Bebida con Alcohol"
PRECIO_MINIMO = 6000


def calcular_precio_final(producto):
    nombre = producto[0]
    categoria = producto[1]
    precio_base = producto[2]

    if categoria == CATEGORIA_OBJETIVO and precio_base >PRECIO_MINIMO:
        descuento = precio_base * 0.15
        precio_final = precio_base - descuento
    else:
        precio_final = precio_base 

    return precio_final

print("\n--- REPORTE DE PRECIOS Y PROMOCIONES---")
for producto in menu:
    precio_final_calculado= calcular_precio_final(producto)
    print(f"producto: {producto[0]} | Categoria: {producto[1]} | precio base: ${producto[2]} | precio final: ${precio_final_calculado}")
