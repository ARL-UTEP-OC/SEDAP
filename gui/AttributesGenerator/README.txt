netStateBuilderFromRoutes.py
-this file will take input (typically from an emulation/simulation) in xml format.

Steps:

1. Create and execute a CORE scenario
2. Grab routes from each node in the scenario (after routes converge)
3. Modify sampleInput.xml
4. execute the following:
	python netStateBuilderFromRoutes.py > <output filename>.xml
	
The resulting file should be used as the Attributes input file in the GUI

