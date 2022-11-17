
import sys

import argparse

parser = argparse.ArgumentParser(prog = 'gen_search',
                    description = 'make some savedsearch.conf files for testing scheduling',
                    epilog ='''Writes to ./savedsearches.conf, copy that over your local version.  
                    See README for instructions and examples.  
                    See savedsearches.conf.spec for details of params used.''')
parser.add_argument('name')
parser.add_argument('-c', '--cron', default="* * * * *", help="A valid cron schedule, def is every minute")
parser.add_argument('-s', '--skew', default=None, help="value for allow_skew, eg one of: 80%% 3m 1h 1d, default None set")
parser.add_argument('-p', '--pause', default=10, help="sets the sleep pause in secs to simulate slow search, default 10 secs")
parser.add_argument('-x', '--priority', default='default', help="highest, higher, default")
parser.add_argument('-n', '--count', default=100, help="number of searches to schedule, default=100")
parser.add_argument('-w', '--window', default="auto", help="schedule_window value, default is auto")
parser.add_argument('-o', '--overwrite', action='store_true', default=False, help="overwrites savedsearches.conf creating a new file, default is append")
args = parser.parse_args()

pause = int(float(args.pause)*1000)
skew = "" if args.skew is None else f'\nallow_skew = {args.skew}'

with open('savedsearches.conf', mode='w' if args.overwrite else 'a') as conf:
    conf.write(f'#####################################\n')
    conf.write(f'# Schedule Testing name:{args.name} count:{args.count}\n')
    conf.write(f'#####################################\n\n')
    for i in range(1,int(args.count)+1):
        str = f'''
[ScheduleTesting n:{i} - {args.name}]
schedule_priority = {args.priority}
schedule_window = {args.window}
search = | makeresults | sleep pause={pause}{skew}
cron_schedule = {args.cron}
enableSched = 1

'''

        conf.write(str)

    conf.close()    
