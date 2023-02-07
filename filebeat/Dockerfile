FROM docker.elastic.co/beats/filebeat:8.5.2
ENV cloudId=${cloudId}
ENV cloudAuth=${cloudAuth}
ENV TZ=America/Mexico_City
USER root
RUN chown -R root /usr/share/filebeat/
RUN chmod -R go-w /usr/share/filebeat/
EXPOSE 5068