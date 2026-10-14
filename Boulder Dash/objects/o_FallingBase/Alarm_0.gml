alarm[0] = FallDelay;

// The cell below is empty: fall down one cell
if (place_empty(x, y + TILE))
{
    y += TILE;
    falling = true;
    exit;
}

// We were falling and have just landed on something
if (falling)
{
    falling = false;
    audio_play_sound(snd_Boulder, 1, false);

    // Landed on the player or a firefly?
    var victim = instance_place(x, y + TILE, [o_Player, o_Firefly]);
    if (victim != noone)
    {
        victim.Die();
        exit;
    }
}

// Lying on a boulder, a diamond or a wall: roll off to the side (left preferred)
if (place_meeting(x, y + TILE, o_FallingBase))
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
