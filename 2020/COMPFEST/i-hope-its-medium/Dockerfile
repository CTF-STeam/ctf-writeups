FROM nsjail
# forked from https://github.com/google/nsjail

RUN mkdir /app && apt-get update && apt-get install lib32z1 -y && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install python3-pip -y && rm -rf /var/lib/apt/lists/*
RUN pip3 install pycrypto

WORKDIR /app
COPY files/ihopeitsmedium.py .
COPY files/flag.txt .
RUN chmod 555 ihopeitsmedium.py
RUN chmod 444 flag.txt

COPY nsjail.sh /
RUN chmod 555 /nsjail.sh
ENTRYPOINT ["/nsjail.sh"]
CMD ["ihopeitsmedium.py"]
