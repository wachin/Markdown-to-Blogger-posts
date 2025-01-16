
### 1. **Instalar Qt Creator y Qt**
   - Abre una terminal y ejecuta el siguiente comando para instalar Qt Creator y las bibliotecas de Qt:
     ```
     sudo apt-get install cmake build-essential libqt5x11extras5-dev qt5-qmake \
     	dh-make qtbase5-dev-tools extra-cmake-modules qtdeclarative5-dev-tools \
     	qtdeclarative5-dev qtcreator qttools5-dev
     ```
     
   - Añado que en la siguiente siguiente.

### 5. **Configurar el kit de desarrollo**
   - **"Build System"** cambia la opciòn por defecto (CMake) por qmake (si no hace esto en Debian 12 luego no se crea el archivo .pro).

   - **"Summary"** Verá allí en la lista de los archivos que serán añadidos a .pro sin el cual no se puede hacer nada, ejemplo:

     Files to be added in
     /home/wachin/Dev-Qt/Pruebas/ChordT:
     
### 9. Abrir un ejemplo de aplicación escrita en Qt

- Cierre Qt Creator y vuelvalo a abrir
- Clone el siguiente repositorio en algún directorio (debe tener instalado git):

   ```
   git clone https://github.com/Anchakor/MRichTextEditor
   ```

- En Qt Creator de clic en **"File"** > **"Open File or Project..."** y busque el archivo.
