#!~replace
FROM sundwarf/skier-base
MAINTAINER eyesismine@gmail.com

# Clone app
RUN mkdir /var/skier/log /var/skier/pyapp
RUN git clone https://github.com/SkierPGP/Skier.git /var/skier/pyapp

# Add config.yml
ADD config.yml /var/skier/pyapp/config.yml

# Add startup script
ADD startup.sh /var/skier/startup.sh

# Add supervisor config - tbd
ADD cfgs/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Verify sources
RUN keybase dir verify --assert github:sundwarf --assert reddit:octagonclock --assert dns:naval.tf --assert dns:veriny.tf /var/skier/pyapp

# Set virtualenv
ENV VIRTUAL_ENV="/var/skier/venv"
ENV PATH="/var/skier/venv/bin:$PATH"

# Run setup script
RUN /var/skier/pyapp/setup.sh /var/skier/pyapp

# Change WORKDIR
WORKDIR /var/skier/pyapp
# Run migrations
RUN /var/skier/pyapp/manager.py db upgrade

# Expose ports
EXPOSE 5000




