#Download base image python 3.5
FROM registry.bale.ai:2443/python:3.5
RUN echo "Asia/Tehran" > /etc/timezone
RUN ln -fs /usr/share/zoneinfo/Asia/Tehran /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

WORKDIR /reminder

COPY ./requirements.txt /reminder/requirements.txt

RUN pip install -r requirements.txt

COPY ./ /reminder

CMD ["python3.5", "main.py"]

