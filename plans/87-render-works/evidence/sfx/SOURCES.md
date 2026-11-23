# R6 SFX sources and licences

Every file in `final/` is listed. Processing on all of them: trim, fade, level, 48 kHz 24-bit WAV; recorded files also a 1-pole high-pass (120 Hz bells, 80 Hz horn). No pitch-shift, synthesis or layering. Exact trims and levels: `final/process_log.json`.

## Recorded (CC0)

Licence read from each sound's own Freesound page (link to creativecommons.org/publicdomain/zero/1.0) on 22 Nov 2026; the search was also filtered to CC0. Downloaded as the public HQ preview MP3, no login.

| Asset key | Page | Author | Licence | Title | Part used | Uploader's description |
|---|---|---|---|---|---|---|
| R6-SFX-DING-D | https://freesound.org/people/wjauch/sounds/610096/ | wjauch | CC0 1.0 | Door_chime.wav | 0.068–1.068 s of the take (the high bar) | Door chime from about 1995. Recorded indoors about 18" away from the unit mounted high on kitchen wall. Recorded with Zoom H4n. |
| R6-SFX-DONG-D | https://freesound.org/people/wjauch/sounds/610096/ | wjauch | CC0 1.0 | Door_chime.wav | 1.578–2.778 s of the take (the low bar) | Door chime from about 1995. Recorded indoors about 18" away from the unit mounted high on kitchen wall. Recorded with Zoom H4n. |
| R6-SFX-WAH-D | https://freesound.org/people/TaranP/sounds/362206/ | TaranP | CC0 1.0 | horn_fail_wahwah_1.wav | 0–2.6 s | A "wah wah" sound produced using the right hand in the bell of a horn. Makes a great comedic effect for "fail" or "you lose" situations. Notes: E4, Eb4, D4. Recorded with |

## Model-generated

| Asset key | Model | Raw file | duration, prompt_influence | Prompt |
|---|---|---|---|---|
| R6-SFX-DING | ElevenLabs Sound Effects v3 via WaveSpeed (`elevenlabs/sound-effects-v3`) | raw/r1_ding_desk_2.mp3 | 1.5 s, 0.5 | A single bright desk bell ding. One clean strike of a small brass reception bell, crisp attack, short shimmering ring, dry close recording, no reverb. |
| R6-SFX-DONG | ElevenLabs Sound Effects v3 via WaveSpeed (`elevenlabs/sound-effects-v3`) | raw/r3_dong_desk_1.mp3 | 1.6 s, 0.6 | A single strike of a large, lower-pitched desk service bell. One clean dong with a clear mellow pitch, rings for about one second, dry close recording, no reverb, no background. |
| R6-SFX-DING-B | ElevenLabs Sound Effects v3 via WaveSpeed (`elevenlabs/sound-effects-v3`) | raw/r3_ding_glock_1.mp3 | 1.3 s, 0.6 | Glockenspiel: one single bright high note struck once, clean and pure, rings for under one second, dry studio recording, nothing else. |
| R6-SFX-DONG-B | ElevenLabs Sound Effects v3 via WaveSpeed (`elevenlabs/sound-effects-v3`) | raw/r3_dong_glock_2.mp3 | 1.6 s, 0.6 | Glockenspiel: one single low note struck once with a soft mallet, mellow, damped after one second, dry studio recording, nothing else. |
| R6-SFX-DING-C | ElevenLabs Sound Effects v3 via WaveSpeed (`elevenlabs/sound-effects-v3`) | raw/r1_ding_show_1.mp3 | 1.5 s, 0.5 | Game show correct-answer ding: one single clear bright bell note, warm and charming, clean, quick natural decay, no reverb. |
| R6-SFX-DONG-C | ElevenLabs Sound Effects v3 via WaveSpeed (`elevenlabs/sound-effects-v3`) | raw/r3_dong_brass_3.mp3 | 1.6 s, 0.6 | One single lower bell note, the dong of a ding-dong: a struck brass bell, warm and round, clear low-mid pitch, short decay under one second, dry, no reverb. |
| R6-SFX-WAH | ElevenLabs Sound Effects v3 via WaveSpeed (`elevenlabs/sound-effects-v3`) | raw/r1_wah_D_2.mp3 | 3.5 s, 0.5 | Classic sad trombone fail sound effect, four descending notes, wah wah wah waaah, muted brass, mellow and subtle, dry. |
| R6-SFX-WAH-B | ElevenLabs Sound Effects v3 via WaveSpeed (`elevenlabs/sound-effects-v3`) | raw/r1_wah_B_1.mp3 | 3.5 s, 0.5 | Solo trumpet with harmon wah mute plays a quiet comedic fail phrase: four slow descending wah notes, gentle and wry, real brass with breath, dry small room, nothing else. |
| R6-SFX-WAH-C | ElevenLabs Sound Effects v3 via WaveSpeed (`elevenlabs/sound-effects-v3`) | raw/r1_wah_A_1.mp3 | 3.5 s, 0.5 | Sad trombone: wah wah wah wah. Four slow descending notes on a real muted trombone with a plunger mute, played softly and understated, dry close recording, no reverb, no audience, no music. |

