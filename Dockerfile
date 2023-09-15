FROM python:3.11.5

RUN mkdir -p /std

COPY . /std

RUN python3 -m pip install -r /std/requirements.txt

EXPOSE 5000

CMD ["python","/std/app.py"]
