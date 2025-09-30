FROM 225665832482.dkr.ecr.us-east-1.amazonaws.com/fema/trustworthy:legacy-app-base-1.9
COPY ./ /opt/trustworthy/
WORKDIR /opt/trustworthy/
RUN chmod 777 -R .
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "src/genai_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
