move_delay = 8;   // steps between two moves (smaller = faster)
move_timer = 0;

function Die()
{
    instance_create_layer(x, y, "Instances", o_Explosion);
    audio_play_sound(snd_Explosion, 1, false);

    // Restart the room in 2 seconds
    o_GameController.alarm[0] = 2 * game_get_speed(gamespeed_fps);
    instance_destroy();
}
