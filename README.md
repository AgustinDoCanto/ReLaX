# ReLaX
 
ReLaX (Rendering Enviroment for LaTeX) es un entorno de renderizado para LaTeX permitiendo la automatización de creación de documentos a través de plantillas.

![relax-version-image.png](./img/relax-version.png)

# Instalación

## Local (enlace editable)

Por el momento **ReLaX** solamente se puede instalar mediante un link editable (Linux o Sistemas Operativos tipo Unix)

**Crear una carpeta para el proyecto:**

```bash
relax new -p <project_name>
``` 
**Crear un entorno virtual y activarlo:**

```bash
python -m venv venv
source venb/bin/activate
```

Instalar en modo editable la libreria a traves del apuntando a la carpeta con el proyecto Relax:

```bash
pip install -e <route_to_relax_library>
```

Para verificar la correcta instalación y funcionamiento puede correr el comando:

```bash
relax version
```

## Mediante Dockerfile (Virtualizado)

Se provee un archivo Dockerfile que permite desplegar una version del ecosistema ReLaX con lo básico para el desarrollo:

Para trabajar mediante contenedores primero se debe crear una carpeta donde se va realizar el proyecto con ReLaX:

```bash
mkdir <nombre_de_carpeta>
```
Posteriormente nos situamos dentro de la misma:

```bash
cd <nombre_de_carpeta>
```

**NOTA:** Para la siguiente sección es necesario tener instalado y corriendo correctamente el demonio de docker (en Linux) o docker-desktop abierto (en Windows).

Copiamos dentro de la carpeta recientemente creada el archivo *Dockerfile* de este repositorio y posteriormente situados dentro de ese directorio realizamos el build del contenedor con:

```bash
docker build -t <nombre_del_contenedor> .
```
Una vez creado el contenedor podemos ejecutarlo en modo interactivo para empezar con el desarrollo del proyecto con:

**En Linux:**

```bash
docker run -it --rm -v "$(pwd)":/<nombre_de_la_carpeta> <nombre_del_contenedor>
```
o tambien

```bash
docker run -it --rm -v $PWD:/relax-docker relax-local
```

**En Windows (Powershell)**

```powershell
docker run -it --rm -v ${PWD}:/<nombre_de_la_carpeta> <nombre_del_contenedor>
```

**En Git bash**

```bash
docker run -it --rm -v "$(pwd -W):/<nombre_de_la_carpeta>" <nombre_del_contenedor>
```

Esto correra una consola interactiva con el contenedor que te permitira crear directorios y utilizar ReLaX a través de la carpeta montada como volumen.

Para salir de la misma simplemente escribe *exit*.

# ReLaX commands

Los comandos se ejecutan directamente en la shell


## Ver comandos disponibles

```bash
relax --help
```

## Ver version de ReLaX

```bash
relax version
```
## Crear un nuevo proyecto

```bash
relax new -p <project_name>
```
O tambien

```bash
relax new --project <project_name>
```

Esto crea una carpeta con la estructura basica del proyecto

## Crear un nuevo Componente

```bash
relax create -c <component_name>
```
O tambien

```bash
relax create --project <component_name>
```

Esto crea un componente con el nombre especificado

## Compilar el documento ReLaX a PDF

ReLaX hace uso de 'pdflatex' para compilar el documento, por lo que es necesario tenerlo instalado correctamente

```bash
relax build --project <project_name>
```
O tambien

```bash
relax build --project <project_name> --clean <boolean>
```

La flag "--clean" o "-c" en el comando "build" suprime la generacion de los archivos: "aux","log", "out", "toc" si esta en "True" y permite la generacion si esta en "False"

**IMPORTANTE:** Para correr el comando relax build se necesita apuntar a el directorio que contiene al proyecto.

# Utilizacion de Componentes

Al crear un componente con el comando "relax create" se crea una carpeta dentro del proyecto que contiene el archivo del componente .py y el archivo .tex:

```bash
relax create -c ExampleComponent
```
Creara el siguiente arbol de subdirectorios:

ExampleComponent
- ExampleComponent.py
- ExampeComponent.tex


El archivo .py esta destinado a todas las operaciones, importaciones, o conexiones con otros modulos o componentes relacionadas a python mientras que el .tex se encarga de presentar la plantilla de como se renderizaran esos resultados cada vez que se utilize el componente.

