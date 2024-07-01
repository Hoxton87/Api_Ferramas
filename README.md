# Indicaciones para Consultar Api con Postman

## Activar Entorno Virtual
> Windows:
```
venv\Scripts\activate
```
macOS/Linux:
```
source venv/bin/activate
```

## Instalar Django y Django REST Framework
```
pip install django djangorestframework
```` 
## Cargar Datos desde JSON
```
pip install djangorestframework-simplejwt==5.3.1
```
```
python manage.py load_productos
```

## Crear Superusuario
> Para crear un superusuario en Django, puedes usar el siguiente comando:

```
python manage.py createsuperuser
````

## Ejecutar Servidor de Desarrollo
```
python manage.py runserver
```
## Ver Productos

Método: GET
URL: http://127.0.0.1:8000/api/productos


## Consultas API
> [!IMPORTANT]
Para realizar las consultas API, necesitas obtener un token primero.

>Obtener Token

Método: POST

URL: http://127.0.0.1:8000/api/token/

Headers:

Key:Content-Type

Value:application/json

Body (JSON)

```
{
    "username": "tu_usuario",
    "password": "tu_contraseña"
}
```

## Agregar Productos al Carrito

Método: POST

URL: http://127.0.0.1:8000/api/carrito/agregar/

Headers:

Key:Content-Type

Value:application/json

Authorization: Bearer <tu_token> (Reemplaza <tu_token> con el valor del token de acceso obtenido)

Body (JSON):

```
{
    "producto_id": 1,
    "cantidad": 2
}
```

## Verificar Contenido del Carrito

Método: GET

URL: http://127.0.0.1:8000/api/carrito/

Headers:

Key: Authorization

Value: Bearer <tu_token>


## Realizar Compra del Carrito

Método: POST

URL: http://127.0.0.1:8000/api/carrito/comprar/

Headers:

Key: Content-Type

Value: application/json

Key: Authorization

Value: Bearer <tu_token>

## Realizar Test

Categoria Prueba Unitaria
```
 python manage.py test categorias.tests.test_categoria_unit
```

Categoria Prueba de integracion
```
python manage.py test categorias.tests.test_categoria_integration
```

Item Carrito prueba de integracion: 

```
python manage.py test items_carrito.tests.test_itemcarrito_integration
```

Item Carrito prueba unitaria: 
```
python manage.py test items_carrito.tests.test_itemcarrito_unit
```



