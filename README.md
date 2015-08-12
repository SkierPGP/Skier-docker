## Skier

*Skier* is a free and open-source PGP server, designed as a replacement to the aging SKS set of servers running on most common keyservers.

### Skier_Docker

This repository serves to hold the Dockerfiles and launcher for the Skier docker containers. It serves as an easy way to use and install Skier without having to install the trillions of dependencies a Python and Flask install pulls in.
The base image is derived from ubuntu:15.04.

Skier uses three containers - a keyring (persistent) data storage, a redis container and an application container.

### Setup instructions

1. **Build the images.**
    
   ``./launcher.py --build-all``
   
   This will build both the base and skier docker image, and save them as 'skier-base' and 'skier'.
   If you wish to skip building the base image, and just build the Skier image from SunDwarf/skier-base, run:
   
   `./launcher.py --build-skier`
   
   If you want to use your own local image for skier-base or skier, run:
   
   `./launcher.py --build-base --from-local --local-image <image>`
    
1. **Bootstrap**

    `./launcher.py --bootstrap`
    
    This will build the data-only container, the redis container, and an empty skier container before deleting it.
    
1. **Start**

    `./launcher.py --start (--detached)`
    
    If you omit the --detached argument, this will start Skier in an attached session. If you wish to detach and run in a detached session:
    
    ```
    ./launcher.py --stop
    ./launcher.py --destroy
    ./launcher.py --bootstrap
    ./launcher.py --start --detached
    ```
    

    
    