El script tenía una falla, cuando el script revisaba un archivo markdown .md y encuentraba listas con guiones: "-", o con asteriscos: "*", o con una lista numerada: "1. 2. 3. 4. etc" los dejaba intactos

El Ejemplo 1 siguiente es de una lista con guiones, pero lo mismo es para asteriscos:

**Ejemplo 1**
Mecanismo autoinmune: La bacteria podría provocar una reacción cruzada donde el sistema inmune:
- La evidencia actual no es concluyente.
- No se ha establecido una relación causa-efecto directa
- La presencia de H. pylori no necesariamente lleva al desarrollo de artritis. 
Si sospechas que tienes H. pylori y problemas articulares, lo más recomendable el medico.

Lo correcto debe ser:

<p><b>Ejemplo 1</b></p><p>Mecanismo autoinmune: La bacteria podría provocar una reacción cruzada:<br /></p><ul style="text-align: left;"><li>La evidencia actual no es concluyente</li><li>No se ha establecido una relación causa-efecto directa</li><li>La presencia de H. pylori no necesariamente lleva al desarrollo de artritis. </li></ul><p>Si sospechas que tienes H. pylori y problemas articulares, visita al medico.<br />

donde a cada parrafo de la lista se inicó con <ul style="text-align: left;"> y en  cada línea al inicio <li> al final cerrar con </li> y luego al final del párrafo de la línea lo terminar con </ul> 

y también pongo el siguiente ejemplo 2 de listas numeradas en markdown:

**Ejemplo 2**
Limitaciones:
1. Variabilidad en los métodos de detección
2. Diferentes criterios para definir AR activa
3. Posibles factores de confusión no controlados
4. Tamaños de muestra relativamente pequeños en algunos estudios
Falta de seguimiento longitudinal

lo correcto es de la siguiente manera:

<b>Ejemplo 2</b></p><p>Limitaciones:<br /></p><ol style="text-align: left;"><li>Variabilidad en los métodos de detección</li><li>Diferentes criterios para definir AR activa</li><li>Posibles factores de confusión no controlados</li><li>Tamaños de muestra relativamente pequeños en algunos estudios</li></ol><p>Falta de seguimiento longitudinal<br /></p>

donde a cada parrafo de la lista se inicia con <ol style="text-align: left;"> y en cada línea al inicio <li> al final cerrar con </li> y luego al final del párrafo de la línea lo terminar con </ol>

