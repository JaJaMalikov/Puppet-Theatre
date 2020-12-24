#include <iostream>
#include <vector>
#include <windows.h>

#include <GL/glew.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>

#include <sstream>
#include <string>

#include "def.h"
#include "roller.h"
#include "character.h"
#include "prop.h"

constexpr float width     = 1920;
constexpr float height    = 1080;

int frame = 0;

std::vector<state> frame_states;

int main(){

    sf::ContextSettings settings;
    settings.antialiasingLevel = 8;
    sf::RenderWindow window(sf::VideoMode(width,height), "LW Finger Puppet Theatre", sf::Style::Default, settings);
    //window.setVerticalSyncEnabled(true);
    sf::WindowHandle handle = window.getSystemHandle();

    sf::RenderTexture camera;
    sf::ContextSettings CS;
    CS.antialiasingLevel = 2;
    camera.create(width*2, height*2);
    camera.setSmooth(true);

    std::vector<std::vector<int>> test_array = {{100,100},{200,100},{200,200},{100,200},{150,150}};

    sf::VertexArray concave(sf::TrianglesStrip, test_array.size());

    Fori(test_array.size()){
        concave[i].position = sf::Vector2f(test_array[i][0],test_array[i][1]);
        concave[i].color = sf::Color::Red;
    }

    character * atlas = new character("atlas",5);
    atlas -> load_from_images();
    atlas->set_flip();

    prop * chalkboard = new prop("board",26);
    chalkboard->load_from_images();


    sf::Clock clocks;
    float lastTime = 0;
    float total_times = 0;
    int checks = 0;

    sf::Font font;
    font.loadFromFile("arial.ttf");
    sf::Text text;
    text.setFont(font);
    text.setColor(sf::Color::Black);

    while (window.isOpen())
    {
        float current_time = clocks.restart().asSeconds();
        checks++;
        total_times += 1.0f/current_time;
        if(checks == 100){
            text.setString(toStr(total_times/100));
            checks = 0;
            total_times = 0;
        }

        sf::Event event;
        while (window.pollEvent(event))
        {
            switch(event.type){
            case sf::Event::Closed:
                window.close();
                break;
            case sf::Event::KeyPressed:
                atlas->set_input();
                chalkboard->set_input();
                break;
            default:
                break;
            }
        }

        camera.clear(sf::Color(255,255,255,255));

        camera.draw(chalkboard->get_sprite());
        camera.draw(atlas->get_sprite());
        camera.draw(atlas->get_sprite());
        frame_states.push_back(atlas->get_state());
        const sf::Texture cam_texture = camera.getTexture();
        //cam_texture.copyToImage().saveToFile("frames/derp.png");
        //cam_texture.copyToImage().saveToFile("frames/" + std::string(5 - std::to_string(frame).length(), '0') + std::to_string(frame) + ".png");
        frame++;
        sf::Sprite sprite(cam_texture);
        window.draw(sprite);
        window.draw(text);
        window.display();

    }

}

