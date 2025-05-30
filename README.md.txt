Proyecto: Diseño Geométrico de Exoesqueleto Modular y Parametrizable

Descripción:
Este repositorio contiene el material completo del desarrollo de un exoesqueleto modular y vestible, diseñado para adaptarse a distintos tipos de cuerpos mediante modelado geométrico 3D y técnicas de análisis antropométrico. Este proyecto fue realizado como parte de una tesis de grado en ingeniería.

Estructura del repositorio:

- /Manga Patterns/ → Contiene los patrones de las mangas y estructuras vestibles del exoesqueleto, diseñados para ajustarse al contorno del brazo.
- /CAD/ → Archivos de modelado CAD de los módulos del exoesqueleto, en distintos formatos (Blender, STL, STEP, etc.), organizados por talla y segmento.
- /Renders/ → Imágenes y visualizaciones renderizadas del diseño final del exoesqueleto en sus distintas tallas y vistas.
- /Modelos SMPL-X/ → Contiene los cuerpos generados sintéticamente a partir del modelo paramétrico SMPL-X, tanto completos como segmentados (brazos, piernas).
- /Scripts/ → Códigos en Python para automatizar la generación de cuerpos, extraer datos de vértices, realizar clustering y análisis estadístico.

- /Datos generados/ → Archivos CSV y JSON con datos extraídos de los modelos: coordenadas de vértices, valores `beta`, tallas asignadas, etc.

Tecnologías utilizadas:
- Blender + Add-ons de SMPL-X
- Python (NumPy, Pandas, Scikit-learn)
- SMPL-X Model (paramétrico basado en datos reales)
- Herramientas CAD para modelado técnico

Uso del contenido:
Este proyecto es de uso exclusivamente educativo y académico. Todos los derechos están reservados por el autor. Si deseas utilizar o citar este trabajo, debes referenciar la tesis original como se indica en el archivo `LICENSE.txt`.

Autor:
Oscar Andres Aguirre Colorado  
oscarandresaguirre@hotmail.com
