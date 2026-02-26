# Guía de Arquitectura: Serverless Orientada a Dominios

Este documento explica la refactorización realizada en el backend, el porqué de los cambios y cómo entender el flujo actual de la aplicación.

---

## 🚀 1. ¿Por qué el cambio de arquitectura?

Antes, el código estaba disperso y duplicado. Cada Lambda (función) tenía su propia lógica de base de datos y validaciones, lo que causaba:
- **Código Duplicado**: Si querías cambiar cómo se guardaba un Cliente, tenías que editar 5 archivos diferentes.
- **Dificultad de Mantenimiento**: Era fácil olvidar actualizar un archivo y causar errores.
- **Desorden**: No estaba claro dónde terminaba la validación y dónde empezaba la lógica de negocio.

**La Solución:** Una arquitectura **Orientada a Dominios** con **Capas Consolidadas**. Ahora, cada dominio (Ventas, Clientes, etc.) tiene un "Cerebro Central" (`core`) que comparten todas sus Lambdas.

---

## 📂 2. Organización de Carpetas

La estructura ahora es predecible y organizada:

```text
src/domains/nombre_dominio/
├── core/                       <-- EL CEREBRO (Lógica Compartida)
│   ├── repository.py           <-- Habla con la Base de Datos (Supabase/DB)
│   ├── use_case.py             <-- Lógica de Negocio (Reglas, Cálculos)
│   └── schemas/                <-- Validaciones y Transformación de Datos
└── lambdas/                    <-- LOS GATILLOS (Puntos de Entrada API)
    ├── agregar_item/
    │   ├── main.py             <-- Orquestador de la Lambda
    │   └── params.py           <-- Limpieza y captura de parámetros
    └── ...
```

---

## 🌊 3. Flujo de Ejecución (Explicación Sencilla)

Imaginalo como un restaurante:
1.  **Lambda (`main.py`)**: Es el **Mesero**. Recibe el pedido (evento API).
2.  **Params (`params.py`)**: Es el **Filtro del Mesero**. Revisa que el pedido tenga sentido (campos obligatorios).
3.  **Schema (`core/schemas`)**: Es el **Control de Calidad**. Revisa que los ingredientes (datos) sean del tipo correcto y los prepara para la cocina.
4.  **Use Case (`core/use_case.py`)**: Es el **Chef**. Aplica las reglas (receta), hace cálculos y decide qué cocinar.
5.  **Repository (`core/repository.py`)**: Es la **Despensa**. Va a buscar o guardar los ingredientes en el refrigerador (Base de Datos).

---

## 🛠️ 4. Ejemplo Real: Dominio Mecánicos (`mechanics`)

### Archivo por Archivo:

1.  **`lambdas/add_mechanic/main.py`**:
    - Recibe el request de la API.
    - Llama a `params.py` para obtener los datos limpios.
    - Llama al `MechanicUseCase` para ejecutar la acción.
    - Devuelve una respuesta bonita (201 Created).

2.  **`lambdas/add_mechanic/params.py`**:
    - Extrae el JSON del cuerpo (`body`).
    - Llama al **Schema** para validar que el nombre no esté vacío.

3.  **`core/schemas/mechanic_schema.py`**:
    - Se asegura de que los datos parezcan un mecánico real (nombre, especialidad, etc.).
    - Genera el ID (UUID) automáticamente.

4.  **`core/use_case.py`**:
    - Recibe el objeto mecánico validado.
    - Aquí podrías poner reglas como: "No permitir dos mecánicos con el mismo DNI".
    - Le pide al **Repository** que lo guarde.

5.  **`core/repository.py`**:
    - Ejecuta el comando SQL o la función de Supabase (`insert`).
    - No sabe nada de reglas de negocio, solo sabe guardar y leer.

---

## ✅ Beneficios Finales
- **Orden**: Sabes exactamente dónde buscar si algo falla.
- **Rapidez**: Para crear una nueva función, solo necesitas el `main.py` y `params.py`; la lógica pesada ya está en el `core`.
- **Elegancia**: Nombres cortos (`params.py` en vez de `load_initial_parameters.py`) y código fácil de leer.
