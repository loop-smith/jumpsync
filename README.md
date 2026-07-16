# JumpSync — Stable Management Portal

A vintage, old-money styled barn management app. Everything lives in one file (`index.html`) — open it in your browser and you're in the barn.

*Based in Reno, Nevada · Built July 2026 · Name "JumpSync" is a placeholder (click ✎ rename on the home page).*

---

## Getting started

1. Open `index.html` in Chrome or Edge.
2. Sign in with your name and access level.
3. **First thing, once:** click **"⚠ Not backed up — click to fix"** in the header and save the data file into this folder. Every change auto-saves to it from then on.

## Accounts & access

| Role | Sign-in | What they see |
|---|---|---|
| **Manager** | name only | Everything — all tiles, all chats, billing, contacts, delete rights |
| **Employee** | name only | Everything except Billing and Contacts; no delete rights |
| **Rider** | name + password | Their lessons, shows & barn events, horse profiles (minus feeding), their statement, their results, private chat with staff |

**Rider passwords:** the rider must already exist in Rider Profiles (added by staff). Password = full name, no spaces, plus `1` — e.g. Alice Cooper → `AliceCooper1`. First login walks them through a welcome questionnaire (history, goals, allergies, questions — questions go straight to the manager's messages). *Email logins planned for the hosted version.*

## The tiles

- **Calendar** — month view. Click a day to see or book. Repeating appointments (weekly through every-8-weeks, monthly, or custom every-N-days) expand automatically. Editing/deleting a repeat asks *"just this visit or the whole series?"*
- **Horses** — profile with photo, barn/show name, breed, age; history & temperament; allergies; grain/hay what-and-when (staff only); turnout time, location & buddies; blanketing rules; assigned riders. Care alerts appear when a vet/farrier date is within 10 days. Weekly ride tally on each card.
- **Rider Profiles** (staff) — contact, DOB, address, emergency contact, allergies, medical, riding history & goals, upcoming lessons, season points. "Book ride" from any card.
- **Upcoming Events** — barn agenda. Riders see only their lessons + shows/clinics/barn-wide events. Vet/farrier visits carry a **Provider** so staff know who's coming (mini-EMR).
- **Message Portal** — public barn board + **Private messages** (rider ↔ staff only; managers see every conversation in the barn).
- **Contacts** (manager) — vets, farriers, acupuncturists, dentists, etc. These fill the Provider dropdown when scheduling; new providers can be added right inside the event form.
- **Ride Stats** (staff) — per-horse workload bars over week / 2 weeks / month / 3 months / year, jumping vs. flatwork vs. other, plus saddle hours.
- **Billing** — charges (board, lessons, pass-throughs, show fees), payments (cash/check/Venmo/Zelle/card), running balances, barn-wide outstanding total. "Bill N lessons" auto-charges unbilled past lessons at your rate. Riders see their own statement. *Online payments (Stripe) planned for the hosted version.*
- **Show Bulletin** — the real 2026 SNHSA season (from [snhsa.org](https://snhsa.org/events/)) with venues, dates, entry deadlines, detail links, and one-click **Add to barn calendar** (deadline reminders included). USHJA and rulebook links in Resources. Ask Claude to refresh the list anytime.
- **Results & Points** — show results per rider with true ribbon colors (blue/red/yellow/white/pink/green), points auto-filled from the classic scale (10-6-4-2-1-½, editable to match SNHSA), season standings leaderboard. Riders see "My results" on their account.

## Home page extras

- **Tonight at the barn** — live Reno forecast (low, tomorrow, rain). When the low crosses a temperature in any horse's blanketing rules, staff get a blanket-check alert naming the horses.

## Your data

- Auto-saves to browser storage **and** to your backup `.json` file on every change ("Saved ✓" toast confirms).
- If the browser wipes itself, the app offers **"Reconnect & restore 💾"** on open — one click brings everything back.
- Export/Import buttons in the header for manual copies.
- Photos are resized automatically to keep the file lean.

## Known limits (single-file version)

- One computer at a time — riders can't log in from their phones yet.
- Passwords are a gate, not a vault.
- Show Bulletin and fonts need internet; data does not.
- The path forward is a hosted rebuild (React + Supabase + Stripe) — roughly $0–25/month at barn scale. The prototype keeps working throughout.

## Files in this folder

- `index.html` — the entire app
- `logo-concepts.html` — three logo directions (Monogram, Hallmark, Crest)
- `Logo Ideas/` — inspiration images
- `README.md` — this file
- your backup `.json` — the barn's data (don't delete!)
