#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

# Crear superusuario automáticamente
python manage.py shell -c "
from django.contrib.auth.models import User
from Aplicaciones.Personas.models import Persona

if not User.objects.filter(username='axel').exists():
    user = User.objects.create_superuser('axel', 'aiza4840@gmail.com', 'aiypwzqp')
    print('✅ Superusuario axel creado')
    
    try:
        persona = Persona.objects.create(
            usuario=user,
            nombre='Administrador',
            apellido='Sistema',
            cedula='9999999999',
            correo='aiza4840@gmail.com',
            telefono='0999999999',
            direccion='Dirección del administrador',
            es_admin=True
        )
        print('✅ Persona admin creada')
    except Exception as e:
        print(f'✅ Usuario admin listo (persona puede existir)')
else:
    print('✅ Usuario admin ya existe')
"