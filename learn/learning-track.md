# JumpSync SQL + Python — a learning track built on your own database

Hi Jolie. This isn't a generic SQL tutorial with a fake `employees` table. Every query
in here runs against **your actual JumpSync database** — the horses, riders, and rides
you (or your barn) already entered. You're going to learn to query real data by asking
real questions about a system you built and understand better than anyone.

You already know HTML/CSS and some Python and SQL. This track assumes that and pushes
from "I can write a SELECT" to "I can answer a real operational question with SQL,
and then do it again from Python." That's the actual skill — not memorizing syntax,
but knowing which tool to reach for and how to ask a database a precise question.

---

## Before you start: connect to your real data

Your database is the JumpSync **Supabase** project. Everything below is wired to it.

**For Part 1 (SQL)** — nothing to install. Open the SQL Editor directly:

> **https://supabase.com/dashboard/project/ieslmsaerwxbdglfyjoj/sql/new**

Paste any query below, hit **Run** (or Ctrl+Enter), and real rows from your barn come
back. (If it asks you to log in, it's the same account that owns the dashboard.)

Want to *see* the tables first, like a spreadsheet? The Table Editor:
> **https://supabase.com/dashboard/project/ieslmsaerwxbdglfyjoj/editor**

**For Part 2 (Python)**, you'll need your connection string:
**Project Settings → Database → Connection string → URI** —
> **https://supabase.com/dashboard/project/ieslmsaerwxbdglfyjoj/settings/database**

That's the value you paste into `jumpsync-stats.py` (it has a clearly marked
placeholder at the top). Full instructions are in Part 2 below.

> A note on `barn_id`: every table in JumpSync has a `barn_id` column because the app
> is built to support multiple barns. If you're the only barn in your database, you
> can ignore it for now — every query below will just work. If you ever see rows that
> don't look like yours, that's your signal to add `where barn_id = '...'` to a query.

---

## Part 1 — SQL, taught through your barn

Each lesson: a real question → the query that answers it → what's new about it.
Then a **Now You Try** for you to write yourself before moving on. Don't skip those —
reading a query and writing one are different muscles.

### Lesson 1 — SELECT and WHERE: picking rows that match

**Question:** Which horses in your barn are Thoroughbreds?

```sql
select name, show_name, breed, yob
from horses
where breed = 'Thoroughbred';
```

