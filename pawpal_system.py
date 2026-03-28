# Logic Layer where all Backend Classes Lives

from dataclasses import dataclass
from typing import List


class Owner:
    """Represents a pet owner."""
    
    def __init__(self, name: str, timeAvailability: float):
        self.name = name
        self.timeAvailability = timeAvailability
    
    def getName(self) -> str:
        """Get the owner's name."""
        pass
    
    def getTimeAvailability(self) -> float:
        """Get the owner's available time."""
        pass


@dataclass
class Pet:
    """Represents a pet."""
    
    name: str
    type: str
    ownerPreferences: str
    
    def getName(self) -> str:
        """Get the pet's name."""
        pass
    
    def getType(self) -> str:
        """Get the pet's type."""
        pass
    
    def getPreferences(self) -> str:
        """Get the owner's preferences for this pet."""
        pass


@dataclass
class Task:
    """Represents a task for a pet."""
    
    name: str
    duration: float
    priority: str
    
    def getName(self) -> str:
        """Get the task's name."""
        pass
    
    def getDuration(self) -> float:
        """Get the task's duration."""
        pass
    
    def getPriority(self) -> str:
        """Get the task's priority level."""
        pass
    
    def setPriority(self, priority: str) -> None:
        """Set the task's priority level."""
        pass


class Schedule:
    """Represents a schedule containing multiple tasks."""
    
    def __init__(self):
        self.tasks: List[Task] = []
    
    def generateSchedule(self) -> None:
        """Generate an optimized schedule."""
        pass
    
    def addTask(self, task: Task) -> None:
        """Add a task to the schedule."""
        pass
    
    def getTasks(self) -> List[Task]:
        """Get all tasks in the schedule."""
        pass

