# Logic Layer where all Backend Classes Lives

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta
from itertools import combinations
from typing import List


class Owner:
    """Represents a pet owner."""
    
    def __init__(self, name: str, timeAvailability: float):
        """Initialize an Owner with name and available time for pet care."""
        self.name = name
        self.timeAvailability = timeAvailability
        self.pets: List[Pet] = []
    
    def getName(self) -> str:
        """Get the owner's name."""
        return self.name
    
    def getTimeAvailability(self) -> float:
        """Get the owner's available time."""
        return self.timeAvailability
    
    def setTimeAvailability(self, timeAvailability: float) -> None:
        """Set the owner's available time."""
        self.timeAvailability = timeAvailability
    
    def addPet(self, pet: Pet) -> None:
        """Add a pet to the owner's list."""
        if pet not in self.pets:
            pet.owner = self
            self.pets.append(pet)
    
    def getPets(self) -> List[Pet]:
        """Get all pets owned by this owner."""
        return self.pets
    
    def removePet(self, pet: Pet) -> None:
        """Remove a pet from the owner's list."""
        if pet in self.pets:
            self.pets.remove(pet)
            pet.owner = None
    
    def getAllTasks(self) -> List[Task]:
        """Get all tasks from all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.getTasks())
        return all_tasks
    
    def getTotalTaskDuration(self) -> float:
        """Calculate total duration of all tasks across all pets."""
        return sum(task.getDuration() for task in self.getAllTasks())
    
    def __str__(self) -> str:
        """Return a string representation of the owner."""
        return f"Owner: {self.name} - Pets: {len(self.pets)}, Available Time: {self.timeAvailability}h"


@dataclass
class Pet:
    """Represents a pet."""
    
    name: str
    type: str
    ownerPreferences: str
    owner: Owner = field(default=None)
    tasks: List[Task] = field(default_factory=list)
    
    def getName(self) -> str:
        """Get the pet's name."""
        return self.name
    
    def getType(self) -> str:
        """Get the pet's type."""
        return self.type
    
    def getPreferences(self) -> str:
        """Get the owner's preferences for this pet."""
        return self.ownerPreferences
    
    def addTask(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        if task not in self.tasks:
            task.pet = self
            self.tasks.append(task)
    
    def getTasks(self) -> List[Task]:
        """Get all tasks assigned to this pet."""
        return self.tasks
    
    def removeTask(self, task: Task) -> None:
        """Remove a task from the pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)
            task.pet = None
    
    def getCompletedTasks(self) -> List[Task]:
        """Get all completed tasks for this pet."""
        return [task for task in self.tasks if task.isCompleted()]
    
    def getIncompleteTasks(self) -> List[Task]:
        """Get all incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.isCompleted()]
    
    def __str__(self) -> str:
        """Return a string representation of the pet."""
        return f"{self.name} (Type: {self.type}) - Tasks: {len(self.tasks)}"


@dataclass
class Task:
    """Represents a task for a pet."""
    
    name: str
    duration: float
    priority: str
    time: str = "00:00"
    recurrence: str = None          # "daily", "weekly", or None
    due_date: date = field(default_factory=date.today)
    pet: Pet = field(default=None)
    completed: bool = False
    
    def getName(self) -> str:
        """Get the task's name."""
        return self.name
    
    def getDuration(self) -> float:
        """Get the task's duration."""
        return self.duration
    
    def getPriority(self) -> str:
        """Get the task's priority level."""
        return self.priority
    
    def setPriority(self, priority: str) -> None:
        """Set the task's priority level."""
        self.priority = priority
    
    def markCompleted(self) -> None:
        """Mark this task as completed and schedule the next occurrence if recurring."""
        self.completed = True
        if self.recurrence and self.pet:
            next_task = self.next_occurrence()
            self.pet.addTask(next_task)

    def next_occurrence(self) -> Task:
        """Return a new incomplete Task for the next occurrence based on recurrence."""
        if self.recurrence == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.recurrence == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
        else:
            return None

        return Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            time=self.time,
            recurrence=self.recurrence,
            due_date=next_date,
        )
    
    def isCompleted(self) -> bool:
        """Check if this task is completed."""
        return self.completed
    
    def __str__(self) -> str:
        """Return a string representation of the task."""
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.name} ({self.duration}min) - Priority: {self.priority}"


