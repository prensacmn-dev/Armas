from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import openai
import PyPDF2
import json
import re

# Descargar recursos de NLTK

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Configuración de OpenAI
openai.api_key = OPENAI_API_KEY

pdf_text = """
    Competencia Lingüística
Actividades
Eje temático
“Consumos problemáticosen jóvenes: las apuestas en
línea”
2
3
Hoja de ruta
La propuesta de
actividades que
presentamos permite
abordar la comprensión
discursiva de una
problemática social
actual: “Consumos
problemáticos en
jóvenes: las apuestas en
línea”.
Desde el punto de vista de la aproximación didáctica de las
prácticas letradas en el Nivel Superior, nuestro objetivo será
acompañar la comprensión de los discursos circulantes en torno
del tema, la puesta en relación de posicionamientos sobre la
cuestión y la producción de textos que puedan dar cuenta del
estado de la problemática.
En definitiva, a través de un tema de importancia social, nuestra
pretensión es acompañar la comprensión de textos en grados
crecientes y la producción discursiva que permita sortear el
examen de ingreso al Colegio Militar de la Nación.
4
Desagregado del corpus: textos, descripciones y
actividades.
5
Texto Descripción Actividad
Imagen gráfica de El juego del
calamar de Hwang Dong-hyuk
(Capítulo I: “Luz verde, luz
roja”).
Serie de televisión
surcoreana que aborda la
vida de un jugador en la
ruina.
El Puntapié. Visualización,
análisis de la temática y de
fragmentos dialógicos.
Cut de streaming: “Clase
turista” perteneciente al sitio
Estación Sur.
Entrevista en la que se
aborda la ludopatía juvenil.
Entrevistada: Julieta
Calmels.
El Puntapié. Escucha
orientada: selección de
segmentos, análisis y puesta
en común.
El juego del calamar de Hwang
Dong-hyuk (Capítulo I: “Luz
verde, luz roja”).
Capítulo de la serie de
televisión surcoreana
En Marcha. Primera escala.
Análisis de la estructura
narrativa y de la temática de la
propuesta.
Ley N° 6330. Ciudad de Buenos
Aires. Prevención y
concientización del juego
patológico y asistencia a
quienes lo padecen y a sus
familiares.
Texto legislativo que aborda
consumos problemáticos
vinculados con los juegos de
azar.
En Marcha. Primera escala.
Deconstrucción de la
estructura de la definición.
Artículo del Ministerio de
Salta
Sitio de difusión de difusión
de las actividades de
gobierno.
En Marcha. Primera escala.
Comparación de conceptos.
Aproximación a las
explicaciones.
Artículo de La Nación Artículo periodístico que
retoma los resultados de una
investigación sobre
apuestas en línea realizadas
por jóvenes.
En Marcha. Segunda escala.
Análisis de paratextos.
Ejercitación con conectores e
inferencias.
Artículo de La Nación
“¿Jugamos una fichita en el
recreo?”
Artículo hipervinculado con
el anterior. Su producción es
periodística bajo
asesoramiento profesional.
En Marcha. Segunda escala.
Elaboración de resúmenes
comparativos de fuentes.
Sitio web de Opina Argentina Sitio de difusión de la
consultora de opinión.
En Marcha. Segunda escala.
Análisis de datos y puesta en
contraste de resultados.
Artículo (UNLP), “Las
apuestas online bajo la lupa”
Sitio de divulgación CyT
(UNLP)
En Marcha. Tercera escala.
Aproximación a los discursos
polifónico-argumentativos.
Ejercitación con marcos de
discurso.
Artículo (UBA), “Apuestas
online. Adicción al juego en la
adolescencia”
Sitio de divulgación de la
Facultad de Farmacia y
Bioquímica (UBA)
En Marcha. Tercera escala.
Aproximación a los discursos
polifónico-argumentativos.
Ejercitación con marcos de
discurso.
6
Artículo académico
(CONICET), “Apuestas
deportivas online y jóvenes
en Argentina: entre la
sociabilidad, el dinero y el
riesgo”
Sitio Ludopédio,
especializado en
investigaciones vinculadas
con el fútbol.
En Marcha. Tercera escala.
Aproximación a los discursos
polifónico-argumentativos.
Ejercitación con marcos de
discurso.
“Pautas para evitar que los
adolescentes apuesten
online”
Sitio del Ministerio de
Justicia.
Apuntes de cierre.
Socialización de
recomendaciones
ministeriales.
Actividades
Objetivos
• Que los ingresantes analicen y comprendan formas de
construcción discursiva de debates propios de las ciencias
humanas y sociales.
• Que los ingresantes comprendan el sentido de las
enunciaciones como fruto de un entramado polifónico y
argumentativo.
• Que los ingresantes se aproximen a discursos acerca de los
consumos problemáticos juveniles, en especial, el tema de las
apuestas en línea.
• Que los ingresantes puedan realizar producciones escritas en
los que den cuenta de una controversia actual.
• Que los ingresantes reflexionen sobre una problemática que
afecta especialmente a las juventudes.
El Puntapié
1. Observar la imagen publicitaria de la serie surcoreana llamada “El
juego del calamar”.
7
2. Luego, preguntarse: ¿han visto la serie?, ¿qué recuerdos generales
tienen de ella?, ¿en qué problema se centra la trama?
3. Vuelvan a la imagen y describan en dos o tres líneas la gráfica de la serie.
Para hacerlo,tengan en cuenta las relaciones que pueda haber entre las imágenes
del afiche y el título de la obra audiovisual.
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………...
4. Reflexionar sobre los sentidos a los que alude el título: ¿a qué refiere el
nombre de la serie?, ¿en qué consiste el juego infantil mencionado?,
¿cuál es la diferencia entre el juego infantil y el juego de la serie?
5. Para continuar con la relación juego y vida, escuchar el streaming
“Clase turista” perteneciente al sitio Estación Sur.
Particularmente, se espera que pueda responder de a pares las siguientes
consignas a partir de la entrevista:
a. ¿Quién es la entrevistada y qué cargo ocupa en el gobierno de la provincia
de Buenos Aires?
Audio: "La ludopatía se vuelve problemática cuando altera ámbitos de la vida"
https://radiocut.fm/audiocut/embed/mini/julieta-calmels-ludopatia-se-vuelveproblematica-cuando-altera-ambitos-vida/
8
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
b. ¿Cuál es la representación dominante sobre consumos problemáticos?
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
c. ¿Cuáles son las alertas respecto de los consumos problemáticos que señala
Calmels? Para responder utilice los términos esporádico- permanente.
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
d. Extraiga fragmentos en los que la funcionaria mencione el rol del Estado,
de la tecnología y de la publicidad frente al problema. Transcriba dichos
segmentos en el cuadro que presentamos a continuación:
Cita textual1
Rol del Estado
Rol de la tecnología
Rol de la publicidad
e. En un momento, Calmels enuncia: “Muchas veces cortar de golpe con lo
que uno tiene una relación compulsiva, ustedes dijeron sacar el celular,
es parte de lo que hacen los adultos, suele desencadenar grandes crisis”.
Para analizar este fragmento, proponemos delimitar dos conceptos:
Enunciado2
: el enunciado es una manifestación, concreta y real de la actividad
verbal.
1 Se espera trabajar con aspectos vinculados con los PdV alusivos a partir del uso de comillas
que marcan los límites entre el discurso citante y citado.
2
9
Discursos argumentativos: posiciones a las que apunta un segmento o
enunciado.
● Para recuperar el sentido, es necesario analizar el vínculo entre el primer
segmento (A) y la EVALUACIÓN RESULTANTE (B).
● Este tipo de análisis permite arribar al posicionamiento que ofrece el
LOCUTOR -es decir, el responsable de la enunciación- en el discurso. En el
caso del recuadro, podemos decir que estamos frente a una advertencia
de esa figura discursiva.
● Estas continuaciones discursivas constituyen la argumentación a la que apunta el
enunciado
● Por último, las relaciones entre A y B pueden responder a las formas: POR
LO TANTO o SIN EMBARGO de acuerdo con las continuaciones discursivas
que vehiculizan. Así, POR LO TANTO manifiesta una consecuencia y SIN
EMBARGO una restricción.
f. Para sistematizar esta actividad, proponemos el análisis de los
siguientes segmentos:
● “Un consumo se vuelve problemático cuando altera una esfera de
nuestra vida”.
MD: cambios de conductas son signos de alerta PLT (padres y
allegados)...…………………………………………………………………………………………
Posicionamiento enunciativo del LOCUTOR: ………………………………
Considerando esas nociones, es posible afirmar que el sentido de la cita
puede ser analizada retomando el propio enunciado (A) y, a su vez,
identificando los posicionamientos argumentativos suscitados en pos de la
construcción de sentido (B):
Por ejemplo: prohibir el uso del celular suele desencadenar crisis (A) POR LO
TANTO es necesario que los adultos sean cuidadosos (B)”.
10
● “El consumo y la oferta del mercado deben ser regulados por el
Estado”
MD: El Estado es el responsable de las regulaciones SE
…………………………………………………………………………………………………………….
Posicionamiento enunciativo del LOCUTOR: …………………………………..
g. Finalmente, considerando lo analizado anteriormente, ¿cuáles serían las
recomendaciones a los padres?, ¿cuál debería ser el rol del Estado?,
¿cuáles son las políticas o líneas de acción que propone la provincia de
Buenos Aires?
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
6. A modo de cierre, se indica la visualización del capítulo: “Luz verde, luz roja”
de El juego del calamar.
En marcha
Primera escala: encendiendo motores
El juego patológico no es una problemática nueva, sin embargo, las tecnologías
han dado un impulso a su proliferación dado que facilitan el alcance mediante
un click. Por esa razón, el sistema de apuestas digitales constituye una
preocupación de la sociedad en su conjunto. En los últimos años, la difusión de
estos juegos de azar ha ameritado que organismos estatales e instituciones
privadas se manifestaran sobre la cuestión. En particular, en este segmento se
trabajará con el capítulo “Luz verde, luz roja” de la serie, con la Ley N°
6330/2020, con un artículo publicado en el sitio web de la Secretaría de Prensa
y de Comunicación del Gobierno de Salta y con artículo periodístico de La
Nación que difunde una investigación sobre la ludopatía en Argentina.
11
7. El capítulo “Luz verde, luz roja” puede dividirse en dos partes: una en la
que el protagonista está fuera del juego y otra en la que está dentro. Respecto
de cada una de ellas, ¿qué situaciones son narradas en cada segmento? Elabore
en un texto teniendo en cuenta los siguientes requerimientos:
● Una introducción con la mención del audiovisual, la enunciación de la
temática tratada y el objetivo por el que la leemos.
● Un desarrollo en el que sean contrastadas las dos partes en las que puede
dividirse la acción en la serie y los sucesos fundamentales.
● Un cierre en el que se recuperen los objetivos propuestos en la
introducción.
En el primer ……………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
A modo de cierre, ……………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
8. Para continuar profundizando en el tema, lea el texto de la Ley N°
6330/2020, “Prevención y concientización del juego patológico y asistencia a
quienes lo padecen y a sus familiares”. Asimismo, complete el cuadro con la
información que se solicita.
12
Concepto Definición (40 palabras como máximo)
Juegos de Apuesta
Juego Patológico
Publicidad de juegos de
apuesta
Promoción de juegos de
apuesta
9. De acuerdo con lo analizado en “Luz verde, luz roja”, ¿cuáles de los
conceptos definidos en la ley se abordan en la serie El juego del calamar? Elija
uno de ellos y fundamente en unas pocas líneas.
En la serie El juego del calamar se aborda la idea de ………………………………………..
dado que ………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………...
Link: https://www.argentina.gob.ar/normativa/provincial/ley-6330-123456789-0abc-defg-033-6000xvorpyel/actualizacion
13
10. Las definiciones se componen de un concepto a definir y de una definición
propiamente dicha. Luego de leer el texto del Gobierno de Salta, preste
especial atención a la definición de “ludopatía”.
En efecto, el siguiente esquema facilita la explicación de la idea de “definición”:
Concepto Marca de
definición
Categoría
clasificatoria
Rasgos característicos
Ludopatía se llama impulso
incontrolable
por las apuestas o el azar a pesar de
causarnos pérdidas económicas y
consecuencias negativas para el trabajo,
familia y amigos.
11. Siguiendo el mismo patrón, reconstruya la definición de “juego
recreativo”. Para ello, tomen en consideración el siguiente fragmento del texto
del Ministerio de Prensa y Comunicación del Gobierno de Salta.
Concepto Marca de Categoría Rasgos característicos
Se trata de una adicción que afecta a todas las clases sociales con mayor
incidencia en la adolescencia, especialmente entre los varones. No es lo
mismo el juego recreativo que funciona como actividad de esparcimiento que
el problemático que anula nuestra voluntad haciendo necesario la intervención
de un profesional de la salud.
Link: https://www.salta.gob.ar/prensa/noticias/el-ministerio-de-salud-advierte-sobre-el-incremento-de-la-ludopatia-entreadolescentes-y-jovenes-96004
Se llama ludopatía digital al impulso incontrolable por las apuestas o el azar a pesar de
causarnos pérdidas económicas y consecuencias negativas para el trabajo, familia y
amigos.
14
definición clasificatoria
Juego
recreativo
12. Elabore un texto en el que se comparen las definiciones de “juego
recreativo” y de “juego patológico”. Tenga en cuenta dos cuestiones:
● La definición de “juego” se utilizará como punto de partida de la
introducción.
● Son conceptos en contraste por lo que será necesario un conector que
marque diferencias (“por el contrario”3
, por ejemplo). Utilicen un
marcador textual distinto para dar cuenta de esa función.
● Son definiciones que se enuncian en dos textos del corpus, por lo tanto,
citarlos de acuerdo con la normativa APA4
.
Por “juego” se entiende ………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
3 https://educaciodigital.cat/ioc-batx/moodle/pluginfile.php/14531/mod_page/content/16/Conectores_textuales.pdf
4
https://udesa.edu.ar/como-citar
15
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
A modo de cierre, ……………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
Segunda escala: a fondo
Esta sección del recorrido de actividades propone, por un lado, la
lectura y el análisis conjunto del artículo de La Nación titulado “El 16% de
los jóvenes reconoce que realiza apuestas online, según un estudio de
Opina Argentina”; por otro, se indica el seguimiento de un hipertexto
inserto en dicho artículo de La Nación. Esta puesta en relación
pretende determinar en qué cuestiones se centra la discusión
acerca de las apuestas en línea.
Actividades
1. Para comenzar esta segunda etapa proponemos la aproximación al
artículo a través del enlace que se adjunta a continuación. Por lo tanto, proceda
a abrir el vínculo y a analizar algunos elementos paratextuales. Particularmente,
confeccionen una lista con tres paratextos que consideren exclusivos de los
artículos periodísticos mediados por tecnologías. Coloquen sus respuestas en el
cuadro diseñado para tal fin.
PARATEXTO FUNCIÓN
Link: https://www.lanacion.com.ar/sociedad/el-16-de-los-jovenes-reconoce-que-realiza-apuestas-onlinesegun-un-estudio-de-opina-argentina-nid30052024/
16
2. Elaboramos una reflexión sobre los rasgos característicos que tienen los
textos que circulan en la web y sobre las exigencias que demandan al lector.
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
3. Retomando el título, determine a quién corresponde la afirmación “El 16%
de los jóvenes reconoce que realiza apuestas online”. Fundamente la respuesta
señalando algún elemento presente en el paratexto que estamos analizando.
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
4. Dado que estamos frente a un informe presentado a partir de una
investigación, los datos obtenidos permiten sacar algunas conclusiones.
Analice algunas derivaciones posibles que se desprenden de la pesquisa.
Aspecto Porcentaje Relación Inferencia de Opina
Conocimiento de
personas afectadas por
la ludopatía
por lo tanto
Conocimiento entre
personas jóvenes de
sujetos afectados por la
ludopatía
por lo tanto
Personas que admiten
apostar
sin embargo
17
5. Teniendo en cuenta los resultados obtenidos en el esquema podemos
proponer algunas conclusiones. Completamos los espacios en pequeños grupos
y, luego, compartimos las producciones.
● Introducción: proponer una presentación de la consultora Opina
Argentina (seguir el hipervínculo en el cuerpo del texto) y del trabajo
realizado sobre ludopatía.
● Desarrollo: plantear la relación entre ludopatía y juventud siguiendo los
datos obtenidos por la consultora y su análisis en el cuadro del punto
anterior. A su vez, incorporar dos posibles acciones del Estado para
enfrentar la problemática de la que se da cuenta en el estudio.
● Conclusión: delimitar la importancia de la investigación en relación con
el tema abordado.
Opina Argentina ……………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
En cuanto a la relación entre ludopatía y juventud,
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
En lo vinculado con el rol del Estado, la encuesta ……………………………………………….
………………………………………………………………………………………………………………………………..
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………………..
18
En definitiva, ………..…………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
6. Para cerrar la segunda etapa, seguir el primer hipervínculo en el cuerpo
del artículo que hemos trabajado. Leer el texto. Para ello, centrarse en:
● Título: “¿Jugamos una fichita en el recreo?”.
● Autora y especialistas consultados.
● Destinatarios posibles.
● Formato interactivo del artículo.
● Imágenes ilustrativas.
● Relatos en primera persona.
Luego proponer acciones para enfrentar institucionalmente el problema de las
apuestas en línea.
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
Tercera escala: a la pesca de las voces
Esta última sección nos invita a ir un poco más allá. En efecto, busca
profundizar en las ideas que han emergido de las escalas anteriores.
Por ello, para finalizar este recorrido, proponemos la lectura y
análisis de tres textos que abordan la problemática desde la
comunidad académica. Los dos primeros de ellos son artículos de
19
la agencia de noticias de la Universidad Nacional de La Plata (UNLP)
y de la Universidad de Buenos Aires (UBA); el tercero es un artículo
académico de un investigador del CONICET. ¡Exploremos el discurso
un poco más!
Actividades
1. Hasta el momento hemos leído textos de circulación masiva que abordan
un problema acuciante entre los jóvenes: las apuestas en línea. En este
caso, nos aproximamos a la discursividad académica mediante textos
centrados en dicha temática. Para comenzar, siguiendo el link, lean el
texto propuesto por la UNLP. A continuación, responda las siguientes
preguntas:
a. La agencia de la UNLP decide llamar a la sección en la que publica
el artículo “Bajo la lupa” ¿Qué sentidos evoca la frase? De a pares,
expresen dos interpretaciones posibles.
Sentido 1: ……………………………………………………………………………………………………
Sentido 2: ……………………………………………………………………………………………………
b. Observe el texto, ¿cómo se organiza estructuralmente? ¿De qué
manera se despliegan los temas asociados con la problemática? ¿Qué
efecto produce esa organización en el lector?
…………………………………………………………………………………………………………………….
……………………………………………………………………………………………………………………..
……………………………………………………………………………………………………………………..
c. En el artículo se señala:
“La ludopatía digital (...) puede afectar a todas las clases sociales y
generar problemas financieros, laborales y familiares”. Proponga un MD
para la afirmación que se construya con PLT.
20
2. Tanto César Barletta como Soledad Fuster señalan que es necesario que se
realicen acciones tendientes a limitar el crecimiento de la adicción al juego en
línea. Complete el cuadro que se adjunta:
Profesional Acción a realizar Entidad encargada
3. Retomando los ejes organizadores podemos decir que dos profesionales
señalan la importancia de ejecutar acciones para atender la problemática. A
partir de las citas, reconstruya el MD.
a. Barletta considera que “es fundamental implementar medidas legales
efectivas para proteger a la población de los riesgos asociados con estas
actividades”.
b. Por su parte, Fuster entiende que es “esencial incorporar una
perspectiva digital en la Educación Sexual Integral”.
MD: ………………………………………………………………………………………………………………
……………….PLT................................................................................................................De
allí que la enunciación resulte asertiva/refutativa (Tachar lo que no
corresponde).
MD: no hay marco normativo para proteger a la población PLT
……………………………………………………………………………………………………………………….
De allí que el posicionamiento del locutor es
……………………………………………………………………………………………………………………….
21
4. Para finalizar con este artículo, complete en los espacios de puntos las
conclusiones obtenidas:
Respecto de la problemática vinculada con las apuestas en línea, tanto Barletta
como Fuster consideran que se deben realizar acciones para su abordaje. Por
un lado, …………………………………………………………………………………………..
……………………….. Por otro, ……………………………………………………………………………………..
…………………………………………………………………………………………………………….…………………
…………………………………………………………………………………………. En consecuencia,
………………………………………………………………………………………………………………………………..
………………………………………………………………………………………………………………………………..
………………………………………………………………………………………………………………………………..
5. Lea el copete del artículo “Apuestas online. Adicción al juego en la
adolescencia” de Laura Deluca. A posteriori, respondan las siguientes
preguntas:
a. ¿Cómo se define la adicción al juego?
………………………………………………………………………………………………………………………………..
………………………………………………………………………………………………………………………………..
b. ¿Qué institución internacional se cita como fuente?
………………………………………………………………………………………………………………………………..
………………………………………………………………………………………………………………………………..
6. En el apartado que se ocupa de adolescencia, se enuncia: “Nuestra
MD: la incorporaración de la perspectiva digital en la materia ESI resulta
fundamental SE
…………………………………………………………………………………………………………………….
De allí que el posicionamiento del locutor es
………………………………………………………………………………………………………………………
22
investigación bipartidista ha llegado a una conclusión solemne: Meta ha estado
dañando a nuestros niños y adolescentes, cultivando la adicción para aumentar
las ganancias corporativas”,
a. ¿A quién corresponde la cita? ¿Qué rol cumple socialmente el
responsable de la enunciación?
………………………………………………………………………………………………………………………………..
………………………………………………………………………………………………………………………………..
b. Propongan un MD para ese enunciado. Utilicen palabras vinculadas
con “responsabilidad” o “culpabilidad”.
c. El reclamo hacia la empresa Meta se asienta en el funcionamiento del
mecanismo de recompensa. En no más de cinco renglones describa dicho
mecanismo.
Un mecanismo de recompensa es ………………………………………………………………………..
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
d. Finalmente, Deluca despliega algunas recomendaciones para abordar el
problema. Enúncielas en las líneas de puntos.
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..………………………
…………………………………………………………………………………………………………………………………
…………………………………………………………………………………………………………………………………
MD: ……………………………………………………………………………………………………………….
……………………………………………………………………………………………………De allí que
la posición del locutor es
……………………………………………………………………………………………………………………….
23
7. Para finalizar esta última escala, les proponemos la lectura de un artículo
académico. Esto supone que el lenguaje del texto será más técnico y que las
ideas sostenidas serán presentadas con mayor rigurosidad porque para la
publicación de artículos académicos es necesaria la aprobación de un tribunal
de expertos. Dicho esto, observe de los elementos paratextuales, completen el
cuadro e indiquen su función de cada paratexto.
Paratexto Función
8. Luego, determine qué paratextos son característicos del discurso académico
y cuáles son transversales a diferentes formas discursivas.
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..………………………
…………………………………………………………………………………………………………………………………
9. El primer párrafo del apartado “Introducción” cumple una función específica.
Para determinarlo, opte por una de las posibilidades.
El primer párrafo…
a. presenta datos generales sobre una opinión.
b. contextualiza una problemática.
c. describe una serie de problemas vinculados.
Justifique su respuesta utilizando uno de los siguientes conectores: DADO
QUE/ DEBIDO A QUE.
24
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..………………………
…………………………………………………………………………………………………………………………………
10. En el segundo párrafo se enuncian factores que inciden en que la
problemática de las apuestas alcance dimensiones importantes. Elija una y
explique por qué ese aspecto incide en el problema.
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..……………………….
…………………………………………………………………………………………………………………………………
11. En el tercer párrafo aparece una citación autoral entre paréntesis: (Etuk et
al.,2022). ¿Qué indica cada uno de los elementos contenidos en dicho signo de
puntuación?
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..……………………….
…………………………………………………………………………………………………………………………………
12. Pasamos al análisis del quinto párrafo. ¿Qué cuestiones se explicitan allí?
¿Por qué resulta importante esta información en el artículo académico?
…………………………………………………………………………………………………………………………………
………………………………………………………………………………………………………..……………………….
…………………………………………………………………………………………………………………………………
13. Finalmente, en el último párrafo de la “Introducción” se enuncian tres ejes
de abordaje para el desarrollo. Transcríbalos en los siguientes espacios:
a. ………………………………………………………………………………………………………………………
b. ………………………………………………………………………………………………………..…………….
c. ………………………………………………………………………………………………………..……………
Primer apartado: las apuestas, la diversión y la socialización juvenil masculina
25
d. En el primer párrafo se utiliza la palabra driver, ¿a qué se refiere? ¿De
dónde procederá su uso? Proponga una hipótesis en la línea punteada.
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
e. Las motivaciones juveniles para apostar son dos. En un texto de cuatro
líneas, explique qué características, según Branz y Murzi, tienen estos
factores motivantes.
De acuerdo con la investigación de Branz y Murzi (2024), existen dos
grandes factores motivacionales que inciden en las apuesta adolescentes,
por un lado,
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
Por otro lado, ………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
Segundo apartado: la forma de apreciar lo deportivo
f. En el penúltimo párrafo se utiliza la palabra tipsters, ¿a qué se refiere?
¿De dónde procederá su uso? Proponga una hipótesis en la línea
punteada.
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
g. Branz y Murzi (2024) señalan que “Las apuestas, con la posibilidad de
competir en tiempo real, trastocan en buena medida esas formas
26
tradicionales de observar y relacionarse con un partido o evento para los
espectadores, ya que introducen un elemento de cálculo y de eventual
beneficio personal.” Complete el texto fundamentando la afirmación con dos
razones que aporte el artículo.
Branz y Murzi (2024), entienden que …………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
… Se basan en que, por un lado,
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
Por otro lado, ………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
Tercer apartado: entre el azar y el saber
h. En el último párrafo se utilizan comillas en la palabra “chicanas”, ¿a qué
se debe su uso? ¿Qué significa la palabra? Proponga una hipótesis en la
línea punteada.
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
i. El trabajo de campo de Branz y Murzi (2024) se interesa por las estrategias
utilizadas por los jóvenes para potenciar logros en las apuestas. Entre las
respuestas, encuentran que señalan que la suerte y el conocimiento se
vinculan con el éxito. Complete el texto
27
fundamentando cuál de los dos factores es mejor valorado por los
jóvenes. Incluya una cita textual.
El trabajo de campo de Branz y Murzi (2024) demuestra que
……………………………………………………………………………………………………………………….
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
… Sin embargo, el conocimiento …………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
……………………………………………………………………………………………………………………….
……………………………………………………………………………………………………………………….
j. ¿Cómo se titulan las conclusiones? Transcriba el título. Luego, relacione
los tres factores considerados fundamentales en la parte final del escrito.
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
……………………………………………………………………………………………………………………….
……………………………………………………………………………………………………………………….
k. En la conclusión, sobre los entrevistados se afirma: “el origen del dinero
apostado es importante en sus valoraciones: apostar (y perder) dinero
ganado con el trabajo propio es legítimo, mientras que perder dinero
otorgado por los padres o prestado genera más auto-cuestionamientos
morales.“ Proponga un MD para ese enunciado. Utilice palabras vinculadas
con “legitimidad” o “culpabilidad”.
MD: creen que ……………………………………………………………………………………………..
…………………………………………………………………PLT ………………………………………….
28
l. Finalmente, en el párrafo final se enuncia: “las apuestas deportivas entre
los jóvenes tensionan la relación conceptual entre trabajo y ocio”.
Explique brevemente en qué consiste dicha tensión.
………………………………………………………………………………………………………………………
………………………………………………………………………………………………………………………
……………………………………………………………………………………………………………………….
……………………………………………………………………………………………………………………….
m. Para concluir el abordaje del tema, se propone leer y difundir las
recomendaciones aportadas por el Ministerio de Justicia de la Nación.
Una idea puede ser socializar los factores que inciden en la problemática
y teléfonos de ayuda.
……………………………………………………………………………………………………………………..
De allí que la posición del locutor es
……………………………………………………………………………………………………………………….
29
Ministerio de Justicia
Pautas para evitar que los
adolescentes apuesten online
30
¿Qué son los juegos en línea?
A través de Internet, los juegos en línea son aquellos en los
interviene el azar generando adicción y siendo obligatorio arriesgar
nuestro dinero. Por ejemplo, los casinos online; apuestas deportivas
y loterías virtuales.
La habilidad del jugador queda relegada a un segundo plano. Las
posibilidades de ganar se reducen a un porcentaje ínfimo que está
condicionado por la suerte del participante.
El peligro del consumo problemático
Un consumo problemático implica perder el auto-control dañando
nuestra salud física y/o psíquica y perjudicando los vínculos
personales, familiares o laborales. No importa el objeto de consumo
sino la forma en que la persona se relaciona con él. Puede ser
alcohol, tabaco, drogas, tecnología, compras, alimentación o los
juegos en línea que nos llevan a la ludopatía.
Diversión no es adicción
El juego en línea se vuelve problemático cuando se realiza en forma
recurrente. Se llama ludopatía digital al impulso incontrolable por
las apuestas o el azar a pesar de causarnos pérdidas económicas y
consecuencias negativas para nuestro trabajo, familia y amigos.
Se trata de una adicción que afecta a todas las clases sociales con
mayor incidencia en la adolescencia, especialmente entre los
varones. No es lo mismo el juego recreativo que funciona como
31
actividad de esparcimiento que el problemático que anula nuestra
voluntad haciendo necesario la intervención de un profesional de la
salud.
Cinco factores que hacen populares a los juegos en línea entre los
adolescentes
● Publicidad agresiva en TV y redes sociales. Equipos de fútbol, youtubers,
tiktokers, celebridades e influencers promocionan las apuestas.
● Falta de regulación de la actividad a nivel nacional.
● Facilidad para acceder a medios de pago como billeteras virtuales.
● Disponibilidad de las plataformas virtuales para jugar las 24 horas, los
siete días de la semana.
● Libre acceso, alcanza con ingresar a la página o descargar la aplicación
de la casa de apuestas, cargar nuestros datos, medios de pago y
contactar por WhatsApp para que nos carguen crédito.
Regulación jurídica de los juegos online de apuestas en Argentina
Argentina no tiene una ley nacional sobre juegos en línea. Hay 17
provincias que dictaron su propia legislación. El gran problema
consiste en los sitios ilegales que no están sometidos a ningún
32
control estatal haciendo publicidad por redes sociales donde
incentivan a los adolescentes para que apuesten su dinero.
Los menores de 18 años no pueden participar
en apuestas
Pese a la prohibición, los adolescentes suelen
falsear datos y documentación o crear
perfiles falsos con información de algún
adulto para poder apostar.
Pautas que podrían indicar que un adolescente
abusa de los juegos de azar online
● Cambios significativos en el comportamiento o estado de ánimo como
ansiedad, irritabilidad, cambios de humor repentinos, aislamiento social.
● Pérdida de interés repentina en otras actividades que antes disfrutaba
como deportes, estudios o relaciones sociales y que ahora reemplazar
por el juego online.
● Preocupación constante por el juego como hablar constantemente
sobre apuestas, consultar resultados de manera compulsiva o buscar en
forma reiterada oportunidades para jugar.
● Problemas financieros como dificultades para pagar deudas o rápido
agotamiento de sus recursos económicos sin una explicación clara.
● Aumento del tiempo que dedica al juego.
● Negación o minimización del problema como justificar su
comportamiento o mentir sobre la cantidad de tiempo o dinero que
dedica al juego.
33
Consejos para padres y maestros que quieran prevenir la adicción en
los adolescentes por los juegos en línea:
● Generá una comunicación abierta. Animalos a que te compartan sus
preocupaciones y experiencias.
● Establecé límites. Reduciles el tiempo y el dinero que le dedican al juego.
● Concientizá. Informales sobre los riesgos asociados al juego de azar y a la
ludopatía digital.
● Promové actividades alternativas. Incentivalos a participar en actividades
recreativas, deportivas o artísticas.
● Educá sobre seguridad en línea. Enseñales la importancia de la
privacidad online y el manejo seguro de su información personal.
● Predicá con el ejemplo. Usá equilibradamente los dispositivos
electrónicos y juegos en línea.
● Supervisá el tiempo que pasan frente a las pantallas y qué tipo de juegos
eligen.
● Buscá ayuda profesional si es necesario.
Si querés más información sobre los consumos problemáticos,
podés consultar la ley 26.934, Plan Integral para el Abordaje de los
Consumos Problemáticos (Plan IACOP).
Si vos o alguien que conocés necesita ayuda, llamá al 108 o escribí
"ludopatía" en Boti, el WhatsApp de la Ciudad (11 5050-0147)

INDICE
Unidad 1......................................................................................................... 6
Números reales.............................................................................................. 6
Conjuntos numéricos .......................................................................................................................... 6
Operaciones con números enteros..................................................................................................... 7
Adición y sustracción....................................................................................................................... 7
Supresión de paréntesis.................................................................................................................. 8
Supresión de paréntesis, corchetes y llaves.................................................................................... 8
Multiplicación y división.................................................................................................................. 9
Regla de signos:........................................................................................................................... 9
Potenciación.................................................................................................................................. 10
Potencias con base negativa y positiva..................................................................................... 10
Propiedades de la potenciación.................................................................................................... 11
Radicación ..................................................................................................................................... 12
Raíces de índice par................................................................................................................... 12
Raíces de índice impar............................................................................................................... 12
Operaciones con números racionales............................................................................................... 13
Adición y sustracción..................................................................................................................... 13
Multiplicación y división................................................................................................................ 14
Potenciación.................................................................................................................................. 14
Radicación ..................................................................................................................................... 15
Propiedades de la radicación ........................................................................................................ 16
Potencia fraccionaria..................................................................................................................... 17
Pasaje de decimal a fracción ......................................................................................................... 18
Unidad 2....................................................................................................... 19
Expresiones algebraicas................................................................................ 19
Expresiones Algebraicas.................................................................................................................... 19
Polinomios......................................................................................................................................... 19
Características de los polinomios:................................................................................................. 20
Valor numérico o especialización de un polinomio ...................................................................... 20
Operaciones entre polinomios.......................................................................................................... 21
Suma de polinomios...................................................................................................................... 21
Resta de polinomios...................................................................................................................... 21
Multiplicación................................................................................................................................ 22
Multiplicación de monomios..................................................................................................... 22
Multiplicación de un polinomio por un número real................................................................ 22
3
Multiplicación de un polinomio por un monomio .................................................................... 22
Multiplicación de polinomios.................................................................................................... 22
Potencia de un monomio.................................................................................................................. 23
Productos Notables........................................................................................................................... 24
Cuadrado de un binomio........................................................................................................... 24
Cubo de un binomio.................................................................................................................. 24
Producto de binomios conjugados............................................................................................ 25
Casos especiales de factoreo ............................................................................................................ 25
Factor Común................................................................................................................................ 26
Diferencia de Cuadrados............................................................................................................... 26
Unidad 3....................................................................................................... 27
Ecuaciones ................................................................................................... 27
Ecuaciones de Primer grado.............................................................................................................. 27
Resolución de ecuaciones de Primer grado .................................................................................. 27
Ejercicios resueltos........................................................................................................................ 28
Ecuaciones de segundo grado........................................................................................................... 30
Resolución de ecuaciones de Segundo grado............................................................................... 30
Fórmula resolvente ................................................................................................................... 30
Ejercicios resueltos........................................................................................................................ 30
Unidad 4....................................................................................................... 33
Rectas .......................................................................................................... 33
Ecuación de la recta .......................................................................................................................... 34
Gráfico de la recta a partir de una tabla de valores...................................................................... 34
Gráfico de la recta con pendiente y ordenada.............................................................................. 37
Intersección de la recta con el eje 𝑥 ............................................................................................. 40
Ecuaciones de rectas: distintos casos para hallarlas......................................................................... 41
1. Cuando se conoce la pendiente y la ordenada al origen .......................................................... 41
2. Cuando se conoce la ordenada al origen y un punto cualquiera.............................................. 41
3. Cuando se conoce la pendiente y un punto cualquiera............................................................ 41
4. Cuando se conocen dos puntos ................................................................................................ 42
Ejercicio resuelto:...................................................................................................................... 42
Rectas verticales:............................................................................................................................... 43
Rectas paralelas y perpendiculares................................................................................................... 44
Rectas paralelas............................................................................................................................. 44
Ejercicio resuelto:...................................................................................................................... 44
Rectas perpendiculares................................................................................................................. 45
4
Ejercicio resuelto:...................................................................................................................... 45
Unidad 5....................................................................................................... 46
Sistemas de ecuaciones lineales................................................................... 46
Métodos para resolver sistemas de ecuaciones lineales.................................................................. 47
Sustitución..................................................................................................................................... 47
Igualación ...................................................................................................................................... 48
Tipos de soluciones........................................................................................................................... 49
Ejercicios resueltos........................................................................................................................ 49
Unidad 6....................................................................................................... 54
Geometría.................................................................................................... 54
Punto y recta ..................................................................................................................................... 54
Más definiciones ........................................................................................................................... 54
Posiciones relativas de dos rectas:.................................................................................................... 55
Ángulos.............................................................................................................................................. 55
Clasificación de los ángulos........................................................................................................... 56
Relaciones entre ángulos.............................................................................................................. 56
Ángulos complementarios ........................................................................................................ 56
Ángulos suplementarios............................................................................................................ 57
Ángulos opuestos por el vértice................................................................................................ 57
Triángulos.......................................................................................................................................... 57
Propiedad fundamental de los ángulos interiores........................................................................ 57
Clasificación de los triángulos....................................................................................................... 57
Perímetro y área de triángulos...................................................................................................... 59
Ejercicio resuelto:...................................................................................................................... 59
Cuadriláteros..................................................................................................................................... 59
Propiedad fundamental de los ángulos interiores........................................................................ 59
Clasificación de los cuadriláteros.................................................................................................. 59
Paralelogramos.......................................................................................................................... 59
Trapecios................................................................................................................................... 60
Trapezoides............................................................................................................................... 60
Área y Perímetro de figuras planas................................................................................................... 60
Unidad 7....................................................................................................... 62
Trigonometría .............................................................................................. 62
Razones trigonométricas................................................................................................................... 62
Sistemas de medidas angulares.................................................................................................... 63
Resolución de triángulos rectángulos............................................................................................... 63
5
Teorema de Pitágoras....................................................................................................................... 63
Ejercicios resueltos........................................................................................................................ 63
6
Unidad 1
Números reales
A lo largo del tiempo, las personas fueron creando distintos tipos de números para dar
respuesta a nuevas necesidades: contar objetos, representar deudas, dividir cantidades o
medir con mayor precisión. Así surgieron distintos conjuntos numéricos, cada uno con
características propias.
Conocer cómo se relacionan entre sí, qué operaciones permiten y qué propiedades cumplen
es fundamental para resolver diferentes situaciones matemáticas. En esta secuencia vamos a
explorar los principales conjuntos numéricos, sus elementos, formas de representación y las
operaciones que se pueden realizar en cada uno de ellos.
Conjuntos numéricos
Todos los conjuntos numéricos tienen infinitos elementos. Los números naturales (ℕ) son los
primeros que surgieron, y se utilizan para contar o enumerar objetos. Se representan así:
ℕ = {1, 2, 3, 4, 5, 6, … }
Los números enteros (ℤ), incluye a los naturales, a sus opuestos (negativos) y al cero:
ℤ = {… − 4, −3, −2, −1, 0, 1, 2, 3, 4, … }
Tanto ℕ como ℤ son conjuntos discretos, ya que no existe ningún número entre dos
elementos consecutivos. El conjunto de los números naturales está incluido en el de los
números enteros, es decir, se cumple que ℕ⊂ℤ. Ambos conjuntos pueden representarse en
la recta numérica con puntos aislados.
El conjunto de los números racionales (ℚ) está formado por todos los números que pueden
expresarse como el cociente entre dos enteros, con denominador distinto de cero.
Formalmente:
ℚ = {
𝑏
𝑐
⁄ 𝑏, 𝑐 ∈ ℤ 𝑦 𝑐 ≠ 0}
Al dividir 𝑏 por 𝑐, se obtiene un número decimal que puede ser:
• Decimal exacto: por ejemplo, 0,5 =
1
2
• Decimal periódico: por ejemplo, 0, 2̂ =
2
9
También se incluyen los enteros, ya que pueden escribirse como fracción (por ejemplo, 2 =
2
1
)
Es decir, este conjunto incluye a todos aquellos números que pueden ser escritos como
fracción. Algunos ejemplos de números racionales pueden ser:
1,5 =
3
2
12 =
12
1
0, 1̂ =
1
9
− 3 = −
3
1
Este conjunto también tiene infinitos elementos e incluye a los conjuntos ya vistos ℕ⊂ℤ⊂ℚ.
Siendo un conjunto denso, ya que entre dos números racionales siempre es posible encontrar
7
otro racional. Sin embargo, no es completo, debido a que hay puntos en la recta numérica que
no son racionales.
Para completar la recta numérica aparecen los números irracionales (𝕀), que no pueden
expresarse como fracción y cuya expresión decimal es infinita no periódica. Algunos ejemplos:
𝜋 = 3,1415926 … 𝑒 = 2,718281 … √2 = 1,414213 …
Así, los números racionales unidos a los irracionales conforman el conjunto de los números
reales (ℝ).
ℝ = ℚ ∪ 𝕀
Este conjunto es denso y completo siendo representado en su totalidad por la recta numérica.
Es importante para comenzar con esta lectura que se tome conocimiento de algunos de los
símbolos propios del lenguaje matemático.
= igual < menor que ⊂ incluido {},∅ vacío
≠ distinto ≤ menor e igual que ∧ y ⟹ implica
≅ aproximado ∃ existe ∨ o ⟺ doble implicación
~ proporcional ∄ no existe / tal que ⫽ paralelo
> mayor que ∈ pertenece ∪ unión ⊥ perpendicular
≥ mayor o igual que ∉ no pertenece ∩ intersección ∡ ángulo
Operaciones con números enteros
Adición y sustracción
Para sumar dos números enteros debemos tener en cuenta el signo de cada número:
• Si son iguales, sumamos su valor absoluto y el signo es el de ambos.
• Si son distintos, restamos los valores absolutos y el signo es el del número con
mayor valor absoluto.
Por ejemplo: 2 + 5 = 7 − 2 – 5 = − 7
2 – 5 = − 3 − 2 + 5 = 3
Para restar dos números enteros 𝑎 y 𝑏 operamos de la siguiente manera:
𝑎 – 𝑏 = 𝑎 + (−𝑏)
Es decir, a 𝑎 le sumamos – 𝑏 (el opuesto del número 𝑏).
Por ejemplo: 2 – 5 = 2 + (−5) = −3 4 – (−5) = 4 + 5 = 9
8
Supresión de paréntesis
• Los paréntesis precedidos por un signo + podemos suprimirlos, conservando los
signos de los términos que encierran.
Por ejemplo: Realizar la siguiente operación
2 + ( 4 – 5 )– 6 + ( − 1 + 3 ) =
Como ambos paréntesis están precedidos por signos positivos, entonces:
2 + 4 – 5 – 6 – 1 + 3 =
Ahora podemos agrupar los términos positivos, por otro lado, los negativos y los restamos
(esto es opcional para ordenar el cálculo):
( 2 + 4 + 3 )– ( 5 + 6 + 1 ) =
9 – 12 = − 3
• Los paréntesis precedidos por un signo - podemos suprimirlos, cambiando los signos
de los términos que encierran.
Por ejemplo: Realizar la siguiente operación
6 – ( 7 – 5 )– 2 – ( − 4 + 3 ) =
Como ambos paréntesis están precedidos por signos positivos, entonces:
6 – 7 + 5 – 2 + 4 – 3 =
Agrupamos:
( 6 + 5 + 4 ) – ( 7 + 2 + 3 ) =
15 – 12 = 3
Supresión de paréntesis, corchetes y llaves
Se suprimen en orden: primero los paréntesis ( ), luego los corchetes [ ] y por último las llaves
{ }. Para hacerlo, seguimos el mismo procedimiento que usamos para suprimir paréntesis
comunes. Es importante mirar el signo que está justo antes del signo de agrupación:
• Si hay un signo +, los signos de adentro no cambian.
• Si hay un signo –, los signos de adentro cambian todos.
Por ejemplo: Realizar la siguiente operación
21 − {20 − [10 − (8 − 3) + (8 + 9) − 11] + 2} + 9 =
1. Suprimimos paréntesis
Recordamos: si hay un signo menos delante del paréntesis, cambiamos los signos de
adentro, sino se conserva el mismo signo.
21 − {20 − [10 − 8 + 3 + 8 + 9 − 11] + 2} + 9 =
2. Suprimimos corchetes
9
Corchetes precedidos por –, así que cambiamos todos los signos de adentro:
21 − {20 − 10 + 8 − 3 − 8 − 9 + 11 + 2} + 9 =
3. Suprimimos llaves
Las llaves también están precedidas por –, así que cambiamos todos los signos:
21 − 20 + 10 − 8 + 3 + 8 + 9 − 11 − 2 + 9 =
4. Podemos cancelar el −8 y el 8 pues la suma es cero, es decir −8 + 8 = 0
21 − 20 + 10 + 3 + 9 − 11 − 2 + 9 =
5. Agrupamos los términos (opcional para ordenar el cálculo):
(21 + 10 + 3 + 9 + 9) − (20 + 11 + 2) =
5. Resolvemos:
52 − 33 = 𝟏𝟗
Multiplicación y división
Regla de signos:
• Cuando se multiplican o dividen dos números de igual signo, el resultado será positivo.
Por ejemplo: (−2) ∙ (−3) = 6 , 6 ∙ 2 = 12
• Cuando se multiplican o dividen dos números de distinto signo, el resultado será
negativo.
Por ejemplo: (−5) ∙ 3 = −15 , 5 ∙ (−3) = −15
Ejercicio resuelto: Resolver
(−1 − 8): (−3) + (9 − 2 ∙ 5) ∙ (−2) ∙ (−2) =
En este caso tenemos dos términos bien definidos. Recordemos que los signos de + y – separan
en términos:
(⏞− 1 − 8) : ( − 3 )
𝑝𝑟𝑖𝑚𝑒𝑟 𝑡𝑒𝑟𝑚𝑖𝑛𝑜
+ (⏞9 − 2 ∙ 5 ) ∙ ( − 2 ) ∙ ( − 2 )
𝑠𝑒𝑔𝑢𝑛𝑑𝑜 𝑡𝑒𝑟𝑚𝑖𝑛𝑜
=
A su vez, el segundo término, en el primer paréntesis también se puede separar
(⏞− 1 − 8) : ( − 3 ) + (⏞9 − 2⏞∙ 5) ∙ (−2) ∙ (−2)
⏞
=
Resolvemos los productos
(⏞− 1 − 8) : ( − 3 ) + (⏞9 − 10 ) ∙ 4 =
Luego las sumas/ restas
(⏞− 9 ) : ( − 3 ) + (⏞− 1 ) ∙ 4 =
10
En el primer término dividimos y en el segundo multiplicamos
3 + (−4) =
Finalmente operamos
3 − 4 = −𝟏
Observación: la división por cero es una operación que no está definida. Esto significa que no
se puede realizar una operación de división cuando el divisor es cero. Recuerde entonces: no
se puede dividir por cero.
Propiedad conmutativa
En matemáticas, la propiedad conmutativa establece que el orden de los elementos no afecta
al resultado de una operación. En el caso de la multiplicación de números enteros, esto se
cierto, es decir, el resultado es el mismo sin importar el orden de los elementos. Por ejemplo
2 ∙ 3 = 3 ∙ 2. Ambas expresiones dan por resultado 6 lo que demuestra que la multiplicación
de números enteros sigue la propiedad conmutativa.
Sin embargo, en el caso de la división de números enteros, esta propiedad no se cumple. El
resultado de dividir un número por otro puede cambiar si se intercambian los números. Por
ejemplo: 6 ÷ 2=3 pero 2 ÷ 6=1/3. Esto muestra que el orden de los números sí afecta el
resultado en la división de números enteros, lo que significa que la propiedad conmutativa no
se cumple en este caso.
En resumen, mientras que la multiplicación de números enteros sigue la propiedad
conmutativa, la división de números enteros no lo hace.
Potenciación
Si 𝒂 es cualquier número y 𝒏 un número entero positivo, entonces definimos
𝒂
𝒏 = 𝒂⏟. 𝒂 … . 𝒂
𝒏 𝒇𝒂𝒄𝒕𝒐𝒓𝒆𝒔 𝒂
(se multiplica 𝑎 por sí mismo 𝑛 veces). Además, por convención, definimos:
𝒂
𝟎 = 𝟏 (siempre que 𝒂 ≠ 𝟎)
Notación:
Potencias con base negativa y positiva
Cuando la base es negativa, el signo del resultado depende de si el exponente es par o impar:
• Si el exponente es par, el resultado es positivo.
• Si el exponente es impar, el resultado es negativo.
5
𝟐 = 25
Base
Exponente
Potencia
11
Ejemplos:
(−2)
2 = (−2) ⋅ (−2) = 4 (exponente par → resultado positivo)
(−2)
3 = (−2) ⋅ (−2) ⋅ (−2) = −8 (exponente impar → resultado negativo
¡Cuidado! No es lo mismo:
(−3)
2 = 9 (la base negativa está entre paréntesis)
que
−3
2 = −9 (solo se eleva el 3, luego se aplica el signo menos)
Cuando la base es positiva el resultado siempre es positivo, sin importar si el exponente es
par o impar.
Propiedades de la potenciación
• Propiedad distributiva de la potenciación con respecto a la multiplicación
(𝑎 ⋅ 𝑏)
𝑛 = 𝑎
𝑛
⋅ 𝑏
𝑛
Por ejemplo: (3 ⋅ 5)
2 = 3
2
⋅ 5
2
• Propiedad distributiva de la potenciación con respecto a la división
(𝑎: 𝑏)
𝑛 = 𝑎
𝑛
: 𝑏
𝑛
Por ejemplo: (6: 3)
3 = 6
3
: 3
3
• Propiedad del producto de potencias de igual base
𝑎
𝑛
⋅ 𝑎
𝑚 = 𝑎
𝑛+𝑚
Por ejemplo: 2
3
⋅ 2
2 = 2
3+2
• Propiedad del cociente de potencias de igual base
𝑎
𝑛
: 𝑎
𝑚 = 𝑎
𝑛−𝑚
Por ejemplo: 2
3
: 2
2 = 2
3−2
• Propiedad de la potencia de potencia
(𝑎
𝑛 )𝑚 = 𝑎
𝑛⋅𝑚
Por ejemplo: (3
2
)
3 = 3
2∙3
• Todo número potenciado a la 1 es el mismo número
Por ejemplo: 2
1 = 2
Las potencias NO son distributivas respecto a la suma y a la resta.
Para calcular (2 + 3)
2
, primero sumamos los términos dentro del paréntesis, lo que nos da
2 + 3 = 5. Luego elevamos el resultado del cuadrado, obteniendo 5
2 = 25. Por lo tanto,
12
el resultado correcto de (2 + 3)
2 es 25, que no es lo mismo que 2
2 + 3
2 = 4 + 9 = 13.
Este ejemplo ilustra que la potenciación no es distributiva respecto a la suma.
De manera similar, para calcular (4 − 2)
3
, primero restamos los términos dentro del
paréntesis, lo que nos da 4 − 2 = 2. Luego elevar el resultado al cubo, 2
3 = 8. Por lo tanto,
el resultado correcto de (4 − 2)
3 = 8. Esto no es lo mismo que 4
3 − 2
3 = 64 − 8 = 56.
Este ejemplo muestra que la potenciación no es distributiva respecto de la resta.
(𝒂 + 𝒃)
𝒏 ≠ 𝒂
𝒏 + 𝒃
𝒏
Radicación
La radicación es la operación inversa a la potenciación. Se escribe √𝑎
𝑛
 la raíz de índice 𝑛 o raíz
enésima de 𝑎, donde llamamos:
√𝒂
𝒏 = 𝒄
Se distinguen dos casos según el índice sea par o impar:
Raíces de índice par
• Si el radicando es positivo: √𝑎
𝑛 = 𝑐 ⇔ 𝑐
𝑛 = 𝒂 𝑐𝑜𝑛 𝒄 > 𝟎 (𝒄 𝒆𝒔 𝒑𝒐𝒔𝒊𝒕𝒊𝒗𝒐).
• Si el radicando es negativo: √𝑎
𝑛
no tiene solución en el conjunto de números reales,
porque ningún número real elevado a un exponente par da un resultado negativo.
Por ejemplo:
a) √4 = 𝟐 𝑝𝑜𝑟𝑞𝑢𝑒 𝟐
2 = 4 𝑐𝑜𝑛 𝟐 > 𝟎. LA SOLUCION ES UNICA.
b) √−16 4
𝑛𝑜 𝑡𝑖𝑒𝑛𝑒 𝑠𝑜𝑙𝑢𝑐𝑖𝑜𝑛 𝑒𝑛 ℝ.
c)
Raíces de índice impar
La raíz enésima existe siempre, ya que los números negativos también tienen raíces impares.
√𝑎
𝑛 = 𝑐 ⇔ 𝑐
𝑛 = 𝒂
• Si el radicando es positivo entonces 𝑐 > 0 (𝑐 𝑒𝑠 𝑝𝑜𝑠𝑖𝑡𝑖𝑣𝑜).
• Si el radicando es negativo entonces 𝑐 < 0 (𝑐 𝑒𝑠 𝑛𝑒𝑔𝑎𝑡𝑖𝑣𝑜).
Por ejemplo:
a) √27 3 = 𝟑 𝑝𝑜𝑟𝑞𝑢𝑒 3
3 = 27.
b) √−32 5 = −2 𝑝𝑜𝑟𝑞𝑢𝑒 (−2)
5 = −32.
Además, √0
𝑛 = 0 sea 𝑛 par o impar.
En todos los casos, si la raíz enésima existe en ℝ, entonces es única.
Ejercicio resuelto: Resolver el siguiente ejercicio combinado
[4 − 5 ∙ (−3) + 2 − (2 − 5)
2
]. √5 ∙ 2
3 − 2
2 =
Índice
Radicando Raíz enésima
13
Identificamos los términos a resolver: Dentro del corchete tenemos cuatro términos bien
definidos, y dentro de la raíz cuadrada, dos.
[⏞4 − 5⏞ ∙ (− 3 ) + ⏞2 − (2 − 5) ⏞ 2
]. √5 ∙ 2 ⏟ 3 − 2⏟2 =
Resolvemos las potencias
[⏞4 − 5⏞ ∙ (− 3 ) + ⏞2 − (2 − 5) ⏞ 2
]. √5⏟∙ 8 − ⏟4 =
Calculamos la resta dentro del paréntesis
[⏞4 − 5⏞ ∙ (− 3 ) + ⏞2 − (−3) ⏞ 2
]. √5⏟∙ 8 − ⏟4 =
Calculamos la potencia
[⏞4 − 5⏞ ∙ (− 3 ) + ⏞2 − ⏞9]. √5⏟∙ 8 − ⏟4 =
Resolvemos las multiplicaciones
[⏞4 − (⏞− 15 ) + ⏞2 − ⏞9]. √40 − 4 =
Eliminamos paréntesis
[4 + 15 + 2 − 9]. √40 − 4 =
Operamos sumas y restas
[12]. √36 =
Extraemos raíz cuadrada y finalizamos
12 ∙ 6 =72
Operaciones con números racionales
Recordemos que los números racionales son todos aquellos números que se pueden escribir
como fracción, es decir, son de la forma 𝒂
𝒃
 donde 𝒂 𝑦 𝒃 son números enteros y 𝒃 ≠ 𝟎
Adición y sustracción
• Cuando las fracciones tienen el mismo denominador, se suman o se restan los
numeradores.
Ejemplos:
3
7
+
2
7
=
5
7
5
9
−
1
9
=
4
9
• Cuando las fracciones tienen distinto denominador hay que hallar un común
denominador, preferiblemente el mínimo común múltiplo (m.c.m) de los
denominadores. Una vez que se tiene el m.c.m, hay que convertir ambas fracciones a
fracciones equivalentes con ese denominador, luego sumar o restar los numeradores
y finalmente simplificar el resultado si es posible, esto se realiza dividiendo numerador
y denominador por un mismo número.
Ejemplos:
14
2
3
+
5
4
𝑚. 𝑐. 𝑚(3; 4) = 12
Entonces
2
3
+
5
4
=
8
12 +
15
12 =
También podemos resolver sin escribir las fracciones equivalentes. En lugar de convertir
cada fracción, usamos el mínimo común múltiplo (m.c.m), dividimos el m.c.m por cada
denominador y multiplicamos ese resultado por el numerador correspondiente, como
se muestra en el siguiente ejercicio.
Ejemplo:
5
6
+
1
4
=
2 ∙ 5 + 3 ∙ 1
12 =
13
12 𝑚. 𝑐. 𝑚(6; 4) = 12
Multiplicación y división
• Para la multiplicación sólo se debe multiplicar numerador con numerador y
denominador con denominador.
𝒂
𝒃
⋅
𝒄
𝒅
=
𝒂 ⋅ 𝒄
𝒃 ⋅ 𝒅

Antes de multiplicar, si es posible, se simplificará cruzado (un numerador con el
denominador del otro). Esto hace que el resultado sea más fácil de simplificar después.
Ejemplo:
3
4
⋅ (−
5
2
) = −
15
8
• Para la división se debe invertir la fracción que divide y luego multiplicar.
𝒂
𝒃
:
𝒄
𝒅
=
𝒂
𝒃
⋅
𝒅
𝒄

Ejemplo:
4
7
:
5
2
=
4
7
⋅
2
5
=
8
35
Potenciación
• Cuando elevamos una fracción a un número entero positivo, se eleva tanto el
numerador como el denominador.
(
𝑎
𝑏
)
𝑛
=
𝑎
𝑛
𝑏
𝑛
(𝑐𝑜𝑛 𝑏 ≠ 0)
Ejemplos:
(
2
3
)
2
=
2
2
3
2 =
4
9
(
5
2
)
3
=
5
3
2
3 =
125
8
15
(
2
3
)
4
=
2
4
3
4 =
16
81
• Si el exponente es negativo, se invierte la fracción (se toma el recíproco) y se hace
positivo el exponente
(
𝑎
𝑏
)
−𝑛
= (
𝑏
𝑎
)
𝑛
=
𝑏
𝑛
𝑎
𝑛
Ejemplos:
(
3
4
)
−2
= (
4
3
)
2
=
16
9
(−
5
2
)
-2
= (−
2
5
)
2
=
4
25
• También se pueden aplicar las propiedades generales de la potenciación ya explicadas
para los números enteros (producto de potencias, potencia de una potencia, etc.)
Ejemplo:
(
2
5
)
3
· (
2
5
)
2
= (
2
5
)
5
Radicación
• Se saca la raíz del numerador y del denominador por separado (si es posible).
√
𝑎
𝑏
𝑛
=
√𝑎
𝑛
√𝑏
𝑛
(𝑐𝑜𝑛 𝑎, 𝑏 ≥ 0 𝑦 𝑏 ≠ 0)
Ejemplos:
√
9
16 =
√9
√16
=
3
4
√
8
27
3
=
√8
3
√27 3 =
2
3
• Si no se puede sacar la raíz exacta, dejamos la expresión en forma de raíz o la
convertimos en decimal cuando sea necesario.
√
2
5
=
√2
√5
A veces se racionaliza el denominador para evitar raíces en él:
√2
√5
= (
√2
√5
) ∙ (
√5
√5
) =
√10
5
• Simplificar la fracción antes de sacar la raíz facilita el cálculo.
16
Ejemplo:
√
50
2
= √25 = 5
Ejercicio resuelto: Resolver el siguiente ejercicio combinado
(3
3 ÷ (
3
4
)
2
− 5
2) − [−3 ∙ (√
1
4
− 1)]
2
+ √
25
144
Identificamos tres términos principales:
(3
3 ÷ (
3
4
)
2
⏟
− 5⏟2)
⏞
− [−3 ∙ (√
1
4
− 1)]
⏞ 2
+ √
25
144
⏞
Resolvemos potencias y raíces
(27 ÷
9
⏟ 16
− 25⏟)
⏞
− [−3 ∙ (
1
2
− 1)]
⏞ 2
+
5
12
⏞
División y resta
(27 ∙
16
⏟ 9
− 25⏟)
⏞
− [−3 ∙ (−
1
2
)]
⏞ 2
+
5
12
⏞
Calculamos los productos
(48⏟ − 25⏟)
⏞
− [
3
2
]
⏞2
+
5
12
⏞
Restamos y realizamos la potencia
23 −
9
4
+
5
12
Sacamos m.c.m., operamos y simplificamos
23 ∙ 12 − 9 ∙ 3 + 5
12 =
23 ∙ 12 − 9 ∙ 3 + 5
12 =
254
12 =
𝟏𝟐𝟕
𝟔
Propiedades de la radicación
Las propiedades de la radicación son útiles para manipular expresiones que involucran
radicales. Aun cuando antes no las hayamos trabajado explícitamente con números enteros,
es importante remarcar que estas propiedades son válidas tanto para números enteros,
como para fracciones (números racionales) y también para números reales en general,
siempre que las raíces estén bien definidas. Las principales propiedades son:
• Raíz de una raíz: Cuando tenemos la raíz 𝑚-ésima de la raíz 𝑛-ésima de 𝑎 , podemos
escribir una única raíz cuyo índice es el producto 𝑚 ∙ 𝑛 es decir
√ √𝑎
𝑚 𝑛 = √𝑎
𝑚∙𝑛
• Raíz de un producto: Cuando tenemos la raíz 𝑛-ésima de un producto, podemos
distribuir la raíz a cada uno de los factores del producto, es decir
17
√𝑎 ∙ 𝑏
𝑛
= √𝑎
𝑛
∙ √𝑏
𝑛
• Raíz de un cociente: Cuando tenemos la raíz 𝑛-ésima de un cociente, podemos
distribuir la raíz a cada uno de los factores del cociente, esto es:
√
𝑎
𝑏
𝑛
=
√𝑎
𝑛
√𝑏
𝑛
• Eliminación del radical: √𝑎
𝑛
𝑛 = 𝑎 ⇔ 𝑛 𝑒𝑠 𝑖𝑚𝑝𝑎𝑟 y √𝑎
𝑛
𝑛 = |𝑎| ⇔ 𝑛 𝑒𝑠 𝑝𝑎𝑟, siendo
este último el valor absoluto de 𝑎 que geométricamente se define como la distancia
de 𝑎 al cero y analíticamente como: |𝑎| = {
𝑎 𝑠𝑖 𝑎 ≥ 0
−𝑎 𝑠𝑖 𝑎 < 0
.
Estas propiedades son válidas siempre que la raíz esté bien definida en el conjunto de los
números reales. En particular, cuando el índice de la raíz es par, los valores dentro del radical
deben ser no negativos para que el resultado sea un número real. Por eso, hay que prestar
atención a las condiciones de aplicación. Por ejemplo, la propiedad de la raíz de un producto
o un cociente para el caso de índice par solo es válida si los factores del producto o del cociente
son números reales no negativos. Veamos algunos ejemplos:
√900 = √9 ∙ 100 = √9 ∙ √100 = 3 ∙ 10 = 30
√27 ∙ 8
3
= √27 3
∙ √8
3
= 3 ∙ 2 = 6
√
4
9
=
√4
√9
=
2
3
√−
8
27
3
= √
−8
27
3
=
√−8
3
√27 3 =
−2
3
= −
2
3
√√16 = √16 4
= 2
√√256
4
= √256 8
= 2
Potencia fraccionaria
Por otro lado, las potencias fraccionarias guardan una estrecha relación con las raíces:
𝑛
√𝑎𝑚 = 𝑎
𝑚
𝑛
Sin embargo, esta relación es válida bajo ciertas condiciones. Por eso, es importante tener
precaución, especialmente cuando el índice de la raíz es par y el radicando es negativo. Al
igual que con las otras propiedades, debemos asegurarnos de que los números involucrados
cumplan con las condiciones necesarias para que la raíz esté bien definida en el conjunto de
los números reales.
En este contexto, podemos agregar que las propiedades habituales de las potencias siguen
siendo válidas, ya que se trata simplemente de potencias con exponentes fraccionarios.
√5
6
3
= 5
6
3 = 5
2 = 25 √4
6 = 4
6
2 = 4
3 = 64
Observación: La radicación no es distributiva respecto a la suma ni a la resta
Una confusión común es pensar que se puede "distribuir" la raíz sobre una suma o una resta.
Sin embargo, esto no es válido:
Respecto a la suma
• √4 + 9 ≠ √4 + √9
• √4 + 9 = √13 que es un numero irracional.
• √4 + √9 = 2 + 3 = 5
Respecto a la resta
• √16 − 9 ≠ √16 − √9
• √16 − 9 = √7 que es un numero irracional.
• √16 − √9 = 4 − 3 = 1
Estos ejemplos muestran que la radicación no es distributiva respecto de la suma ni de la
resta, y por eso hay que actuar con cuidado al trabajar con expresiones que involucran
radicales y operaciones combinadas.
Pasaje de decimal a fracción
Decimales exactos, son aquellos números que tienen una cantidad finita de cifras decimales,
y cuando los expresamos como fracción, el denominador es una potencia de 10. Por ejemplo:
1,52 =
152
100 ó 0,923 =
923
1000
Para escribirlo en forma de fracción se colocan en el numerador todas las cifras del número y
se divide por la unidad seguida de ceros, con tantos ceros como cifras decimales tenga el
número.
Decimales periódicos puros, son aquellos números que repiten la totalidad de sus cifras
decimales en forma periódica. Por ejemplo:
1, 52̂ =
152 − 1
99 ó 0, 923 ̂ =
923
999
Para escribirlo en forma de fracción se colocan en el numerador todas las cifras del número y
se resta la parte entera. Dividiendo luego por tantos 9 como cifras decimales tenga el número.
Decimales periódicos mixtos, son aquellos números que tiene cifras decimales periódicas y
no periódicas. Por ejemplo:
1,52̂ =
152 − 15
90 ó 0,923̂ =
923
990
Para escribirlo en forma de fracción se colocan en el numerador todas las cifras del número y
se resta la parte no periódica. Dividiendo luego por tantos 9 como cifras decimales
periódicas tenga el número y tantos 0 como cifras no periódicas.
19
Unidad 2
Expresiones algebraicas
Expresiones Algebraicas
Si consideramos el conjunto de números reales y un conjunto de variables (indicadas con
letras) y combinamos elementos de estos conjuntos con operaciones aritméticas obtenemos
las llamadas expresiones algebraicas. Veamos algunos ejemplos
Expresiones algebraicas
2 − 𝑥
−3 2𝑥
3𝑦 − 16𝑦
𝑥
5 − 4
𝑥
2
𝑥
2 + 2𝑥𝑦 + 𝑦
2 √𝑡 − 3𝑡
Llamaremos expresiones algebraicas enteras a aquellas en las que las variables están
elevadas a exponentes enteros no negativos. Veamos algunos ejemplos
Expresiones algebraicas enteras
2𝑥 − 3𝑥
3 2𝑥
3𝑦 − 16𝑦 √3 − √2𝑔 𝑥
2 + 2𝑥𝑦 + 𝑦
2 2 − 𝑡
Llamaremos términos algebraicos a los sumandos de una expresión algebraica.
Por ejemplo, la siguiente expresión algebraica tiene tres términos
En cada término se distinguen una parte numérica también llamada coeficiente (que es el
número real) y una parte literal (que incluye las variables con sus exponentes)
Aquellos términos algebraicos con idéntica parte literal, se denominan términos semejantes,
por ejemplo
Términos algebraicos semejantes
3
4
𝑥
4 −0.3𝑥
4 3𝑥
4 −√7𝑥
4
En este capítulo estudiaremos expresiones algebraicas con una sola variable (𝑥).
Polinomios
Definición: un polinomio 𝑃 es una expresión algebraica entera. Para el caso de una variable,
se llama polinomio de grado 𝒏 a toda expresión de la forma:
𝑃(𝑥) = 𝑎𝑛𝑥
𝑛 + 𝑎𝑛−1𝑥
𝑛−1 + ⋯ + 𝑎2𝑥
2 + 𝑎1𝑥 + 𝑎0
donde 𝑛 ∈ ℕ0, 𝑎𝑛, 𝑎𝑛−1, … , 𝑎2, 𝑎1, 𝑎0 ∈ ℝ y 𝑎𝑛 ≠ 0 . Estos números son llamados
coeficientes del polinomio 𝑃, en particular, 𝑎𝑛 es el coeficiente principal y 𝑎0 el término
independiente.
−𝟐 𝒙
𝟐𝒚
Coeficiente Parte literal
𝒙
𝟐 − 𝟐𝒙𝒚 + 𝒚
𝟐
20
Observación: De la definición de polinomio se puede observar que las expresiones del tipo
𝑃(𝑥) = 𝑎0 son polinomios de grado 0, pero no incluyen a 𝑃(𝑥) = 0 ya que debe ser 𝑎𝑛 ≠ 0.
Este caso lo consideramos aparte:
Definición: Polinomio nulo es aquel que tiene todos sus coeficientes iguales a 0 y se anota
𝑃(𝑥) = 0
Vamos a convenir en que el polinomio nulo no tiene grado.
Características de los polinomios:
✓ La notación 𝑃(𝑥) es para indicar que el polinomio es una expresión algebraica en la
variable 𝑥.
✓ El grado de un polinomio es 𝑛, es el mayor exponente de la variable 𝑥 y lo denotaremos
por 𝑔𝑟(𝑃).
✓ Un polinomio se llama mónico cuando su coeficiente principal 𝑎𝑛 = 1.
✓ Se dice que un polinomio está ordenado cuando los términos algebraicos que lo
forman están escritos en forma creciente o decreciente según los exponentes de sus
variables. En este curso los ordenaremos en forma decreciente.
✓ Un polinomio está completo si tiene todos los términos.
✓ Según la cantidad de términos, un polinomio se denomina monomio (si tiene un
término); binomio (dos términos); trinomio (tres términos); cuatrinomio (cuatro
términos).
Polinomio Coeficiente
principal
Término
independiente
Grado del
polinomio Clasificación
𝑃(𝑥) = −5𝑥
2 − 2𝑥 + 1 -5 1 2 Trinomio
𝑄(𝑥) = 2𝑥 2 0 1 Monomio
𝑅(𝑥) =
3
4
𝑥
4 −
1
2
𝑥
2 + 𝑥 + 7
3
4
7 4 Cuatrinomio
𝑆(𝑥) = 34𝑥
5 − 17𝑥
2 34 0 5 Binomio
𝑇(𝑥) = −√5𝑥
3 −√5 0 3 Monomio
Valor numérico o especialización de un polinomio
El valor numérico de un polinomio 𝑃(𝑥), es el valor que toma el mismo para un determinado
valor de la variable 𝑥. Se suele decir que el polinomio 𝑃(𝑥) está especializado en ese valor.
Polinomio Valor numérico en…
𝑃(𝑥) = −2𝑥
2 + 3𝑥 − 1 𝑥 = −1 𝑃(−1) = −2(−1)
2 + 3(−1) − 1 = −2 − 3 − 1 = −6
𝑄(𝑥) = 3𝑥
4 + 𝑥
2 − 5 𝑥 = 1 𝑄(1) = 3. 1
4 + 1
2 − 5 = 3 + 1 − 5 = −1
𝑅(𝑥) = 𝑥
4 + 𝑥
3 − 6𝑥
2 𝑥 = 2 𝑅(2) = 2
4 + 2
3 − 6. 2
2 = 16 + 8 − 24 = 0
21
Operaciones entre polinomios
Suma de polinomios
La suma de dos polinomios es otro polinomio cuyos términos se obtienen sumando los
términos semejantes. Dicho de otra manera, dados dos polinomios 𝑃(𝑥) y 𝑄(𝑥) el polinomio
suma 𝑃(𝑥) + 𝑄(𝑥) se obtiene sumando entre si los términos de igual grado de cada uno de
los polinomios.
Ejemplo: Calcular 𝑃(𝑥) + 𝑄(𝑥), siendo
𝑃(𝑥) = 3𝑥
2 − 2𝑥 + 5
𝑄(𝑥) = 𝑥
2 + 4𝑥 − 1
𝑃(𝑥) + 𝑄(𝑥) = (3𝑥
2 − 2𝑥 + 5) + (𝑥
2 + 4𝑥 − 1) = (3𝑥
2 + 𝑥
2
) + (−2𝑥 + 4𝑥) + (5 − 1) =
= 4𝑥
2 + 2𝑥 + 4
Definición: se llama opuesto del polinomio 𝑃(𝑥) = 𝑎𝑛𝑥
𝑛 + ⋯ + 𝑎2𝑥
2 + 𝑎1𝑥 + 𝑎0 al
polinomio que sumado a 𝑃,da como resultado el polinomio nulo. El opuesto de 𝑃 tiene el
mismo grado que 𝑃 y sus coeficientes son opuestos de los coeficientes de 𝑃 .
Se denota por −𝑃:
−𝑃(𝑥) = −𝑎𝑛𝑥
𝑛 − ⋯ − 𝑎2𝑥
2 − 𝑎1𝑥 − 𝑎0
Ejemplo: El opuesto del polinomio 𝑃(𝑥) = −2𝑥
2 + 3𝑥 − 1 es el polinomio
−𝑃(𝑥) = 2𝑥
2 − 3𝑥 + 1
Ya que
𝑃(𝑥) + (−𝑃(𝑥)) = −2𝑥
2 + 3𝑥 − 1 + (2𝑥
2 − 3𝑥 + 1) =
= (−2 + 2)𝑥
2 + (3 − 3)𝑥 + (−1 + 1) = 0
Resta de polinomios
Dados dos polinomios 𝑃(𝑥) y 𝑄(𝑥) la resta 𝑃(𝑥) − 𝑄(𝑥) es el polinomio que se obtiene de
sumarle a 𝑃(𝑥) el opuesto del polinomio 𝑄(𝑥):
𝑃(𝑥) − 𝑄(𝑥) = 𝑃(𝑥) + (−𝑄(𝑥))
Ejemplo: Calcular 𝑃(𝑥) − 𝑄(𝑥), siendo
𝑃(𝑥) = 16𝑥 + 14
𝑄(𝑥) = 3𝑥
2 + 𝑥 − 9
Para realizar esta resta debemos sumar al polinomio 𝑃(𝑥) el opuesto de 𝑄(𝑥).
𝑃(𝑥) − 𝑄(𝑥) = 𝑃(𝑥) + (−𝑄(𝑥))
= (16𝑥 + 14) + (−3𝑥
2 − 𝑥 + 9)
= −3𝑥
2 + (16 − 1)𝑥 + (14 + 9)
= −3𝑥
2 + 15𝑥 + 23
Otra manera de realizar la resta de polinomios es directamente restando los términos
semejantes, es decir, aquellos que tienen la misma parte literal (misma variable y exponente).
22
Es recomendable ordenar los polinomios según los exponentes y usar paréntesis al aplicar la
resta.
Ejemplo: Calcular 𝑃(𝑥) − 𝑄(𝑥), siendo
𝑃(𝑥) = 3𝑥
2 − 2𝑥 + 5
𝑄(𝑥) = 𝑥
2 + 4𝑥 − 1
𝑃(𝑥) − 𝑄(𝑥) = (3𝑥
2 − 2𝑥 + 5) − (𝑥
2 + 4𝑥 − 1) = (3𝑥
2 − 2𝑥 + 5) + (𝑥
2 + 4𝑥 − 1)
= (3𝑥
2 − 𝑥
2
) + (−2𝑥 − 4𝑥) + (5 + 1) = 2𝑥
2 − 6𝑥 + 6
Multiplicación
Multiplicación de monomios
✓ Para multiplicar monomios se deben multiplicar los coeficientes entre sí y luego
multiplicar las partes literales aplicando las propiedades de la potenciación. Cuando
se multiplican dos o más monomios, el resultado es siempre un monomio.
Si alguno de los factores es el polinomio nulo el producto es el polinomio nulo
Ejemplos:
𝑎) (3𝑥) ⋅ (2𝑥) = 6𝑥
2 𝑏) (−4𝑥) ⋅ 𝑥
5
⋅ (
1
2
𝑥
2) = −2𝑥
8
Multiplicación de un polinomio por un número real
✓ Para multiplicar un polinomio por un número real, se aplica la propiedad distributiva
de la multiplicación respecto de la suma:
Ejemplo:
3 ∙ (2𝑥
3 − 3𝑥
2 + 5𝑥 − 1) = 3 ∙ 2𝑥
3 + 3 ∙ (−3𝑥
2
) + 3 ∙ 5𝑥 + 3 ∙ (−1) =
= 6𝑥
3 − 9𝑥
2 + 15𝑥 − 3
Multiplicación de un polinomio por un monomio
✓ Para multiplicar un monomio por un polinomio, se aplica la propiedad distributiva: se
multiplica el monomio por cada término del polinomio, uno a uno.
Ejemplo:
2𝑥 ⋅ (3𝑥
2 − 5𝑥 + 4) = 2𝑥 ⋅ 3𝑥
2 + 2𝑥 ⋅ (−5𝑥) + 2𝑥 ⋅ 4 = 6𝑥
3 − 10𝑥
2 + 8𝑥
Otro ejemplo:
−3𝑥
2
⋅ (𝑥
3 − 2𝑥 + 1) = −3𝑥
2
⋅ 𝑥
3 + (−3𝑥
2
) ⋅ (−2𝑥) + (−3𝑥
2
) ⋅ 1 = −3𝑥
5 + 6𝑥
3 − 3𝑥
2
Multiplicación de polinomios
✓ Para multiplicar dos polinomios, se aplica la propiedad distributiva: cada término del
primer polinomio se multiplica por todos los términos del segundo, y luego se suman
los productos obtenidos.
Ejemplos:
Multiplicar (𝑥 + 2) ⋅ (𝑥 + 3)
(𝑥 + 2)(𝑥 + 3) = 𝑥 ⋅ 𝑥 + 𝑥 ⋅ 3 + 2 ⋅ 𝑥 + 2 ⋅ 3 = 𝑥
2 + 3𝑥 + 2𝑥 + 6 = 𝑥
2 + 5𝑥 + 6
𝒙
𝒏
⋅ 𝒙
𝒎 = 𝒙
𝒏+𝒎
23
Multiplicar (2𝑥 − 1)(𝑥
2 + 3𝑥 − 4)
(2𝑥 − 1)(𝑥
2 + 3𝑥 − 4)=2𝑥 ⋅ 𝑥
2 + 2𝑥 ⋅ 3𝑥 + 2𝑥 ⋅ (−4) − 1 ⋅ 𝑥
2 − 1 ⋅ 3𝑥 − 1 ⋅ (−4) =
2𝑥
3 + 6𝑥
2 − 8𝑥 − 𝑥
2 − 3𝑥 + 4 = 2𝑥
3 + 5𝑥
2 − 11𝑥 + 4
Ejemplo resuelto
Resuelve la siguiente expresión combinando operaciones de suma, resta y multiplicación de
polinomios:
𝐸(𝑥) = 2(3𝑥
2 − 2𝑥 + 5) − (𝑥 − 3)(𝑥 + 4) + 5𝑥(2𝑥 − 1)
En este ejercicio tenemos tres términos bien definidos, en el primero se trata de una
multiplicación de un polinomio por un número real, el segundo es la multiplicación de dos
polinomios y el ultimo es el producto de un monomio por un polinomio. Una vez realizadas
estas tres operaciones se realiza las operaciones de suma y resta combinando términos
semejantes para simplificar la expresión final.
𝐸(𝑥) = 2(3𝑥 ⏟
2 − 2 𝑥 + 5 )
𝑝𝑟𝑖𝑚𝑒𝑟 𝑡𝑒𝑟𝑚𝑖𝑛𝑜
− (⏟𝑥 − 3 )( 𝑥 + 4 )
𝑠𝑒𝑔𝑢𝑛𝑑𝑜 𝑡𝑒𝑟𝑚𝑖𝑛𝑜
+ 5⏟𝑥 ( 2 𝑥 − 1 )
𝑡𝑒𝑟𝑐𝑒𝑟 𝑡𝑒𝑟𝑚𝑖𝑛𝑜
1. Multiplicamos el polinomio por 2:
2(3𝑥
2 − 2𝑥 + 5) = 6𝑥
2 − 4𝑥 + 10
2. Multiplicamos los binomios
(𝑥 − 3)(𝑥 + 4) = 𝑥
2 + 𝑥 − 12
3. Multiplicamos el monomio por el binomio:
5𝑥(2𝑥 − 1) = 10𝑥
2 − 5𝑥
Entonces tenemos
𝐸(𝑥) = 6𝑥
2 − 4𝑥 + 10 − (𝑥
2 + 𝑥 − 12) + 10𝑥
2 − 5𝑥
Podemos restar los primeros dos polinomios
𝐸(𝑥) = (6𝑥
2 − 𝑥
2
) + (−4𝑥 − 𝑥) + (10 − (−12)) + 10𝑥
2 − 5𝑥
𝐸(𝑥) = 5𝑥
2 − 5𝑥 + 22 + 10𝑥
2 − 5𝑥
Finalmente sumamos
𝐸(𝑥) = (5𝑥
2 + 10𝑥
2
) + (−5𝑥 − 5𝑥) + 22
Conclusión, el polinomio obtenido es:
𝐸(𝑥) = 15𝑥
2 − 10𝑥 + 22
Potencia de un monomio
Para resolver la potencia de un monomio se deben aplicar las propiedades:
• Distributiva de la potenciación respecto de la multiplicación
• Potencia de otra potencia
Ejemplos:
𝑎) (3𝑥)
4 = 3
4
∙ 𝑥
4 = 81𝑥
4 𝑏) (−
2
5
𝑥
7)
3
= (−
2
5
)
3
∙ (𝑥
7
)
3 = −
8
125 𝑥
21
(𝒙
𝒏
)
𝒎 = 𝒙
𝒏∙𝒎
(𝒂 ∙ 𝒃)
𝒏 = 𝒂
𝒏
∙ 𝒃
𝒏
24
Productos Notables
Ahora estudiaremos tres casos especiales de productos de polinomios: el cuadrado de un
binomio, el cubo de un binomio y el producto de binomios conjugados. Estos productos se
denominan productos notables porque aparecen con frecuencia en ejercicios matemáticos y
en diversas aplicaciones contextualizadas, y pueden resolverse rápidamente mediante reglas
sencillas.
Llamamos productos notables a aquellos productos de expresiones algebraicas que, por su
estructura particular, permiten ser resueltos aplicando fórmulas conocidas. Reconocer estas
estructuras es útil porque facilita los cálculos y permite resolver operaciones con mayor
rapidez y eficiencia.
Cuadrado de un binomio
El binomio al cuadrado es el más conocido de los productos notables y quizá el más
utilizado en los problemas algebraicos. El desarrollo del cuadrado de un binomio nos da un
trinomio cuadrado perfecto esto es “el cuadrado del primer término más el doble del
primer término por el segundo término más el cuadrado del segundo término”
Es fórmula proviene de aplicar la propiedad distributiva de la multiplicación dos veces. Es
decir, consideramos que (𝑎 + 𝑏)
2 = (𝑎 + 𝑏) ∙ (𝑎 + 𝑏) y multiplicamos los términos de
ambos binomios:
(𝑎 + 𝑏)(𝑎 + 𝑏) = 𝑎(𝑎 + 𝑏) + 𝑏(𝑎 + 𝑏) = 𝑎
2 + 𝑎𝑏 + 𝑎𝑏 + 𝑏
2 = 𝑎
2 + 2𝑎𝑏 + 𝑏
2
Esto demuestra cómo surge esta fórmula, que permite calcular el cuadrado de un binomio
de forma rápida, sin tener que expandir cada término manualmente.
Para el caso del binomio de una resta se tiene:
Para llagar a esta fórmula consideramos que (𝑎 − 𝑏)
2 = (𝑎 − 𝑏) ∙ (𝑎 − 𝑏) y multiplicamos
los términos de ambos binomios aplicando la propiedad distributiva:
(𝑎 − 𝑏)(𝑎 − 𝑏) = 𝑎(𝑎 − 𝑏) − 𝑏(𝑎 − 𝑏) = 𝑎
2 − 𝑎𝑏 − 𝑎𝑏 + 𝑏
2 = 𝑎
2 − 2𝑎𝑏 + 𝑏
2
Ejemplos:
(𝑥 + 3)
2 = 𝑥
2 + 2 ∙ 𝑥 ∙ 3 + 3
2 = 𝑥
2 + 6𝑥 + 9
(3𝑥 − 5)
2 = (3𝑥)
2 − 2 ∙ 3𝑥 ∙ 5 + 5
2 = 9𝑥
2 − 30𝑥 + 25
Cubo de un binomio
Análogamente con el cubo del binomio:
(𝒂 + 𝒃)
𝟑 = 𝒂
𝟑 + 𝟑 ∙ 𝒂
𝟐
∙ 𝒃 + 𝟑 ∙ 𝒂 ∙ 𝒃
𝟐 + 𝒃
𝟑
Trinomio cuadrado perfecto
(𝒂 + 𝒃)
𝟐 = 𝒂
𝟐 + 𝟐 ∙ 𝒂 ∙ 𝒃 + 𝒃
𝟐
Cuadrado de un binomio
(𝒂 − 𝒃)
𝟐 = 𝒂
𝟐 − 𝟐 ∙ 𝒂 ∙ 𝒃 + 𝒃
𝟐
25
En este caso, para llegar a esta fórmula consideramos que (𝑎 + 𝑏)
3 = (𝑎 + 𝑏)
2
∙ (𝑎 + 𝑏) y
utilizamos la formula del cuadrado del binomio desarrollada anteriormente:
(𝑎 + 𝑏)
2
∙ (𝑎 + 𝑏) = (𝑎
2 + 2𝑎𝑏 + 𝑏
2
) ∙ (𝑎 + 𝑏) = 𝑎
2
(𝑎 + 𝑏) + 2𝑎𝑏(𝑎 + 𝑏) + 𝑏
2
(𝑎 + 𝑏)
= 𝑎
2𝑎 + 𝑎
2𝑏 + 2𝑎𝑏𝑎 + 2𝑎𝑏𝑏 + 𝑏
2𝑎 + 𝑏
2𝑏
= 𝑎
3 + 𝑎
2𝑏 + 2𝑎
2𝑏 + 2𝑎𝑏
2 + 𝑏
2𝑎 + 𝑏
3 = 𝑎
3 + 3𝑎
2𝑏 + 3𝑎𝑏
2 + 𝑏
3
Para el caso de la resta se tiene:
Que se obtiene si consideramos que (𝑎 − 𝑏)
3 = (𝑎 − 𝑏)
2
∙ (𝑎 − 𝑏) de la siguiente manera:
(𝑎 − 𝑏)
2
∙ (𝑎 − 𝑏) = (𝑎
2 − 2𝑎𝑏 + 𝑏
2
) ∙ (𝑎 − 𝑏) = 𝑎
2
(𝑎 − 𝑏) − 2𝑎𝑏(𝑎 − 𝑏) + 𝑏
2
(𝑎 − 𝑏)
= 𝑎
2𝑎 − 𝑎
2𝑏 − 2𝑎𝑏𝑎 + 2𝑎𝑏𝑏 + 𝑏
2𝑎 − 𝑏
2𝑏
= 𝑎
3 − 𝑎
2𝑏 − 2𝑎
2𝑏 + 2𝑎𝑏
2 + 𝑏
2𝑎 − 𝑏
3 = 𝑎
3 − 3𝑎
2𝑏 + 3𝑎𝑏
2 − 𝑏
3
Ejemplos:
(𝑥 + 2)
3 = 𝑥
3 + 3𝑥
2
⋅ 2 + 3𝑥 ⋅ 2
2 + 2
3 = 𝑥
3 + 6𝑥
2 + 12𝑥 + 8
(2𝑥 − 1)
3 = (2𝑥)
3 − 3(2𝑥)
2
⋅ 1 + 3(2𝑥) ⋅ 1
2 − 1
3 = 8𝑥
3 − 12𝑥
2 + 6𝑥 − 1
Producto de binomios conjugados
Llamaremos binomios conjugados a aquellos que se diferencian únicamente por el signo de
uno de sus términos, por ejemplo
𝑎) (𝑥 − 3) 𝑦 (𝑥 + 3) 𝑏) (−𝑥
3 + 4𝑥) 𝑦 (𝑥
3 + 4𝑥)
Esta expresión se obtiene con la propiedad distributiva veamos en general que se obtiene
(𝑎 − 𝑏) ∙ (𝑎 + 𝑏) = 𝑎
2 + 𝑎 ∙ 𝑏 − 𝑏 ∙ 𝑎 − 𝑏
2 = 𝑎
2 − 𝑏
2
Ejemplos:
(𝑥 + 4)(𝑥 − 4) = 𝑥
2 − 16
(3𝑥 + 2)(3𝑥 − 2) = (3𝑥)
2 − 2
2 = 9𝑥
2 − 4
Casos especiales de factoreo
El factoreo es el proceso de descomponer una expresión algebraica en un producto de
factores más simples. Esto significa escribir una expresión como el producto de términos que,
multiplicados entre sí, dan como resultado la expresión original. El factoreo es útil para
simplificar las expresiones y resolver ecuaciones de manera más sencilla.
A continuación, se presentan dos casos comunes de factorización que se resuelven con reglas
fáciles de aplicar.
(𝒂 − 𝒃)
𝟑 = 𝒂
𝟑 − 𝟑 ∙ 𝒂
𝟐
∙ 𝒃 + 𝟑 ∙ 𝒂 ∙ 𝒃
𝟐 − 𝒃
𝟑
Producto de binomios conjugados Diferencia de cuadrados
(𝒂 − 𝒃). (𝒂 + 𝒃) = 𝒂
𝟐 − 𝒃
𝟐
26
Factor Común
Este caso consiste en identificar un término que se repite en todos los monomios de una
expresión. Ese término puede extraerse como factor común y colocarse fuera de un
paréntesis, simplificando la expresión.
Por ejemplo, si tenemos:
𝑎 ∙ 𝑏 + 𝑎 ∙ 𝑐 = 𝑎 ∙ (𝑏 + 𝑐)
Cuando todos los términos de un polinomio tienen una parte en común, se puede aplicar el
método del factor común, que consiste en “sacar afuera” aquello que todos los términos
comparten.
Para aplicarlo:
• Se busca el máximo común divisor (MCD) de los coeficientes numéricos de todos los
términos.
• Si todos los términos tienen la misma letra (parte literal), se extrae esa letra con el
menor exponente con que aparece.
Ejemplo:
6𝑥
4 − 9𝑥
3 + 3𝑥
2 = 3𝑥
2
(2𝑥
2 − 3𝑥 + 1)
En este caso:
• El MCD entre 6, 9 y 3 es 3.
• Todos los términos tienen 𝑥, y el menor exponente es 2 → se saca 𝑥
2
.
Otro ejemplo
𝑄(𝑥) = 30𝑥
6 + 18𝑥
5 − 42𝑥
4 + 6𝑥
3
𝑄(𝑥) = 6𝑥
3
. (5𝑥
3 + 3𝑥
2 − 7𝑥 + 1)
En este caso:
• El MCD entre 30, 18 , 42 y 6 es 6.
• Todos los términos tienen 𝑥, y el menor exponente es 3 → se saca 𝑥
3
.
Diferencia de Cuadrados
La diferencia de cuadrados es un caso especial de factorización que ocurre cuando una
expresión tiene la forma de una resta entre dos términos elevados al cuadrado. Es decir, si
tenemos una expresión de la forma:
𝑎
2 − 𝑏
2
Podemos factorizarla usando una fórmula muy sencilla que nos dice que la diferencia de
cuadrados se descompone como el producto de una suma por una resta de las mismas
cantidades:
𝑎
2 − 𝑏
2 = (𝑎 + 𝑏)(𝑎 − 𝑏)
Esta propiedad es muy útil y se aplica siempre que tengamos una expresión en la que ambas
cantidades sean perfectos cuadrados y estén separadas por un signo de resta.
Ejemplo:
Factorizar 𝑥
2 − 9
Podemos reconocer que x2 es un cuadrado perfecto (es decir, 𝑥
2 = (𝑥)
2
) y 9 también es un
cuadrado perfecto (porque 9 = 3
2
).
Por lo tanto, aplicamos la fórmula de la diferencia de cuadrados:
𝑥
2 − 9 = (𝑥 + 3)(𝑥 − 3)
De esta manera, hemos factorizado la diferencia de cuadrados 𝑥
2 − 9 como el producto de
dos binomios (𝑥 + 3)(𝑥 − 3).
27
Unidad 3
Ecuaciones
Ecuaciones de Primer grado
Se denomina ecuación de primer grado o lineal a una igualdad que tiene una o más variables
elevadas a la primera potencia (es decir, elevada a la potencia uno). Resolver una ecuación
lineal significa encontrar el valor, o los valores, de las variables con los que se verifica dicha
igualdad.
Por ejemplo: 3𝑥 + 8 = 10 + 𝑥 es una ecuación
𝑥 = 2 no es solución pues 3.2 + 8 ≠ 10 + 2 ya que 14 ≠ 12
𝑥 = 1 es solución pues 3.1 + 8 = 10 + 1 ya que 11 = 11
Resolución de ecuaciones de Primer grado
Para resolver ecuaciones de primer grado con una incógnita lo que se hace, de ser posible, es
despejar la incógnita, es decir realizar en la ecuación las operaciones convenientes con el
objetivo de que la incógnita quede igualada a su valor.
Veamos un ejemplo: 5𝑥 + 4 = 14
para hallar el valor de “𝑥” debemos buscar un número que sumado (o restado) al “+4”, se
transforme en el elemento neutro de la adición (es decir, en 0). Debe realizarse la misma
operación en ambos miembros para no alterar la igualdad. Entonces restaremos 4:
5𝑥 + 4 − 4 = 14 − 4
Así nos queda
5𝑥 = 10
Ahora debemos dividir al 5 por un número que lo transforme en el elemento neutro de la
multiplicación (es decir, en 1), también en ambos miembros para no alterar la igualdad.
O sea
5
5
𝑥 =
10
5
y nos queda que 𝒙 = 𝟐, es la solución de la ecuación, además podemos verificar que:
5.2 + 4 = 14
14 = 14
Este procedimiento de realizar las operaciones opuestas se lo conoce como “despejar” el valor
de 𝑥. Y abusando del lenguaje matemático se dice que los números “pasan sumando,
restando, multiplicando o dividiendo” según corresponda.
Como procedimiento práctico y utilizando el “pasaje de términos” su solución sería:
5𝑥 + 4 = 14
5𝑥 = 14 − 4
28
𝑥 =
10
5
𝑥 = 2
Ejercicios resueltos
1) Hallar el valor de 𝑥 que verifica la siguiente ecuación:
−10𝑥 + 26 = 2𝑥 + 14
Primero agrupamos en un miembro todos los términos que posean la incógnita y del otro
lado los términos que no la posean
−10𝑥 − 2𝑥 = 14 − 26
Realizamos operaciones de suma y/o resta de ambos lados de la igualdad:
−12𝑥 = −12
𝑥 =
−12
−12
𝒙 = 𝟏
Siendo 𝑥 = 1 la solución de la ecuación.
Verificamos:
−10.1 + 26 = 2.1 + 14
16 = 16
y así se verifica la igualdad.
2) Hallar, si existe, el valor de 𝑥 que verifica la siguiente ecuación:
6𝑥 − 8
2
+
6𝑥 − 9
3
−
3𝑥 − 2
4
= 2
Podemos comenzar distribuyendo los denominadores correspondientes
6𝑥
2
−
8
2
+
6𝑥
3
−
9
3
−
3𝑥
4
+
2
4
= 2
Simplificamos
3𝑥 − 4 + 2𝑥 − 3 −
3
4
𝑥 +
1
2
= 2
Agrupamos
3𝑥 + 2𝑥 −
3
4
𝑥 = 2 −
1
2
+ 4 + 3
Operamos
17
4
𝑥 =
17
2
Despejamos 𝑥
𝑥 =
17
2
:
17
4
𝑥 = 2
Verificamos
29
6 ∙ 2 − 8
2
+
6 ∙ 2 − 9
3
−
3 ∙ 2 − 2
4
=
4
2
+
3
3
−
4
4
= 2
3) Hallar, si existe, el valor de 𝑥 que verifica la siguiente ecuación:
2(𝑥 + 3)
10 +
5(−𝑥 − 2)
5
=
4(𝑥 − 3)
2
Para resolver esta ecuación podemos comenzar aplicando propiedad distributiva de la
multiplicación respecto a la suma, en el numerador:
2𝑥 + 6
10 +
−5𝑥 − 10
5
=
4𝑥 − 12
2
Luego hay varios caminos para continuar, podemos distribuir el denominador en la suma o
en la resta, según corresponda, o bien podemos sacar un denominador común (como suma
de fracciones) o en forma similar multiplicar ambos miembros por un número múltiplo de
todos los denominadores.
Si optamos por esta última propuesta y multiplicamos por 10 (por ser múltiplo de 10, de 5
y de 2) a ambos lados de la igualdad
10 ∙ (
2𝑥 + 6
10 +
−5𝑥 − 10
5
) = 10 ∙ (
4𝑥 − 12
2
)
distribuimos
(2𝑥 + 6) + 2 ∙ (−5𝑥 − 10) = 5 ∙ (4𝑥 − 12)
operamos

2𝑥 + 6 − 10𝑥 − 20 = 20𝑥 − 60
Ahora se transforma en una ecuación similar al ejemplo 2
2𝑥 − 10𝑥 − 20𝑥 = −60 − 6 + 20
−28𝑥 = −46
𝑥 =
−46
−28
𝑥 =
23
14
4) Realizar el planteo correspondiente y resolver
La suma de 3 números consecutivos da como resultado 75. ¿Cuáles son dichos números?
Solución: primero pasamos el enunciado del lenguaje coloquial al simbólico:
La suma de 3 números consecutivos será:

𝑥 + (𝑥 + 1) + (𝑥 + 2), donde 𝑥 representa uno
de los números buscados y esto será igual a 75.
𝑥 + (𝑥 + 1) + (𝑥 + 2) = 75
30
Eliminamos los paréntesis de acuerdo con el criterio visto en la Unidad 1.
𝑥 + 𝑥 + 1 + 𝑥 + 2 = 75
Agrupamos convenientemente:
3𝑥 + 3 = 75
3𝑥 = 75 − 3
𝑥 =
72
3
𝑥 = 24
Si 𝑥 = 24, entonces los tres números consecutivos serán: 24, 25 𝑦 26.
Ecuaciones de segundo grado
Las ecuaciones cuadráticas o ecuaciones de segundo grado son aquellas en donde el
exponente de la variable o incógnita está elevado al cuadrado, es decir, la incógnita está
elevada al exponente 2.
La forma general de la ecuación es: 𝒂𝒙
𝟐 + 𝒃𝒙 + 𝒄 = 𝟎 con 𝒂 ≠ 𝟎, 𝒃, 𝒄 ∈ ℝ.
Resolución de ecuaciones de Segundo grado
Fórmula resolvente
Se puede demostrar que para dar solución a la ecuación
𝒂𝒙
𝟐 + 𝒃𝒙 + 𝒄 = 𝟎
se puede aplicar la siguiente fórmula, llamada fórmula resolvente es la que permite hallar, si
tiene, la o las soluciones de la misma:
𝒙𝟏,𝟐 =
−𝒃 ± √𝒃𝟐 − 𝟒𝒂𝒄
𝟐𝒂
Si analizamos la expresión que se encuentra dentro la raíz cuadrada de la fórmula
resolvente nos encontramos con la expresión: 𝒃
𝟐 − 𝟒𝒂𝒄 que se denomina Discriminante,
consideramos entonces los siguientes tres casos:
✓ Si 𝒃
𝟐 − 𝟒𝒂𝒄 es igual a cero, la ecuación tiene una única solución Real (doble).
✓ Si 𝒃
𝟐 − 𝟒𝒂𝒄 es mayor que cero, la ecuación tiene dos soluciones reales y distintas.
✓ Si 𝒃
𝟐 − 𝟒𝒂𝒄 es menor que cero la ecuación no tiene solución en ℝ .
En consecuencia, las ecuaciones cuadráticas podrán tener a lo sumo dos raíces reales.
La ecuación puede presentarse en forma completa o incompleta. Según su forma de expresión
es conveniente una u otra forma de resolución, veamos algunos ejemplos.
Ejercicios resueltos
Veamos dos ejemplos de ecuaciones cuadráticas incompletas, en los que además de resolver
la ecuación con la fórmula resolvente, es posible hacerlo por otro camino.
Ejemplo 1: Resolver 4𝑥
2 − 64 = 0
31
Esta es una ecuación cuadrática incompleta porque el coeficiente 𝑏 = 0, su forma
de resolución es simplemente despejar la incógnita 𝑥.
4𝑥
2 − 64 = 0
4𝑥
2 = 64
𝑥
2 = 16
aplicando la raíz cuadrada en ambos miembros
√𝑥
2 = √16
Utilizando la propiedad de que para todo 𝑎 ∈ ℝ: √𝑎
2 = |𝑎|, escribimos
|𝑥| = 4
Por lo tanto, las soluciones son 𝑥 = 4 ó 𝑥 = −4.
La verificación queda a cargo del alumno.
Observación: El módulo es muy práctico para despejar potencias pares teniendo en cuenta
que si 𝑛 es par √𝒙
𝒏
𝒏 = |𝒙| (sin embargo, si 𝑛 es impar √𝑥
𝑛
𝑛 = 𝑥).
Ejemplo 2: Resolver 𝑥
2 + 6𝑥 = 0
Esta ecuación de segundo grado también se denomina incompleta porque 𝑐 = 0.
Una forma de resolverla es sacando factor común la variable 𝑥
𝑥
2 + 6𝑥 = 0
𝑥(𝑥 + 6) = 0
y recordando que si un producto es igual a cero es porque alguno, o ambos,
factores son cero.
𝑥 = 0 ó 𝑥 + 6 = 0
siendo las soluciones 𝑥 = 0 ó 𝑥 = −6, simbólicamente 𝑆 = {−6; 0}.
La verificación queda a cargo del alumno.
Ejemplo 3: Resolver 𝑥
2 − 6𝑥 + 8 = 0
Se trata de una ecuación completa por tener todos sus términos distintos de cero.
La resolución, aplicando la fórmula resolvente, siendo 𝑎 = 1, 𝑏 = −6 y 𝑐 = 8
𝑥1,2 =
−𝑏 ± √𝑏
2 − 4𝑎𝑐
2𝑎
𝑥1,2 =
−(−6) ± √(−6)
2 − 4 ∙ 1 ∙ 8
2 ∙ 1
𝑥1,2 =
6 ± √36 − 32
2
=
6 ± √4
2
=
6 ± 2
2
= {
6 + 2
2
= 4
6 − 2
2
= 2
Siendo entonces el resultado 𝑥 = 2 ó 𝑥 = 4, simbólicamente 𝑆 = {2; 4}.
Verificamos:
Si 𝑥 = 2 ⇒ 2
2 − 6 ∙ 2 + 8 = 4 − 12 + 8 = 0
Si 𝑥 = 4 ⇒ 4
2 − 6 ∙ 4 + 8 = 16 − 24 + 8 = 0
Ejemplo 4: Resolver (𝑥 + 3)
2 − 4(3𝑥 − 5) = (2𝑥 + 4)(2𝑥 − 4)
32
Para empezar, debemos desarrollar el cuadrado del binomio del primer término a
la izquierda y aplicar la propiedad distributiva al segundo término. Por otro lado,
podemos resolver la diferencia de cuadrados del término a la derecha o
simplemente aplicar propiedad distributiva. Comencemos:
(𝑥 + 3)
2 − 4(3𝑥 − 5) = (2𝑥 + 4)(2𝑥 − 4)
𝑥
2 + 2 ∙ 3 ∙ 𝑥 + 3
2 − 12𝑥 + 20 = (2𝑥)
2 − 4
2
Realizamos los productos y potencias
𝑥
2 + 6𝑥 + 9 − 12𝑥 + 20 = 4𝑥
2 − 16
Pasamos todo al lado izquierdo
𝑥
2 + 9 − 6𝑥 + 20 − 4𝑥
2 + 16 = 0
Obtenemos una ecuación cuadrática completa por tener todos sus términos
distintos de cero
−3𝑥
2 − 6𝑥 + 45 = 0
La resolución, aplicando la fórmula resolvente, siendo 𝑎 = −3, 𝑏 = −6 y 𝑐 = 45
𝑥1,2 =
−𝑏 ± √𝑏
2 − 4𝑎𝑐
2𝑎
𝑥1,2 =
−(−6) ± √(−6)
2 − 4 ∙ (−3) ∙ 45
2 ∙ (−3)
𝑥1,2 =
6 ± √36 + 540
−6
=
6 ± √576
−6
=
6 ± 24
−6
= {
6 + 24
−6
= −5
6 − 24
−6
= 3
Siendo entonces el resultado 𝑥 = −5 ó 𝑥 = 3, simbólicamente 𝑆 = {−5; 3}.
33
Unidad 4
Rectas
En esta unidad se estudiarán las rectas, tanto desde el punto de vista analítico, a través de sus
ecuaciones, como desde el punto de vista gráfico. Para ello, es importante entender en qué
espacio se representan: el plano cartesiano.
Pero para construir ese plano, primero necesitamos el sistema de ejes. El sistema de ejes
cartesianos fue creado por René Descartes en el siglo XVII y permite localizar cualquier punto
en el plano usando solo dos números, llamados coordenadas. Está formado por dos rectas
numéricas que se cortan perpendicularmente:
• Una horizontal, llamada eje 𝒙 o eje de abscisas.
• Una vertical, llamada eje 𝒚 o eje de ordenadas.
Estas dos rectas se cortan en un punto llamado origen, que tiene coordenadas (0; 0).
Cada punto en el plano se ubica indicando dos coordenadas:
• La primera señala la posición sobre el eje 𝑥 (a la derecha o a la izquierda del origen).
• La segunda indica la posición sobre el eje 𝑦 (hacia arriba o hacia abajo del origen).
Este sistema de coordenadas no solo se utiliza en Matemática, sino también en otras
disciplinas como Física, Geografía, Diseño y hasta en programación de videojuegos, ya que
permite representar posiciones y trayectorias con claridad y precisión.
Por ejemplo, el punto (4; 2) está 4 unidades a la derecha del origen y 2 unidades hacia arriba,
como se muestra en el siguiente gráfico.
Comprender el plano cartesiano será fundamental para poder graficar rectas y estudiar sus
propiedades en los próximos apartados.
34
Ecuación de la recta
Las rectas pueden ser expresadas mediante la ecuación 𝒚 = 𝒂𝒙 + 𝒃; donde: 𝑎 y 𝑏 son
numeros reales.
✓ 𝒂 se llama pendiente de la recta.
✓ 𝒃 se llama ordenada al origen.
Para cada valor asignado a la variable 𝑥, existe un valor correspondiente de 𝑦, por lo que se
forma un par ordenado (𝑥; 𝑦) que puede representarse en el plano cartesiano.
En particular, si 𝑥 = 0, entonces 𝑦 = 𝑏. Por lo tanto, el punto (0; 𝑏) es un punto efectivo de
la recta y se ubica sobre el eje de ordenadas.
La pendiente 𝑎 está relacionada con la inclinación de la recta respecto al eje 𝑥, como veremos
a continuación.
Es importante destacar que no todas las rectas pueden expresarse en esta forma. Más
adelante, estudiaremos otras ecuaciones que también representan rectas.
Primero veamos como graficar rectas cuando se conoce su pendiente y su ordenada al origen,
es decir, cuando se conoce su expresión 𝑦 = 𝑎𝑥 + 𝑏. Existen varias formas de graficar una
recta. Tengamos en cuenta que, con al menos dos puntos de la misma, ya es posible
representarla graficamente.
Para graficar una recta algunas de las opciones son las siguientes:
Gráfico de la recta a partir de una tabla de valores
Para graficar una recta, se puede construir una tabla de valores asignando distintos valores a
𝑥 y reemplazándolos en la ecuación de la recta para calcular los correspondientes valores de
𝑦. Con al menos dos puntos obtenidos de esta manera, es posible trazar la recta en el plano
cartesiano.
Ejemplo 1:
Graficar la recta: 𝒚 = 𝟐𝒙 − 𝟑
Realizamos una tabla en la que elegimos en forma arbitraria los valores de "𝑥", y completamos
el valor de "𝑦" de acuerdo con la expresión dada, también escribimos en este caso el punto
obtenido y luego graficamos.
𝒙 𝒚 = 𝟐𝒙 − 𝟑 (𝒙; 𝒚)
-1 2(−1) − 3 = −5 (−𝟏;−𝟓)
0 2(0) − 3 = −3 (𝟎; −𝟑)
1 𝟐(𝟏) − 𝟑 = −𝟏 (𝟏; −𝟏)
35
Luego de graficar la recta a partir de la tabla de valores, se observa que la recta intersecta al
eje de ordenadas en el punto (0; −3). Este punto corresponde al valor del término
independiente de la ecuación 𝑏 = −3. También se puede ver en el gráfico que por cada unidad
que se avanza hacia la derecha sobre el eje 𝑥, se suben 2 unidades sobre el eje 𝑦. Esto refleja
que la pendiente de la recta es positiva y su valor es 2.
Ejemplo 2
Graficar la recta: 𝒚 = −
𝟐
𝟑
𝒙
𝒙 𝒚 = −
𝟐
𝟑
𝒙 (𝒙; 𝒚)
−𝟑 𝟐 (−𝟑; 𝟐)
𝟎 𝟎 (𝟎; 𝟎)
𝟑 −𝟐 (𝟑; −𝟐)
36
Luego de graficar la recta 𝑦 = −
2
3
𝑥 a partir de la tabla de valores, se puede observar que la
recta pasa por el origen, es decir, por el punto (0,0). Esto se debe a que no hay término
independiente en la ecuación, es decir, 𝑏 = 0.
Además, si se miran los puntos del gráfico, se nota que por cada 3 unidades que se avanza
hacia la derecha sobre el eje x, se bajan 2 unidades sobre el eje y. Este comportamiento nos
indica que la pendiente es negativa, y más específicamente, que su valor es −
2
3
.
Ejemplo 3
Graficar la recta: 𝒚 = 𝟑
En este caso, si hiciéramos una tabla de valores, cada valor arbitrario de 𝑥 tendría el mismo
valor de 𝑦 asignado. Dicho de otra manera, todos los puntos tienen el mismo valor de 𝑦, sin
importar qué valor tome 𝑥. En consecuencia, el gráfico nos queda de la siguiente manera:
El gráfico pasa por el punto (0; 3), sobre el eje de ordenadas, y es una recta horizontal. Esto
se debe a que la ecuación no contiene el término con 𝑥, por lo tanto, la pendiente es cero. En
el gráfico se puede ver claramente que, al avanzar cualquier cantidad sobre el eje 𝑥, el valor
de 𝑦 permanece constante: siempre es 3. Es decir, la pendiente nula, indica que la recta no
sube ni baja: se mantiene constante a lo largo del eje 𝑥.
En resumen: ¿Qué observamos hasta ahora al graficar rectas con tabla de valores?
• Cuando la pendiente 𝑎 es positiva, la recta es ascendente: al graficarla de izquierda a
derecha, sube.
• Cuando la pendiente 𝑎 es negativa, la recta es descendente: al avanzar hacia la
derecha, la recta baja.
• Si la pendiente es nula (es decir, 𝑎 = 0), la recta es horizontal: no sube ni baja,
permanece constante.
• En todos los casos, el punto (0; 𝑏) corresponde a la intersección con el eje de
ordenadas (también llamado ordenada al origen).
37
Estas observaciones nos permiten interpretar cómo se comporta una recta solo con mirar su
ecuación.
Gráfico de la recta con pendiente y ordenada
Hasta ahora vimos cómo graficar una recta construyendo una tabla de valores. Sin embargo,
existe otra forma muy útil y rápida: usar directamente la pendiente y la ordenada al origen
que aparecen en la ecuación 𝑦 = 𝑎𝑥 + 𝑏.
Comenzando con la ordenada al origen, se posiciona inicialmente el punto (0; 𝑏) en el plano.
Luego se aplica el desplazamiento correspondiente utilizando la pendiente 𝑎.
Ejemplo 4:
Graficar la recta de ecuación 𝒚 = −
𝟏
𝟑
𝒙 + 𝟐
En la ecuación de la recta observamos que 𝑏 = 2, por lo tanto, el punto (0; 2) pertenece al
grafico de la misma, lo graficamos:
La pendiente de la recta es 𝑎 = −
1
3
, lo cual indica que, por cada unidad que se avanza hacia la
derecha en el eje 𝑥, el valor de 𝑦 disminuye un tercio de unidad. Esto se puede interpretar
cono que se trata de una recta descendente con un desplazamiento proporcional: por cada 3
unidades que se avanza hacia la derecha, se baja 1 unidad.
Como se indica en el gráfico con línea punteada y flechas, el movimiento será: tres unidades
hacia la derecha y una unidad hacia abajo.
38
Una vez realizado ese recorrido, llegamos al punto (3; 1). Finalmente, trazamos la recta que
pasa por ambos puntos.
𝒚 = −
𝟏
𝟑
𝒙 + 𝟐
Ejemplo 5:
Graficar la recta de ecuación 𝒚 =
𝟏
𝟐
𝒙 − 𝟏
En la ecuación de la recta observamos que 𝑏 = −1, por lo tanto, el punto (0; −1) pertenece
al grafico de la misma, ya tenemos un primer punto para ubicar en el plano.
La pendiente de la recta es 𝑎 =
1
2
, lo cual indica que, por cada unidad que se avanza hacia la
derecha en el eje 𝑥, el valor de 𝑦 aumenta media unidad. Esto se puede interpretar como una
recta ascendente, con un desplazamiento proporcional: por cada 2 unidades que se avanza
hacia la derecha, se sube 1 unidad.
39
Entonces desde el punto (0; −1) el movimiento será: dos unidades hacia la derecha y una
unidad hacia arriba. Una vez realizado ese recorrido, llegamos al punto (2; 0). Finalmente,
trazamos la recta que pasa por ambos puntos.
𝒚 =
𝟏
𝟐
𝒙 − 𝟏
Ejemplo 6:
Graficar la recta de ecuación 𝒚 = 𝟑𝒙 − 𝟐
De acuerdo al valor que toma 𝑏 = −2, la recta pasa por el punto (0; −2).
La pendiente es 3, lo que indica que la recta es ascendente. En este caso, por cada unidad que
se avanza hacia la derecha, se suben 3 unidades. Luego, desde (0; −2), el recorrido sería:
una unidad hacia la derecha y tres unidades hacia arriba, como se muestra en el siguiente
gráfico:
Entonces, podemos decir en general lo siguiente
40
• El punto (0; 𝑏) se ubica primero en el plano: es el punto donde la recta interseca al eje
de ordenadas.
• A partir de ese punto, se aplica la pendiente 𝑎 como una indicación del
desplazamiento:
o Se avanza una unidad hacia la derecha (sobre el eje 𝑥), y luego se sube o baja
según el valor de la pendiente:
▪ Si 𝑎 es positiva, se sube.
▪ Si 𝑎 es negativa, se baja.
▪ Si 𝑎 es cero, no se sube ni baja: la recta es horizontal.
o Si la pendiente es una fracción, por ejemplo 𝑎 =
3
5
, se puede interpretar como:
avanzar 5 unidades en el eje 𝑥 y subir 3 en el eje 𝑦. Si fuera 𝑎 = −
3
5
, sería el
mismo desplazamiento horizontal, pero bajando 3 unidades.
Intersección de la recta con el eje 𝑥
Si bien la ordenada al origen nos indica el punto donde la recta corta al eje de ordenadas (es
decir en (0; 𝑏)), la ecuación 𝑦 = 𝑎𝑥 + 𝑏 no muestra explícitamente en qué punto la recta
intersecta al eje de abscisas.
Sin embargo, suele resultar útil conocer dónde la recta intersecta al eje 𝒙
Para encontrar esa intersección (también llamada abscisa al origen), hay que tener en cuenta
que corresponde al valor de 𝑥 cuando 𝑦 = 0, es por eso que es necesario resolver la ecuación
𝑎𝑥 + 𝑏 = 0
y despejar 𝑥.
Una vez que se conocen las intersecciones con ambos ejes, se pueden ubicar esos dos puntos
en el plano y trazar directamente la recta que los une, sin necesidad de calcular más valores.
Este método también es especialmente útil cuando se quiere analizar gráficamente dónde una
recta corta o toca los ejes del sistema.
Ejemplo 7:
Hallar la intersección con el eje 𝑥 de la recta 𝑦 = −
1
3
𝑥 + 2.
Igualamos a cero:
−
1
3
𝑥 + 2 = 0
Resolvemos la ecuación lineal como vimos en la Unidad 2:
−
1
3
𝑥 = −2
𝑥 = −2: (−
1
3
)
𝑥 = 6
41
Basándonos en los calculos, hemos identificado un punto por donde pasa esta recta (6; 0).
Entonces, considerndo que la recta pasa por (0; 2) y (6; 0) podemos realizar un grafico de la
misma.
Ecuaciones de rectas: distintos casos para hallarlas
Hasta aquí vimos cómo graficar una recta cuando conocemos su pendiente y su ordenada al
origen, ya sea usando una tabla de valores o aplicando directamente el concepto de
pendiente como desplazamiento.Ahora vamos a ver el proceso inverso, conocidos ciertos
datos, como obtener la ecuacion de la recta.
1. Cuando se conoce la pendiente y la ordenada al origen
Ya vimos que, si conocemos la pendiente 𝑎 y la ordenada al origen 𝑏, la ecuación de la recta
se puede escribir directamente en la forma:
𝑦 = 𝑎𝑥 + 𝑏
Por ejemplo, si 𝑎 = −
1
3
y 𝑏 = 2, la ecuación es:
𝑦 = −
1
3
𝑥 + 2
2. Cuando se conoce la ordenada al origen y un punto cualquiera
Si conocemos el valor de 𝑏 y también un punto (𝑥1; 𝑦1) que pertenece a la recta, podemos
determinar la pendiente reemplazando en la ecuación:
𝑦1 = 𝑎𝑥1 + 𝑏
Y luego despejar 𝒂, para escribir la ecuación completa.
Ejemplo:
Hallar la ecuación de la recta que pasa por el punto (3; −1) y tiene ordenada 𝑏 = −2.
Reemplazamos:
−1 = 3 ∙ 𝑎 − 2
Resolvemos el producto y pasamos el −2
1 = 3𝑎
Despejamos a
1
3
= 𝑎
Entonces:
𝑦 =
1
3
𝑥 − 2
3. Cuando se conoce la pendiente y un punto cualquiera
Si no conocemos 𝒃, pero sí la pendiente 𝑎 y un punto (𝑥1; 𝑦1), podemos usar esa información
para hallarla.
42
Sabemos que la ecuación de la recta es:
𝑦 = 𝑎𝑥 + 𝑏
Reemplazamos el punto y la pendiente 𝑎:
𝑦1 = 𝑎𝑥1 + 𝑏
Despejamos 𝒃, y así obtenemos la ecuación completa.
Ejemplo:
Hallar la ecuación de la recta que pasa por el punto (2; 1) y tiene pendiente 𝑎 = 3.
Reemplazamos:
1 = 3 ∙ 2 + 𝑏
Resolvemos el producto
1 = 6 + 𝑏
Despejamos 𝑏
−5 = 𝑏
Entonces:
𝑦 = 3𝑥 − 5
4. Cuando se conocen dos puntos
El procedimiento en este caso para hallar la ecuacion de la recta es elmas general y se basa en
lo que ya aprendimos: la pendiente indica cuánto varía 𝑦 cada vez que avanzamos una unidad
en el eje 𝑥, entonces, si se conocen dos puntos 𝐴: (𝑥1; 𝑦1
) y 𝐵: (𝑥2; 𝑦2
) sobre una recta, la
pendiente 𝑎 se calcula con la siguiente fórmula:
𝒂 =
𝒚𝟐 − 𝒚𝟏
𝒙𝟐 − 𝒙𝟏
(𝒙𝟐 ≠ 𝒙𝟏)
Esta fórmula nos dice cuántas unidades sube (si el resultado es positivo) o baja (si es negativo)
la recta en el eje 𝑦 por cada unidad que avanza en el eje 𝑥. Una vez calculada la pendiente,
reemplazamos en la expresión de la recta 𝑦 = 𝑎𝑥 + 𝑏 y usamos uno de los puntos conocidos
para hallar el valor de 𝑏, la ordenada al origen.
Ejercicio resuelto:
Determinar la ecuación de la recta que pasa por los puntos 𝐴 = (−2; 1) y 𝐵 = (3; 5).
𝑎 =
5 − 1
3 − (−2)
𝑎 =
4
5
Entonces la recta se podrá plantear cómo: 𝑦 =
4
5
𝑥 + 𝑏 . Utilizando cualquier de los puntos
dados, por ejemplo 𝐴 = (−2; 1), se obtiene:
1 =
4
5
(−2) + 𝑏
13
5
= 𝑏
43
Así la ecuación de la recta requerida es: 𝒚 =
𝟒
𝟓
𝒙 +
𝟏𝟑
𝟓
. Graficamos.
Rectas verticales:
Hasta ahora vimos que para calcular la pendiente entre dos puntos se usa la fórmula:
𝒂 =
𝒚𝟐 − 𝒚𝟏
𝒙𝟐 − 𝒙𝟏
(𝒙𝟐 ≠ 𝒙𝟏)
Pero esta fórmula no puede aplicarse si 𝑥2 = 𝑥1, ya que el denominador da cero, y la división
por cero no está definida. Esto sucede cuando ambos puntos tienen la misma coordenada 𝑥,
lo que significa que están alineados en una recta vertical. En estos casos, la pendiente no está
definida y la ecuación de la recta no se puede escribir como 𝑦 = 𝑎𝑥 + 𝑏.
En cambio, su ecuación es muy sencilla:
𝑥 = 𝑐
donde 𝑐 es el valor constante de las coordenadas 𝑥.
Por ejemplo, si los puntos son (4,1) y (4, −3), la recta tiene ecuación 𝑥 = 4
Este tipo de recta no sube ni baja, sino que se mueve exclusivamente en dirección vertical,
paralela al eje 𝑦.
44
Rectas paralelas y perpendiculares
Rectas paralelas
Debido a que la pendiente de una recta determina la inclinación de esta respecto al eje de las
abscisas, es sencillo deducir que dos o más rectas paralelas tienen la misma pendiente.
Formalmente podemos decir que:
𝑅1: 𝒚 = 𝒂𝟏𝒙 + 𝒃𝟏 y 𝑅2: 𝒚 = 𝒂𝟐𝒙 + 𝒃𝟐 son paralelas sí y sólo sí 𝒂𝟏 = 𝒂𝟐. (𝑅1//𝑅2)
Ejercicio resuelto:
Verificar que las rectas dadas en el gráfico anterior son paralelas.
Se puede observar la recta R1 que pasa por los puntos 𝐸 = (−3; 1) y 𝐹 = (1; 3). Su pendiente
se calculará como:
𝑎1 =
3 − 1
1 − (−3)
=
2
4
=
1
2
45
Y la recta R2 que pasa por los puntos 𝐺 = (1; −1) y 𝐻 = (7; 2). Su pendiente se calculará
como:
𝑎2 =
−1 − 2
1 − 7
=
−3
−6
=
1
2
Como 𝑎1 = 𝑎2 =
1
2
podemos concluir que las rectas son paralelas.
Rectas perpendiculares
Dos rectas son perpendiculares sí y sólo sí, la pendiente de una de ellas es inversa y opuesta a
la pendiente de la otra. Formalizando:
𝑅1: 𝒚 = 𝒂𝟏𝒙 + 𝒃𝟏 y 𝑅2: 𝒚 = 𝒂𝟐𝒙 + 𝒃𝟐 son perpendiculares, sí y sólo sí 𝒂𝟏 = −
𝟏
𝒂𝟐
.
Es decir que el producto de las pendientes será -1. (𝑅1 ⊥ 𝑅2)
Ejercicio resuelto:
Verificar que las rectas dadas en el siguiente gráfico son perpendiculares.
Se puede observar la recta R1 que pasa por los puntos 𝐺 = (5; 1) y 𝐻 = (8; 3). Su pendiente
se calculará como:
𝑎1 =
3 − 1
8 − 5
=
2
3
Y la recta R2 que pasa por los puntos 𝐸 = (3; −3) y 𝐹 = (−1; 3). Su pendiente se calculará
como:
𝑎2 =
3 − (−3)
−1 − 3
=
6
−4
= −
3
2
Como 𝑎1 =
2
3
 y 𝑎2 = −
3
2
, inversos y opuestos y 2
3
(−
3
2
) = −1, podemos concluir que las
rectas son perpendiculares.
46
Unidad 5
Sistemas de ecuaciones lineales
Un sistema de ecuaciones lineales de dos incógnitas es un conjunto formado por 𝑛 ecuaciones
de primer grado, con 2 incógnitas. Resolver un sistema significa hallar valores para cada una
de las incógnitas que verifiquen todas las igualdades simultáneamente. Los sistemas de
ecuaciones surgen en la vida cotidiana. Estos se pueden resolver de forma analítica o forma
gráfica. Analicemos el siguiente problema:
En un colegio se elaboran dulce de leche y pan, para recaudar fondos. Por cada kilo de dulce
de leche y de pan que se venden, se tiene una ganancia de $35 y $25, respectivamente.
Analizando lo vendido años anteriores, se observa que se puede vender el 50% más de dulce
de leche que de pan. Para el presente año, los alumnos del colegio quieren obtener una
ganancia total de $15500. ¿Cuántos kilos de cada producto deben vender?
Solución. Observemos que hay dos datos que no conocemos, ¿cuáles? Los kilos de dulce de
leche y los kilos de pan a vender. Por lo cual, se pueden definir dos incógnitas a las que se les
pueden asignar dos letras cualesquiera, para identificarlas llamémoslas 𝑥 e 𝑦 :
𝑥:"kilos de dulce de leche"
𝑦:"kilos de pan"
Ahora tenemos que poder plantear ecuaciones que relacionen estas dos incógnitas.
Analicemos el enunciado.
Cuando dice: Por cada kilo de dulce de leche y de pan que se venden, se tiene una ganancia de
$35 y $25, respectivamente. […] los alumnos del colegio quieren obtener una ganancia total
de $15500.
La primera oración nos dice que por cada kilo de dulce de leche se gana $35, como los kilos
de dulce de leche están representado por la 𝑥, podemos escribir 35𝑥. El mismo análisis
podemos hacer para el pan, por lo que podemos escribir 25𝑦. Sabemos que en total queremos
$15500, este total se obtiene sumando lo que ganamos por el dulce con lo que ganamos por
el pan. Por lo tanto, podemos escribir la siguiente ecuación lineal:
35𝑥 + 25𝑦 = 15500
Sigamos analizando el enunciado: Analizando lo vendido años anteriores, se observa que se
puede vender el 50% más de dulce de leche que de pan. ¿Qué nos dice esto? Que la cantidad
de dulce es mayor a la de pan, ¿cuánto mayor? Para obtener la cantidad total de dulce de
leche hay que sumarle a la cantidad de pan, el 50% de éste. Expresemos esta relación con una
ecuación:
𝑥 = 𝑦 + 50% 𝑦 = 𝑦 + 0,50 𝑦 = 1,50 𝑦
47
En consecuencia, tenemos el siguiente sistema de dos ecuaciones lineales con dos incógnitas:
{
35𝑥 + 25𝑦 = 15500
𝑥 = 1,5𝑦
Hasta este punto, hemos definido las incógnitas y planteado el sistema de ecuaciones
correspondiente al problema. Ahora, debemos resolverlo para encontrar, si existe, solución,
es decir, los valores de las incógnitas que satisfacen ambas ecuaciones lineales.
Métodos para resolver sistemas de ecuaciones lineales
Existen varios métodos para resolver un sistema de ecuaciones, dependiendo de cómo se
expresen las ecuaciones y de cuántas sean. En este curso, exploraremos dos de ellos: el
método de sustitución y el método de igualación. A continuación, desarrollaremos estos
métodos en detalle.
Sustitución. En este método, primero se despeja una incógnita en una de las ecuaciones.
Luego, la expresión obtenida se sustituye en la otra ecuación, permitiendo despejar la segunda
incógnita. Finalmente, se reemplaza el valor hallado en la primera ecuación para encontrar la
otra incógnita.
Veamos con nuestro ejemplo cómo se aplicaría, para empezar, enumeramos las ecuaciones,
esto no es necesario, puede ayudarnos a organizar el procedimiento:
{
35𝑥 + 25𝑦 = 15500 (I)
𝑥 = 1,5𝑦 (II)
Una simple inspección del sistema nos permite ver que, en este caso particular, en la ecuación
(II) la incógnita "𝑥" ya está despejada, entonces directamente pasamos a sustituir su
resultado en la ecuación (I) de la siguiente manera:
35 ∙ (1,5𝑦) + 25 𝑦 = 15500
Se observa que llegamos a una ecuación con una única incógnita “𝑦”, que ya aprendimos a
resolver en la Unidad 2. La resolvemos:
Realizamos el producto del primer término
52,5 𝑦 + 25 𝑦 = 15500
Sumamos términos semejantes
77,5 𝑦 = 15500
Despejamos 𝑦
𝑦 =
15500
77,5
𝑦 = 200
Este número en términos del problema nos dice que hay que vender 200 kilos de pan. Luego,
con este valor reemplazamos en la ecuación (II) para obtener los kilos de dulce de leche:
48
𝑥 = 1,5 ∙ 200
𝑥 = 300
Este número nos dice que hay que vender 300 kilos de dulce de leche. Para finalizar escribimos
la respuesta a la pregunta del problema, la cual decía: ¿Cuántos kilos de cada producto deben
vender? La respuesta es: se deben vender 300 kilos de dulce de leche y 200 kilos de pan para
poder obtener una ganancia de $15500.
¿Cómo verifico que la respuesta está bien? Tenemos que reemplazar estos dos valores en las
ecuaciones originales y chequear que se cumpla la igualdad.
Las ecuaciones originales: {
35𝑥 + 25𝑦 = 15500
𝑥 = 1,5𝑦
, y obtuvimos que 𝑥 = 300 y que 𝑦 = 200.
Verifiquemos la primera ecuación:
35 ∙ 300 + 25 ∙ 200 = 10500 + 5000 = 15500 ✔
Y verificamos la segunda ecuación:
𝑥 = 1,5 ∙ 𝑦 = 1,5 ∙ 200 = 300 ✔
Igualación. En este método, primero se despeja la misma incógnita en ambas ecuaciones,
obteniendo dos expresiones equivalentes. Luego, se igualan estas expresiones y se resuelve
la ecuación resultante para hallar el valor de una incógnita. Finalmente, se sustituye este valor
en una de las ecuaciones originales para encontrar la otra incógnita.
Resolvamos ahora nuestro ejemplo con este método
{
35𝑥 + 25𝑦 = 15500 (I)
𝑥 = 1,5𝑦 (II)
Considerando que ya tenemos despejada la 𝑥 de la ecuación (II), despejamos la misma
incógnita de la ecuación (I).
𝑥 =
15500 − 25𝑦
35
Podemos mejorar esta expresión distribuyendo el denominador
𝑥 =
15500
35 −
25𝑦
35
Y simplificar convenientemente
𝑥 =
3100
7
−
5
7
𝑦
Luego igualamos ambas ecuaciones que expresan a 𝑥 en función de 𝑦:
1,5𝑦 =
3100
7
−
5
7
𝑦
49
Podemos expresar el decimal como fracción y resolvemos esta ecuación para obtener el valor
de 𝑦.
3
2
𝑦 =
3100
7
−
5
7
𝑦
3
2
𝑦 +
5
7
𝑦 =
3100
7
31
14 𝑦 =
3100
7
𝑦 =
3100
7
∙
14
31
𝑦 = 200
El que así lo desea, puede trabajar con numero decimales.
A continuación, reemplazamos el valor de 𝑦 en cualesquiera de las dos ecuaciones de 𝑥 y
calculamos su valor:
𝑥 = 1,5𝑦 = 1,5 ∙ 200 → 𝑥 = 300
Obtenemos el mismo resultado que al resolverlo por el método de sustitución.
Tipos de soluciones
No siempre el sistema tiene una única solución. Puede pasar que no exista solución al
problema planteado o que haya infinitas. Dependiendo de la cantidad de soluciones los
sistemas de ecuaciones se pueden clasificar en:
Sistemas compatibles: tienen solución.
• Determinado (SCD): dicha solución es única.
• Indeterminado (SCI): hay más de una solución.
Sistema incompatible (SI): no tiene solución.
Ejercicios resueltos
Vemos unos ejemplos
Ejemplo 1: {
3𝑥 + 2𝑦 = 4
5𝑥 − 2𝑦 = 3
Podemos resolverlo analíticamente aplicando por ejemplo el método de sustitución. Primero
debemos despejar una de las incógnitas de alguna de las dos ecuaciones, en este caso
elegimos despejar 𝑦 de la primera ecuación
3𝑥 + 2𝑦 = 4
2𝑦 = 4 − 3𝑥
𝑦 =
4 − 3𝑥
2
𝑦 =
4
2
−
3𝑥
2
50
𝑦 = 2 −
3
2
𝑥
Sustituimos en la segunda ecuación
5𝑥 − 2𝑦 = 3
5𝑥 − 2 ∙ (2 −
3
2
𝑥) = 3
Aplicamos distributiva
5𝑥 − 4 + 3𝑥 = 3
Y despejamos 𝑥
−4 + 8𝑥 = 3
8𝑥 = 3 + 4
8𝑥 = 7
𝑥 =
7
8
El valor de 𝑦 , lo obtenemos reemplazando en cualquiera de las dos ecuaciones originales o
directamente en el primer despeje realizado:
𝑦 = 2 −
3
2
∙
7
8
= 2 −
21
16 =
11
16
La solución es única, ya que hay un único valor para 𝑥 y un único valor de 𝑦. Por lo tanto,
tenemos un sistema compatible determinado.
Las ecuaciones originales son:{
3𝑥 + 2𝑦 = 4
5𝑥 − 2𝑦 = 3
, y obtuvimos que 𝑥 =
7
8
y que 𝑦 =
11
16
.
Verifiquemos la primera ecuación:
3 ∙
7
8
+ 2 ∙
11
16 =
21
8
+
11
8
=
32
8
= 4
Y verificamos la segunda ecuación:
5 ∙
7
8
− 2 ∙
11
16 =
35
8
−
11
8
=
24
8
= 3
Ejemplo 2: {
3𝑥 + 2𝑦 = 4
15𝑥 + 10𝑦 = 20
Aplicando el método de igualación, despejamos de ambas ecuaciones la misma incógnita, por
ejemplo, 𝑥:
{
3𝑥 + 2𝑦 = 4 (I)
15𝑥 + 10𝑦 = 20 (II)
De (I)
3𝑥 + 2𝑦 = 4
3𝑥 = 4 − 2𝑦
𝑥 =
4 − 2𝑦
3
𝑥 =
4
3
−
2
3
𝑦
51
De (II)
15𝑥 + 10𝑦 = 20
15𝑥 = 20 − 10𝑦
𝑥 =
20 − 10𝑦
15
𝑥 =
20
15 −
10
15 𝑦
𝑥 =
4
3
−
2
3
𝑦
Igualamos los resultados obtenidos
4
3
−
2
3
𝑦 =
4
3
−
2
3
𝑦
Si observamos esta igualdad con atención, se puede ver que cualquiera sea el valor real de 𝑦,
se verifica la igualdad. No obstante, si continuamos con el despeje:
2
3
𝑦 −
2
3
𝑦 =
4
3
−
4
3
se llega a
0 = 0
Esta igualdad indica que el sistema es compatible indeterminado, es decir, tiene infinitas
soluciones. Además, muestra que una de las ecuaciones no aporta información adicional, ya
que ambas son múltiplos escalares, si a la ecuación (I) la multiplicamos por 5 nos da
exactamente la ecuación (II). Por lo tanto, el sistema puede resolverse considerando solo una
de ellas. Entonces, ¿cómo escribimos la solución? Hay varias formas, la más sencilla es:
Solución: el sistema es compatible indeterminado, y las infinitas soluciones se obtienen de
𝑥 =
4−2𝑦
3
con 𝑦 ∈ ℝ.
Ejemplo 3: {
5𝑦 = 4 − 2𝑥
6𝑥 − 20 = −15𝑦
Aplicamos el método de igualación, despejamos de ambas ecuaciones la misma incógnita, en
este caso, 𝑦:
{
5𝑦 = 4 − 2𝑥 (I)
6𝑥 − 20 = −15𝑦 (II)
De (I)
5𝑦 = 4 − 2𝑥
𝑦 =
4 − 2𝑥
5
𝑦 =
4
5
−
2
5
𝑥
De (II)
6𝑥 − 20 = −15𝑦
6𝑥 − 20
−15 = 𝑦
52
−
6𝑥
15 +
20
15 = 𝑦
−
2
5
𝑥 +
4
3
= 𝑦
Igualando los resultados obtenidos luego de despejar 𝑦 se tiene que
4
5
−
2
5
𝑥 = −
2
5
𝑥 +
4
3
Si analizamos esta igualdad con atención, podemos notar que no se cumple para ningún valor
real de 𝑥. Sin embargo, si continuamos con el despeje:
2
5
𝑥 −
2
5
𝑥 =
4
3
−
4
5
0 =
8
15
¡Esto es un absurdo! Esta contradicción indica que el sistema no tiene solución, es decir, es
incompatible. Entonces, ¿cómo escribimos la solución?
Solución: es un sistema incompatible, 𝑆 = ∅.
Ejemplo 4: Veamos otro ejemplo
{
3 (𝑥 −
𝑦
3
) − 9 = 0
2 (𝑦 −
𝑥
2
) = 𝑥 − 10
En este caso aplicamos el método de sustitución para afianzar mejor su comprensión.
Enumeremos las ecuaciones:
{
3 (𝑥 −
𝑦
3
) − 9 = 0 (I)
2 (𝑦 −
𝑥
2
) = 𝑥 − 10 (II)
Trabajemos con la ecuación (I):
3 (𝑥 −
𝑦
3
) − 9 = 0
Primero aplicamos distributiva
3𝑥 − 𝑦 − 9 = 0
Y ahora despejamos 𝑦
3𝑥 − 9 = 𝑦
Sustituimos en (II)
2 (3𝑥 − 9 −
𝑥
2
) = 𝑥 − 10
Aplicamos distributiva
6𝑥 − 18 − 𝑥 = 𝑥 − 10
Y ahora despejamos 𝑥
6𝑥 − 𝑥 + 𝑥 = 18 − 10
6𝑥 = 8
𝑥 =
8
6
53
𝑥 =
4
3
Entonces el valor de 𝑦 es:
3 ∙
4
3
− 9 = 𝑦
−5 = 𝑦
Ejemplo 5: Finalmente, veamos una situación problemática.
Un transportista lleva en su camioneta sacos de arroz de dos pesos distintos. Los sacos grandes
tienen un peso de 30 kg, mientras que los pequeños pesan 15 kg. El conductor recuerda que el
número de sacos pequeños es el doble del de sacos grandes, y que el peso total de la mercancía
es de 600 kg.
Solución. Primero definimos las dos incógnitas del problema, a las que se les pueden asignar
dos letras cualesquiera, 𝐺 e 𝑃 :
𝐺:"cantidad de sacos grandes"
𝑃:"cantidad de sacos pequeños"
Ahora tenemos que poder plantear ecuaciones que relacionen estas dos incógnitas. Si
analizamos el enunciado, vemos que se conocen el peso de cada saco grande: 30 kg y el de
cada saco pequeño: 15 kg, así como también se conoce el peso total que es de 600 kg,
entonces podemos plantear una ecuación que vincule estos datos considerando que 𝐺 sacos
grandes pesaran 30𝐺 kg y que 𝑃 sacos pequeños pesaran 15𝑃 kg, si sumamos estas
cantidades nos dará el peso total, es decir.
30𝐺 + 15𝑃 = 600
Por otro lado, el enunciado dice que el número de sacos pequeños es el doble del de sacos
grandes, matemáticamente escribimos:
𝑃 = 2𝐺
Y así tenemos nuestro sistema de dos ecuaciones con dos incógnitas:
{
30𝐺 + 15𝑃 = 600 (I)
𝑃 = 2𝐺 (II)
Si reemplazamos la ecuación (II) en la (I) se obtiene la siguiente ecuación
30𝐺 + 15 ∙ 2𝐺 = 600
Resolvemos
30𝐺 + 30𝐺 = 600
60𝐺 = 600
𝐺 = 600/60
𝐺 = 10
¿Cuántos sacos de cada tipo que se transportan? Transportan 10 sacos grandes y por lo
tanto 20 sacos pequeños.
54
Unidad 6
Geometría
En esta unidad, nos adentraremos en el estudio de conceptos fundamentales de la geometría.
Retomaremos ideas ya trabajadas en unidades anteriores, como los puntos y las rectas, y al
mismo tiempo incorporaremos nuevos contenidos, profundizando en sus definiciones y
propiedades. Nos enfocaremos especialmente en las figuras planas, con particular atención
en los cuadriláteros y los triángulos. Este recorrido servirá como preparación para la última
unidad, donde exploraremos en mayor profundidad los triángulos rectángulos y sus
características.
Punto y recta
¿Qué es un punto?
Un punto es el elemento más básico de la geometría. Representa una posición exacta en el
espacio, carece de dimensión y constituye la base sobre la cual se construyen todas las demás
figuras geométricas. Es una referencia fundamental en geometría que nos permite describir y
estudiar las relaciones espaciales entre objetos.
¿Qué es una recta?
Una recta es una sucesión continua e infinita de puntos que están perfectamente alineados
en una misma dirección. Es un objeto geométrico unidimensional y no tiene curvatura ni
límites, por lo tanto, no se puede medir su longitud.
Más definiciones
✓ Semirrecta: Es una parte de una recta que tiene un punto origen, pero no tiene un final
definido. No se puede medir.
✓ Segmento: Un segmento es una porción finita de una recta que tiene un punto de inicio y
un punto final claramente definidos. Es posible medir su longitud.
✓ Poligonal: Una poligonal es una sucesión de segmentos de recta que están conectados
uno tras otro, pero no necesariamente están alineados. Puede ser abierta, cuando al
menos uno de sus extremos está desconectado, o cerrada, cuando el primer extremo se
une al último. Si es cerrada, la poligonal forma una figura plana llamada polígono.
55
✓ Curva: Una curva está formada por puntos que no están alineados en una misma
dirección. Puede ser una curva abierta, en la que los extremos no están conectados,
una curva cerrada, en la que los extremos están conectados, o una curva mixta, que
está formada por una combinación de segmentos y tramos curvos unidos.
Posiciones relativas de dos rectas:
• Dos rectas en un mismo plano son paralelas si tienen la misma dirección y nunca se
cruzan es decir no tiene ningún punto en común esto implica que a lo largo de toda su
extensión las rectas mantienen una distancia constante entre sí.
• Dos rectas son secantes si se cruzan en algún punto común.
• Dos rectas en un mismo plano son perpendiculares si forman cuatro ángulos rectos en el
punto donde se cruzan.
Ángulos
Para medir ángulos utilizaremos el sistema de grados sexagesimales. Este sistema se basa en
la división de un ángulo llano en 180 partes iguales, cada una de las cuales se denomina grado
y se anota con el símbolo °. A su vez, cada grado, a su vez, se divide en 60 minutos (´), y cada
minuto se divide en 60 segundos (´´).
Este método de medición se utiliza ampliamente en disciplinas como la navegación, la
astronomía, la ingeniería y la física, ya que permite expresar con precisión y de forma universal
las medidas angulares que emplearemos en este curso.
56
Clasificación de los ángulos
Antes de comenzar a resolver situaciones que involucren ángulos, es importante conocer
cómo se clasifican según su medida. A continuación, presentaremos las distintas clases de
ángulos, acompañadas de gráficos que facilitarán su identificación.
Clasificación de los ángulos
Nulo
𝛼̂ = 0°
Agudo
0° < 𝛼̂ < 90°
Recto
𝛼̂ = 90°
Obtuso
90° < 𝛼̂ < 180°
Llano
𝛼̂ = 180°
Completo
𝛼̂ = 360°
Una vez que conocemos los distintos tipos de ángulos, es fundamental comprender algunas
relaciones que pueden establecerse entre ellos. Estas relaciones aparecen frecuentemente al
trabajar con figuras geométricas y nos permiten deducir medidas y resolver problemas con
mayor facilidad.
Relaciones entre ángulos
En esta sección exploraremos tres casos particulares: los ángulos complementarios,
suplementarios y los opuestos por el vértice.
Ángulos complementarios
Se denomina ángulos complementarios a aquellos cuya suma de medidas es igual a 90 grados
sexagesimales. Esta relación puede establecerse entre dos ángulos contiguos o no contiguos,
y se utiliza con frecuencia en la resolución de problemas geométricos que involucran el ángulo
recto como referencia. Por ejemplo:
57
Ángulos suplementarios
Dos ángulos son suplementarios cuando la suma de sus medidas es igual a 180 grados
sexagesimales. Esta condición puede presentarse tanto en ángulos adyacentes, que forman
un ángulo llano, como en ángulos independientes cuya suma total cumple dicha relación. Por
ejemplo
Ángulos opuestos por el vértice
Cuando dos rectas se intersecan, se generan cuatro ángulos. Los ángulos que se encuentran
enfrentados entre sí con respecto al punto de intersección se denominan ángulos opuestos
por el vértice. Estos ángulos son congruentes, es decir, poseen la misma medida, y se
caracterizan por no compartir lados, aunque sí un vértice común. Por ejemplo:
Triángulos
Un triángulo es un polígono formado por tres segmentos de recta, llamados lados, que se
intersectan de a dos en tres puntos distintos llamados vértices. Estos lados delimitan tres
ángulos interiores.
Propiedad fundamental de los ángulos interiores
• La suma de los ángulos interiores de cualquier triángulo es siempre igual a 180°.
Clasificación de los triángulos
Los triángulos pueden clasificarse:
• Según sus lados
• Según sus ángulos
58
Criterio
Tipo de
triángulo
Características Gráfico
Según sus
lados
Equilátero Tiene tres lados iguales y
tres ángulos iguales de 60°.
Isósceles Tiene dos lados iguales y
dos ángulos iguales.
Escaleno
Tiene los tres lados
desiguales y los tres
ángulos distintos.
Según sus
ángulos
Acutángulo Tiene tres ángulos agudos,
es decir, menores a 90°.
Rectángulo Tiene un ángulo recto (de
90°) y dos ángulos agudos.
Obtusángulo
Tiene un ángulo obtuso, es
decir, mayor a 90° y menor
a 180°.
59
Perímetro y área de triángulos
Perímetro
El perímetro de un triángulo es igual a la suma de las longitudes de sus tres lados.
Área
El área de un triángulo se calcula multiplicando la longitud de la base (𝑏) por la altura
correspondiente (ℎ) y dividiendo el resultado entre 2. La altura es la longitud del segmento
perpendicular trazado desde un vértice al lado opuesto o a su prolongación.
𝑨 =
𝒃 . 𝒉
𝟐
Ejercicio resuelto:
Dado el siguiente triangulo, hallar perímetro y superficie
Para hallar el perímetro debemos sumar los tres lados que son dato del problema de acuerdo
con la figura de análisis:
𝑃 = 11𝑐𝑚 + 11𝑐𝑚 + 7,5𝑐𝑚 = 𝟐𝟗, 𝟓𝒄𝒎
Para hallar área o superficie utilizamos la fórmula ya que la base y la altura son dato del
problema de acuerdo con la figura de análisis:
𝐴 =
11𝑐𝑚 ∙ 7𝑐𝑚
2
= 𝟑𝟖, 𝟓𝒄𝒎𝟐
Cuadriláteros
Los cuadriláteros son polígonos de cuatro lados.
Propiedad fundamental de los ángulos interiores
• La suma de los ángulos interiores de cualquier cuadrilátero es igual a 360°.
Clasificación de los cuadriláteros
Paralelogramos: los paralelogramos son cuadriláteros que tienen sus lados opuestos
paralelos entre sí. Se clasifican en
✓ Cuadrado: Sus cuatro lados son iguales y tiene cuatro ángulos rectos.
✓ Rectángulo: Tiene dos pares de lados iguales y los 4 ángulos rectos.
60
✓ Rombo: Sus cuatro lados son iguales y tiene ángulos opuestos
iguales además las diagonales de un rombo se cortan
perpendicularmente en su punto medio.
Trapecios: Cuadriláteros que tienen dos lados paralelos, llamados base mayor y base menor.
Se clasifican en
✓ Trapecio rectángulo: Tiene un ángulo recto.
✓ Trapecio isósceles: Tiene dos lados no paralelos iguales.
✓ Trapecio escaleno: No tiene ningún lado igual ni ángulo
recto.
Trapezoides: Cuadriláteros que no tiene ningún par de lados
paralelos.
✓ Romboide: tiene dos pares de lados consecutivos iguales y ángulos
opuestos de igual medida se caracteriza porque la diagonal mayor (D)
corta perpendicularmente a la diagonal menor (d) de en su punto
medio.
Área y Perímetro de figuras planas
El perímetro de una figura plana es la longitud total del contorno de la misma. En otras
palabras, es la suma de las longitudes de todos los lados de la figura. Se expresa en unidades
de longitud como centímetros, metros, etc.
El área de una figura plana es la medida de la superficie cubierta por la misma. Se calcula
mediante fórmulas específicas para cada figura geométrica. El área se expresa en unidades
cuadradas, como centímetros cuadrados, metros cuadrados, etc.
Comprender estos conceptos es fundamental para resolver situaciones cotidianas y
problemas geométricos, como calcular la cantidad de cerámicos necesarios para cubrir un
piso o el alambre para rodear un terreno.
61
Luego de haber trabajado con triángulos, nos enfocaremos ahora en los cuadriláteros,
estudiando cómo calcular su perímetro y su área según las características de cada tipo.
FIGURA PLANA PERIMETRO AREA
CUADRADO
𝑃 = 4 ∙ 𝐿
𝐿: 𝑙𝑎𝑑𝑜
𝐴 = 𝐿
2
RECTÁNGULO
𝑃 = 2 ∙ 𝐿 + 2 ∙ 𝑙
𝐿, 𝑙: 𝑙𝑎𝑑𝑜𝑠
𝐴 = 𝐿 ∙ 𝑙
TRAPECIO
𝑃 = 𝐵 + 𝑏 + 𝐿 + 𝐿’
𝐵, 𝑏, 𝐿, 𝑙: 𝑙𝑎𝑑𝑜𝑠
𝐴 =
(𝐵 + 𝑏) ∙ ℎ
2
ℎ: 𝑎𝑙𝑡𝑢𝑟𝑎
PARALELOGRAMO
𝑃 = 2 ∙ 𝐵 + 2 ∙ 𝐿
𝐵, 𝐿: 𝑙𝑎𝑑𝑜𝑠
𝐴 = 𝐵 ∙ ℎ
ℎ: 𝑎𝑙𝑡𝑢𝑟𝑎
ROMBO
𝑃 = 4 ∙ 𝐿
𝐿: 𝑙𝑎𝑑𝑜
𝐴 =
𝐷 ∙ 𝑑
2
𝐷, 𝑑: 𝑑𝑖𝑎𝑔𝑜𝑛𝑎𝑙𝑒𝑠
POLIGONO
REGULAR
𝑃 = 𝑛 ∙ 𝐿
𝐿: 𝑙𝑎𝑑𝑜 𝑑𝑒𝑙 𝑝𝑜𝑙𝑖𝑔𝑜𝑛𝑜
𝑛: 𝑐𝑎𝑛𝑡𝑖𝑑𝑎𝑑 𝑑𝑒 𝑙𝑎𝑑𝑜𝑠
𝐴 =
𝑃 ∙ 𝑎𝑝
2
𝑎𝑝: 𝑎𝑝𝑜𝑡𝑒𝑚𝑎
62
Unidad 7
Trigonometría
La trigonometría, según la etimología de su nombre, se ocupa del estudio y la resolución
analítica de los triángulos. Esto significa que, conociendo tres elementos adecuados de un
triángulo, es posible determinar las dimensiones de los elementos restantes, ya sea la medida
de sus lados o la amplitud de sus ángulos. En esta unidad nos enfocaremos en la aplicación de
la trigonometría en triángulos rectángulos. Como vimos en la unidad anterior, un triángulo
rectángulo es aquel que posee un ángulo recto, es decir, un ángulo de 90°.En este tipo de
triángulos, los lados que forman el ángulo recto se denominan catetos, mientras que el lado
opuesto al ángulo recto se llama hipotenusa.
Razones trigonométricas
En todo triángulo rectángulo se cumplen ciertas igualdades que permiten relacionar sus lados
y ángulos. Si tomamos como referencia uno de los ángulos agudos del triángulo, podemos
establecer los siguientes cocientes:
Si tomamos como referencia el ángulo

, obtenemos los siguientes cocientes:
Estas expresiones se conocen como razones trigonométricas, y permiten vincular los ángulos
agudos del triángulo rectángulo con la razón (o división) entre sus lados.
Seno de 𝛼 = 𝐬𝐞𝐧𝜶 =
𝒄𝒂𝒕𝒆𝒕𝒐 𝒐𝒑𝒖𝒆𝒔𝒕𝒐 𝒂𝒍 𝒂𝒏𝒈𝒖𝒍𝒐 𝜶
𝒉𝒊𝒑𝒐𝒕𝒆𝒏𝒖𝒔𝒂
=
𝒂
𝒄
Coseno de 𝛼 = 𝐜𝐨𝐬𝜶 =
𝒄𝒂𝒕𝒆𝒕𝒐 𝒂𝒅𝒚𝒂𝒄𝒆𝒏𝒕𝒆 𝒂𝒍 𝒂𝒏𝒈𝒖𝒍𝒐 𝜶
𝒉𝒊𝒑𝒐𝒕𝒆𝒏𝒖𝒔𝒂
=
𝒃
𝒄
Tangente de 𝛼 = 𝐭𝐠𝜶 =
𝒄𝒂𝒕𝒆𝒕𝒐 𝒐𝒑𝒖𝒆𝒔𝒕𝒐 𝒂𝒍 𝒂𝒏𝒈𝒖𝒍𝒐 𝜶
𝒄𝒂𝒕𝒆𝒕𝒐 𝒂𝒅𝒚𝒂𝒄𝒆𝒏𝒕𝒆 𝒂𝒍 𝒂𝒏𝒈𝒖𝒍𝒐 𝜶
=
𝒂
𝒃
𝐬𝐞𝐧𝜷 =
𝒃
𝒄
𝐜𝐨𝐬𝜷 =
𝒂
𝒄
𝐭𝐠𝜷 =
𝒃
𝒂
63
Sistemas de medidas angulares
En trigonometría, para expresar la medida de los ángulos se utilizan distintos sistemas. Los
principales son:
• El sistema sexagesimal o inglés
• El sistema centesimal o francés
• El sistema radial o circular
En este curso utilizaremos únicamente el sistema sexagesimal, cuyo ángulo unidad es el grado
sexagesimal (°). Este sistema divide una vuelta completa de la circunferencia en 360 partes
iguales, y cada una de esas partes corresponde a un grado (1°).
Cada grado se subdivide en 60 minutos ('), y cada minuto en 60 segundos ('').
En las calculadoras, este sistema suele identificarse con la abreviatura DEG (de “degree”, en
inglés).
Resolución de triángulos rectángulos
Resolver un triángulo consiste en determinar el valor de sus tres lados y tres ángulos.
Un triángulo queda completamente determinado si se conocen tres de sus elementos,
siempre que al menos uno de ellos sea un lado.
En el caso de los triángulos rectángulos, como uno de los ángulos ya es recto (90°), para
poder resolverlo es suficiente con:
• Conocer un ángulo agudo y un lado, o
• Conocer el valor de dos de sus lados.
A partir de esa información, utilizando las razones trigonométricas y el teorema de Pitágoras,
es posible calcular los elementos restantes del triángulo.
Teorema de Pitágoras
En todo triángulo rectángulo, se cumple una relación fundamental entre las medidas de sus
lados:
El cuadrado de la hipotenusa es igual a la suma de los cuadrados de los catetos.
Si llamamos 𝑐 a la hipotenusa (el lado opuesto al ángulo recto), 𝑎 y 𝑏 a los catetos, la expresión
matemática del teorema es:
𝒄
𝟐 = 𝒂
𝟐 + 𝒃
𝟐
Este teorema permite calcular la medida de un lado si se conocen los otros dos, y es una
herramienta esencial para resolver triángulos rectángulos cuando no se dispone de ángulos.
Ejercicios resueltos
Ejemplo 1. ¿Cuál es la longitud de 𝑋 en el siguiente triángulo?
64
Considerando que se trata de un triángulo rectángulo y que dos de sus lados son conocidos,
aplicamos el Teorema de Pitágoras:
𝑋
2 = 3
2 + 4
2
𝑋
2 = 9 + 16
𝑋
2 = 25
𝑋 = √25
𝑋 = 5
Ejemplo 2. ¿Cuál es la longitud de 𝑌 en el siguiente triángulo?
Aplicamos nuevamente el Teorema de Pitágoras:
132 = 122 + 𝑌
2
169 = 144 + 𝑌
2
25 = 𝑌
2
𝑌 = √25
𝑌 = 5
Ejemplo 3. Resolver el siguiente triangulo rectángulo
Ángulo 𝜶
De acuerdo con lo visto la unidad anterior, en todo triángulo, la suma de los ángulos interiores
es 180°, por lo tanto, en este caso:
𝛼 + 90° + 42° = 180°
𝛼 = 180° − 90° − 42°
65
𝛼 = 48°
Longitud del lado 𝒂. Utilizando el ángulo de 42° y la hipotenusa que mide 8, usamos la razón
trigonométrica coseno:
cos 42° =
𝑎
8
Luego despejamos
a
:
8. cos 42° = 𝑎
𝑎 = 5,95
Para calcular cos 42°con la calculadora es: COS 42 =
Recuerda que, al operar con grados sexagesimales, la calculadora debe estar en modo DEG.
Longitud del lado 𝒃. Utilizando el ángulo de 42° y la hipotenusa que mide 8, usamos la razón
trigonométrica seno:
sen42° =
𝑏
8
Luego despejamos 𝑏:
8. sen42° = 𝑏
𝑏 = 5,35
Para hallar este último valor, se podría haber utilizado también el teorema de Pitágoras:
8
2 = 𝑏
2 + 5,95
2
𝑏
2 = 8
2 − 5,95
2
𝑏
2 = 28,5975
𝑏 = √28,5975
𝑏 = 5,35
Ejemplo 4. Dado el siguiente triángulo, donde 𝑥 = 10, 𝑦 = 17. Calcular el ángulo 𝛼.
En este caso, la incógnita es el ángulo.
La razón trigonométrica que relaciona los lados 𝑥 e 𝑦 con el ángulo

es la tangente:
tg𝛼 =
𝑦
𝑥
66
tg𝛼 =
17
10
𝜶 = 𝟓𝟗°𝟑𝟐´𝟒, 𝟎𝟒´´
En una razón trigonométrica, cuando la incógnita es el ángulo, utilizamos la función inversa
en la calculadora. Para este caso es:
SHIFT tan 17/10 = °´ ´´
Ejemplo 5: Resolver la siguiente situación problemática:
Un dron que vuela a 800 m de altura distingue un objetivo con un ángulo de depresión
α=50°15′. Determinar la distancia entre el dron y el objetivo.
Realizamos una figura de análisis:
𝑠𝑒𝑛(50°15´) =
800 𝑚
𝑑
𝑑 =
800 𝑚
𝑠𝑒𝑛(50°15´)
𝑑 ≈ 1.040,53𝑚
La distancia entre el dron y el objetivo es de 1040,53 m
    """
