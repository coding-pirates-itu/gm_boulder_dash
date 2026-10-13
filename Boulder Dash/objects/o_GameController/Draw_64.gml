// Diamond counter in the top left corner of the screen
draw_sprite_ext(s_Diamond, 0, 16, 16, 2, 2, 0, c_white, 1);

draw_set_font(fnt_Hud);
draw_set_halign(fa_left);
draw_set_valign(fa_middle);
draw_set_colour(c_white);
draw_text(96, 48, string(diamonds) + " / " + string(diamonds_needed));
