// Wait a little between two moves
move_timer -= 1;
if (move_timer > 0)
{
    exit;
}

// Which way does the player want to go?
var dx = 0;
var dy = 0;

if (keyboard_check(vk_left) || keyboard_check(ord("A")))
{
    dx = -1;
    sprite_index = s_PlayerLeft;
}
else if (keyboard_check(vk_right) || keyboard_check(ord("D")))
{
    dx = 1;
    sprite_index = s_PlayerRight;
}
else if (keyboard_check(vk_up) || keyboard_check(ord("W")))
{
    dy = -1;
}
else if (keyboard_check(vk_down) || keyboard_check(ord("S")))
{
    dy = 1;
}
else
{
    // No key is pressed: stand still
    sprite_index = s_PlayerIdle;
    exit;
}

move_timer = move_delay;

// The cell we want to move to
var new_x = x + dx * TILE;
var new_y = y + dy * TILE;

// Walls stop the player
if (place_meeting(new_x, new_y, o_Wall))
{
    exit;
}

// The exit: go to the next level, but only when it is open
if (place_meeting(new_x, new_y, o_Exit))
{
    if (o_Exit.is_open)
    {
        audio_play_sound(snd_Win, 1, false);
        room_goto_next();
    }
    exit;
}

// Walking into a firefly is a bad idea
if (place_meeting(new_x, new_y, o_Firefly))
{
    Die();
    exit;
}

// Push a boulder - only left or right, and only into an empty cell
var boulder = instance_place(new_x, new_y, o_Boulder);
if (boulder != noone)
{
    if (dy != 0 || !place_empty(new_x + dx * TILE, new_y))
    {
        exit;
    }
    boulder.x += dx * TILE;
}

// Dig away the dirt
var dirt = instance_place(new_x, new_y, o_Dirt);
if (dirt != noone)
{
    instance_destroy(dirt);
    audio_play_sound(snd_Dig, 1, false);
}

// Collect a diamond
var diamond = instance_place(new_x, new_y, o_Diamond);
if (diamond != noone)
{
    instance_destroy(diamond);
    o_GameController.AddDiamond();
}

// Move!
x = new_x;
y = new_y;
