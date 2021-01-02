FROM sktrinh12/bdb-omiqpipeline:base_v1

ARG UNAME
ARG VERSION 
ARG PASSWORD
ENV PASSWORD "${PASSWORD}"
ENV UNAME "${UNAME}"
ENV VERSION "${VERSION}"
ENV APP_HOME /home/${UNAME}
ENV RETICULATE_PYTHON /usr/local/bin/python3

RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python-setuptools \
    python3-pypdf2 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install paramiko psycopg2-binary numpy pandas

RUN useradd -m -d $APP_HOME "${UNAME}" \
    && chown -R ${UNAME}:${UNAME} $APP_HOME \
    && echo "${UNAME}:${PASSWORD}" | chpasswd 

USER ${UNAME}

# set up ssh github
RUN mkdir -p $APP_HOME/.ssh/
COPY services/romiq/id_rsa $APP_HOME/.ssh/
RUN touch $APP_HOME/.ssh/known_hosts
RUN ssh-keyscan github.com >> $APP_HOME/.ssh/known_hosts

# git clone romiq branch
RUN mkdir -p $APP_HOME/R/install \
    && mkdir $APP_HOME/R/omiq_v${VERSION} \
    && git clone -b postgres-exptl-brach --single-branch git@github.com:sktrinh12/omiq.git $APP_HOME/R/omiq_v${VERSION}/OmiqPipeline

# export env var for bdb user (ENV does not carry over?) read from Rscript, install_omiq.R
RUN echo "${VERSION}" > $APP_HOME/env.version.tmp

# use root for r installing packages; use renv for caching; use of experimental docker
USER root
# install omiq
# COPY services/romiq/install_omiq.R $APP_HOME/R/omiq_v${VERSION}/OmiqPipeline/install_omiq.R
# COPY services/romiq/reticulate.sh $APP_HOME/R/
RUN sed -i "s/py_install/#py_install/g" $APP_HOME/R/omiq_v${VERSION}/OmiqPipeline/install_omiq.R \
    && sed -i "s/library/#library/g" $APP_HOME/R/omiq_v${VERSION}/OmiqPipeline/install_omiq.R
RUN Rscript $APP_HOME/R/omiq_v${VERSION}/OmiqPipeline/install_omiq.R

# change ownership so UNAME can import libraries
RUN chown -R $UNAME:$UNAME /usr/local/lib/R/site-library \
    && chown -R $UNAME:$UNAME /usr/local/lib/R/library \
    && chown -R $UNAME:$UNAME $APP_HOME/R

# testing
COPY services/romiq/test.R $APP_HOME/R/
EXPOSE 22
CMD service ssh start && while true; do sleep 500; done
