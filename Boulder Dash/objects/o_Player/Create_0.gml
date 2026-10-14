// Separate two consequent moves
move_timer = 0;


function Die()
{
    o_GameController.PlayerDied(x, y);
    instance_destroy();
}
