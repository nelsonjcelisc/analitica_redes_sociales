========================================================================================
DATASET Y DOCUMENTACIÓN COMPLETA DE LA INVESTIGACIÓN MATEMÁTICA IB
========================================================================================

Título del Proyecto: Auditoría de Algoritmos de Recomendación en la Red Social X
========================================================================================

1. DESCRIPCIÓN DEL DATASET (tweets_dataset.csv):
----------------------------------------------------------------------------------------
El archivo 'tweets_dataset.csv' contiene un total de 33,675 publicaciones (tweets) recolectadas
durante el periodo de experimentación utilizando tres cuentas de usuario apolíticas de control:
  • Gamer_Project (@gamer): 10,621 tweets recolectados (1,068 políticos -> λ = 10.06%)
  • animecol300_Project (@animecol): 12,040 tweets recolectados (1,065 políticos -> λ = 8.85%)
  • marthasteward295 (@marthasteward): 11,014 tweets recolectados (932 políticos -> λ = 8.46%)

Estructura de las columnas en el archivo CSV:
  1. tweet_id: Identificador único global asignado al tweet por la plataforma X.
  2. account_label: Identificador de la cuenta de control que recibió la publicación.
  3. author: Nombre de usuario (@handle) del creador original de la publicación.
  4. timestamp_posted: Fecha y hora original de publicación del tweet.
  5. timestamp_detected: Fecha y hora exacta en la que el bot capturó el tweet en la línea de tiempo.
  6. content: Texto completo original del tweet.

2. RESUMEN DE LOS RESULTADOS MATEMÁTICOS:
----------------------------------------------------------------------------------------
• Modelo de Poisson: P(X = k) = (λ^k * e^-λ) / k!
• Tasa promedio de intrusión política por cada 100 tweets (n = 100):
    - Gamer_Project: λ = 10.06 | P(X = 0) = 0.004% | P(X >= 1) = 99.996%
    - animecol300_Project: λ = 8.85 | P(X = 0) = 0.014% | P(X >= 1) = 99.986%
    - marthasteward295: λ = 8.46 | P(X = 0) = 0.021% | P(X >= 1) = 99.979%
• Prueba Chi-Cuadrado de Independencia: χ² = 18.0837, p-valor = 0.0001 (p < 0.05).
  Conclusión: Existe una personalización algorítmica estadísticamente significativa.

3. CONTENIDO DEL PAQUETE COMPRIMIDO (.ZIP):
----------------------------------------------------------------------------------------
  • tweets_dataset.csv: Matriz completa de datos (33,675 registros).
  • readme_dataset.txt: Este archivo descriptivo.
  • Andres Celis_Exploración matemática.docx: Documento master en formato Word con portada,
    índice, 8 gráficas incrustadas, tablas de contingencia y metadatos del autor.
  • Andres Celis_Exploracion Matematica.ipynb: Cuaderno Jupyter ejecutable y 100% pre-renderizado
    con los 8 módulos del tutorial de Poisson, NLP y dispersión semántica 3D.
  • Andres Celis_Exploracion Matematica.pdf: Versión exportada en PDF del Jupyter Notebook.
  • images/: Carpeta con las 8 gráficas exportadas en alta resolución (PNG).

========================================================================================
