# proyectofinalSO

## Paso 1: Instalar Python y pip

Antes de comenzar, asegúrate de tener Python y pip instalados. En Ubuntu, puedes instalarlos con:
          **sudo apt update**
        **sudo apt install python3 python3-pip**

## Paso 2: Crear un Entorno Virtual

Para evitar conflictos con otros proyectos, creamos un entorno virtual:

   **python3 -m venv venv**
  **source venv/bin/activate  # Activar el entorno virtual**

## Paso 3: Instalar Flask y Módulos Necesarios

Ejecuta:

  **pip install flask flask-login flask-wtf pyotp qrcode[pil]**

## Paso 4: Hacer apropiado uso de los archivos que hay en el repositorio

## Paso 5: Ejecutar la Aplicación

Guarda todos los archivos y ejecuta:

  **python app.py**

Luego, abre en el navegador:
    **http://127.0.0.1:5000**
    
*NOTA: En caso de que salga un error en la pagina setup_2fa.html, instalar pillow de lleno con:
    **pip install pillow***

Claro todo esto dentro del mismo venv.
