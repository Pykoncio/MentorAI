# 📚 MentorAI

MentorAI es un sistema de tutoría virtual que utiliza agentes inteligentes para proporcionar tutoría en diversas materias académicas utilizando técnicas de inteligencia artificial.

## 📌 Objetivos

- Desarrollar agentes de IA capaces de tutorizar en diferentes materias académicas.
- Implementar Procesamiento de Lenguaje Natural (NLP) para un aprendizaje interactivo.
- Adaptar las estrategias de tutoría basadas en el progreso y la retroalimentación del estudiante.

## 🛠️ Configuración

### Requisitos

- Python 3.11.9
- Instalar las dependencias del proyecto:

```sh
pip install -r requirements.txt
```

### Variables de entorno

Crear un archivo `.env` en la raiz del proyecto con las siguientes variables:

```sh
OPENAI_API_KEY=tu_clave_de_openai
NEWS_API_KEY=tu_clave_de_newsapi
```

### Ejecuciión del Proyecto

Para iniciar el servidor FastAPI:

```sh
uvicorn app.main:app --reload
```

Para iniciar la aplicación de Streamlit:

```sh
streamlit run app/streamlit/streamlit_app.py
```

### 📂 Estructura del Proyecto

```markdown
app/
    __init__.py
    agents/
        __init__.py
        biology_teacher.py
        chemistry_teacher.py
        economy_teacher.py
        history_teacher.py
        languaje_teacher.py
        math_teacher.py
        news_agent.py
        physics_teacher.py
        planner.py
        programming_teacher.py
    core/
        __init__.py
        config.py
    main.py
    models/
        __init__.py
        filtering_model/
    schemas/
        __init__.py
        chat.py
    services/
        __init__.py
        filtering_service.py
        openai_service.py
    streamlit/
        streamlit_app.py
README.md
requirements.txt
.gitignore
```

## 📄 Descripción de Archivos

### `main.py`

Archivo principal que configura y ejecuta el servidor FastAPI. Este archivo contiene la configuración de los endpoints y la inicialización de la aplicación.

### `agents`

Contiene los agentes de tutoría para diferentes materias. Cada agente es responsable de proporcionar respuestas y tutoría en su área específica:

- `biology_teacher.py`: Agente de tutoría en biología.
- `chemistry_teacher.py`: Agente de tutoría en química.
- `economy_teacher.py`: Agente de tutoría en economía.
- `history_teacher.py`: Agente de tutoría en historia.
- `languaje_teacher.py`: Agente de tutoría en lenguaje.
- `math_teacher.py`: Agente de tutoría en matemáticas.
- `news_agent.py`: Agente de noticias que proporciona información actualizada.
- `physics_teacher.py`: Agente de tutoría en física.
- `planner.py`: Agente planificador que ayuda a organizar el estudio.
- `programming_teacher.py`: Agente de tutoría en programación.

### `config.py`

Configuración del proyecto utilizando `pydantic`. Este archivo define las configuraciones globales y las variables de entorno necesarias para el funcionamiento del proyecto.

### `models`

Contiene los modelos utilizados en el proyecto, incluyendo el modelo de filtrado de lenguaje soez. Estos modelos son utilizados para estructurar y validar los datos que se manejan en la aplicación.

### `schemas`

Define los esquemas de datos utilizando `pydantic`. Estos esquemas son utilizados para validar y estructurar las solicitudes y respuestas de los endpoints:

- `chat.py`: Esquema para las solicitudes y respuestas del chat.

### `services`

Contiene los servicios utilizados por los agentes, incluyendo el servicio de OpenAI y el servicio de filtrado. Estos servicios encapsulan la lógica de negocio y las interacciones con APIs externas:

- `filtering_service.py`: Servicio para filtrar lenguaje inapropiado.
- `openai_service.py`: Servicio para interactuar con la API de OpenAI.

### `streamlit_app.py`

Aplicación Streamlit para interactuar con el sistema de tutoría. Esta aplicación proporciona una interfaz gráfica para que los usuarios puedan interactuar con los agentes de tutoría. Contiene un chat donde ingresar la pregunta y un historial con las conversaciones anteriores almacenadas en la sesión.

## 📝 Ejemplos de Uso

### Endpoint de Chat

Para interactuar con los agentes de tutoría, puedes enviar una solicitud POST al endpoint `/chat` con el siguiente formato:

```json
{
    "message": "What you know about Roman Empire?"
}
```

La respuesta incluirá el mensaje del agente de tutoría correspondiente.

### Interfaz Web

Puedes acceder a una interfaz web simple para probar el chat en el endpoint `/chat`.

### Aplicación de Streamlit

Para ejecutar la aplicación de Streamlit 

## 🧪 Pruebas

### Pruebas Unitarias
Para ejecutar las pruebas unitarias, utiliza el siguiente comando:

```sh
pytest
```

### Cobertura de Pruebas
Para generar un informe de cobertura de pruebas, utiliza el siguiente comando:

```sh
pytest --cov=app
```

## 📜 Licencia
RELLENAR.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## 📧 Contacto
Para cualquier consulta o sugerencia, puedes contactarnos a través de:

- Email: RELLENAR
- GitHub: MentorAI

## 🌟 Agradecimientos

RELLENAR





