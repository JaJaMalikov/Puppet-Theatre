#ifndef DEF_H
#define DEF_H

#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>

#define toStr(a) std::to_string(a)
#define Print(a) std::cout << a << std::endl
#define Fori(a) for(int i = 0; i<a;i++)

struct state{
    sf::Vector2f position;
    float rotation;
    int scale;
    int mood;
    float flip;
};

#endif // DEF_H

