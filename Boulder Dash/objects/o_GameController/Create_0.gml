// How many diamonds the player has collected.
// diamonds_needed is set for each room in the room editor
// (double-click the instance -> Variables).
diamonds = 0;


function AddDiamond()
{
    diamonds += 1;
    audio_play_sound(snd_Diamond, 1, false);

    if (diamonds == DiamondsNeeded)
    {
        // Enough diamonds: open the exit
        IsExitOpen = true;
        o_Exit.sprite_index = s_ExitOpen;
        audio_play_sound(snd_ExitOpen, 1, false);
    }
}


function PlayerOnExit()
{
    if (IsExitOpen)
    {
        audio_play_sound(snd_Win, 1, false);
        room_goto_next();
    }
}


function PlayerDied(playerX, playerY)
{
    instance_create_layer(playerX, playerY, "Instances", o_Explosion);
    audio_play_sound(snd_Explosion, 1, false);

    // Restart the room in 2 seconds
    alarm[0] = 2 * game_get_speed(gamespeed_fps);
}