// Big dancing player
draw_self();

draw_set_halign(fa_center);
draw_set_valign(fa_middle);

draw_set_font(fnt_Win);
draw_set_colour(c_yellow);
draw_text(room_width / 2, y + sprite_height + 80, "You win!");

draw_set_font(fnt_Hud);
draw_set_colour(c_white);
draw_text(room_width / 2, y + sprite_height + 180, "Press Enter to play again");
