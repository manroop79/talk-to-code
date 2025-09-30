FROM 225665832482.dkr.ecr.us-east-1.amazonaws.com/fema/trustworthy:fema-base-1.50
COPY ./ /opt/femademo/
WORKDIR /opt/femademo/
RUN chmod 777 -R .
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "genai_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
