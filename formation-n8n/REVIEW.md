# REVIEW — Formation Automatisation n8n (16:9 + 9:16)

## Creative calls
- Built storyline A « Le fil » (STORYLINES.md): the routine around a ticking clock (CHRONO) → n8n wires the apps →
  an e-mail runs through the real ESURSI workflow → a request runs through MapSante → « VOUS » build step by step →
  title + logo → zoom through the globe of the logo's C into Africa → Kinshasa → the Silikin Village room → sign-up
  and contacts → the logo built on the score's impact. Not built: B « Chrono » (stopwatch match cuts), C « Silikin
  d'abord » (one endless zoom from the room).
- Look taken from the reference film's grammar (airy blue light, white cards, orbiting app tiles, flowing
  connectors, a hub at the centre, logo assembled from pieces, end card with a button) in the brand's own blues;
  n8n's real dark canvas for the product beats, rebuilt node by node from the two screenshots (node names,
  positions, icons and colours measured on them), ending on the real ESURSI screenshot.
- Logo: traced to vectors from the white PNG (the globe-C version), split into arch / letters / globe-C /
  « CONCEPT GROUP » so it can be built; coloured with the palette of the colour PNG.
- Vertical cut is recomposed, not cropped: content in the 168–1150 px band, burned-in word-by-word captions at
  1176 px (TikTok's caption/handle zone starts at 1330 px), nothing readable under the right-hand rail.

## Facts and what is not in the film
- Every claim traces to the request: n8n automation training, organised by CHRONOCONCEPT GROUP, Kinshasa, Silikin
  Village, chronoconcept.net, WhatsApp +243 853 420 317, registration form and details via the description link.
- chronoconcept.net could not be reached from this session (network policy), so **no dates, price, duration or
  programme** appear. Example data on screen (« Facture n°2041 », « Client A · 1 200 · Payé ») is illustrative UI.

## Measured
- `npx hyperframes check`: lint, runtime, layout, contrast, motion, audio OK on both cuts (0 errors).
- Voice (ElevenLabs, voice RBhYSNMNu6b2CGZ9Fn1M « Felix », eleven_v4, take A of 2): −15.8 LUFS, true peak −4.5 dBFS.
- Music (original, music/compose.py, 120 BPM, 28 bars): spectrum balanced (10–30 s: 43 % < 150 Hz, 45 % 150 Hz–3 kHz),
  ducked −9 dB under the voice (≈14 dB below the voice while it speaks); full mix −15.6 LUFS, peak −2.4 dBFS.
- Sync: « Avec n8n » lands on bar 6 (10.0 s, the drop); title on bar 16 (30.0 s); Kinshasa section on bar 18;
  logo lands on the impact at 50.0 s; WhatsApp digits appear group by group as they are spoken.

## Not checked (nobody heard it)
- I cannot listen: the sound was measured, not heard. Please listen for the TTS pronunciation of « n8n »,
  « Silikin Village », « chronoconcept.net » and the phone number. The ElevenLabs alignment returned the script text,
  so it does not prove what was said. A second take (B) exists in the ElevenLabs flow if A has a slip.
- The voice is Québécois (the requested voice id); the accent is the voice's own.

## Weakest shots, and what I would change with more time
- 10.0 s (the drop): the first two frames of s2 are almost empty (the clock has shrunk to a point before the n8n mark
  bursts out) — intended as a breath on the drop, but it is the emptiest frame of the film.
- s5 « VOUS » build: the canvas is sparse at 1920 px; a camera push on each new node would give it more energy.

## Warnings kept on purpose
- Node labels sweep past in under 1 s while the camera tracks the workflows (the process runs fast; the payoff and the
  title hold); n8n port micro-labels (« true », « Chat Model ») stay under 28 px like in the real UI.
- `duplicate_media_discovery_risk`: the same app icon is used several times in s1.