## Project media ids (imported 22 Nov 2026)

| Asset key | Project media id |
|---|---|
| R6-SFX-DING | `sha256:37bc2840b563ba9fa80beca5b178c710882daf80887c8c847b484ecf071ea83d` |
| R6-SFX-DING-B | `sha256:32d4c01f4f4b5bada169a5e8a14394b0362a190bf986f7a896c6f8522d6f981c` |
| R6-SFX-DING-C | `sha256:fbb152010c20b5a6622f405985b34c1cc73a6c86d1d6869fd4779981c23c6f96` |
| R6-SFX-DING-D | `sha256:522d5441acbfec22eae6afdecf9164f01ec8592aad91a1f952c9bbd717173c45` |
| R6-SFX-DONG | `sha256:e1b9237e8896308deac1c6836fc082b5f332a56529f7d97aa58e951b7d09a72a` |
| R6-SFX-DONG-B | `sha256:724a945112c03a9afa0208c26ee91123e1d0564fef52b236ce494d8680a0a6e5` |
| R6-SFX-DONG-C | `sha256:6e3c443e04e2869ade44ccc3720881f7ba131015bacf60568afaf165b233d6bf` |
| R6-SFX-DONG-D | `sha256:2173f088dd797cd7e7eb7889788ea5cc89fe9aec4db2a1df723fc53016b340fa` |
| R6-SFX-WAH | `sha256:d02a24ef016bca88ebd8c4a3b46beab52ab5883334a633fe9777ce93be9a3aa3` |
| R6-SFX-WAH-B | `sha256:387fbd4ea1b5b8ff635d66e45c175349e428dfbaf11e5ad1621480e912b922db` |
| R6-SFX-WAH-C | `sha256:c851e9f7784a4f903ecff812f7b9859c417d9be952e477f9a3dc0db6f2009a81` |
| R6-SFX-WAH-D | `sha256:7de88a313941d2ce60db21f38f7b9a9022909a27c2b0808b3d5e3f99ee364b42` |

## Fetched but not used

CC0 Freesound previews kept in `src/` (licence checked the same way; details in `src/meta.json`): 175409 (kirbydx), 181354 (unfa), 335906 (LittleRainySeasons), 543966 (sweet_niche), 449070 (ricniclas), 539593 (GeraRamirez), 161314 (husky70), 134000 (davidkyoku), 361564 (MatthewWong), 555016 (oganesson), 640766 (fabiopx), 709948 (Squidems), 827464 (jonahlpayne), 442280 (jwheeler91), 479991 (craigsmith), 879804 (Qvantor), 571513 (LegitCheese), 187314 (carroll27), 685111 (tonmayster), 879808 (Qvantor), 573381 (ammaro), 434627 (Dr.%20Macak), 532751 (iwanPlays), 96521 (kleinhirn2000), 116779 (domrodrig), 611113 (5ro4), 333694 (Khrinx), 830476 (evgeny134), 648960 (IENBA), 394625 (Diego25), 879801 (Qvantor).
Excluded on reading the descriptions: 879804/879808/879801 (browser synth), 335906 (piano-roll editor), 181354 (voice), 161314/134000 (guitar), 648960 (pitched up), 442280/532751 (edits of other users' sounds).
