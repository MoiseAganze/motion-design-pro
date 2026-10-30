# SPEC — « Le fil » (Formation Automatisation n8n)

GOAL:    the viewer understands that CHRONOCONCEPT GROUP runs a hands-on n8n automation training in Kinshasa
         (Silikin Village) and knows the two ways to act: the link in the description, or WhatsApp / site.
OUTPUT:  HyperFrames, 1920×1080 (index.html, YouTube) and 1080×1920 (vertical.html, TikTok), 30 fps.
TIME:    56 s × 30 = 1680 frames. Music 120 BPM = 15 frames a beat, 60 frames a bar; bar n starts at (n-1)×2 s.
         Voice (ElevenLabs, voice RBhYSNMNu6b2CGZ9Fn1M, take A) placed at +0.56 s so "Avec n8n" = 10.0 s.

LOOK:
  world 1 (story)   ground #F4F8FD; light = two soft radial pools, #0078C3 at 22% and #0AA4BC at 16%,
                    radius 900–1200 px, drifting ≤ 40 px over a scene (the reference film's air, brand hues).
                    ink #0B2A45; brand navy #054C7A (logo); accent blue #0078C3 (one word / the CTA);
                    cyan #0AA4BC only for connector light; n8n coral #EA4B71 only on the n8n mark.
                    cards #FFFFFF, radius 24 px, shadow 0 22px 48px rgba(11,42,69,.14) + 0 2px 6px rgba(11,42,69,.08).
  world 2 (product) n8n's editor as captured: canvas #171717, dot grid #262626 every 24 px, nodes #2B2B2B with
                    2 px #444 border, radius 12 px; icons: code #FFB966, if #00C950, webhook #FF4D80,
                    http #898FFF, execute button #FF6900; labels #E8E8E8 Open Sans 600, sub-labels #BBBBBB.
                    Success = #00C950 ring + check, as n8n shows it.
  world 3 (place)   Africa map from Natural Earth: land #DCE7F3, DRC #0078C3, Kinshasa pin #EA4B71;
                    the Silikin Village photo, untreated.
  type              display Poppins 800, 92–150 px (16:9) / 110–170 px (9:16), tracking -2%;
                    secondary Poppins 600 40–56 px; UI Open Sans 600 26–34 px. Nothing read under 28 px.
OBJECTS: clock face (white disc, navy ticks, cyan second hand, centre cap); app tiles (white 120 px rounded
         squares with the real brand glyph, red unread badge); task cards (white, icon + one line);
         n8n nodes (the real node names from the two screenshots); the cursor (white arrow, navy outline, 56 px);
         the logo traced from the person's white PNG (arch, CHRON, globe-C, CONCEPT GROUP as separate groups);
         the registration card, the website card (browser bar), the WhatsApp card (green glyph + number).
MOTION:  arrive expo.out 0.6–0.9 s; UI pops back.out(1.6) 0.45 s (damping ≈ 0.6); camera power2.inOut 0.8–1.4 s;
         exits power3.in 0.3–0.4 s (≈ 45% of the entrance); stagger words 0.07 s, tiles 0.06 s;
         motion blur only on whips (12–18 px, horizontal). Landed titles never move.
SHOTS:
  s1 0.0–10.0   routine: clock hub + orbiting tiles; badges climb on "e-mails" (0.7), sheet rows copy on
                "données" (2.6), reminder cards pile on "relancer" (4.2); clock stops on "Et si" (7.3);
                everything blurs back, question title (8.0). Hands off: clock face becomes the n8n node.
  s2 10.0–14.6  drop: n8n mark lands on 10.0, tiles snap into a ring, connectors draw between them with
                travelling dots on "se parlent" (11.2); chain straightens on "s'enchaînent" (12.6);
                camera dives into the first node → dark canvas.
  s3 14.6–20.3  ESURSI: e-mail card drops into "Email Trigger (IMAP)" (14.8); camera tracks the real path;
                checks land on "lu" (16.4), "analysé" (16.9 AI Agent), "classé" (17.8 Décision);
                "Accusé de réception" sends on "part" (19.0); pull back onto the real screenshot (19.4).
  s4 20.3–25.0  MapSante: whole real workflow at 1.7×; cursor clicks Execute (20.4); webhook POST card,
                nodes run in sequence; SQL rows on "interrogée" (22.2); response card flies out on "renvoyé" (23.8).
  s5 25.0–30.0  "VOUS" (26.2) giant; nodes added one by one with the + button (27.3…); AI Agent with
                Chat Model / Memory / Tool lands on "agents IA" (29.4).
  s6 30.0–34.2  colour flood to brand; "Formation" / "Automatisation n8n" per-word blur-in on 30.2;
                "organisée par" + logo performed on "Chronoconcept" (33.5).
  s7 34.2–37.5  zoom through the globe in the logo's C into Africa; DRC fills, pin drops on Kinshasa (35.4);
                iris from the pin into the Silikin Village room on "Silikin" (36.3).
  s8 37.5–48.9  the room becomes a card beside the registration card ("lien en description" 39.8, arrow ↓);
                "Des questions ?" (41.0); site card (42.6); WhatsApp card, number typed 45.2–48.4; both held.
  s9 48.9–56.0  logo built: arch tiles drop in, letters wipe, globe-C spins in, lands on the 50.0 impact;
                "Gagnez du temps" accent line (50.7); contact strip + "Inscription : lien en description" held to 56.
BANNED:  dark void with floating dots; glow, bloom, particles; glass cards; a cream/serif/mono-label look;
         everything fading and sliding up; three cards in a row; a title over a dimmed screenshot; the logo
         docked in a corner; breathing/floating loops on titles; invented dates, prices, programme or
         audience claims; a made-up n8n dashboard (only nodes and labels from the person's screenshots).
QA:      0.0 (thumbnail: clock + tiles + title readable), 10.1 (n8n mark landed), 16.9 (AI Agent lit),
         20.6 (Execute click), 26.3 (VOUS), 31.0 (title), 33.8 (logo + "organisée par"), 35.6 (Kinshasa pin),
         36.8 (room), 40.0 (lien en description), 47.5 (both contacts readable), 52.0 (end card).
