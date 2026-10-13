alarm[0] = fall_delay;

// 1. The cell below is empty: fall down one cell
if (place_empty(x, y + TILE))
{
    y += TILE;
    falling = true;
    exit;
}

// 2. We were falling and have just landed on something
if (falling)
{
    falling = false;
    audio_play_sound(snd_Boulder, 1, false);

    // Landed on the player or a firefly? Boom!
    var victim = instance_place(x, y + TILE, [o_Player, o_Firefly]);
    if (victim != noone)
    {
        victim.Die();
        exit;
    }
}

// 3. Lying on a boulder, a diamond or a wall: roll off to the side
if (place_meeting(x, y + TILE, o_FallingBase) || place_meeting(x, y + TILE, o_Wall))
{
    if (place_empty(x - TILE, y) && place_empty(x - TILE, y + TILE))
    {
        x -= TILE;
    }
    else if (place_empty(x + TILE, y) && place_empty(x + TILE, y + TILE))
    {
        x += TILE;
    }
}
