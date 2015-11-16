//
// scengen.cc
//

#include "defs.h"

#include "util.h"
#include "spec.h"
#include "modelspec.h"
#include "scenspec.h"
#include "model.h"
#include "random.h"
#include "nodeman.h"
#include "scengen.h"

// the main function
int main()
{
    ScenGen *sg = ScenGen::instance();

    Move *move = new Move();
    model_time_t time = 0;

    sg->printComments();
    while ( (time = sg->nextMove(move)) >= 0) {
        sg->formatMove(move);
    }// while

    return 0;
}

// Implementation of class ScenGen (singleton)

// static member variable
ScenGen *ScenGen::instance_ = NULL;

// constructor and destructor
ScenGen::ScenGen()
{
    // Note: the order of initialization is important here

    // load the model specifications
    modelSpec_ = ModelSpec::instance();
    assert(modelSpec