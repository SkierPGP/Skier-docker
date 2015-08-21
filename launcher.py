#!/usr/bin/env python3
# Skier docker container launcher.
# This file is licenced under the MIT Licence.
# For more information, view the LICENCE file.

import argparse
import copy
import os
import subprocess
import sys


green = "\033[0;32m"
red = "\033[0;31m"
blue = "\033[0;34m"
purple = "\033[0;35m"
normal = "\033[0m"

def _build_image(target, from_local: bool=False, local_image: str="skier-base"):
    # Build the desired image.
    command = ["docker", "build"]
    dir = target
    if not os.path.exists(dir):
        print(red + "STOP: Target {} does not exist.".format(target) + normal, file=sys.stderr)
        sys.exit(1)
    print(green + "LAUNCH: Beginning build of target {} {}".format(dir, "from local image {}".format(local_image) if from_local else "") + normal)
    # First, replace any FROM images if defined.
    with open(dir + "/Dockerfile", "r") as f:
        lines = f.readlines()
        nlines = copy.copy(lines)
        for num, line in enumerate(lines):
            if '#!~replace' in line:
                if from_local:
                    nlines[num+1] = "FROM {}\n".format(local_image)
                    break
        del lines
        nf = open("{t}/Dockerfile-temp-{t}".format(t=target), 'w')
        nf.write(''.join(nlines))
        nf.close()

    command.extend(["-t", "{}".format(target if target != "base" else "skier-base")])
    command.extend(["--no-cache"])
    command.extend(["--file={t}/Dockerfile-temp-{t}".format(t=target)])
    command.extend([dir])
    print(blue + "BUILD: Running command \"{}\"".format(' '.join(command)) + normal)
    proc = subprocess.Popen(command)
    proc.wait()
    if proc.returncode != 0:
        print(red + "BUILD: Build failed with non-zero exit code {}".format(proc.returncode) + normal)
    else:
        print(green + "BUILD: Build completed successfully." + normal)

def _bootstrap(from_local: bool=False, local_image="skier"):
    currdir = os.getcwd() + "/" # Safety first!

    if not from_local:
        local_image = "skier"

    basecommand = ["docker", "run"]

    print(purple + "LAUNCH: Beginning bootstrap for new Skier app...")
    print("LAUNCH: Using base image {}".format(local_image) + normal)


    print(purple + "BOOTSTRAP: Building redis container..." + normal)

    rediscmd = basecommand + ["--name", "skier-redis", "-d", "redis", "redis-server"]

    proc = subprocess.Popen(rediscmd)
    proc.wait()
    if proc.returncode != 0:
        print(red + "BOOTSTRAP: Redis container failed to start." + normal, file=sys.stderr)
        sys.exit(1)

    print(purple + "BOOTSTRAP: Verifying first launch of Skier container..." + normal)
    skiercmd = basecommand + ["--name", "skier", "--volumes-from", "skier-keyring", local_image, "true"]
    proc = subprocess.Popen(skiercmd)
    proc.wait()
    if proc.returncode != 0:
        print(red + "BOOTSTRAP: Building Skier container failed with non-zero exit code {}".format(proc.returncode) + normal, file=sys.stderr)
        sys.exit(1)

    print(purple + "BOOTSTRAP: Deleting temporary container" + normal)
    delcmd = "docker rm skier".split()
    proc = subprocess.Popen(delcmd)
    proc.wait()
    if proc.returncode != 0:
        print(red + "BOOTSTRAP: Deleting temporary Skier container failed with non-zero exit code {}".format(proc.returncode) + normal, file=sys.stderr)
        sys.exit(1)

    print(green + "BOOTSTRAP: Bootstrap completed successfully!" + normal)


def _start(target: str, detached: bool=False):
    print(purple + "LAUNCH: Starting Skier containers.." + normal)
    basecommand = ["docker", "run", "--link", "skier-redis:redis", "--name", "skier", "-p", "5000:5000", "-p", "2222:2222", "skier"]
    command = basecommand
    if detached:
        command.insert(-1, "-d")

    command += ["/usr/bin/supervisord"]
    subprocess.call(command)

def _stop(target: str):
    print(purple + "LAUNCH: Stopping Skier containers.." + normal)
    basecommand = "docker stop skier skier-redis".split()
    proc = subprocess.Popen(basecommand)
    proc.wait()
    if proc.returncode != 0:
        print(red + "LAUNCH: Stopping Skier containers failed with non-zero exit code {}".format(proc.returncode) + normal, file=sys.stderr)
        sys.exit(1)

def _destroy(target: str):
    basecommand = ["docker", "rm"]
    print(red + "DESTROY: Destroying target {}".format(target) + normal)
    proc = subprocess.Popen(basecommand + [target])
    proc.wait()
    if proc.returncode != 0:
        print(purple + "DESTROY: Destroying target failed with return code {}".format(proc.returncode) + normal, file=sys.stderr)
    else:
        print(green + "DESTROY: Target destroyed successfully." + normal)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skier PGP Launcher")

    builds = parser.add_mutually_exclusive_group()
    builds.add_argument("-a", "--build-all", help="Build all images.", action="store_true", default=False)
    builds.add_argument("--build-base", help="Build the base image.", action="store_true", default=False)
    builds.add_argument("--build-skier", help="Build the Skier image.", action="store_true", default=False)

    parser.add_argument("--from-local", help="Use a local image.", action="store_true", default=False)
    parser.add_argument("--local-image", help="Local image to use.", default="skier-base")

    parser.add_argument("-b", "--bootstrap", help="Bootstrap Skier.", action="store_true", default=False)

    runs = parser.add_mutually_exclusive_group()
    runs.add_argument("-s", "--start", help="Start the container.", action="store_true", default=False)
    runs.add_argument("-e", "--stop", help="Stop the container.", action="store_true", default=False)

    parser.add_argument("--detached", help="Start container in detched mode.", action="store_true", default=False)

    parser.add_argument("-d", "--destroy", help="Destroy the container.", action="store_true", default=False)
    parser.add_argument("--destroy-data", help="Destroy the keyring too.", action="store_true", default=False)

    args = parser.parse_args()

    if args.from_local:
        image = args.local_image
        bs_image = args.local_image
    else:
        image = "sundwarf/skier_base"
        bs_image = "skier"


    if args.destroy:
        if args.destroy_data:
            _destroy("skier-keyring")
        _destroy("skier-redis")
        _destroy("skier")
        sys.exit(0)

    if args.bootstrap:
        _bootstrap(from_local=args.from_local, local_image=bs_image)
        sys.exit(0)

    if args.start:
        _start("gunicorn", args.detached)
        sys.exit(0)

    if args.stop:
        _stop("")
        sys.exit(0)

    if args.build_all:
        _build_image("skier-base", False)
        _build_image("skier", True, "skier-base")

    if args.build_base:
        _build_image("skier-base", from_local=args.from_local, local_image="ubuntu:15.04" if not args.from_local else image)

    if args.build_skier:
        _build_image("skier", from_local=args.from_local, local_image=image)