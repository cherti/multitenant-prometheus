# Multitenant capable Prometheus-setup

## Background

This ansible repository contains a playbook `multitenant-prometheus.yml` which deploys a system equivalent to the one described in [this PromCon 2018 talk](https://www.youtube.com/watch?v=AO_I1oVcqBM).

## Requirements

This playbook is written for a Debian GNU/Linux. If you want to run it on other systems, you will need to change parts of the roles (at least package installation via the `apt` module) and you will most likely have to replace the `debian`-role entirely.

Furthermore, there are some binaries in `files/bin`. These are represented as text files in this repo, containing a link to the softwares' repositories with which they have to be replaced.


## Remarks

The repository contains a role `register_with_monitoring`.
This role is not required for the setup, but is an example of how Ansible playbooks can directly register new monitoring targets to it by just including another role.


