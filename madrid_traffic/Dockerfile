FROM python:3.7.2-slim-stretch

COPY requirements.txt /
RUN pip install -r requirements.txt
COPY run.py tinybird.py madrid_traffic.py /cgi-bin/
RUN chmod +x /cgi-bin/run.py
EXPOSE 8080
CMD ["python", "-m", "http.server", "--cgi", "8080"]