class Schedule:
    """Represents a schedule containing multiple tasks."""
    
    def __init__(self, owner: Owner):
        """Initialize a Schedule for organizing tasks for a specific owner."""
        self.owner = owner
        self.tasks: List[Task] = []
    
    def generateSchedule(self) -> None:
        """Generate an optimized schedule based on owner availability and pet tasks."""
        # Get all tasks from all owned pets
        all_tasks = self.owner.getAllTasks()
        
        # Sort tasks by priority (high first) and then by duration (short first)
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(
            all_tasks,
            key=lambda t: (priority_order.get(t.getPriority(), 3), t.getDuration())
        )
        
        # Add sorted tasks to the schedule
        self.tasks = sorted_tasks
    
    def addTask(self, task: Task) -> str | None:
        """Add a task to the schedule.

        Returns a warning string if the task's time conflicts with an existing
        task, or None if the task was added without issue. The task is always
        added regardless of conflicts.
        """
        if task in self.tasks:
            return None

        warning = None
        for existing in self.tasks:
            if existing.time == task.time:
                existing_pet = existing.pet.name if existing.pet else "Unknown"
                new_pet = task.pet.name if task.pet else "Unknown"
                warning = (
                    f"WARNING: '{task.name}' ({new_pet}) conflicts with "
                    f"'{existing.name}' ({existing_pet}) -- both scheduled at {task.time}"
                )
                break

        self.tasks.append(task)
        return warning
    
    def removeTask(self, task: Task) -> None:
        """Remove a task from the schedule."""
        if task in self.tasks:
            self.tasks.remove(task)
    
    def getTasks(self) -> List[Task]:
        """Get all tasks in the schedule."""
        return self.tasks
    
    def getTasksByPriority(self, priority: str) -> List[Task]:
        """Get tasks filtered by priority level."""
        return [task for task in self.tasks if task.getPriority() == priority]
    
    # Sorting Logic
    def sort_by_time(self) -> List[Task]:
        """Return tasks sorted by their time attribute (earliest first)."""
        return sorted(self.tasks, key=lambda t: t.time)

    def getTasksByPet(self, pet: Pet) -> List[Task]:
        """Get tasks for a specific pet from the schedule."""
        return [task for task in self.tasks if task.pet == pet]

    # Conflict Detection
    def getConflicts(self) -> List[tuple]:
        """Return pairs of tasks scheduled at the same time.

        Returns:
            A list of (Task, Task) tuples where both tasks share the same time value.
            Each conflicting pair appears once.
        """
        return [
            (a, b) for a, b in combinations(self.tasks, 2)
            if a.time == b.time
        ]

    def hasConflicts(self) -> bool:
        """Return True if any two tasks share the same scheduled time."""
        return len(self.getConflicts()) > 0

    # Filtering Logic
    def filterTasks(self, completed: bool = None, pet_name: str = None) -> List[Task]:
        """Filter tasks by completion status, pet name, or both.

        Args:
            completed: If True, return only completed tasks. If False, return only
                       incomplete tasks. If None, completion status is not filtered.
            pet_name:  If provided, return only tasks belonging to a pet with this name.
                       If None, all pets are included.

        Returns:
            A list of Task objects matching all specified criteria.
        """
        result = self.tasks

        if completed is not None:
            result = [task for task in result if task.isCompleted() == completed]

        if pet_name is not None:
            result = [task for task in result if task.pet and task.pet.getName() == pet_name]

        return result
    
    def canFitSchedule(self) -> bool:
        """Check if all scheduled tasks fit within owner's available time."""
        total_duration = sum(task.getDuration() for task in self.tasks)
        return total_duration <= self.owner.getTimeAvailability()
    
    def getTotalScheduledTime(self) -> float:
        """Get the total time required for all scheduled tasks."""
        return sum(task.getDuration() for task in self.tasks)
    
    def getScheduleSummary(self) -> str:
        """Get a summary of the current schedule."""
        if not self.tasks:
            return "No tasks scheduled."
        
        total_time = self.getTotalScheduledTime()
        available_time = self.owner.getTimeAvailability()
        fits = "✓ Fits" if self.canFitSchedule() else "✗ Exceeds"
        
        summary = f"Schedule Summary for {self.owner.getName()}:\n"
        summary += f"  Total Tasks: {len(self.tasks)}\n"
        summary += f"  Total Time: {total_time}h / {available_time}h available {fits}\n"
        summary += f"  High Priority: {len(self.getTasksByPriority('high'))}\n"
        summary += f"  Medium Priority: {len(self.getTasksByPriority('medium'))}\n"
        summary += f"  Low Priority: {len(self.getTasksByPriority('low'))}\n"
        
        return summary
    
    def __str__(self) -> str:
        """Return a string representation of the schedule."""
        return f"Schedule with {len(self.tasks)} tasks (Total: {self.getTotalScheduledTime()}h)"