`select` says which *columns* you want back (instead of `*`, everything — naming
columns is better practice, it's faster and it's clearer what you're actually using).
`where` filters which *rows* qualify, evaluated per row before anything is returned.
Text values in Postgres SQL go in single quotes: `'Thoroughbred'`, not double quotes.

**Now you try:** Write a query that returns the name and year of birth (`yob`) of
every horse born *before* 2015. (Hint: `yob` is a plain integer, so you can compare
it with `<` just like a number.)

---

### Lesson 2 — ORDER BY and LIMIT: newest first, top N

**Question:** What are the 10 most recent rides logged in JumpSync?

```sql
select date, time, horse_id, rider, type, duration
from rides
order by date desc, time desc
limit 10;
```

`order by` sorts the result set; `desc` means descending (newest/largest first), `asc`
(the default) means ascending. Sorting by two columns (`date desc, time desc`) means:
sort by date first, and for rides on the *same* date, sort by time next. `limit 10`
cuts the sorted list down to the first 10 rows — without it, you'd get every ride ever
logged, sorted.

**Now you try:** Find the 5 *oldest* rides in the table (the very first rides ever
logged).

---

### Lesson 3 — COUNT and GROUP BY: counting per bucket

**Question:** How many rides has each horse had?

```sql
select horse_id, count(*) as ride_count
from rides
group by horse_id
order by ride_count desc;
```

This is the first genuinely new idea, so slow down here. `group by horse_id` tells
Postgres: "collapse all the rows that share the same `horse_id` into one row per
horse." Once rows are collapsed into groups, you can't ask for a plain column like
`date` anymore (which date would it even show — there are many per horse?) — you can
only ask for the grouping column itself, or an *aggregate* like `count(*)`, which
counts how many rows landed in each group. `as ride_count` just renames the output
column so it reads clearly instead of showing `count`.

**Now you try:** Count how many rides each *rider* (the `rider` text column on
`rides`) has logged.

---

### Lesson 4 — SUM and AVG: totals and averages

**Question:** How many total minutes has each horse spent in lessons? And what's
the average ride duration across the whole barn?

```sql
-- total lesson minutes per horse
select horse_id, sum(duration) as total_lesson_minutes
from rides
where type = 'Lesson'
group by horse_id
order by total_lesson_minutes desc;
```

```sql
-- average ride duration, barn-wide
select avg(duration) as avg_ride_minutes
from rides;
```

`sum()` and `avg()` are aggregates, same family as `count()` — they collapse a group
of numbers into one number. Notice the `where type = 'Lesson'` in the first query runs
**before** the grouping happens: Postgres filters down to lesson rides first, *then*
groups what's left by horse. Filter-then-group is the standard order of operations.

**Now you try:** Find the average ride duration for `'Jumping'` rides only.

---

### Lesson 5 — JOIN: the most important concept in this track

**Question:** Every query so far has shown you `horse_id` — a value like `hrs_04f2a1`
that means nothing to a human. You actually want to see the horse's **name**.

```sql
select horses.name as horse_name, rides.date, rides.type, rides.duration
from rides
join horses on rides.horse_id = horses.id
order by rides.date desc
limit 10;
```

Here's why `horse_id` exists at all: JumpSync doesn't repeat "Buttercup, Thoroughbred,
2014, bay" on every single one of Buttercup's hundred ride rows — that would be
wasteful and error-prone (what if you fixed a typo in her name and it only updated
50 of 100 rows?). Instead, `horses` is the *one true source* of horse facts, and
`rides` just stores a pointer to it: `horse_id`. This is called a **foreign key** —
`rides.horse_id` refers to `horses.id`.

`join horses on rides.horse_id = horses.id` tells Postgres: "for every row in `rides`,
find the one row in `horses` whose `id` matches this ride's `horse_id`, and stitch
their columns together into one wide row." Once joined, you can pull `name` from
`horses` and `date`/`type`/`duration` from `rides` in the same `select`, which is why
you prefix column names with the table they came from (`horses.name`, `rides.date`)
— it disambiguates which table each column is coming from.

**Now you try:** Join `rides` to `horses` and show every ride for horses with
`breed = 'Warmblood'` — you'll need a `where` on `horses.breed` alongside the join.

---

### Lesson 6 — GROUP BY + JOIN together: the real payoff

**Question:** What's the total workload — ride count and total minutes — per horse,
shown by name instead of by ID?

```sql
select
    horses.name as horse_name,
    count(rides.id) as ride_count,
    sum(rides.duration) as total_minutes
from rides
join horses on rides.horse_id = horses.id
group by horses.name
order by total_minutes desc;
```

This combines Lessons 3, 4, and 5. Think of it as two steps happening in order: first
the `join` attaches each ride's horse name onto that ride's row (exactly like Lesson
5), and *then* `group by horses.name` collapses those joined rows into one row per
horse, with `count()` and `sum()` summarizing each horse's group. This exact shape —
join to get readable names, then group to summarize — is probably the single most
common pattern you'll write in any real system, not just JumpSync.

**Now you try:** Add `avg(rides.duration) as avg_minutes` to the same query, so you
get count, total, and average side by side per horse.

---

### Lesson 7 — Date filtering: "recent" and "coming up"

**Question:** Which rides happened in the last 7 days? Which horses have health care
due in the next 30 days?

```sql
-- rides in the last 7 days
select horses.name as horse_name, rides.date, rides.type, rides.duration
from rides
join horses on rides.horse_id = horses.id
where rides.date >= current_date - 7
order by rides.date desc;
```

```sql
-- health care due in the next 30 days (and not already overdue)
select horses.name as horse_name, health_records.type, health_records.next_due
from health_records
join horses on health_records.horse_id = horses.id
where health_records.next_due <= current_date + 30
  and health_records.next_due >= current_date
order by health_records.next_due asc;
```

`current_date` is a built-in Postgres value — today's date, evaluated fresh every time
you run the query. In Postgres, you can do date arithmetic directly with plain
integers: `current_date - 7` really does mean "7 days ago," and `current_date + 30`
means "30 days from now." Combining two conditions with `and` (both must be true)
is how you build a *window* — "due soon" instead of just "due before some date," which
would also match things that are already overdue.

**Now you try:** Write a query for health records that are *already overdue* —
`next_due` is in the past.

---

### Lesson 8 — HAVING: filtering the groups themselves

**Question:** Which horses have been ridden more than 5 times?

```sql
select horses.name as horse_name, count(rides.id) as ride_count
from rides
join horses on rides.horse_id = horses.id
group by horses.name
having count(rides.id) > 5
order by ride_count desc;
```

Here's the subtlety: `where` filters individual *rows*, before grouping happens. But
`ride_count` doesn't exist until *after* grouping — it's the result of counting a
group. So you can't say `where ride_count > 5`; Postgres won't know what `ride_count`
means yet at that point in the query. `having` is `where`'s counterpart for filtering
*after* the aggregation — it runs on the groups, not the raw rows. Rule of thumb:
filtering on a real column → `where`; filtering on a `count()`/`sum()`/`avg()` result →
`having`.

**Now you try:** Find horses with more than 300 total ride minutes (`sum(duration) >
300`, using `having`).

---

### Lesson 9 — INSERT and UPDATE: changing data, carefully

Everything above only *reads* data. Let's write some, so you can see how JumpSync's
own "add a ride" or "mark as billed" buttons work under the hood — they're running
SQL just like this.

**Insert a new ride:**

```sql
insert into rides (id, barn_id, horse_id, date, time, duration, type, rider, notes, billed)
values ('ride_test_001', '<your-barn-id>', '<a-real-horse-id>', current_date, '09:00', 45, 'Flatwork', 'Jolie Paddock', 'test row from the SQL lesson', false);
```

You'll need to swap in a real `barn_id` and `horse_id` from your own `horses` table —
run `select id, barn_id from horses limit 1;` first to grab real values to paste in.

**Update that ride to mark it billed:**

```sql
update rides
set billed = true
where id = 'ride_test_001';
```

> **Stop and read this before you ever run an UPDATE:** the `where` clause is what
> limits an update to *specific* rows. If you run `update rides set billed = true;`
> with **no `where` at all**, Postgres will happily mark **every single ride in the
> entire table** as billed — no confirmation, no undo button. Before running any
> `update`, first run the exact same condition as a `select` (`select * from rides
> where id = 'ride_test_001';`) to see precisely which rows you're about to touch.
> If that `select` returns the wrong rows, or too many rows, fix the `where` before
> you ever touch `update`.

**Now you try:** Insert a `health_records` row for one of your horses (`type =
'Farrier'`, `next_due` = 6 weeks from today — you can write that as `current_date +
42`), then write an `update` that changes its `notes` column, using its `id` in the
`where` clause.

---

## Part 2 — Python: reading your real data from code

The Supabase SQL Editor is great for asking one-off questions. Python is what you
reach for when you want to *do something* with the answer — print a formatted report,
combine it with other data, run it on a schedule, build it into a feature. The
companion script, `jumpsync-stats.py`, is a small, real example of that.

### What it does

It connects to your JumpSync database, runs one SQL query — the same join-then-group
idea from Lesson 6 — and prints a table like:

```
Horse                 Rides  Total Min  Jump Min  Flat Min
----------------------------------------------------------
Buttercup                 12        480       210       270
Ranger                     7        315         0       315
```

### How to run it

1. Install the one dependency: `pip install psycopg2-binary`
2. Open `jumpsync-stats.py` and find `SUPABASE_DB_URL` near the top — replace the
   placeholder with your real connection string from **Supabase dashboard → Project
   Settings → Database → Connection string → URI** (fill in your real password and
   project ref).
3. Run it: `python jumpsync-stats.py`

### What's actually happening (the concepts)

- **Connecting**: `psycopg2.connect(SUPABASE_DB_URL)` opens a network connection to
  your Postgres database — same database, different door than the SQL Editor.
- **Running a query**: `cursor.execute("select ...")` sends SQL text over that
  connection, exactly like pasting it into the SQL Editor. `cursor.fetchall()` pulls
  the results back into Python as a list of tuples — one tuple per row.
- **Looping over rows**: `for horse_name, ride_type, duration in rows:` unpacks each
  tuple into named variables, one row at a time, so you can process each one.
- **Aggregation: SQL vs. Python** — the script deliberately does the `join` in SQL
  but the counting/summing in a Python dictionary, so you can see both. As a rule:
  push aggregation into SQL when the table is large or the logic is a standard
  count/sum/avg — the database is built for this and it's much faster than pulling
  a million rows into Python first. Reach for Python aggregation when the logic is
  awkward to express in SQL, or you're about to do something with the result that
  isn't itself a query (print a report, call another API, write a file).

### Now you try — 4 modifications

Work through these in order; each builds on the last.

1. **Add a walk/trot column.** Right now the split is just Jumping vs. Flatwork.
   Add a third bucket for any other `type` value and print it as a "Other Min"
   column.
2. **Rider leaderboard by show points.** Write a *new* query against the `results`
   table — `select rider_name, sum(points) as total_points from results group by
   rider_name order by total_points desc;` — and print it as a ranked leaderboard
   (1st place, 2nd place, etc.). This is the same GROUP BY pattern from Lesson 3,
   just pointed at a different table.
3. **Last 30 days only.** Add `where rides.date >= current_date - 30` to the main
   query (same idea as Lesson 7) so the report reflects recent activity instead of
   the horse's entire history.
4. **Write the report to a CSV file** instead of just printing it, using Python's
   built-in `csv` module (`import csv`, `csv.writer(open('report.csv', 'w'))`). This
   is the same output, just saved somewhere you can open in Excel or attach to an
   email.

---

## Part 3 — why this actually matters for your work

This isn't a side skill. The clinic EMR system you work in every day *is* a database
with tables like `patients`, `visits`, and `charges` standing in for `horses`,
`rides`, and `ledger` — the shape of the problem is identical, just different nouns.
When you're staring at a fellowship take-home that asks you to analyze a dataset or
show how you'd query operational data, this is exactly the muscle being tested: can
you turn a plain-English question into a precise filter, join, or aggregate. SQL is
the closest thing the software world has to a universal language — nearly every real
system, healthcare or otherwise, has a database like this one underneath it, and now
you've read and written against a real one you built yourself.
