# Crear estructura de carpetas
New-Item -ItemType Directory -Force -Path src
New-Item -ItemType Directory -Force -Path notebooks
New-Item -ItemType Directory -Force -Path models
New-Item -ItemType Directory -Force -Path archive

# Mover código fuente (ignorando carpetas internas por ahora)
Move-Item "main, models\*.py" src\

# Mover Notebooks
Move-Item "*.ipynb" notebooks\

# Archivar scripts de prueba y utilidades antiguas
Move-Item "ejemplo_exclusion_palabras_stopwords.py" archive\
Move-Item "test_imports.py" archive\
Move-Item "test_torch.py" archive\
Move-Item "traductor_csv.py" archive\

# Mover modelos generados si existen en la carpeta antigua
if (Test-Path "main, models\modelos_clasicos") {
    Move-Item "main, models\modelos_clasicos\*" models\
    Remove-Item "main, models\modelos_clasicos" -Recurse -Force
}

# Limpiar carpeta antigua si está vacía o contiene basura
if (Test-Path "main, models") {
    Remove-Item "main, models" -Recurse -Force
}

Write-Host "Reorganización completada."
