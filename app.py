import streamlit as st
from pawpal_system import Task, Pet, Owner, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Owner setup ────────────────────────────────────────────────────────────────
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
time_available = st.number_input("Available time today (hours)", min_value=0.5, max_value=24.0, value=4.0, step=0.5)

if st.button("Set / Update Owner"):
    st.session_state.owner = Owner(owner_name, time_available)
    # Clear schedule when owner changes
    st.session_state.pop("schedule", None)

if "owner" not in st.session_state:
    st.info("Set the owner above to get started.")
    st.stop()

owner: Owner = st.session_state.owner
st.success(f"Owner: **{owner.getName()}** — {owner.getTimeAvailability()}h available")

st.divider()

# ── Add a Pet ──────────────────────────────────────────────────────────────────
st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    preferences = st.text_input("Owner preferences", value="Prefers morning walks")

if st.button("Add Pet"):
    existing_names = [p.getName() for p in owner.getPets()]
    if pet_name in existing_names:
        st.warning(f"A pet named **{pet_name}** is already added.")
    else:
        new_pet = Pet(pet_name, species, preferences)
        owner.addPet(new_pet)
        st.success(f"Added **{pet_name}** ({species}) to {owner.getName()}'s care list.")

pets = owner.getPets()
if pets:
    st.caption("Current pets")
    st.dataframe(
        [{"Name": p.getName(), "Type": p.getType(), "Preferences": p.getPreferences(), "Tasks": len(p.getTasks())} for p in pets],
        use_container_width=True,
        hide_index=True,
    )

st.divider()

# ── Add a Task ─────────────────────────────────────────────────────────────────
st.subheader("Add a Task")

PRIORITY_BADGE = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}
DONE_BADGE = {True: "✅", False: "⬜"}

if not pets:
    st.info("Add at least one pet before scheduling tasks.")
else:
    pet_names = [p.getName() for p in pets]
    target_pet_name = st.selectbox("Assign task to pet", pet_names)
    target_pet = next(p for p in pets if p.getName() == target_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=480, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add Task"):
        new_task = Task(task_title, int(duration), priority)
        target_pet.addTask(new_task)
        st.success(f"Task **{task_title}** added to **{target_pet_name}**.")

    all_tasks = owner.getAllTasks()
    if all_tasks:
        st.caption("All tasks across pets")
        st.dataframe(
            [
                {
                    "Pet": t.pet.getName() if t.pet else "—",
                    "Task": t.getName(),
                    "Duration (min)": t.getDuration(),
                    "Priority": PRIORITY_BADGE.get(t.getPriority(), t.getPriority()),
                    "Done": DONE_BADGE[t.isCompleted()],
                }
                for t in all_tasks
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.caption("Edit or delete a task")
        task_labels = [f"{t.pet.getName()} — {t.getName()} ({t.getDuration()} min)" for t in all_tasks]
        selected_label = st.selectbox("Select task", task_labels, key="edit_select")
        selected_task = all_tasks[task_labels.index(selected_label)]

        with st.expander("Edit selected task"):
            edit_col1, edit_col2, edit_col3 = st.columns(3)
            with edit_col1:
                new_title = st.text_input("Title", value=selected_task.getName(), key="edit_title")
            with edit_col2:
                new_duration = st.number_input("Duration (min)", min_value=1, max_value=480,
                                               value=int(selected_task.getDuration()), key="edit_dur")
            with edit_col3:
                pri_options = ["low", "medium", "high"]
                new_priority = st.selectbox("Priority", pri_options,
                                            index=pri_options.index(selected_task.getPriority()),
                                            key="edit_pri")
            if st.button("Update Task"):
                selected_task.name = new_title
                selected_task.duration = int(new_duration)
                selected_task.priority = new_priority
                st.session_state.pop("schedule", None)
                st.success("Task updated.")
                st.rerun()

        if st.button("Delete Selected Task", type="secondary"):
            if selected_task.pet:
                selected_task.pet.removeTask(selected_task)
            st.session_state.pop("schedule", None)
            st.success(f"Deleted **{selected_task.getName()}**.")
            st.rerun()

st.divider()

# ── Generate Schedule ──────────────────────────────────────────────────────────
st.subheader("Build Schedule")

if st.button("Generate Schedule"):
    if not owner.getAllTasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        sched = Schedule(owner)
        sched.generateSchedule()
        st.session_state.schedule = sched

if "schedule" in st.session_state:
    sched: Schedule = st.session_state.schedule

    # ── Availability banner ────────────────────────────────────────────────────
    if sched.canFitSchedule():
        st.success("All tasks fit within your available time.")
    else:
        st.error("Tasks exceed available time — consider removing lower-priority items.")

    # ── Conflict warnings via Schedule.getConflicts() ──────────────────────────
    if sched.hasConflicts():
        conflicts = sched.getConflicts()
        st.warning(f"{len(conflicts)} scheduling conflict(s) detected.")
        with st.expander("View conflicts"):
            for a, b in conflicts:
                a_pet = a.pet.getName() if a.pet else "?"
                b_pet = b.pet.getName() if b.pet else "?"
                st.write(f"- **{a.getName()}** ({a_pet}) and **{b.getName()}** ({b_pet}) — both at `{a.time}`")

    # ── Summary metrics ────────────────────────────────────────────────────────
    total_min = sched.getTotalScheduledTime()
    avail_h = owner.getTimeAvailability()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total tasks", len(sched.getTasks()))
    m2.metric("Total time (min)", int(total_min))
    m3.metric("Available (h)", avail_h)
    m4.metric("High priority", len(sched.getTasksByPriority("high")))

    # ── Filter by pet via Schedule.filterTasks() ───────────────────────────────
    pet_options = ["All pets"] + [p.getName() for p in owner.getPets()]
    selected_pet = st.selectbox("Filter by pet", pet_options)

    filtered = (
        sched.filterTasks()
        if selected_pet == "All pets"
        else sched.filterTasks(pet_name=selected_pet)
    )

    # ── Table sorted by time via Schedule.sort_by_time() ──────────────────────
    sorted_tasks = sorted(filtered, key=lambda t: t.time)

    st.caption(f"{len(sorted_tasks)} task(s) — sorted by scheduled time")
    if sorted_tasks:
        st.dataframe(
            [
                {
                    "Time": t.time,
                    "Pet": t.pet.getName() if t.pet else "—",
                    "Task": t.getName(),
                    "Duration (min)": t.getDuration(),
                    "Priority": PRIORITY_BADGE.get(t.getPriority(), t.getPriority()),
                    "Done": DONE_BADGE[t.isCompleted()],
                }
                for t in sorted_tasks
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No tasks match the selected filter.")
