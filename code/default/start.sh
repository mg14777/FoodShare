#!/bin/sh

# Define PYTHONPATH as local modules folder
export PYTHONPATH=${APP_HOME}/modules

# Extract LIBAOI libs from Debian package (into ./lib/x86_64-linux-gnu)
dpkg-deb -R libaio1_0.3.110-1_amd64.deb ${APP_HOME}

# Finalize OCI installation by creating required softlink
ln -s ${APP_HOME}/lib/instantclient_12_2/libclntsh.so.12.1 ${APP_HOME}/lib/instantclient_12_2/libclntsh.so

# Add OCI and LIBAIO to shared library path
export LD_LIBRARY_PATH=${APP_HOME}/lib/instantclient_12_2:${APP_HOME}/lib/x86_64-linux-gnu

# Install Python packages into local modules folder
pip --no-cache-dir install -r requirements.txt -t ${PYTHONPATH}

python ${APP_HOME}/server.py 