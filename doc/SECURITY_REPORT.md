# Documentación de Auditoría de Seguridad: Decorador `@cognito_auth_required`

## Contexto del Problema
Durante las pruebas locales para la integración de AWS SAM con Insomnia, se detectó una inconsistencia grave en los bloqueos de seguridad de diversos endpoints de la API. 

Algunos endpoints requerían un Token de Cognito válido (generando un error `401 Unauthorized` si el token expiraba), mientras que otros endpoints (principalmente de lectura `GET`) no exigían ninguna autenticación y se podían consultar libremente.

### ¿A qué se debió esto?
Al inspeccionar el código, descubrimos que la línea `@cognito_auth_required`, que actúa como candado de seguridad, había sido comentada (`# @cognito_auth_required`) en varios archivos `main.py`.

**Motivo Técnico:**
1. **Velocidad de Desarrollo:** Durante la fase de construcción de la interfaz (Frontend), estar pidiendo o renovando un Token de Cognito cada hora ralentiza las pruebas. Al comentar esta línea, el desarrollador permitía que él mismo o su equipo pudieran consultar la base de datos velozmente y sin restricciones durante esa semana de trabajo intensivo.
2. **Olvido Humano:** Una vez que confirmaron que el endpoint funcionaba y entregaba los datos (ej: las ventas), olvidaron remover el símbolo `#` antes de enviar su código (commit/push) al servidor central en AWS.

## Listado de Archivos Auditados

A continuación, se detalla el estado exacto de los archivos en el momento de la auditoría. Todos los archivos han sido reparados y se encuentran correctamente securizados a la fecha de hoy.

### 🔴 Archivos que ESTABAN VULNERABLES (Línea Comentada con `#`)
- Identificados y reparados en: Dashboard, Cajas (abrir), Mecánicos (id/update), Ventas (get/id), Reparaciones (id), Proveedores (id).

### 🟢 Archivos que ESTABAN SEGUROS
- Todos los métodos `POST`, `DELETE` y `UPDATE` de Clientes, Productos, Ventas, etc., siempre mantuvieron su seguridad activa.

## Solución Definitiva Implementada
Para prevenir que el equipo de desarrollo vuelva a recurrir a esta práctica insegura de comentar el código para hacer pruebas, se modificó el archivo maestro ubicado en `layers/shared/decorators/lambda_decorators.py`. 

Se implementó un **"Switch Automático"** que examina las variables de entorno del servidor. 
- Si detecta la variable `AWS_SAM_LOCAL=true` (es decir, el desarrollador está en su computadora local trabajando mediante AWS SAM CLI), inyectará validación automática sin pedir tokens, acelerando el desarrollo.
- Si no la detecta (es decir, el código está subido a la nube real de AWS), forzará la revisión criptográfica estricta contra Internet a través de Amazon Cognito, protegiendo los datos.
