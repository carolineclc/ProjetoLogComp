{

float => diameter;
float => radius;
float => circumferance;
int => km = 1;
float => rpm;


diameter = 4.0;
radius = diameter * 2.0;
circumferance = pi() * diameter;

float => init_speed = 0.0;
float => target_speed = 50.0;
float => time = 0.0;
float => aceletation = 3.5;
float => time_to_reach_target_speed = (target_speed - init_speed) / aceletation;


START (id : "abc_123", station : "Santa Rosa", region : "Norte");
while (time < time_to_reach_target_speed ) {

    init_speed = init_speed + aceletation;
    time = time + 1.0;
    rpm = init_speed * 60.0 / circumferance;
    STOP (name : "GOING TO Pinheiros", speed: init_speed, rotation: rpm);
    }
}