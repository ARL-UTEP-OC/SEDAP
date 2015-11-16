1. Compiling the Scenario Generator

Simply do a "make" to compile. Makefile can be modified if needed.

2. Running the Scenario Generator

Run "./scengen" to generate scenarios. 

The program takes two inputs. One is "model-spec", which contains the
default parameters, and normally does not need to be changed. If changes
are needed, it has to be done with caution. The other input, scenario
specification is the file "scen-spec", which describes the scenario
needed.

3. Viewing the scenario

The "ad-hockey" program, initially developed for the wireless extention to 
NS-2 by CMU, can be used to view the mobility scenario without running any 
simulations. The original ad-hockey is available at:
    http://www.monarch.cs.cmu.edu/cmu-ns.html

However, the ad-hockey needs some slight modifications before it can not 
display the scenario 