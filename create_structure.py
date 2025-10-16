"""
Script para crear la estructura completa del proyecto
"""

import os
from pathlib import Path

def create_project_structure():
    """Crea toda la estructura de carpetas y archivos base"""
    
    # Definir estructura
    structure = {
        'data': ['raw', 'processed', 'cache'],
        'src': {
            'data': [],
            'analysis': [],
            'visualization': [],
            'utils': []
        },
        'streamlit_app': {
            'pages': []
        },
        'docs': ['images'],
        'notebooks': [],
        'tests': []
    }
    
    def create_folders(base_path, struct):
        """Función recursiva para crear carpetas"""
        for folder, subfolders in struct.items():
            folder_path = base_path / folder
            folder_path.mkdir(exist_ok=True)
            print(f"✅ Creada: {folder_path}")
            
            # Crear __init__.py en carpetas de Python
            if folder in ['src', 'data', 'analysis', 'visualization', 'utils', 'tests']:
                init_file = folder_path / '__init__.py'
                if not init_file.exists():
                    init_file.touch()
                    print(f"   📄 Creado: __init__.py")
            
            # Crear .gitkeep en carpetas de datos
            if folder in ['raw', 'processed', 'cache', 'images']:
                gitkeep = folder_path / '.gitkeep'
                if not gitkeep.exists():
                    gitkeep.touch()
                    print(f"   📄 Creado: .gitkeep")
            
            # Recursión para subcarpetas
            if isinstance(subfolders, dict):
                create_folders(folder_path, subfolders)
            elif isinstance(subfolders, list):
                for subfolder in subfolders:
                    subfolder_path = folder_path / subfolder
                    subfolder_path.mkdir(exist_ok=True)
                    print(f"✅ Creada: {subfolder_path}")
                    
                    # __init__.py para subcarpetas de Python
                    if folder == 'src' or folder_path.parent.name == 'src':
                        init_file = subfolder_path / '__init__.py'
                        if not init_file.exists():
                            init_file.touch()
                            print(f"   📄 Creado: __init__.py")
    
    # Crear estructura
    base_path = Path.cwd()
    print(f"\n🚀 Creando estructura en: {base_path}\n")
    create_folders(base_path, structure)
    
    # Crear archivos raíz
    root_files = {
        'requirements.txt': '',
        '.gitignore': '',
        'README.md': '# S&P 500 Stock Analyzer\n\nProyecto de análisis de acciones del S&P 500.',
        'MANUAL_USO.md': '# Manual de Uso\n\nDocumentación completa del proyecto.'
    }
    
    print(f"\n📄 Creando archivos raíz...\n")
    for filename, content in root_files.items():
        file_path = base_path / filename
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Creado: {filename}")
    
    print(f"\n🎉 ¡Estructura creada exitosamente!\n")
    print("📂 Estructura del proyecto:")
    print("""
    SP500-Stock-Analyzer/
    ├── 📁 data/
    │   ├── raw/
    │   ├── processed/
    │   └── cache/
    ├── 📁 src/
    │   ├── data/
    │   ├── analysis/
    │   ├── visualization/
    │   └── utils/
    ├── 📁 streamlit_app/
    │   └── pages/
    ├── 📁 docs/
    │   └── images/
    ├── 📁 notebooks/
    ├── 📁 tests/
    ├── 📄 requirements.txt
    ├── 📄 .gitignore
    ├── 📄 README.md
    └── 📄 MANUAL_USO.md
    """)

if __name__ == "__main__":
    create_project_structure()