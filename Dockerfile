#Download base image python 3.5
FROM python:3.5
RUN echo "Asia/Tehran" > /etc/timezone

WORKDIR /bmi_assistant

COPY ./requirements.txt /bmi_assistant/requirements.txt

RUN pip install -r requirements.txt

COPY ./ /bmi_assistant

CMD ["python3.5", "main.py"]

