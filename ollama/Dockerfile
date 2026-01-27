FROM ollama/ollama:latest

EXPOSE 11434

COPY start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]
