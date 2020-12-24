#ifndef ROLLER_H
#define ROLLER_H

#include "def.h"

class Random
    {
    private:
        int current;
    public:
        Random();
        int gen(int range);
        int flip();
        int d4();
        int d6();
        int d8();
        int d10();
        int d12();
        int d20();
        int p3d6();
        int d100();
    };


#endif // ROLLER_H

