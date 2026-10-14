alarm[0] = MoveDelay;

// The cell in front of the firefly
var new_x = x + round(lengthdir_x(TILE, move_dir));
var new_y = y + round(lengthdir_y(TILE, move_dir));

// Is the player in front of us?
var player = instance_place(new_x, new_y, o_Player);
if (player != noone)
{
    player.Die();
    exit;
}

if (place_empty(new_x, new_y))
{
    // Fly forward
    x = new_x;
    y = new_y;
}
else
{
    // Something is in the way: turn right
    move_dir -= 90;
}
