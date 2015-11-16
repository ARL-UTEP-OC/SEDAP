//
// waypoint.cc
//
// Random Waypoint Model

#include "defs.h"

#include "modelspec.h"
#include "waypoint.h"


// Constructor
Waypoint::Waypoint() : Model()
{
    type_ = MODEL_WAYPOINT;

    T_max_ = 0;
    T_min_ = 0;
    T_dist_ = DIST_CONST;

    V_max_ = 10;
    V_min_ = 10;
    V_dist_ = DIST_CONST;

    randomPos_ = true;
}

// Destructor
Waypoint::~Waypoint()
{
}

// Member functions

// initialize the model. prepare for the movement generation
void Waypoint::init(model_time_t startTime, \
                    model_time_t stopTime, \
                    node_id_t startID, \
                    int num_nodes, \
                    Area *area, \
                    bool cp)
{
    Model::init(startTime, stopTime, startID, num_nodes, area, cp);

    assert(paramList_ != NULL);

    // init parameters
    T_max_ = getf("T_max");
    T_min_ = getf("T_min");
    getDistType(get("T_dist"), T_dist_);

    V_max_ = getf("V_max");
    V_min_ = getf("V_min");
    getDistType(get("V_dist"), V_dist_);

    initialized_ = true;
}

// assumed that posistions are randomly chosen
//
// for the Waypoint model, a node behaves like this: 
// step 1: pause for a certain ti