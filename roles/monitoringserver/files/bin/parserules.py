#!/usr/bin/env python3

import sys, subprocess, yaml, os, shutil
from subprocess import Popen, PIPE

homes = os.listdir('/home')

devnull = open(os.devnull, 'w')

for user in homes:
    groups = []
    rulefiles = [f for f in os.listdir('/home/{}/rules'.format(user)) if f.endswith('.yml') or f.endswith('.yaml')]
    for rf in rulefiles:
        rulefilepath = '/home/{}/rules/{}'.format(user, rf)
        if subprocess.call(["/usr/bin/promtool", "check", "rules", rulefilepath], stdout=devnull, stderr=devnull) != 0:
            print(" :: rulefile {} faulty, skipping".format(rulefilepath), file=sys.stderr)
        else:
            with open(rulefilepath, 'r') as f:
                y = yaml.load(f)
                for g in y['groups']:
                    g['name'] = '{}: {}'.format(user, g['name'])
                    for rule in g['rules']:
                        if 'alert' in rule:
                            rule['alert'] = '{}: {}'.format(user, rule['alert'])
                        elif not 'record' in rule:
                            continue

                        p = Popen(['/opt/promql-labelinjector', '-l', 'job', '-v', user, '-e', rule['expr']], stdout=PIPE)
                        out, _ = p.communicate()
                        if p.returncode != 0:
                            rule['expr'] = ''
                        else:
                            rule['expr'] = out.decode('utf-8').strip()

                        if not 'labels' in rule:
                            rule['labels'] = {}

                        rule['labels']['job'] = user

                        if 'annotations' in rule:
                            for k in rule['annotations']:
                                if '{' in rule['annotations'][k]:
                                    rule['annotations'][k] = "Value expansions in alerting templates are unfortunately not supported by this system."

                groups.append(g)

    userrulefile = "/etc/prometheus/rules/{}.yml".format(user)
    with open(userrulefile, 'w') as f:
        print('---', file=f)
        print('groups:', file=f)
        if len(groups) > 0:
            print(yaml.dump(groups), file=f)

    shutil.chown(userrulefile, user='prometheus', group='prometheus')
    os.chmod(userrulefile, 400)

subprocess.call(["/bin/systemctl", "reload", "prometheus.service"])
