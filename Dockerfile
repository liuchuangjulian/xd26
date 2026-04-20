FROM localhost:50000/python3920:0.2.8
ADD src /app
RUN chown -R app:app /app && chmod +x /app/start.sh
RUN mkdir /app/cert

ENV PYTHONPATH=/app
WORKDIR /app
# USER app ./start.sh
CMD ["./start.sh"]
