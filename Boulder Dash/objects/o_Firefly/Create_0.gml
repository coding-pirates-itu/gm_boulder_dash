move_dir = 180;    // 0 = right, 90 = up, 180 = left, 270 = down
alarm[0] = MoveDelay;


function Die()
{
    instance_create_layer(x, y, "Instances", o_Explosion);
    audio_play_sound(snd_Explosion, 1, false);
    instance_destroy();
}
