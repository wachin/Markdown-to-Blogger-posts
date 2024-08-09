# pin-no-instala-paquetes-python
En el año 2024 la unica manera que me ha funcionado de instalar paquetes desde pip es usando venv el entorno virtual de python

Para que puedas usar programas en python que dependen de paquetes pip esta es la solución

Instala

```
sudo apt install python3 python3-pip python3.*-venv
```

ahora en HOME abre una terminal pues necesitamos usar el comando "python3 -m venv .venv" que se utiliza para crear un entorno virtual en Python, este comando sólo hay que usarlo una vez. Poner en la terminal:

```
python3 -m venv .venv
```

y se creará el entorno virtual

Un entorno virtual es una herramienta que permite mantener dependencias y paquetes específicos para un proyecto aislado del sistema global de Python. Esto es especialmente útil para evitar conflictos entre versiones de paquetes en diferentes proyectos.

## Activar el entorno virtual
Ahora allí en HOME en la termial ponga:

```
source .venv/bin/activate
```

Mi nombre de usuario es wachin y el nombre de la maquina es netinst y a continuación les pongo como puse el comando y lo que  aparece en la terminal:

```
wachin@netinst:~$ source .venv/bin/activate
(.venv) wachin@netinst:~$
```

si pongo ls se muestran normalmente los directorios:

/home/wachin/Descargas  
/home/wachin/Documentos  
/home/wachin/Escritorio  
/home/wachin/Música  
etc   

y si pongo: ls -a se muestran además los archvos ocultos:

/home/wachin/.cache 
/home/wachin/.config  
/home/wachin/.local  
/home/wachin/.venv  
/home/wachin/Descargas  
/home/wachin/Documentos  
/home/wachin/Escritorio  
/home/wachin/Música  
etc  

Como ve allí está la carpeta .venv

el comando mencionado hace que se active el entorno virtual, y desde ahora podremos instalar paquetes pip dentro del entorno virtual:

```
pip install nombre_del_paquete
```

Ejemplo voy a instalar para hacer un test:

```
pip install requests
```

## Desactivar el entorno virtual
cuando ya no lo necesites pon:

```
deactivate
```

**Nota:** Los programas que dependen de paquetes pip no funcionan si no está activado su entorno virtual.

# Script para hacer un test a VENV

Ahora creemos un script en python para que por medio del paquete requests probar si funciona el entorno virtual VENV correctamente, el código es el siguiente:


```python
import requests

def check_requests():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
        if response.status_code == 200:
            print("El paquete 'requests' está instalado y funciona correctamente.")
            print("Respuesta del servidor:")
            print(response.json())
        else:
            print("El paquete 'requests' está instalado, pero hubo un problema con la solicitud.")
    except Exception as e:
        print("Ocurrió un error:", e)

if __name__ == "__main__":
    check_requests()
```

ejemplo el scritp deberá tener un nombre como el siguiente:

`test_venv.py`

en este caso guardelo dentro del directorio .venv pues este tutorial lo hago para un amigo el cual tenía que poner dentro de la carpeta virtual de python un script en python (si desea puede ver los archivos ocultos desde su administrador de archivos con Ctrl + H), entonces:

```
cd .venv
```

además luego poner ls para ver los archivos allí presentes:

```
(.venv) wachin@netinst:~$ cd .venv
(.venv) wachin@netinst:~/.venv$ ls
bin  include  lib  pyvenv.cfg
```

para que lo cree y guarde use nano, ponga así:

```
nano test_venv.py
```

y allí pegue el codigo, y guardelo con Ctrl + O, luego de Enter y Ctrl + X para sarlir. Si necesita algún tutorial sobre como usar nano vea: https://facilitarelsoftwarelibre.blogspot.com/2024/08/como-usar-nano-en-linux.html o puede usar vi

luego ponga ls y ya lo verá allí, ejemplo:

```
(.venv) wachin@netinst:~/.venv$ ls
bin  include  lib  pyvenv.cfg  test_venv.py
```

## Qué hace el script:

