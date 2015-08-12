#!~replace
FROM sundwarf/skier-base
MAINTAINER eyesismine@gmail.com

# Clone app
RUN mkdir /var/skier/{logs,pyapp,keyring}
RUN git clone https://git.sundwarf.me/Skier/Skier.git /var/skier/pyapp

# Add config.yml
ADD config.yml /var/skier/pyapp/config.yml

# Add startup script
ADD startup.sh /var/skier/startup.sh

# Add supervisor config - tbd

# Verify sources
RUN keybase dir verify /var/skier/pyapp

# Set virtualenv
ENV VIRTUAL_ENV="/var/skier/venv"
ENV PATH="/var/skier/venv/bin:$PATH"

# Run setup script
RUN /var/skier/pyapp/setup.sh /var/skier/pyapp

# Expose ports
EXPOSE 5000




