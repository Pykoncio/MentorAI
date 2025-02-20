FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
ENTRYPOINT [ "streamlit", "run", "streamlit/streamlit_app.py" ]