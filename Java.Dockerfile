FROM azul/zulu-openjdk:19-latest

# Run as non-root user
RUN groupadd -g 322 lavalink && \
    useradd -r -u 322 -g lavalink lavalink
USER lavalink

WORKDIR /home/Lavalink

COPY lavalink/Lavalink.jar .
COPY lavalink/application.yml .

ENTRYPOINT ["java", "-Djdk.tls.client.protocols=TLSv1.1,TLSv1.2", "-Xmx1G", "-jar", "Lavalink.jar"]
