#include "roller.h"

#include <iostream>
#include <time.h>

Random::Random(){
    current = 0;
    srand(time(0));
    Fori(rand()%50){
        rand();
    };
    srand(rand());
    current = rand();
}

int Random::gen(int range){
    //srand(rand());
    return (int)rand()%range;
}

int Random::flip(){

    int result;
    result = gen(2) +1;
    return result;
}

int Random::d4(){
    int result;
    result = gen(4) +1;
    return result;
}

int Random::d6(){
    int result;
    result = gen(6) +1;
    return result;
}

int Random::d8(){
    int result;
    result = gen(8) +1;
    return result;
}

int Random::d10(){
    int result;
    result = gen(10) +1;
    return result;
}

int Random::d12(){
    int result;
    result = gen(12) +1;
    return result;
}

int Random::d20(){
    int result;
    result = gen(20) +1;
    return result;
}

int Random::d100(){
    int result;
    result = gen(100) +1;
    return result;
}

int Random::p3d6(){
    int result;
    result = gen(6)+gen(6)+gen(6) +3;
    return result;
}


