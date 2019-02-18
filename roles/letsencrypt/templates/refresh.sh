#!/bin/bash

cd {{ le_cert_dir }}/certs || exit 1
for domain in *
do
	../dehydrated -c -f ../config -d $domain
done

source {{ le_cert_dir }}/reload-services/*
