# Boulder Dash — plan and progress

A simple Boulder Dash clone in GameMaker, made for teaching children.
It must stay on the same level as the other example games
(`gm_farm_builder`, `gm_tower_defense`, `gm_xenon`, `gm-eldervale`):
few objects, short events, plain GML, no clever tricks.

## Reference projects — what we copy

| Topic | Taken from | Decision |
|-------|------------|----------|
| Project format | Farm Builder (IDE 2026.0) | Same `.yyp` / `.yy` format, same options, `.gitignore`, `.gitattributes`. Project lives in `Boulder Dash/` sub-folder. |
| Naming | Farm Builder, Tower Defense | `o_Player`, `s_Player`, `snd_Dig`, `rm_Level1`, `fnt_Hud`. Variables in `snake_case`. |
| Code style | Farm Builder, Tower Defense | Plain GML code events (not DnD), braces on own lines, short comments. |
| Parent objects | Farm Builder (`o_CropBase`), Tower Defense (`o_Enemy_Base`) | `o_FallingBase` is the parent of `o_Boulder` and `o_Diamond`. |
| Controller + functions in Create | Farm Builder (`AddWheat`, `CheckWin`) | `o_GameController.AddDiamond()` opens the exit. |
| Variable Definitions | Farm Builder (`o_Field.Growing`) | `o_GameController.diamonds_needed` is set per room in the room editor. |
| Camera that follows the player | Eldervale | Viewport 0 follows `o_Player`. |
| Next level / win room | Farm Builder, Tower Defense | `room_goto_next()`, last room is `rm_Win`. |
| Fonts | Farm Builder | `fnt_Hud`, `fnt_Win` copied from Farm Builder (Bernard MT Condensed). |

## Game rules (keep them few!)

- The world is a grid of 32×32 px cells. Everything moves one whole cell at a time.
- **Player** (Rockford) moves with the arrow keys (or WASD). Moving into
  - **dirt** digs it away,
  - a **diamond** collects it,
  - a **boulder** pushes it sideways if the cell behind it is empty,
  - a **wall** is not possible,
  - the **exit** finishes the level, but only when it is open.
- **Boulders and diamonds** fall down when the cell below is empty.
  When they lie on another boulder, diamond or wall they roll off to the left or right if there is room.
- A boulder or diamond that is *falling* and lands on the player or a firefly makes it explode.
  (A boulder that is already lying on the player's head is safe — just like the original.)
- **Firefly** flies straight ahead and turns right when blocked. Touching it is deadly.
- Collect enough diamonds → the exit opens (blinks).
- When the player dies the level restarts after 2 seconds. `R` restarts the level any time.
- Two levels, then a "You win!" room.

## Resources

### Sprites (32×32, origin top-left, own pixel art drawn with a Python script)

| Sprite | Frames | Notes |
|--------|--------|-------|
| `s_Wall` | 1 | brick wall |
| `s_Dirt` | 1 | brown soil |
| `s_Boulder` | 1 | round grey rock |
| `s_Diamond` | 8 | sparkling, animated |
| `s_PlayerIdle` | 4 | blinking / tapping foot |
| `s_PlayerLeft` | 4 | walking left |
| `s_PlayerRight` | 4 | walking right |
| `s_Firefly` | 4 | spinning square, animated |
| `s_ExitClosed` | 1 | looks like a steel door |
| `s_ExitOpen` | 2 | blinking door |
| `s_Explosion` | 6 | animated, the object destroys itself at the end |

The HUD re-uses `s_Diamond` frame 0 as the diamond icon.

### Sounds (made with the free sfxr generator, https://sfxr.me — public domain)

| Sound | When |
|-------|------|
| `snd_Dig` | player digs dirt |
| `snd_Diamond` | diamond collected |
| `snd_Boulder` | boulder lands |
| `snd_Explosion` | player / firefly explodes |
| `snd_ExitOpen` | enough diamonds, exit opens |
| `snd_Win` | player enters the exit |

### Objects

| Object | Parent | Events | Purpose |
|--------|--------|--------|---------|
| `o_GameController` | — | Create, Key press R, Alarm 0, Draw GUI | diamond counter, HUD, restart after death |
| `o_Player` | — | Create, Step | moving, digging, collecting, pushing, dying |
| `o_Wall` | — | — | blocks everything |
| `o_Dirt` | — | — | gets dug away |
| `o_FallingBase` | — | Create, Alarm 0 | falling and rolling logic |
| `o_Boulder` | `o_FallingBase` | — | can be pushed |
| `o_Diamond` | `o_FallingBase` | — | can be collected |
| `o_Firefly` | — | Create, Alarm 0 | enemy |
| `o_Exit` | — | Create | closed / open door |
| `o_Explosion` | — | Animation End | short animation |
| `o_WinText` | — | Draw, Key press Enter | win screen |

### Scripts

| Script | Content |
|--------|---------|
| `Grid` | `#macro TILE 32` — the size of one cell, used everywhere |

### Rooms

| Room | Size | Notes |
|------|------|-------|
| `rm_Level1` | 40×22 cells (1280×704) | easy, 20 diamonds, 12 needed, 1 firefly |
| `rm_Level2` | 40×22 cells (1280×704) | many boulders, 21 diamonds, 15 needed, 3 fireflies |
| `rm_Win` | 1280×704 | "You win!" |

Camera: 640×352 (20×11 cells) shown in a 1280×704 window, following `o_Player`.

Layers in level rooms: `Instances` (everything), `Background` (dark colour).

## Lessons (1.5 hours each)

1. Project, sprites `s_Wall` + `s_Dirt`, objects, room with 32×32 grid, draw a level. `o_Player` moves one cell with the arrow keys and digs dirt.
2. Boulders: `o_FallingBase` with Alarm 0 — fall down; then roll off; player pushes boulders.
3. Diamonds as a child of `o_FallingBase`, `o_GameController` with `AddDiamond()`, HUD (Draw GUI), the exit and the next room.
4. Dying: falling objects crush the player, `o_Explosion`, restart. Sounds.
5. Firefly enemy, camera, second level, win room.

## Progress

- [x] Study the example projects (format, naming, code style)
- [x] Plan (this file)
- [x] Graphics — own pixel art, `tools/make_art.py`
- [x] Sounds — sfxr (jsfxr), `tools/make_sfx.js`
- [x] Project skeleton (`.yyp`, options and fonts copied from Farm Builder)
- [x] Objects and code
- [x] Rooms (levels were written as text maps and converted by a script; edit them in the room editor from now on)
- [x] README with lessons, level pictures in `docs/`
- [x] Commit and push
- [ ] Open the project in GameMaker and play-test both levels (could not be done here — no GameMaker in the build environment)

## Notes

- The online asset sites (opengameart.org, kenney.nl, freesound.org) and the GameMaker manual
  were blocked by the network policy of the build environment, so graphics are own pixel art
  and sounds were generated with sfxr — both are free to use.
- Fireflies: the original turns *left* along walls; ours simply turns *right* when blocked. Simpler to explain.
- Possible extra lessons: a time limit, lives, butterflies that turn into diamonds, amoeba, magic wall.
