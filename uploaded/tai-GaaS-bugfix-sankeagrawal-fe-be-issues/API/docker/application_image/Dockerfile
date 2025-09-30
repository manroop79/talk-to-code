FROM 225665832482.dkr.ecr.us-east-1.amazonaws.com/fema/trustworthy:api-base-1.0
COPY ./ /opt/api/
WORKDIR /opt/api/
RUN chmod 777 -R .
EXPOSE 8501
ENTRYPOINT ["uvicorn", "app:app", "--host", "localhost", "--port", "8000", "--reload"]
