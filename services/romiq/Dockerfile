FROM bdbcontainerreg.azurecr.io/bdb-omiq:v2

ARG UNAME
ARG PASSWORD
ARG VERSION
ENV PASSWORD $PASSWORD
ENV UNAME $UNAME
ENV VERSION $VERSION

ENV APP_HOME /home/${UNAME}

RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python-setuptools \
    python3-pypdf2 \
    curl \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install numpy pandas

RUN useradd -m -d $APP_HOME "${UNAME}" \
    && chown -R ${UNAME}:${UNAME} $APP_HOME \
    && echo "${UNAME}:${PASSWORD}" | chpasswd

# testing
COPY services/romiq/OmiqPipeline $APP_HOME/R/omiq_v$VERSION/OmiqPipeline

# install omiq
RUN Rscript $APP_HOME/R/omiq_v${VERSION}/OmiqPipeline/install_omiq.R

# change ownership so UNAME can import libraries
RUN chown -R $UNAME:$UNAME /usr/local/lib/R/site-library \
    && chown -R $UNAME:$UNAME /usr/local/lib/R/library \
    && chown -R $UNAME:$UNAME $APP_HOME/R

EXPOSE 22
CMD service ssh start && while true; do sleep 500; done
