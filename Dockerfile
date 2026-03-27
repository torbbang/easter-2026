FROM alpine:3.20
RUN apk add --no-cache python3 ucspi-tcp6
COPY easter.py /easter.py
EXPOSE 23
CMD ["tcpserver", "-v", "0", "23", "python3", "-u", "/easter.py"]
