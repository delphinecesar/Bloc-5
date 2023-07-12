FROM python:3.9
COPY . /home/app

WORKDIR /home/app

RUN pip install boto3 pandas gunicorn streamlit sklearn matplotlib seaborn plotly openpyxl

CMD streamlit run --server.port $PORT --server.address "0.0.0.0" getaround.py