import os
from fontTools.designspaceLib import DesignSpaceDocument

subFamilyName = ['Roman', 'Italic'][0]
folder = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(folder, 'Sources', subFamilyName)
designspacePath = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}_avar2.designspace')

_sources   = True
_instances = True

assert os.path.exists(designspacePath)

doc = DesignSpaceDocument()
doc.read(designspacePath)

# validate sources
if _sources:
    locations = []
    for src in doc.sources:
        if src not in locations:
            locations.append(src.location)
        else:
            print(src.name, src.location)

# validate instances
if _instances:
    expandAxes = {}
    print(f'validating AmstelvarA2 {subFamilyName} instance locations...\n')
    axes = { axis.tag: axis for axis in doc.axes }
    for instance in doc.instances:
        # print(instance.name)
        for axisName, value in instance.designLocation.items():
            axis = axes[axisName]
            if not axis.minimum <= value <= axis.maximum:
                if axisName not in expandAxes:
                    expandAxes[axisName] = []
                expandAxes[axisName].append(value)
                # print(f"\t!! {axisName} {value} ({axis.minimum} {axis.maximum}) {'-' if value < axis.minimum else '+' if value > axis.maximum else ''} ")
        # print()

    for axisName, values in expandAxes.items():
        print(f'{axisName}:')
        if min(values) < axes[axisName].minimum:
            print(f'\t- {min(values)} ({axes[axisName].minimum})')
        if max(values) > axes[axisName].maximum:        
            print(f'\t+ {max(values)} ({axes[axisName].maximum})')
        print()

    print('...done!\n')
