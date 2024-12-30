FROM python:3.11

RUN pip install pandas yfinance boto3 kagglehub

COPY main.py main.py
COPY get_financials.py get_financials.py
COPY upload.py upload.py
COPY util.py util.py

ENTRYPOINT ["python","main.py"]

