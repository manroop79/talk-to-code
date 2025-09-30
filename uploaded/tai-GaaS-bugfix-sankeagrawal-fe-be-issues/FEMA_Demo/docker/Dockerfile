FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends linux-libc-dev
RUN apt-get install -y vim emacs nano software-properties-common gnupg2 python3-pip

WORKDIR /app

# Many installation processes are run in this script
# It is located at docker/installation_media/install_base_deps.sh
COPY docker/installation_media /app
RUN bash install_base_deps.sh
# Separating out requirements installs as they are commonly changed
RUN python -m pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "src/genai_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
