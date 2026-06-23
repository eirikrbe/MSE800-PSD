```
Day 0        Environment & Foundation (1–2 days, pre-Sprint)
─────────────────────────────────────────────────────────────
Week 1       Sprint 1 Begins
             User authentication + role system + seed data

Week 2       Sprint 1 Ends / Sprint 2 Begins
             Flashcard management (Kaiako track)
             Practice sessions (Ākonga track) — parallel

Week 3       Sprint 2 Ends
             Demo: full practice flow working end-to-end

Week 4       Sprint 3 Begins
             Progress tracking + acceptance testing + documentation

Week 5       Sprint 3 Ends
             Acceptance sign-off + production deployment + final demo
─────────────────────────────────────────────────────────────
```

---

# Day 0 — Environment & Foundation
*(1–2 days, does not count as a Sprint)*

## Objective
Establish a stable, deployable foundation so that Sprint 1 can begin immediately without any environment blockers.

## Tasks
1. Initialise Flask project directory structure (`app/`, `models/`, `routes/`, `templates/`, `static/`)
2. Configure `.env` file (`DATABASE_URL`, `SECRET_KEY`) and `.gitignore`
3. Create all 6 database tables in Supabase:

```
users             — id, email, password_hash, role, created_at
categories        — id, name, description
flashcards        — id, category_id, card_type, front, back, created_by
practice_sessions — id, user_id, category_id, score, total, created_at
practice_attempts — id, session_id, flashcard_id, is_correct
progress_records  — id, user_id, category_id, attempts, correct, last_practiced
```

4. Write `DatabaseManager` class using psycopg2 and verify connection
5. Connect GitHub repository to Render and confirm auto-deploy pipeline
6. Import seed data (2 categories, ≥16 flashcards) and verify via SQL query
7. Complete cultural review and sign-off on all seed vocabulary

## Deliverables
- Flask app runs locally (`flask run` displays homepage)
- All 6 Supabase tables created; `DatabaseManager` connection test passes
- Render deployment URL accessible (placeholder homepage is sufficient)
- Seed data imported and confirmed via `SELECT COUNT(*) FROM flashcards`

## Outcomes
- Any team member can run the app locally after `git pull` and configuring `.env`
- Render URL returns HTTP 200
- Database query returns ≥16 flashcards across 2 categories

---

# Sprint 1 — Authentication & Role System
*(Week 1 – first half of Week 2)*

## Objective
Implement secure registration, login, and logout for Student and Kaiako roles. Enforce role-based access control so that all subsequent features can be built within correct permission boundaries.

## Tasks

**Authentication Core**
1. Install and configure `Flask-Login` and `bcrypt`
2. Implement `POST /register` route (form validation + password hashing + database write)
3. Implement `POST /login` route (database lookup + bcrypt verification + session creation)
4. Implement `GET /logout` route (session clear + redirect to login)
5. Apply `@login_required` decorator to all dashboard and protected routes

**OOP Class Structure**
6. Write `User` base class (`id`, `email`, `role`; methods: `get_id()`, `get_role()`)
7. Write `Student(User)` subclass — `get_role()` returns `"student"`
8. Write `Kaiako(User)` subclass — `get_role()` returns `"kaiako"`
9. Implement `user_loader` callback to restore the correct subclass instance from the database by user id

**Frontend Pages**
10. Create `register.html` (email, password, role selector, validation error messages)
11. Create `login.html` (email, password, error message display)
12. Create `student_dashboard.html` placeholder (welcome message + role confirmation)
13. Create `kaiako_dashboard.html` placeholder (welcome message + role confirmation)

**Testing**
14. Manual test: register → login → access protected page → logout → confirm redirect back to login
15. Write unit tests for password hashing and `get_role()` return values on both subclasses

## Deliverables
- Working registration and login flow with form validation and error messages
- `models/user.py` containing `User`, `Student`, and `Kaiako` classes
- Separate dashboard pages for each role
- All non-public routes protected by `@login_required`
- Sprint 1 test record (manual test screenshots or unit test output)

## Outcomes
- An ākonga can register; their password is stored as a hash (confirmed via SQL — no plaintext)
- Student and Kaiako users are redirected to their respective dashboards after login
- Accessing `/dashboard` without a session redirects to `/login`
- `Student().get_role()` returns `"student"` and `Kaiako().get_role()` returns `"kaiako"` (unit tests pass)
- Entering an incorrect password shows a user-friendly error message rather than a server error

---

# Sprint 2 — Flashcard Management & Practice Sessions
*(Second half of Week 2 – Week 3)*

## Objective
Enable Kaiako to create, view, edit, and delete flashcards through the web interface. Enable ākonga to select a category, complete a full practice session with card flipping and self-marking, and have all results persisted to the database.

## Tasks

**Track A — Flashcard Management (Kaiako)**
1. Write `Flashcard` base class (`id`, `front`, `back`, `card_type`, `category_id`; method: `get_display_content()`)
2. Write `VocabularyCard(Flashcard)` subclass with `validate()` checking single-word format
3. Write `PhraseCard(Flashcard)` subclass with `validate()` checking phrase length
4. Implement `GET /kaiako/flashcards` — list all flashcards filtered by category
5. Implement `GET/POST /kaiako/flashcards/new` — create flashcard form and database write
6. Implement `GET/POST /kaiako/flashcards/<id>/edit` — edit form and database update
7. Implement `POST /kaiako/flashcards/<id>/delete` — delete with confirmation prompt
8. Implement `GET/POST /kaiako/categories` — list and create vocabulary categories
9. Create templates: `flashcard_list.html`, `flashcard_form.html`, `category_list.html`