El archivo .py y .tex se conectan mediante el diccionario de retorno en el archivo .py, en el mismo se definen las variables o datos que se vayan a retornar (si es que se retorna alguno).

## Static Components (Componentes Estáticos)

Los componentes estaticos son componentes que no reciben ningun parametro externo y solo se encargan de renderizar codigo LaTeX en especifico.

Un ejemplo de creacion de un componente estatico seria el siguiente:


### Creacion del componente

```bash
relax create -c FirstExampleComponent
```

Luego de la creacion del componente, el directorio deberia verse asi:

**FirstExampleComponent.py**
```python

from RelaxCore import Component

@Component(template="FirstExampleComponent.tex")
def FirstExampleComponent(**kargs):
	return kargs

```

**FirstExampleComponent.tex**

```LaTeX
FirstExampleComponent works!
```

Y el archivo main asi (ya que aun no incluimos el componente)

**main.py**

```python
from SectionComponent.SectionComponent import SectionComponent
from RelaxCore import Component

@Component(template="main.tex")
def main(**kargs):
	return kargs

```

### Inclusion del componente

Este primer componente se encargará de imprimir "*Esto es un texto en Italica*" cada vez que se llame al componente, para esto haremos los siguientes cambios en el proyecto:


#### En FirstExampleComponent

**FirstExampleComponent.py**
```python
from RelaxCore import Component

@Component(template="FirstExampleComponent.tex")
def FirstExampleComponent(**kargs):
	return kargs
```

**FirstExampleComponent.tex**
```LaTeX
\textit{Esto es un texto en italica} \newline
```

#### En main

Incluimos el componente en archivo main 

**main.py**
```python
from FirstExampleComponent.FirstExampleComponent import FirstExampleComponent
from RelaxCore import Component

@Component(template="main.tex")
def main(**kargs):
	return { 'FirstExampleComponent' : FirstExampleComponent }

```

Llamamos al componente dentro del main.tex

**main.tex**
```LaTeX
\documentclass{article}

\usepackage[utf8]{inputenc} % Codificación UTF-8
\usepackage[T1]{fontenc}    % Codificación de fuentes
\usepackage{lipsum}         % Texto de relleno opcional

\title{Título del Documento}
\author{Autor}
\date{\today}

\begin{document}

\maketitle

<< FirstExampleComponent() >> %Llamamos a FirstExampleComponent


\end{document}
```

Posteriormente renderizamos el documento con:

```bash
relax build -p <path_to_project> -c <boolean>
```

Con esto el texto "*Esto es un texto en italica*" deberia aparecer en nuestro documento PDF.

De esta manera haz renderizado tu primer componente estático en ReLaX.

## Dinamic Components (Componentes Dinámicos)

Si bien los componentes estáticos son de gran utilidad para encapsular grandes cantidades de texto y tambien nos permiten reutilizar texto preformateado aumentando asi la legibilidad y mantenibilidad del codigo tambien nos limitan a usar siempre el mismo texto o las mismas etiquetas no permitiendo variar el contenido del componente a nuestro gusto, es aqui donde entran los componentes dinámicos.

Los componentes dinamicos son idénticos a los estáticos con la diferencia de que estos permiten el ingreso de variables en base a las cuales el componente podrá ejecutar lógica interna y renderizar el contenido dependiendo de la entrada.

### Creación del Componente

El comando para crear un componente dinámico es el mismo que para un estático ya que la diferencia es lógica, no física (no código):

```bash
relax create -c SecondExampleComponent
```

Siguiendo el ejemplo anterior haremos que este componente renderize el texto recibido a través de una variable, en italica, para esto el código seria el siguiente:

#### En SecondExampleComponent

**SecondExampleComponent.py**
```python
from RelaxCore import Component

@Component(template="SecondExampleComponent.tex")
def SecondExampleComponent(**kargs):
	return {
		'textToRender' : None
	}
```

**SecondExampleComponent.tex**
```LaTeX
\textit{<< textToRender >>} \newline
```

#### En main

Incluimos el componente en archivo main, cabe destacar que tambien esta incluido FirstExampleComponent del ejemplo anterior 

**main.py**
```python
from FirstExampleComponent.FirstExampleComponent import FirstExampleComponent
from SecondExampleComponent.SecondExampleComponent import SecondExampleComponent
from RelaxCore import Component

components_to_include = { 
'FirstExampleComponent' : FirstExampleComponent,
'SecondExampleComponent' : SecondExampleComponent 
}

@Component(template="main.tex")
def main(**kargs):
	return components_to_include

```