- Importa el módulo `requests`.
- Define una función `check_requests` que hace una solicitud GET a un endpoint de prueba (`https://jsonplaceholder.typicode.com/todos/1`).
- Verifica si la solicitud fue exitosa (código de estado 200).
- Imprime un mensaje confirmando que el paquete `requests` está instalado y funcionando correctamente.
- Imprime la respuesta JSON obtenida del servidor para que puedas ver que la solicitud se realizó correctamente.
- Maneja cualquier excepción que pueda ocurrir durante la solicitud.

Si el paquete `requests` está correctamente instalado y no hay problemas de conexión a internet, deberías ver un mensaje indicando que está funcionando, junto con los datos obtenidos de la solicitud.

Entonces para ejecutarlo pongo en la terminal:

```
python3 test_venv.py
```

claro que debe entener el lugar donde estámos ubicados, bueno aquí pongo todo:

```
(.venv) wachin@netinst:~/.venv$ python3 test_venv.py
El paquete 'requests' está instalado y funciona correctamente.
Respuesta del servidor:
{'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}
(.venv) wachin@netinst:~/.venv$ 
```

Funciona bien.


# Script en BASH para abrir el entorno virtual si el código del script en PYTHON está en .venv
Si usted como en este ejemplo con estas indicación por algún motivo debe tener su script python en su home/usuario dentro de la carpeta oculta:

.venv  

**Nota:** la ruta completa desde la raíz de linux es: /home/wachin/.venv donde wachin es el nombre de mi usuario.

que en este caso se llama:

test_venv.py  

o sea por todo estaría así:

/home/wachin/.venv/test_venv.py  

podemos acceder fácilmente a el desde un script en **BASH** desde HOME, ejemplo:

/home/wachin/venv_home_launcher.sh

Desactíve el entorno virtual si lo tenía activado, ponga en su HOME:

```
deactivate
```

o sea así:

```
(.venv) wachin@netinst:~$ deactivate 
wachin@netinst:~$  
```

  Créelo con el siguiente contendo, copielo:

```
#! /bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Change to the directory containing the Python script
cd .venv

# Run the Python script
python3 test_venv.py
```

Guarde este script con ejemplo el nombre ( si desea puede ponerle otro nombre):

```
wachin@netinst:~$ nano venv_home_launcher.sh
```

y allí pegue el codigo, y guardelo con Ctrl + O, luego de Enter y Ctrl + X para sarlir.

y desde una terminal abierta en HOME láncelo así:

```
bash ./venv_home_launcher.sh
```

así logrará hacerlo funcionar:

```
wachin@netinst:~$ bash ./venv_home_launcher.sh
El paquete 'requests' está instalado y funciona correctamente.
Respuesta del servidor:
{'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}
```



# Scritp en bash para abrir el entorno virtual VENV desde cualquier lugar donde esté el script en python
Si usted tiene su script en python que depende para funcionar de un paquete pip y lo tiene ejemplo en **Documentos**, para este ejemplo usemos el ya hecho, aquí les pongo el lugar donde lo tengo:

```
wachin@netinst:~/Documentos$ tree
.
├── e-Sword
│   ├── Bookmarks.lstx
│   ├── journal.jnlx
│   ├── markup.ovlx
│   ├── study.notx
│   └── topic.topx
├── FeatherNotes
│   └── 2024-07-15-wachi.fnx
└── test_venv.py

3 directories, 7 files
```

navego hasta donde está donde quiero crear el script en bash, en este caso:

```
wachin@netinst:~$ cd Documentos
wachin@netinst:~/Documentos$
```

y ponga lo siguiente y de Enter:

```
wachin@netinst:~/Documentos$ nano venv_dir_launcher.sh
```

**Nota:** Además usted puede abrir una terminal allí donde esté su script en python desde su administrador de archivos en vez de hacer eso desde la terminal.

copie el siguiente contenido:

```
#! /bin/bash

# Si su programa en python usa algun paquete desde
# pip, esta es la manera de lanzarlo rapidamente
# Pon este script en cualquier lugar donde está
# programa en python
# Activate the virtual environment
source $HOME/.venv/bin/activate

# Automáticamente se redigirá a este lugar desde
# la activación de .venv
# Run the Python script
python3 test_venv.py
```

y allí pegue el codigo, y guardelo con Ctrl + O, luego de Enter y Ctrl + X para sarlir.

