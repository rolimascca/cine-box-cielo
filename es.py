import os

def mostrar_estructura_directorio(ruta, nivel=0):
    prefijo = '    ' * nivel  # indentación según nivel
    try:
        with os.scandir(ruta) as it:
            for entrada in it:
                if entrada.is_dir():
                    print(f"{prefijo}📁 {entrada.name}/")
                    mostrar_estructura_directorio(os.path.join(ruta, entrada.name), nivel + 1)
                else:
                    print(f"{prefijo}📄 {entrada.name}")
    except PermissionError:
        print(f"{prefijo}Acceso denegado a {ruta}")

# Cambia 'media' por la ruta que quieres inspeccionar
ruta_media = 'media'

print(f"Estructura del directorio '{ruta_media}':")
mostrar_estructura_directorio(ruta_media)