Llamamos al componente dentro del main.tex

**main.tex**
```LaTeX
\documentclass{article}

\usepackage[utf8]{inputenc} % Codificación UTF-8
\usepackage[T1]{fontenc}    % Codificación de fuentes
\usepackage{lipsum}         % Texto de relleno opcional

\title{Título del Documento}
\author{Autor}
\date{\today}

\begin{document}

\maketitle

<< FirstExampleComponent() >> %Llamamos a FirstExampleComponent

<< SecondExampleComponent(textToRender="Esto es un dinámico") >> % Renderiza el texto ingresado, en este caso: "Esto es un dinámico"

\end{document}

```

Al buildear el documento en el PDF deberia haberse agregado la linea "*Esto es un texto dinámico*" también en italicas.

La ventaja de este nuevo tipo de componentes radica en su reutilización y posibilidad de calcular lógica interna en base a variables.

 **main.tex**
```LaTeX
\documentclass{article}

\usepackage[utf8]{inputenc} % Codificación UTF-8
\usepackage[T1]{fontenc}    % Codificación de fuentes
\usepackage{lipsum}         % Texto de relleno opcional

\title{Título del Documento}
\author{Autor}
\date{\today}

\begin{document}

\maketitle

% Llamamos 3 veces a FirstExampleComponent
<< FirstExampleComponent() >> 
<< FirstExampleComponent() >> 
<< FirstExampleComponent() >> 
% En todos los casos renderizara en el documento "Esto es un texto en italicas"


% Mientras que si hacemos distintas llamadas con SecondExampleComponent
<< SecondExampleComponent(textToRender="Esto es un dinámico") >> % Renderiza el texto ingresado, en este caso: "Esto es un dinámico"
<< SecondExampleComponent(textToRender="Me encanta usar ReLaX") >> % Renderiza el texto ingresado, en este caso: "Me encanta usar ReLaX"
% Renderiza textos distindos dependiendo de la entrada
\end{document}

```

Con los componentes dinámicos no estamos limitados a utilizar una única variable, sino que podemos hacer uso de varias o incluir valores por defecto en ellas que nos avisen, por ejemplo, de que no incluimos un valor al llamar al componente.

Un claro ejemplo de esto seria un componente para incluir imagenes o figuras dentro del documento:


```bash
relax create -c ImageComponent
```


**ImageComponent.py**

```python
from RelaxCore import Component

@Component(template="ImageComponent.tex")
def ImageComponent(**kargs):
	return {
		'source': "[!]SOURCE REQUIRED[!]", 
		'scale': '[!]SCALE REQUIRED[!]',
		'label': None,
		'caption': None
	}
```

**ImageComponent.tex**


```LaTeX
\begin{figure}
    \centering
    \includegraphics[scale=<< scale >>]{<< source >>}<$ if caption $>
    \caption{<< caption >>}<$ endif $><$ if label $>
    \label{<< label >>}<$ endif $>
\end{figure}
```

**Nota:** El uso de la tag if se especifica más adelante, en este caso la tag se utiliza para incluir la linea si se ingresa algún dato y no incluirla si no.

**main.py**

```python
from FirstExampleComponent.FirstExampleComponent import FirstExampleComponent
from SecondExampleComponent.SecondExampleComponent import SecondExampleComponent
from ImageComponent.ImageComponent import ImageComponent
from RelaxCore import Component

components_to_include = { 
	'FirstExampleComponent' : FirstExampleComponent,
	'SecondExampleComponent' : SecondExampleComponent, 
	'ImageComponent' : ImageComponent 
}

@Component(template="main.tex")
def main(**kargs):
	return components_to_include

```

**main.tex**

