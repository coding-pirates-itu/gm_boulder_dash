// How many diamonds the player has collected.
// diamonds_needed is set for each room in the room editor
// (double-click the instance -> Variables).
diamonds = 0;

function AddDiamond()
{
    diamonds += 1;
    audio_play_sound(snd_Diamond, 1, false);

    if (diamonds == diamonds_needed)
    {
        // Enough diamonds: open the exit
        o_Exit.is_open = true;
        o_Exit.sprite_index = s_ExitOpen;
        audio_play_sound(snd_ExitOpen, 1, false);
    }
}
