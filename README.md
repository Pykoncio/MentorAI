# 📚 **MentorAI**

<img src="https://drive.google.com/uc?id=1mzgfusMIpaVrHRGtVSgGEr7EyiA_T6gs"/>

MentorAI is a virtual tutoring system that utilizes intelligent agents to provide tutoring in various academic subjects using artificial intelligence techniques.

# 👥 Contributors
Jesus Ruiz Toledo – [Github](https://github.com/jesusruiztoledo) – Email: jesusruiz2829@gmail.com – Contribution: 33.3%

Hugo Peralta Muñoz - [Github](https://github.com/Pykoncio) – Email: hugoperalta2003@gmail.com – Contribution: 33.3%

Borja Bravo Casermeiro – [Github](https://github.com/boorjabraavo21) – Email: borjabravo07@gmail.com – Contribution: 33.3%

## 📌 Objectives
- Develop AI agents capable of tutoring in various academic subjects.
- Implement Natural Language Processing (NLP) for interactive learning.
- Enhance scalability and performance through containerized deployment with Docker.
- Provide real-time news updates and external API integrations to keep content relevant.

MentorAI is a virtual tutoring system that utilizes intelligent agents to provide tutoring in a variety of academic subjects using advanced artificial intelligence techniques.

## 📑 Table of Contents
- [Installation Guide with Docker](#️-installation-guide-with-docker)
- [Installation Guide without Docker (Not Recommended)](#installation-guide-without-docker-not-recommended)
- [Project Structure](#-project-structure)
- [File Descriptions](#-file-descriptions)
- [Presentation Resources](#-presentation-resources)
- [Bibliography](#-bibliography)

## 🛠️ **Installation Guide with Docker**

This is the easiest way to install and run MentorAI using Docker and Docker Compose.

### **Requirements**

- Docker
- Docker Compose

### **Installation**

1. Create an `.env` file in the root of the project with the following variables:

```sh
OPENAI_API_KEY=your_openai_key
NEWS_API_KEY=your_newsapi_key
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_ROOT_PASSWORD=your_mysql_root_password
MYSQL_DATABASE=your_mysql_database
``` 

2. Start the containers by running the following command from the project's root directory:

`docker-compose -f app/docker/docker-compose.yml up --build`

This will start the FastAPI server on port 8000 and the Streamlit application on port 8501, as well as the MySQL server on the port 3307.

Once the containers are running, access the Streamlit web interface at: `http://localhost:8501`

## **Installation Guide without Docker (Not Recommended)**

### **Requirements:**

- Python 3.11
- A running database with the characteristics defined below.
- All project dependencies installed.

**Create a virtual environment**
1. Create the virtual environment:
`python -m venv venv`

2. Activate the virtual environment:
    * On Windows: 
        ```terminal
        venv/Scripts/activate
        ```

    * On macOS/Linux:
        ```terminal
        source venv/bin/activate
        ```

3. Install the project dependencies:

    `pip install -r requirements.txt`

### **Environment Variables**
Create an `.env` file in the root of the project with the following variables:

```sh
OPENAI_API_KEY=your_openai_key
NEWS_API_KEY=your_newsapi_key
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_ROOT_PASSWORD=your_mysql_root_password
MYSQL_DATABASE=your_mysql_database
``` 

> [!NOTE]  
> When running without Docker, ensure that you have a database set up with the above characteristics.

#### Running the Project
To start the FastAPI server:

`uvicorn app.main:app --reload`

To start the Streamlit application:

`streamlit run app/streamlit/streamlit_app.py`

When deployment is complete, open your web browser and navigate to: `http://localhost:8501` to access the MentorAI interface.

## 📂 **Project Structure**
```markdown
.env  
.gitignore  
app/  
├── __init__.py  
├── agents/  
│   ├── __init__.py  
│   ├── biology_teacher.py  
│   ├── chemistry_teacher.py  
│   ├── economy_teacher.py  
│   ├── history_teacher.py  
│   ├── languaje_teacher.py  
│   ├── math_teacher.py  
│   ├── news_agent.py  
│   ├── physics_teacher.py  
│   ├── planner.py  
│   └── programming_teacher.py  
├── core/  
│   ├── __init__.py  
│   └── config.py  
├── docker/  
│   ├── docker-compose.yml  
│   ├── Dockerfile.fastapi  
│   └── Dockerfile.streamlit  
├── main.py  
├── models/  
│   ├── __init__.py  
│   └── filtering_model/  
│       ├── filter_model_badwords.ipynb  
│       └── toxic_classifier.joblib  
├── schemas/  
│   ├── __init__.py  
│   └── chat.py  
├── services/  
│   ├── __init__.py  
│   ├── filtering_service.py  
│   └── openai_service.py  
└── streamlit/  
    └── streamlit_app.py
docs/  
├── logo_mentorai.png  
└── Presentacion_MentorAI.pdf  
output/  
└── messages_output.csv  
README.md  
requirements.txt  
src/
└── templates/
```


## 📄 **File Descriptions**
`main.py`
This is the main file that configures and runs the FastAPI server. It contains the endpoints configuration and application initialization.

`agents`
This directory contains the tutoring agents for different subjects. Each agent is responsible for providing answers and tutoring in its specific subject area:

* `biology_teacher.py`: Biology tutoring agent.
* `chemistry_teacher.py`: Chemistry tutoring agent.
* `economy_teacher.py`: Economy tutoring agent.
* `history_teacher.py`: History tutoring agent.
* `language_teacher.py`: Language tutoring agent.
* `math_teacher.py`: Mathematics tutoring agent.
* `news_agent.py`: News agent providing updated information.
* `physics_teacher.py`: Physics tutoring agent.
* `planner.py`: Planning agent that helps organize study sessions.
* `programming_teacher.py`: Programming tutoring agent.

`config.py` 

This file uses pydantic to configure the project. It defines the global configurations and the environment variables required for the project to work.

`models`

This directory contains the model used in the project for filtering inappropriate language. The model validates all data within the application before it's processed by the APIs.

`schemas`

Defines data schemas using pydantic. These schemas are used to validate and structure the incoming requests and outgoing responses from the endpoints:

* `chat.py:` Schema for chat requests and responses.

`services`

This directory contains the services used by the agents, including the OpenAI service and the filtering service. These services encapsulate business logic and interactions with external APIs:

* `filtering_service.py`: Service for filtering inappropriate language.
* `openai_service.py`: Service for interacting with the OpenAI API.

`streamlit_app.py`

The Streamlit application provides a graphical interface for interacting with the tutoring system. It includes a chat where users can input questions and displays the conversation history during the session.

## 🎬 Presentation Resources
- [Project Presentation Video](https://www.youtube.com/watch?v=5s27SuEfBg0)
- [Project Canvas](https://www.canva.com/design/DAGgZwpR4OY/wBnTFRACWRTl7wDuxULeVw/edit?utm_content=DAGgZwpR4OY&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
- [Presentation PDF](/docs/Presentacion_MentorAI.pdf)

## 📚 Bibliography
* [Streamlit Documentation](https://docs.streamlit.io/)

* [FastAPI Documentation](https://fastapi.tiangolo.com/)

* [Docker Documentation](https://docs.docker.com/)

* [Mini-course on SQLAlchemy](https://www.youtube.com/watch?v=XSAjQDM8ZS4)

* [OpenAI Api Reference](https://platform.openai.com/docs/api-reference/introduction)

* [Advances in Intelligent Tutoring Systems](https://link.springer.com/book/10.1007/978-3-642-14363-2) - Nkambou, R., Mizoguchi, R., & Bourdeau, J. (2010). Springer Berlin Heidelberg.