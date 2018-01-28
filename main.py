# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import csv
from operator import itemgetter

# toy-matching-engine
# Invocation: python3 main.py CONFIGFILE INFILE OUTFILE
# See README for more info

configPath = sys.argv[1]
infilePath = sys.argv[2]
outfilePath = sys.argv[3]
config = list(csv.reader(open(configPath)))
people = list(csv.DictReader(open(infilePath)))


def calculateFitness(attribute, relationship, weight, prsn1, prsn2):
    """
    Calculate fitness between individuals for a single attribute.
    """
    if relationship == 'similar' and prsn1[attribute] == prsn2[attribute]:
        return int(weight)
    elif relationship == 'different' and prsn1[attribute] != prsn2[attribute]:
        return int(weight)
    else:
        return 0


def match(config, person1, person2):
    """
    Calculate total fit match between two individuals.
    """
    fit = 0
    for row in config:
        attribute = row[0]
        relationship = row[1]
        weight = row[2]

        fit += calculateFitness(attribute,
                                relationship,
                                weight,
                                person1,
                                person2)
    return fit

memo = {'groups': {}}
for person1 in people:
    for person2 in people:
        groupID = tuple(sorted([person1['name'], person2['name']]))

        # We don't compare people against themselves
        if person1 == person2:
            continue
        if groupID not in memo['groups']:
            memo['groups'][groupID] = {}

        memo['groups'][groupID]['fit'] = match(config, person1, person2)

# output
outfile = open(outfilePath, 'w')
i = 0
outfile.write('group,fit,name\n')
for row in sorted([[memo['groups'][key]['fit'], key] for key in memo['groups']],
                  key=itemgetter(0),
                  reverse=True):
    output = ''.join([str(i),
                      ',',
                      str(row[0]),
                      ',',
                      row[1][0],
                      '\n',
                      str(i),
                      ',',
                      str(row[0]),
                      ',',
                      row[1][1],
                      '\n'])
    outfile.write(str(output))
    i += 1

outfile.close()
