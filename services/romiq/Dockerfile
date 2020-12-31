FROM bioconductor/bioconductor_docker:RELEASE_3_10

ARG UNAME
ARG VERSION 
ARG PASSWORD
ENV PASSWORD "${PASSWORD}"
ENV UNAME "${UNAME}"
ENV VERSION "${VERSION}"
ENV APP_HOME /home/${UNAME}

RUN apt-get -y update

RUN apt-get install -y git \
    ssh \
    sshpass \
    curl \
    libssl-dev \
    zlib1g-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    libpng-dev \
    openssh-server \
    libgit2-dev \
    sudo 

RUN useradd -m -d $APP_HOME "${UNAME}" \
    && chown -R ${UNAME}:${UNAME} $APP_HOME \
    && echo "${UNAME}:${PASSWORD}" | chpasswd 

# # remove rstudio-server
# RUN dpkg --remove rstudio-server \
#     && rm /etc/init.d/rstudio-server \
#     && rm -rf /etc/services.d/rstudio \
#     && rm -rf /home/rstudio

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

# move install pacakges files to diff directory or else renv will try to pre-emptively install (renv::init())
RUN mv $APP_HOME/R/omiq_v${VERSION}/OmiqPipeline/renv*.R $APP_HOME/R/install \
    && mv $APP_HOME/R/omiq_v${VERSION}/OmiqPipeline/install.R $APP_HOME/R/install

# export env var for bdb user (ENV does not carry over?) read from Rscript, install_omiq.R
RUN echo "${VERSION}" > $APP_HOME/env.version.tmp

# add to libpaths for R to find the renv libraries
RUN touch $APP_HOME/.Renviron \
    && echo "R_LIBS_USER=/home/${UNAME}/R/install/renv/library/R-3.6/x86_64-pc-linux-gnu" >> $APP_HOME/.Renviron

# use root for r installing packages; use renv for caching; use of experimental docker
USER root
# RUN Rscript $APP_HOME/R/install/renv_install.R
# RUN Rscript $APP_HOME/R/install/renv_install_packages.R
RUN sed -i 's/renv/BiocManager/g' $APP_HOME/R/install/install.R \
    && sed -i 's/bioc:://g' $APP_HOME/R/install/install.R

RUN Rscript $APP_HOME/R/install/install.R

# update rlang and vctrs (separate from renv)?
RUN Rscript -e "install.packages('rlang')" \
    && Rscript -e "install.packages('vctrs')"

# install omiq
COPY services/romiq/install_omiq.R $APP_HOME/R/omiq_v${VERSION}/OmiqPipeline/install_omiq.R
RUN Rscript $APP_HOME/R/omiq_v${VERSION}/OmiqPipeline/install_omiq.R

# change ownership so UNAME can import libraries
RUN chown -R $UNAME:$UNAME /usr/local/lib/R/site-library \
    && chown -R $UNAME:$UNAME /usr/local/lib/R/library \
    && chown -R $UNAME:$UNAME $APP_HOME/R/install

EXPOSE 22
CMD service ssh start && while true; do sleep 500; done
