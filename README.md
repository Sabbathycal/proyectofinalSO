# proyectofinalSO

### Paso 1: Instalar Python y pip

Antes de comenzar, asegúrate de tener Python y pip instalados. En Ubuntu, puedes instalarlos con:
          **sudo apt update**
        **sudo apt install python3 python3-pip**

### Paso 2: Crear un Entorno Virtual

Para evitar conflictos con otros proyectos, creamos un entorno virtual:

   **python3 -m venv venv**
  **source venv/bin/activate  # Activar el entorno virtual**

### Paso 3: Instalar Flask y Módulos Necesarios

Ejecuta:

  **pip install flask flask-login flask-wtf pyotp qrcode[pil]**

### Paso 4: Hacer apropiado uso de los archivos que hay en el repositorio

### Paso 5: Ejecutar la Aplicación

Guarda todos los archivos y ejecuta:

  **python app.py**

Luego, abre en el navegador:
    **http://127.0.0.1:5000**
    
*NOTA: En caso de que salga un error en la pagina setup_2fa.html, instalar pillow de lleno con:
    **pip install pillow***

*Claro todo esto dentro del mismo venv.*

## Convertir la pagina en HTTPS

Apache2 actuará como un servidor proxy inverso, manejando solicitudes HTTPS y redirigiéndolas a tu aplicación Flask.
### Paso 1: Instalar Apache2 y módulos necesarios

Ejecuta en la terminal:

**sudo apt update**
**sudo apt install apache2 libapache2-mod-wsgi-py3 -y**
Para que Apache envíe tráfico a Flask, debemos configurar un VirtualHost.
### Paso 2: Habilitar módulos de proxy en Apache

Ejecuta:

**sudo a2enmod ssl**
**sudo a2enmod proxy**
**sudo a2enmod proxy_http**
**sudo systemctl restart apache2**

Si no tienes un dominio, podemos usar un certificado autofirmado para probar.
### Paso 3: Crear el certificado SSL

Ejecuta:

**sudo mkdir -p /etc/ssl/myapp**
**sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/myapp/myapp.key -out /etc/ssl/myapp/myapp.crt**

### Paso 4: Crear un archivo de configuración en Apache

Ejecuta:

**sudo nano /etc/apache2/sites-available/myapp-ssl.conf**

Agrega este contenido:

         <VirtualHost *:443>
                  ServerName localhost

                  SSLEngine on
                  SSLCertificateFile /etc/ssl/myapp/myapp.crt
                  SSLCertificateKeyFile /etc/ssl/myapp/myapp.key

                  ProxyPass / http://127.0.0.1:5000/
                  ProxyPassReverse / http://127.0.0.1:5000/

                  <Directory /var/www/html>
                           Require all granted
                  </Directory>
         </VirtualHost>

### Paso5: Activar el sitio SSL y reiniciar Apache

Ejecuta:

**sudo a2ensite myapp-ssl**
**sudo systemctl restart apache2**


### Paso6: Probar la configuración

Abre tu navegador y ve a:

**https://localhost**
