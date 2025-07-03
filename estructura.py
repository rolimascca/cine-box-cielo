import os

def print_tree(startpath, prefix=''):
    try:
        entries = sorted(os.listdir(startpath))
    except FileNotFoundError:
        print(f"❌ Error: La ruta '{startpath}' no existe.")
        return
    except PermissionError:
        print(f"🔒 Error: Sin permiso para acceder a '{startpath}'.")
        return

    # Separar carpetas y archivos (de cualquier tipo)
    dirs = [e for e in entries if os.path.isdir(os.path.join(startpath, e))]
    files = [e for e in entries if os.path.isfile(os.path.join(startpath, e))]

    all_entries = dirs + files  # Primero carpetas, luego archivos

    for i, entry in enumerate(all_entries):
        path = os.path.join(startpath, entry)
        connector = '└── ' if i == len(all_entries) - 1 else '├── '
        print(prefix + connector + entry)

        # Recursión solo para carpetas
        if os.path.isdir(path):
            extension = '    ' if i == len(all_entries) - 1 else '│   '
            print_tree(path, prefix + extension)

if __name__ == "__main__":
    project_root = r"C:\Users\Rolando\mi_proyecto"  # Cambia por la ruta que necesites
    print(f"\n📁 Árbol de carpetas y archivos en: {project_root}\n")
    print_tree(project_root)
