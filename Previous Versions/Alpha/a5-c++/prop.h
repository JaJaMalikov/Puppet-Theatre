#ifndef PROP_H
#define PROP_H

#include <GL/glew.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include "def.h"
#include "roller.h"


class prop
{
private:
    std::vector<sf::Texture> texture_map;
    std::string name;
    int sizes;
    float blowup;
    float angle;
    float flip;
    int block;
    float rot_set;
    sf::Vector2f position;
    int scale;
    int mood;
    std::vector<std::string> moods;
    int size_x;
    int size_y;
public:
    prop(std::string new_name, int new_sizes);
    void new_size();
    void load_from_images();
    void load_from_file(std::string filename);
    void set_input();
    void set_rotation(float angle);
    void set_position(int x_axis);
    void set_scale(int new_scale);
    void set_flip();
    void set_mood(int new_mood);
    //position, rotation, scale, mood, flip
    state get_state();
    sf::Sprite get_sprite();

};

#endif // PROP_H

