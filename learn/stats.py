"""
jumpsync-stats.py

Connects to Jolie's real JumpSync Supabase database and prints a
per-horse workload summary: rides, total minutes, and the Jumping vs
Flatwork split for each horse.

Install:
    pip install psycopg2-binary

Run:
    python jumpsync-stats.py
"""

import psycopg2

# --- STEP 1: paste your connection string here -----------------------------
# Supabase dashboard -> Project Settings -> Database -> Connection string
# -> "URI". It looks like:
#   postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
# Get [YOUR-PASSWORD] from that same page (or reset it there -- normal,
# everyone does this the first time). NEVER commit this file to git with a
# real password filled in below.
SUPABASE_DB_URL = "postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres"


def get_connection():
    """Connect to Postgres, with a beginner-friendly error if it fails."""
    try:
        return psycopg2.connect(SUPABASE_DB_URL)
    except Exception as e:
        print("Could not connect to the database.")
        print("Check SUPABASE_DB_URL above -- did you paste your real")
        print("password and project ref in place of the placeholders?")
        print(f"\n(details: {e})")
        raise SystemExit(1)


def main():
    conn = get_connection()
    cur = conn.cursor()

    # Ask Postgres to do the JOIN (see Lesson 5 in the learning track): match
    # each ride to its horse's name instead of a raw horse_id value. We keep
    # this query simple and do the counting/summing ourselves in Python below
    # so you can see both approaches side by side.
    cur.execute("""
        select horses.name, rides.type, rides.duration
        from rides
        join horses on rides.horse_id = horses.id
        order by horses.name;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("No rides found yet. Log one in JumpSync and run this again.")
        return

    # Aggregate in Python: a dict keyed by horse name holding running totals.
    # (SQL's GROUP BY does this same job -- see Lesson 3/6 -- this script does
    # it here on purpose so you can compare the two ways of aggregating.)
    summary = {}
    for horse_name, ride_type, duration in rows:
        stats = summary.setdefault(
            horse_name, {"rides": 0, "minutes": 0, "jumping": 0, "flatwork": 0}
        )
        minutes = duration or 0  # guard against a NULL duration
        stats["rides"] += 1
        stats["minutes"] += minutes
        if ride_type == "Jumping":
            stats["jumping"] += minutes
        elif ride_type == "Flatwork":
            stats["flatwork"] += minutes

    # Print a clean, readable report.
    print(f"{'Horse':<20}{'Rides':>7}{'Total Min':>11}{'Jump Min':>10}{'Flat Min':>10}")
    print("-" * 58)
    for horse_name, s in sorted(summary.items()):
        print(
            f"{horse_name:<20}{s['rides']:>7}{s['minutes']:>11}"
            f"{s['jumping']:>10}{s['flatwork']:>10}"
        )


if __name__ == "__main__":
    main()
