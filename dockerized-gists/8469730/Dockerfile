FROM python:2.7.13
ADD snippet.py snippet.py
RUN ["pip", "install", "email"]
RUN ["pip", "install", "imapclient"]
CMD ["python", "snippet.py"]