```LaTeX
\documentclass{article}

\usepackage[utf8]{inputenc} % Codificación UTF-8
\usepackage[T1]{fontenc}    % Codificación de fuentes
\usepackage{lipsum}         % Texto de relleno opcional
\usepackage{graphicx}

\title{Título del Documento}
\author{Autor}
\date{\today}

\begin{document}

\maketitle

% Llamamos 3 veces a FirstExampleComponent
<< FirstExampleComponent() >> 
<< FirstExampleComponent() >> 
<< FirstExampleComponent() >> 
% En todos los casos renderizara en el documento "Esto es un texto en italicas"


% Mientras que si hacemos distintas llamadas con SecondExampleComponent
<< SecondExampleComponent(textToRender="Esto es un dinámico") >> % Renderiza el texto ingresado, en este caso: "Esto es un dinámico"
<< SecondExampleComponent(textToRender="Me encanta usar ReLaX") >> % Renderiza el texto ingresado, en este caso: "Me encanta usar ReLaX"
% Renderiza textos distindos dependiendo de la entrada


<< ImageComponent(scale="1.0", source="Img/cat_image.jpg") >> % ImageComponent recibiendo la escala de uno y una imagen

<< ImageComponent(scale="1.0", source="Img/cat_image.jpg", caption="Caption de imagen generica", label="Etiqueta") >> % Imagen con escala, directorio fuente y caption

\end{document}

```


Luego de compilar el codigo .tex dentro de output, la parte correspondiente a las imagenes, se veria asi:


```LaTeX

\begin{figure}
    \centering
    \includegraphics[scale=1.0]{Img/cat_image.jpg}
\end{figure} % ImageComponent recibiendo la escala de uno y una imagen

\begin{figure}
    \centering
    \includegraphics[scale=1.0]{Img/cat_image.jpg}
    \caption{Caption de imagen generica}
    \label{Etiqueta}
\end{figure} % Imagen con escala, directorio fuente y caption

```

## Jinja Tags (Etiquetas de Jinja)

ReLaX hace uso de la herramienta de templating "Jinja 2" la cual permite crear templates de documentos para rellenarlos en base a una lógica o dinámicamente.

Hacer uso de esta herramienta le permite a ReLaX extender sus capacidades mediante las tags de la misma lo que puede ser de ayuda en el caso de querer renderizar Componentes de manera dinámica o en base a una lógica (como se ejemplifico en el Componente ImageComponent).

Las tags se denotan entre '<$' y '$>'.

### Conditional Tags (Tags condicionales)

Las etiquetas condicionales permiten evaluar expresiones y controlar el flujo de ejecución en una plantilla. Las principales etiquetas condicionales son:

#### 1. `if`
Evalúa una condición y ejecuta el bloque si es verdadera.

```python
<$ if condicion $>
    Este texto se renderizará si se cumple la condicion
<$ endif $>
```

#### 2. `if-else`

Evalúa una condición y ejecuta el bloque `if` si es verdadera, ejecuta el bloque `else` si no.

```python
<$ if condicion $>
    Este texto se renderizará si se cumple la condición
<$ else $>
	Este texto se renderizará si no se cumple la condición
<$ endif $>
```

#### 2. `if-elif-else`

Evalúa determinadas condiciones y ejecuta el bloque dependiendo de la cual condición se cumpla, si ninguna se cumple entonces ejecuta el bloque `else`.

```python
<$ if primera_condicion $>
    Solo este texto se renderizará si la primera condicion se cumple.
<$ elif segunda_condicion $>
	Solo este texto se renderizará si la segunda condicion se cumple.
<$ else $>
	Este texto se renderizará si no se cumple ninguna condición.
<$ endif $>
```

### Conditional Operators (Operadores condicionales)

En ReLaX se puede hacer uso de los operadores para hacer comparaciones dentro de las condiciones:

- Comparación: ==, !=, <, >, <=, >=
- Lógicos: and, or, not
- Pertenencia: in, not in
- Existencia: is defined, is not defined, is none

### Loop Tags (Tags de bucles)

Las tags de bucle permiten iterar sobre una condición o hasta que la misma se cumpla, esto permite llamar N veces a un Componente de una manera muy cómoda. Para esto se utiliza la tag "for":

```python
<$ for item in items $>
	Contenido dentro del bucle
<$ endfor $>
```

Por ejemplo, si quisieramos agregar 10 veces 'cat_image.jpg' en nuestro documento bastaria con un bucle for que iterase sobre una lista con la ruta de "cat_image.jpg" repetida 10 veces, cabe destacar que esa lista podria contener no solo la ruta de una imagen sino de varias, permitiendo asi la renderización de un lote de imagenes de manera directa.

Si seguimos trabajando con el ejemplo de Componente ImageComponent:


**main.py**
```python
from FirstExampleComponent.FirstExampleComponent import FirstExampleComponent
from SecondExampleComponent.SecondExampleComponent import SecondExampleComponent
from ImageComponent.ImageComponent import ImageComponent
from RelaxCore import Component


image_path = "component-examples/Img/cat_image.jpg"
images_list = []
for _ in range(10):
	images_list.append(image_path)


dictionary_of_includes = { 
	'FirstExampleComponent' : FirstExampleComponent,
	'SecondExampleComponent' : SecondExampleComponent, 
	'ImageComponent' : ImageComponent,
	'images_list': images_list 
}

@Component(template="main.tex")
def main(**kargs):
	return dictionary_of_includes

```

**main.tex**

```LaTeX
\documentclass{article}

\usepackage[utf8]{inputenc} % Codificación UTF-8
\usepackage[T1]{fontenc}    % Codificación de fuentes
\usepackage{lipsum}         % Texto de relleno opcional
\usepackage{graphicx}
\usepackage{float}

\title{Título del Documento}
\author{Autor}
\date{\today}

\begin{document}

\maketitle


% Incluimos las imagenes de images_list
<$ for image in images_list $>
	<<ImageComponent(scale="1.0", source=image) >>
<$ endfor $>

\end{document}
```

Este código renderiza la imagen correspondiente al path indicado 10 veces dentro del documento, en este caso "cat_image.jpg"

### Macro Tags 

Las Tags Macro de Jinja 2 permiten al usuario definir "Macros" que actuan como un conjunto de instrucciones que se ejecutan en conjunto con una llamada, similar a auna función. Las mismas se definen de la siguiente forma

``` LaTeX
 <$ macro NombreMacro() $> % Declaración de una macro sin parametros de entrada
 	Al llamar esta macro, se imprimirá este texto!
 <$ endmacro $>

 <$ macro NombreMacro(parametro1, parametro2,etc) $> % Declaración de una macro con parametros de entrada
 	Al llamar a esta macro imprimiremos este texto con << parametro1 >>, << parametro2 >>
 <$ endmacro $>
```

Las macros son una potente herramienta ya que nos permiten encapsular código dentro de las mismas similar a como lo hariamos con un componente, veamos un ejemplo:


**Creamos el componente**
```bash
relax create -c MacroComponentExample	
```

**Definimos el código dentro del mismo**

*MacroComponentExample.py*
```python
from RelaxCore import Component

@Component(template="MacroComponentExample.tex")
def MacroComponentExample(**kargs):
	return kargs

```
*MacroComponentExample.tex*
```LaTeX
<$ macro MacroWithoutParameters() $>
	\textit{Este texto se renderiza desde la macro MacroWithoutParameters}
<$ endmacro $>
```

Al importar y utilizar esta macro en main.tex se renderizara el texto en italica "Este texto se renderiza desde la macro MacroWithoutParameters":

*main.py*

```python
from FirstExampleComponent.FirstExampleComponent import FirstExampleComponent
from SecondExampleComponent.SecondExampleComponent import SecondExampleComponent
from ImageComponent.ImageComponent import ImageComponent
from MacroComponentExample.MacroComponentExample import MacroComponentExample
from RelaxCore import Component


dictionary_of_includes = { 
	'FirstExampleComponent' : FirstExampleComponent,
	'SecondExampleComponent' : SecondExampleComponent, 
	'ImageComponent' : ImageComponent,
	'MacroComponentExample' : MacroComponentExample
}

@Component(template="main.tex")
def main(**kargs):
	return dictionary_of_includes

```

*main.tex*
```LaTeX
% Debemos importar la macro MacroWithoutParameter desde el componente
<$ from "MacroComponentExample/MacroComponentExample.tex" import MacroWithoutParameters $> 

\documentclass{article}

\usepackage[utf8]{inputenc} % Codificación UTF-8
\usepackage[T1]{fontenc}    % Codificación de fuentes
\usepackage{lipsum}         % Texto de relleno opcional
\usepackage{graphicx}
\usepackage{float}

\title{Título del Documento}
\author{Autor}
\date{\today}

\begin{document}

\maketitle

<< MacroWithoutParameters() >>

\end{document}

```

Como se puede visualizar en *main.tex* siempre es necesario importar las macros creadas en el componente para poder usarlas.

#### Macros con parametros

El mecanismo de macros de Jinja 2 permite recibir parámetros en su definición que nos permiten utilizar los mismos más tarde. Estos parámetros pueden ser de diversos tipos, incluyendo otras macros lo que habilita la interpolación de strings (concatenar texto con el resultado de ejecutar una macro), veamos un ejemplo:


**Creamos el componente**
```bash
relax create -c MacroWithParameters
```

**MacroWithParameters.py**

```python
from RelaxCore import Component

@Component(template="MacroWithParameters.tex")
def MacroWithParameters(**kargs):
	return kargs

```

**MacroWithParameters.tex**

```LaTeX
<$- macro ShowMessage(text) -$> % La macro ShowMessage muestra el texto recibido
<< text >>
<$- endmacro -$>

<$- macro TextBold(text) -$>
\textbf{<< text >>}
<$- endmacro -$>
```

**NOTA:** Los guiones en las etiquetas sirven para eliminar el espacio que dejan en blanco al remplazar las tags por espacios en blanco, pero se puede prescindir de ellas.

**main.py**

```python
from FirstExampleComponent.FirstExampleComponent import FirstExampleComponent
from SecondExampleComponent.SecondExampleComponent import SecondExampleComponent
from ImageComponent.ImageComponent import ImageComponent
from MacroComponentExample.MacroComponentExample import MacroComponentExample
from MacroWithParameters.MacroWithParameters import MacroWithParameters
from RelaxCore import Component


dictionary_of_includes = { 
	'FirstExampleComponent' : FirstExampleComponent,
	'SecondExampleComponent' : SecondExampleComponent, 
	'ImageComponent' : ImageComponent,
	'MacroComponentExample' : MacroComponentExample,
	'MacroWithParameters' : MacroWithParameters
}

@Component(template="main.tex")
def main(**kargs):
	return dictionary_of_includes

```

**main.tex**

```LaTeX
<$ from "MacroWithParameters/MacroWithParameters.tex" import ShowMessage $>
<$ from "MacroWithParameters/MacroWithParameters.tex" import TextBold $>

\documentclass{article}

\usepackage[utf8]{inputenc} % Codificación UTF-8
\usepackage[T1]{fontenc}    % Codificación de fuentes
\usepackage{lipsum}         % Texto de relleno opcional
\usepackage{graphicx}
\usepackage{float}

\title{Título del Documento}
\author{Autor}
\date{\today}

\begin{document}

\maketitle

<< ShowMessage("Este es un texto normal que se renderizará comunmente") >> % Pasamos el texto como parametro a ShowMessage

\end{document}

```
 
El primer "ShowMessage" se encarga de mostrar "Este es un texto normal que se renderizará comunmente" pasado como parámetro a la macro, dentro del documento. 


#### Interpolación de parametros y macros


```LaTeX
<$ from "MacroWithParameters/MacroWithParameters.tex" import ShowMessage $>
<$ from "MacroWithParameters/MacroWithParameters.tex" import TextBold $>

\documentclass{article}

\usepackage[utf8]{inputenc} % Codificación UTF-8
\usepackage[T1]{fontenc}    % Codificación de fuentes
\usepackage{lipsum}         % Texto de relleno opcional
\usepackage{graphicx}
\usepackage{float}

\title{Título del Documento}
\author{Autor}
\date{\today}

\begin{document}

\maketitle

<< ShowMessage("Este es un texto que incluye el siguiente texto pero en negrita " ~ TextBold("Este es el texto que debe estar en negrita") ~ ", Aqui finalizamos la cadena") >> % Interpolamos el texto que recibe ShowMessage con TextBold

\end{document}

```
 
En el segundo componente se logra algo similar, pero se interpola la llamada a la macro "TextBold" con la cual logramos renderizar texto en negrita dentro de texto normal, esto se puede generalizar para cualquier tipo de macro y cualquier parámetro del mismo. 

### Diferencias entre Macro Tags y Componentes ReLaX

La principal diferencia entre las Macro Tags y los Componentes ReLaX es que los componentes son funciones python mientras que las Macros actuan de acuerdo al funcionamiento interno de Jinja 2, pero ambos poseen mecanismos similares, por lo que la interpolación de texto y parametros dentro y otras funcionalidades de las macros también son utilizables con los Componentes de ReLaX.


Para profundizar sobre algunas características avanzadas de "Jinja 2" como herencia de plantillas o funcionamiento interno de macros, puede visitar la [documentación oficial](https://jinja.palletsprojects.com/en/stable/templates/) que detalla el sistema de herencia de plantillas y tags a profundidad. 