**Track B — Practice Sessions (Ākonga)**
10. Implement `GET /student/practice` — category selection page
11. Implement `POST /student/practice/start` — create `PracticeSession`, randomly draw ≥5 cards, store card queue in session
12. Implement `GET /student/practice/card` — display current card front face
13. Implement card flip (JavaScript toggle to reveal back face, or separate `/practice/card/reveal` route as fallback)
14. Implement `POST /student/practice/attempt` — write `PracticeAttempt` record, advance to next card
15. Implement `GET /student/practice/result` — calculate score, update `PracticeSession`, display result page
16. Create templates: `category_select.html`, `practice_card.html`, `practice_result.html`

**Testing**
17. Manual test of full Kaiako CRUD flow with screenshots at each step
18. Manual test of full ākonga practice flow (select category → flip card → mark → result page)
19. Database verification: confirm `practice_sessions` and `practice_attempts` contain correct records after a completed session

## Deliverables
- `models/flashcard.py` containing `Flashcard`, `VocabularyCard`, and `PhraseCard` classes
- Kaiako flashcard CRUD interface (list, create, edit, delete pages)
- Kaiako category management page
- Ākonga complete practice flow (category selection → card flip → self-marking → result page)
- Database screenshot confirming `practice_sessions` and `practice_attempts` are populated
- Sprint 2 test record

## Outcomes
- A Kaiako can create a new `VocabularyCard` via the web form; it appears in the flashcard list after saving
- Edited flashcard content is updated in the database (confirmed via SQL)
- An ākonga completing a session of ≥5 cards sees a correctly formatted result (e.g. "4 / 5 correct — 80%")
- `practice_attempts` contains exactly 5 records linked to the completed session
- `VocabularyCard().get_display_content()` and `PhraseCard().get_display_content()` return differently formatted content (polymorphism confirmed)
- The practice card page reveals the answer without a full page reload

---

# Sprint 3 — Progress Tracking, Acceptance Testing & Deployment
*(Week 4 – Week 5)*

## Objective
Implement ākonga progress tracking that updates automatically after every practice session. Complete acceptance testing against all defined success criteria. Deliver a stable, documented application running in the Render production environment.

## Tasks

**Progress Tracking**
1. Implement `upsert_progress(user_id, category_id, correct, total)` — inserts or updates `progress_records` after each session
2. Call `upsert_progress()` at the end of the `/student/practice/result` route
3. Implement `GET /student/progress` — query all `progress_records` for the current user
4. Create `progress.html` — display per-category: total attempts, cumulative accuracy, date last practised
5. Add "View My Progress" link on the student dashboard

**OOP Completion**
6. Finalise `validate()` implementations in `VocabularyCard` and `PhraseCard`
7. Add docstrings to all classes (`User`, `Student`, `Kaiako`, `Flashcard`, `VocabularyCard`, `PhraseCard`)

**Acceptance Testing**
8. Write and execute acceptance test cases mapped to all 9 success criteria (see Outcomes below)
9. Test edge cases: selecting a category with no flashcards; progress accumulation across 3+ sessions for the same category
10. Run full end-to-end flow on Render production URL (register → practice → view progress)

**Documentation & Deployment**
11. Write `README.md` (project overview, local setup steps, environment variable list, deployment instructions)
12. Create database ER diagram and include in `README.md` or `/docs`
13. Close all completed GitHub issues; archive Sprint board in GitHub Projects
14. Final Render deployment check — confirm all routes return expected responses in production

## Deliverables
- `progress.html` displaying per-category statistics for the logged-in ākonga
- `upsert_progress()` function triggered automatically at the end of every practice session
- Acceptance test record document — each success criterion tested, with screenshots or test output
- Complete `README.md` with ER diagram and deployment instructions
- Render production URL (publicly accessible, all core features functional)
- Final GitHub repository (complete commit history, closed issues, archived Sprint board)

## Outcomes

| Success Criterion | Acceptance Method |
|---|---|
| Ākonga can register and log in securely | Register a new account; confirm password is hashed in database; login succeeds |
| Ākonga can complete a practice session of ≥5 cards and receive a score | Demonstrate a full session; result page shows X / Y correct |
| Progress updates correctly after each completed session | Complete 3 sessions in the same category; confirm `progress_records` accumulates correctly |
| Kaiako can create, edit, delete, and view flashcards by category | Demonstrate full CRUD; verify each operation via SQL |
| System supports at least two flashcard types | Create and practise both `VocabularyCard` and `PhraseCard` |
| Progress records display correctly after ≥3 practice attempts | Progress page shows cumulative data matching database records |
| System stores and retrieves all entities via Supabase PostgreSQL | SQL query confirms data exists across all 6 tables |
| Protected routes block unauthorised access | Access `/student/progress` without a session; confirm redirect to `/login` |
| Web application deploys successfully on Render | Production URL returns HTTP 200; all core pages load without errors |