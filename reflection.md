# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
    → I created 4 classes, that being [Owner], [Pet], [Task], [Schedule]. The jobs of [Owner], [Pet] and [Task] is to get the Data/Inputs from the User, then [Schedule] gathers the Infos from those 3 classes and creates a Daily Plan of it, keeping in mind of the Constraints and Factors that affects it.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    → I did made some changes based on the CoPilot's Feedback. One such change is adding a Pet Attribute in [Owner] so that it is able to store the Pets the Owners own and Vise Versa where it adds an Owner Attribute to [Pet] to know who owns it, thereby setting the relationship between the Owner and the Pet.

---
 → Enter the Owner and Pet Information.
 → Add, Edit, and Manage Pet Care Tasks.
 → Generates a Schedule that is automatically based on the Constraints and Priorities.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
    → Some constrains my Schedule considers are the Owner's Available Time, Priority of the Tasks, and Time/Tasks Overlapping with one another. I usually decide which contraints matters the most by how it would work in real life. For example, a dog can't be walking while also being groomed at the same time.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
    → One Tradeoff I found in my Schedule is from the function "if existing.time == task.time:". This allows for simple writing for it's single comparison. But from it, there won't be overlapping of tasks's time. I would say this is reasonable by how let's say that an Owner's Pet has 1 hour walk around 8:00 and a Grooming service at around 8:20. Causing it to be impossible for the Pet to do at the same time.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
