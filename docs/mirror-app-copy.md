# Quiet Creek Tarot app: UI copy and the decisions behind it

Every string the app shows, grouped by moment. Static strings live in `index.html`; the ones the script writes live in the `COPY` object at the top of `app.js`. Change them there and run `make app`.

The product rule all of this follows: the app never interprets. The cards carry names and images only. The querent reads them and writes their own interpretation.

## Vocabulary

One term per concept, everywhere: **reading** (one draw and its words), **Log** (all readings), **card**, **deal**, **turn**. Never "entry", "journal", "spread", "session" or "save".

## First open

| Element | Copy |
|---|---|
| Eyebrow | QUIET CREEK TAROT |
| Headline | You do the reading. |
| Body | These 78 cards come with no meanings. Draw one to four, look closely, and write what you see. |
| Privacy | Your readings stay on this phone. No account or sign-in required. |
| Button | Start a reading |

- **Name the absence first.** A tarot app with no meanings looks broken until someone says so. The headline gives the reader the job; the body says what is missing before a card ever turns.
- **Answer the privacy question before it is asked.** No account exists, so say it in six words instead of a policy link.
- **Keep the claim literally true.** "phone" becomes "device" on desktops and tablets.
- **The button names the outcome**, not "Get started" or "Continue".

## The draw

| Step | Copy |
|---|---|
| Choose | How many cards? / Tap a number to begin. (each number reads "Draw 3 cards" to a screen reader) |
| Breathe | Breathe in / Breathe out (one word pair, never overlapping; "Take one slow breath." with reduced motion) |
| Question | Bring a question to mind. / placeholder: Or keep it to yourself. |
| Shuffle | Shuffling. Stop when you're ready. / Stop |
| Stopped | The order is set. / Deal 3 cards |
| Header | Back (only on steps you can step back from) |

- **Buttons are the ritual's verbs.** Shuffle, Stop, Deal, New reading. Each names the act; none says Next, OK or Submit.
- **The Deal button carries the count**, so the reader confirms their choice without a summary screen.
- **The draw belongs to the reader.** "Stop when you're ready" then "The order is set." It is true: the shuffle is fixed at the moment they tap Stop.
- **Optional, without the word optional.** The question is a prompt to think, and the placeholder gives permission not to type.

## The reading

| Element | Copy |
|---|---|
| Hint, cards face down | Tap a card to turn it. |
| Hint, all turned | Tap a card to see it up close. |
| Writing prompt | What do you see? |
| Placeholder | Colors, shapes, a word, a memory. |
| Status | Saved on this phone |
| Buttons | New reading / Delete this reading |

- **One instruction at a time.** The hint changes with the state of the cards.
- **Ask for observation, not meaning.** "What do you see?" points at the image. The placeholder gives four concrete ways in, all visual or personal.
- **No Save button.** Every keystroke is kept; the status line confirms it. Nobody loses words by switching apps.
- **The writing box appears after the first card turns**, so the cards come first.

## Log

| Element | Copy |
|---|---|
| Count | 1 reading / 12 readings |
| Entry with no words | No words yet. |
| Empty state | No readings yet. / Every reading you deal is kept here, with whatever you write. / Start a reading |
| Export | Export Log / Saves every reading as one text file. Your readings live only on this phone, so export now and then to keep a copy. |
| Colophon | Quiet Creek Tarot by Wild-Lake. 78 original cards. No meanings. |

- **"No words yet."** implies later, not failure.
- **The empty state teaches the one rule of the Log** (everything dealt is kept) and offers the one action.
- **Disclose the risk where the remedy is.** On-device only means a lost phone loses the Log, so the warning sits beside Export, not in onboarding.
- **Dates on screen follow the phone's locale**; the export uses 2026-11-05 15:42 so it sorts.

## Errors and system messages

Pattern: what happened, what is safe, what to do. No "Oops", no "Something went wrong", no codes, no blame.

| Situation | Copy | Action |
|---|---|---|
| Storage full | Your Log is out of room on this phone. What you just wrote is still on screen. Export the Log, then delete a few old readings. | Export Log |
| Private window, cannot save | This window can't save. You can still draw and write, but nothing will be kept after you close it. | none |
| Log unreadable | Your Log couldn't be opened, so a copy was set aside on this phone. New readings will save normally. | none |
| Export failed | Export didn't finish. Your Log is unchanged. | Try again |
| Export done (download) | Exported as a text file. | none |
| Share sheet closed | (nothing) | |
| New version | A new version is ready. Your readings are safe. | Update |
| Reading deleted | Reading deleted. | none |
| No JavaScript | Quiet Creek Tarot needs JavaScript to shuffle and deal. | |
| Offline | (nothing: the whole app works offline) | |

- **Lead with safety when data is involved.** Every storage message says what is still there before asking for anything.
- **Silence where nothing is wrong.** An offline banner would announce a problem the app does not have. Closing the share sheet is a choice, not an error.
- **Updates are offered, never forced**, so a reading in progress is never reloaded away.

## Delete

| Element | Copy |
|---|---|
| Title | Delete this reading? |
| Body | Its cards and words will be gone from this phone. This can't be undone. |
| Buttons | Delete / Keep it |

- **Name the object and the consequence; label the buttons with verbs**, so either one reads correctly on its own.

## Install

| Platform | Copy | Actions |
|---|---|---|
| Android, desktop Chrome | Keep Quiet Creek on your home screen. It opens full screen and works offline. | Install / Not now |
| iPhone, iPad | Keep Quiet Creek on your home screen: tap Share, then Add to Home Screen. | Not now |
| Log footer | Install on this phone | |

- **Ask after value.** The card appears only after the first reading is dealt, never on first open.
- **Give iOS the literal path.** iOS has no install button, so the copy names the two taps.
- **"Not now" is final.** The card never returns; the Log footer link stays for anyone who changes their mind.
- **Home-screen name: "Quiet Creek"** (11 characters, fits under an icon on iOS and Android). Shortcuts on a long press: "One card", "Log".