def extract_keywords_from_message(message):
    words = re.findall(r'\b\w+\b', message.lower())
    return set(words)

# Guardar el historial de conversaciones en un archivo JSON
def load_conversations():
    if os.path.exists("conversation_history.json"):
        with open("conversation_history.json", "r") as f:
            return json.load(f)
    return []

def save_conversation_to_json(conversation):
    conversations = load_conversations()
    conversations.append(conversation)
    with open("conversation_history.json", "w") as f:
        json.dump(conversations, f, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    conversation_history = data.get('conversationHistory', [])

    if not user_message:
        return jsonify({"message": "Falta el mensaje"}), 400

    print(f"Mensaje del usuario: {user_message}")

    # Ahora usamos directamente pdf_text en el system prompt
    messages = conversation_history + [
        {"role": "system", "content": f"Información relevante de los manuales:\n{pdf_text}"},
        {"role": "user", "content": user_message}
    ]

    try:
        # Solicitar la respuesta a OpenAI usando el historial de la conversación
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=1000,
            temperature=0.9
        )
        ai_response = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error en la API de OpenAI: {str(e)}")
        ai_response = "Hubo un error al procesar tu solicitud."

    # Guardar la conversación en un archivo JSON
    conversation = {
        "message": user_message,
        "response": ai_response
    }
    save_conversation_to_json(conversation)

    return jsonify({"response": ai_response, "conversationHistory": messages})

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000)
