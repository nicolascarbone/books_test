=================
Pasos
=================

- pip install -r requirements
- python manage.py migrate


Web Auth
    - Login form: accounts/login/?next=<next page>, i.e accounts/login/?next=/book
    luego de autenticar se puede acceder a /book, /author y /library
    en caso contrario se redirecciona a accounts/login

Api
    - Usa Token para autenticar
    - Se puede obtener un token haciendo POST a /api/token con username y password 
        de algun usuario existente, si no hay crearlo con python manage.py createsuperuser
        para este challenge cree uno con username admin y pass admin123456
    - Ese token se puede setear en el environment de postman que adjuntare para poder testear
        los distintos endpoints

Tests
    - Test existentes fueron fixeados
    - Se agregaron algunos tests nuevos para dar soporte a los model methods agregados

Conventions
    - Todos los archivos siguen PEP8
    - Se movieron metodos a los modelos para quitar toda logica de las views y templates

