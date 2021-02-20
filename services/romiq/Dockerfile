FROM sktrinh12/bdb-omiqpipeline:base_v3

ARG UNAME
ARG PASSWORD
ARG VERSION
ENV PASSWORD $PASSWORD
ENV UNAME $UNAME
ENV VERSION $VERSION

ENV APP_HOME /home/${UNAME}
ENV TZ America/Los_Angeles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python-setuptools \
    python3-pypdf2 \
    curl \
    vim \
    sudo \
    netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip \
    && mkdir -p $APP_HOME/app \
    && mkdir -p $APP_HOME/R

COPY services/romiq/app/ $APP_HOME/app
RUN pip3 install -r $APP_HOME/app/requirements.txt

# install omiq
RUN Rscript $APP_HOME/R/omiq_v${VERSION}/OmiqPipeline/install_omiq.R

# change ownership so UNAME can import libraries
# RUN chown -R $UNAME:$UNAME /usr/local/lib/R/site-library \
#     && chown -R $UNAME:$UNAME /usr/local/lib/R/library \
#     && chown -R $UNAME:$UNAME $APP_HOME/R

EXPOSE 5000
WORKDIR $APP_HOME/app/app
CMD ["python3", "app.py"]
