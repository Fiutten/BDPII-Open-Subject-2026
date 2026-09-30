# Fuentes editables

Esta carpeta separa los archivos editables de las versiones PDF conservadas en `teoria/` y `practica/`.

## Teoría

Cada directorio de `teoria/Tema_XX_.../` contiene las fuentes LaTeX, el estilo Beamer y la carpeta `images/` necesarios para su compilación. Desde el directorio del tema:

```bash
latexmk -pdf -shell-escape <archivo>.tex
```

El parámetro `-shell-escape` es necesario por el uso de `minted`. Las fuentes de los temas 1 a 3 requieren además una distribución LaTeX con los paquetes de idioma español para `babel` y `fontawesome5`.

## Prácticas

Los directorios de `practica/Tema_XX_.../` contienen las fuentes DOCX correspondientes a los PDF publicados en `../practica/`.

Los contenidos del antiguo ZIP del tema 4 están completamente extraídos y clasificados aquí. No se conservan comprimidos redundantes en `material_original/`.
