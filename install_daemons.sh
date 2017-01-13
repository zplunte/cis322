#!/usr/bin/env bash
# A bash script for installing PostgreSQL and Apache Httpd
# Co-installs both under a location specified by the arg PREFIX
# Initially written by Z.P.L. for use by OSNAP as installation prep for LOST.

# arg specifying install location
PREFIX=$1

# retrieve/clone PostgreSQL source from GitHub, store in current directory
# need to test clones to current directory
git clone https://github.com/postgres/postgres.git ./rep_loc

# start PostgreSQL build with configure
./rep_loc/configure --prefix=$PREFIX

# full PostgreSQL make/install with docs
make world
make install-world

# download Apache Httpd 2.4.25 using curl
curl -o httpd-2.4.25.tar.gz http://mirrors.ocf.berkeley.edu/apache//httpd/httpd-2.4.25.tar.gz

# extract Apache
gzip -d httpd-2.4.25.tar.gz
tar xvf httpd-2.4.25.tar

# move into httpd-2.4.25
cd httpd-2.4.25

# start Apache build with configure
./configure --prefix=$PREFIX

# make/install Apache
make
make install

# reconfig Apache to listen at Port 8080 instead of Port 80
sed -i '/Listen 80/c\Listen 8080' $PREFIX/conf/httpd.conf

# add PostgreSQL and Apache bins to path
export PATH=$PREFIX/bin:$PATH
