FROM python:3.7-alpine
RUN pip install selenium jinja2
COPY . /src
RUN cd /src && python setup.py install