## Poner permisos de ejecución desde el administrador de archivos
A este script pongale permisos de ejecución puede ser desde el administrador de archivoss con clic derecho y clic la pestaña permisos marcandolo como ejecutable

## Poner permisos de ejecución desde la terminal
Para otorgar permisos de ejecución a un script en Linux desde la terminal, puedes utilizar el comando `chmod`. Aquí tienes dos opciones comunes:

1. **Usando el parámetro `+x`:**
   - Para asignar permisos de ejecución al archivo `venv_dir_launcher.sh`, ejecuta:
     ```
     $ chmod +x venv_dir_launcher.sh
     ```
   Esto permitirá que el archivo se ejecute.

2. **Asignando valores numéricos:**
   - Si prefieres asignar permisos específicos, puedes usar valores numéricos. Por ejemplo, para dar permisos de ejecución al usuario propietario y solo permisos de lectura al grupo y al invitado:
     ```
     $ chmod 0755 venv_dir_launcher.sh
     ```
   En este caso, el `0` indica que no se asignan permisos al grupo y al invitado.

Puedes verificar los permisos con `ls -la venv_dir_launcher.sh`.


Bueno, con esto hemos puesto creado el script en bash junto al script en python, puedo verificarlo con ls:

Para ejecutarlo no debe estar usando venv, desactívelo si tenía activado:

```
deactivate
```

aquí les pongo el ejemplo:

```
(.venv) wachin@netinst:~$ deactivate
wachin@netinst:~$
```
y navego hasta el lugar donde está el script o abro una terminal allí, ejemplo para este caso:

```
wachin@netinst:~$ cd Documentos
wachin@netinst:~/Documentos$ ls
e-Sword  FeatherNotes  test_venv.py
```

y allí ejecutelo abriendo una terminal allí y poniendo:

```
bash ./venv_dir_launcher.sh
```

### Cómo hago para usarlo con mi script
Para su script .py abralo con nano o con un editor de texto y cambie la linea:

```
#! /bin/bash

# Si su programa en python usa algun paquete desde
# pip, esta es la manera de lanzarlo rapidamente
# Pon este script en cualquier lugar donde está
# programa en python
# Activate the virtual environment
source $HOME/.venv/bin/activate

# Automáticamente se redigirá a este lugar desde
# la activación de .venv
# Run the Python script
python3 test_venv.py
```

por el nombre de su script en python, ejemplo:

```
#! /bin/bash

# Si su programa en python usa algun paquete desde
# pip, esta es la manera de lanzarlo rapidamente
# Pon este script en cualquier lugar donde está
# programa en python
# Activate the virtual environment
source $HOME/.venv/bin/activate

# Automáticamente se redigirá a este lugar desde
# la activación de .venv
# Run the Python script
python3 su_script.py
```

y guarde el script en bash

Dios les bendiga



## Consultas

Python Software Foundation. (2023). The Python Standard Library: venv. Recuperado de [https://docs.python.org/3/library/venv.html.](https://docs.python.org/3/library/venv.html.)
Documentación oficial del paquete requests:

Kenneth Reitz & Python Software Foundation. (2023). Requests: HTTP for Humans. Recuperado de [https://docs.python-requests.org/en/latest/](https://docs.python-requests.org/en/latest/)

How to determine if Python is running inside a virtualenv? [https://stackoverflow.com/questions/1871549/how-to-determine-if-python-is-running-inside-a-virtualenv](https://stackoverflow.com/questions/1871549/how-to-determine-if-python-is-running-inside-a-virtualenv)

Issues using the Python Plugin with a Virtual Environment (venv) [https://discourse.orthanc-server.org/t/issues-using-the-python-plugin-with-a-virtual-environment-venv/4258](https://discourse.orthanc-server.org/t/issues-using-the-python-plugin-with-a-virtual-environment-venv/4258)

Python Virtual Environments: A Primer [https://realpython.com/python-virtual-environments-a-primer](https://realpython.com/python-virtual-environments-a-primer)/

Understanding Python virtual environments using venv and virtualenv [https://medium.com/@sukul.teradata/understanding-python-virtual-environments-using-venv-and-virtualenv-283f37d24b13](https://medium.com/@sukul.teradata/understanding-python-virtual-environments-using-venv-and-virtualenv-283f37d24b13)
