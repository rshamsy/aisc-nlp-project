FROM ubuntu:18.04


# EXPOSE 5000

# Set character encoding environment variables
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

# Allow apt-get install without interaction from console
ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && apt-get -y --no-install-recommends install \
		ca-certificates \
		git \
		ssh \
    	wget && \
	apt-get clean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/*

ENV HOME /root

WORKDIR $HOME


# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.5.1-Linux-x86_64.sh && \
	bash Miniconda3-4.5.1-Linux-x86_64.sh -b -p $HOME/miniconda && \
	rm Miniconda3-4.5.1-Linux-x86_64.sh

# Set the path env to include miniconda
ENV PATH /root/miniconda/bin:$PATH

COPY ./flask-app $HOME

# Create a conda environment from the specified conda.yaml
RUN conda env create --file $HOME/models/M0p1-mlpyfunc/mlflow_env.yml

# Add to .bashrc
RUN echo "source activate aisc-base-model-RS" >> .bashrc

COPY start.sh $HOME

# Make our start script executable
RUN ["chmod", "+x", "$HOME/start.sh"]

# Start the API
ENTRYPOINT [ "/root/start.sh" ]
