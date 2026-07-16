# JumpSync — Stable Management, in the cloud

A barn-management web app: horses, riders, lessons, health records, billing, show
results, and a live weather-driven blanket check. Built with Claude Code.

**Live:** https://loop-smith.github.io/jumpsync/
**Just looking?** Click **"View the demo barn"** on the sign-in screen — a real example
stable you can explore, nothing to set up.

---

## What it is now

One file (`index.html`) — a single-page app — backed by a real **Supabase** database.
No build step. Open the URL, sign in, and your barn lives in the cloud: it survives
reloads, new devices, and cleared browsers, and photos are stored properly (no more
"storage full").

- **Accounts** — email + password. Three access levels: **Manager** (everything),
  **Employee** (no billing/contacts, no deletes), **Rider** (their own lessons, horses,
  statement, results, and private messages with staff).
- **Cloud data** — Postgres tables with row-level security, so a rider only ever sees
  their own records. Horse photos go to Supabase Storage.
- **Live** — pulls the local forecast and, when the overnight low crosses a horse's
  blanketing rule, names the horses that need a blanket tonight.

## The tiles

Calendar · Horses · Rider Profiles · Upcoming Events · Message Portal · Contacts ·
Ride Stats · Billing · Show Bulletin · Results & Points — same features as before,
now cloud-backed and multi-user.

## Running / editing it

It's one static HTML file. To run locally: `python -m http.server` in this folder,
then open `http://localhost:8000/index.html`. To change it, edit `index.html` and
push — GitHub Pages redeploys automatically.

The Supabase project URL and **publishable** key are embedded near the top of the first
`<script>` in `index.html`. That key is safe to publish — row-level security protects
the data, not the key.

## The database

Supabase project **jumpsync**. Tables: horses, riders, health_records, rides, events,
contacts, ledger, results, messages, dms, plus barns/profiles for accounts. The
`jumpsync-learning-track.md` companion (in the internship folder) is a hands-on SQL +
Python tour of this exact database.

## Files here

- `index.html` — the entire app (cloud-backed)
- `logo-concepts-jumpsync.html` — logo directions (Monogram / Hallmark / Crest / Arc)
- `jumpsync-signet.html` — the JS signet marks at real favicon sizes
- `README.md` — this file

## Honest limits

- Single barn per install right now (everyone who signs up joins the same barn).
  Multi-barn and per-barn invites are the next step if it goes wider.
- The demo account is shared and editable — treat the demo barn as a sandbox.
- Online payments (Stripe) not wired yet — billing tracks charges/payments by hand.
