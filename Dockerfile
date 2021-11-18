FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
CMD streamlit run app.py --server.enableCORS=false
