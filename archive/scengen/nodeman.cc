CC = g++
CC_FLAGS = -g -Wall

LIBS = -lm
INCLUDES = 

MODELS =  waypoint.o fixedwp.o brownian.o pursue.o column.o gaussmarkov.o

OBJS = $(MODELS) \
       scengen.o util.o random.o \
       spec.o modelspec.o scenspec.o \
       model.o nodegroup.o nodeman.o

TEST_OBJS = test.o util.o random.o \
       spec.o modelspec.o scenspec.o \
       model.o nodegroup.o nodeman.o \
       $(MODELS)

RELEASE = Makefile *.cc *.h README scengen

AD_HOCKEY = /usr/local/ad-hockey/ad-hockey-li

all : scengen

release :
	cp -f $(RELEASE) release

run : scengen
	./scengen

s : scengen scen-spec model-spec
	./scengen 1>s

cs : 
	rm -f s

a : 
	$(AD_HOCKEY) s

clean : 
	rm -f $(OBJS) core

realclean : 
	rm -f $(OBJS) core scengen s

wc :
	wc -l *

scengen : $(OBJS)
	$(CC) $(CC_FLAGS) $(LIBS) -o scengen $(OBJS)

test : $(TEST_OBJS)
	$(CC) $(CC_FLAGS) $(LIBS) -o test $(OBJS)

test.o : test.cc
	$(CC) $(CC_FLAGS) -c test.cc

scengen.o : scengen.cc scengen.h
	$(CC) $(CC_FLAGS) -c scengen.cc

nodeman.o : nodeman.cc nodeman.h
	$(CC) $(CC_FLAGS) -c nodeman.cc

util.o : util.cc util.h
	$(CC) $(CC_FLAGS) -c util.cc

random.o : random.cc random.h
	$(CC) $(CC_FLAGS) -c random.cc

model.o : 