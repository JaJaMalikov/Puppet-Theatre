
#include "prop.h"

prop::prop(std::string new_name, int new_sizes){
    name = new_name;
    sizes = new_sizes;
    blowup = 1.0f;
    angle = 180.0f;
    flip = -1.0f;
    scale = 0;
    block = 1920/7;
    rot_set = 45.0f;
    position.x = 1200;
    position.y = 720;
    mood = 0;
    size_x = 500*blowup;
    size_y = 822*blowup;
}

void prop::new_size(){
    moods.push_back(toStr(moods.size()));
}

void prop::load_from_images(){
    for (int i = 0; i < sizes; i++){
        new_size();
        sf::Texture temp_texture;
        temp_texture.setSmooth(true);
        temp_texture.loadFromFile(name + "/0/" + moods[i] + ".png");
        texture_map.push_back(temp_texture);
    }
}






void prop::set_input(){
    //set position
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Right )){
        mood += 1;
        if (mood == sizes){
            mood = sizes -1;
        }
    };
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Left )){
        mood -= 1;
        if (mood < 0){
            mood = 0;
        }
    };



}

void prop::set_rotation(float new_angle){
    angle = new_angle;
}

void prop::set_position(int x_axis){
    position.x = x_axis;
}

void prop::set_scale(int new_scale){
    scale = new_scale;
}

void prop::set_flip(){
    flip *= -1.0f;
}

void prop::set_mood(int new_mood){
    mood = new_mood;
}

state prop::get_state(){
    state temp_state;
    temp_state.position = position;
    temp_state.rotation = angle;
    temp_state.mood = mood;
    temp_state.scale = scale;
    temp_state.flip = flip;
    return temp_state;

}



sf::Sprite prop::get_sprite(){

    sf::Sprite temp_sprite(texture_map[mood]);
    size_x = temp_sprite.getTexture() ->getSize().x;
    size_y = temp_sprite.getTexture() ->getSize().y;
    temp_sprite.setOrigin(size_x/2,size_y/2);
    temp_sprite.setRotation(angle);
    temp_sprite.setPosition(position);
    temp_sprite.setScale(flip, 1);
    return temp_sprite;
}










