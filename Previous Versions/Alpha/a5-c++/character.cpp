#include "character.h"

character::character(std::string new_name, int new_sizes){
    name = new_name;
    sizes = new_sizes;
    blowup = 1.0f;
    angle = 180.0f;
    flip = 1.0f;
    scale = 0;
    block = 1920/7;
    rot_set = 45.0f;
    position.x = block;
    position.y = 400;
    mood = 0;
    size_x = 500*blowup;
    size_y = 822*blowup;
    moods.push_back("default");
    moods.push_back("happy");
    moods.push_back("angry");
    moods.push_back("bored");
    moods.push_back("confused");
}

void character::new_size(){
    std::map<std::string,sf::Texture> temp_map;
    texture_map.push_back(temp_map);
}

void character::load_from_images(){
    for (int i = 0; i < sizes; i++){
        new_size();
        for(int e = 0; e < moods.size(); e++){
            sf::Texture temp_texture;
            temp_texture.setSmooth(true);
            temp_texture.loadFromFile(name + "/" + std::to_string(i) + "/" + moods[e] + ".png");
            texture_map[i][moods[e]] = temp_texture;
        }
    }
}

void character::load_from_file(std::string filename){

    std::vector<std::vector<int>> temp_points;
    sf::VertexArray final_points;
    final_points.setPrimitiveType(sf::LinesStrip);
    sf::VertexArray outline;
    outline.setPrimitiveType(sf::TrianglesStrip);
    std::vector<int> color;
    bool set_color = true;
    bool set_points = false;
    sf::RenderTexture temp_texture;

    temp_texture.create(size_x, size_y);
    temp_texture.setSmooth(true);

    std::string line;
    std::ifstream current_model (filename + ".mod");
    if(current_model.is_open()){
        while(getline(current_model,line)){
            if(line[0] == '#' && !temp_points.empty()){
                if(line == "#TrianglesStrip"){
                    final_points.setPrimitiveType(sf::TrianglesStrip);
                }else if(line == "#TrianglesFan"){
                    final_points.setPrimitiveType(sf::TrianglesFan);
                }else if(line == "#LinesStrip"){
                    final_points.setPrimitiveType(sf::LinesStrip);
                }else if(line == "#Triangles"){
                    final_points.setPrimitiveType(sf::Triangles);
                }
                set_points = false;
                final_points.clear();
                final_points.resize(temp_points.size());
                outline.clear();
                outline.resize(temp_points.size());

                Fori(temp_points.size()){
                    final_points[i].position = sf::Vector2f(temp_points[i][0],temp_points[i][1]);
                    final_points[i].color = sf::Color(color[0],color[1],color[2]);
                    outline[i].position = sf::Vector2f(temp_points[i][0],temp_points[i][1]);
                    outline[i].color = sf::Color(color[0],color[1],color[2]);
                }
                temp_texture.draw(final_points);
                temp_texture.draw(outline);
                temp_points.clear();
                set_color = true;
            }else if(set_color && !set_points){
                color.clear();
                color = color_nums(line);
                set_color = false;
                set_points = true;
            }else if(!set_color && set_points){
                temp_points.push_back(num_from_string(line));
            }
        }
    }



    const sf::Texture& texture = temp_texture.getTexture();
    texture_map[0]["default"] = texture;

}

//creates vector of ints from comma separated string, only ints and commas work
std::vector<int> character::num_from_string(std::string line){
    std::vector<int> nums;
    std::istringstream iss (line);
    int i;
    while(iss >> i){
        nums.push_back(i*blowup);
        if(iss.peek() == ','){
            iss.ignore();
        }
    }
    return nums;
}

std::vector<int> character::color_nums(std::string line){
    std::vector<int> nums;
    std::istringstream iss (line);
    int i;
    while(iss >> i){
        nums.push_back(i);
        if(iss.peek() == ','){
            iss.ignore();
        }
    }
    return nums;
}

void character::custom_shape(sf::VertexArray &points, sf::RenderTexture &texture){}

void character::custom_sprite(std::map<sf::Color,sf::VertexArray>, sf::RenderTexture &texture){}

void character::set_input(){
    //set position
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::A)) set_position(block*1);
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::S)) set_position(block*2);
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::D)) set_position(block*3);
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::F)) set_position(block*4);
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::G)) set_position(block*5);
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::H)) set_position(block*6);

    //set rotation
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Numpad8)) set_rotation(rot_set*4);
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Numpad7)) set_rotation(rot_set*5);
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Numpad4)) set_rotation(rot_set*6);
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Numpad1)) set_rotation(rot_set*7);
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Numpad2)) set_rotation(rot_set*0);
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Numpad3)) set_rotation(rot_set*1);
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Numpad6)) set_rotation(rot_set*2);
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Numpad9)) set_rotation(rot_set*3);

    //change size
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Z)) scale = 0;
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::X)) scale = 1;
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::C)) scale = 2;
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::V)) scale = 3;
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::B)) scale = 4;

    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Q)) mood = 0;
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::W)) mood = 1;
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::E)) mood = 2;
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::R)) mood = 3;
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::T)) mood = 4;

    if(sf::Keyboard::isKeyPressed(sf::Keyboard::LBracket)) set_flip();

}

void character::set_rotation(float new_angle){
    angle = new_angle;
}

void character::set_position(int x_axis){
    position.x = x_axis;
}

void character::set_scale(int new_scale){
    scale = new_scale;
}

void character::set_flip(){
    flip *= -1.0f;
}

void character::set_mood(int new_mood){
    mood = new_mood;
}

state character::get_state(){
    state temp_state;
    temp_state.position = position;
    temp_state.rotation = angle;
    temp_state.mood = mood;
    temp_state.scale = scale;
    temp_state.flip = flip;
    return temp_state;

}


void character::scale_texture(){



}

sf::Sprite character::get_sprite(){
    sf::Sprite temp_sprite(texture_map[scale][moods[mood]]);
    size_x = temp_sprite.getTexture() ->getSize().x;
    size_y = temp_sprite.getTexture() ->getSize().y;
    temp_sprite.setOrigin(size_x/2,size_y/2);
    temp_sprite.setRotation(angle);
    temp_sprite.setPosition(position);
    temp_sprite.setScale(flip, 1);
    return temp_sprite;
}









