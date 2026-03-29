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
    → Working on this Project, I used 3 AI Tools. ChatGPT, Claude and CoPilot. I used these 3 because each of them gives different answers to the same questions. When brainstorming, debugging and such in my Project, ChatGPT explains it better but lacks the visual or information of it. Claude implements the work but doesn't show the changes first. CoPilot did it better, it shows the changes before implementing and alright explanation, but I was having problems with the limit usage. Basically, I used those 3 to get different opinions, options and even questions regarding the project.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
    → At the start of the project, I ask AI to build me a UML Diagram/Syntax but I ran into problems. One was the AI doing its own thing, assigning variables, functions, and relationships that doesn't match the structure I wanted. So I tried again and again, improving my prompt to create a proper UML Diagram based on the structue I envisioned first. While I kept trying, I use the feedback or the diagram it provided last chat session to improve my UML. So basically, it was helping make my structure more refine.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
    → When I reached Phase 5: Testing and Verification. I had trouble understanding the instructions. I interpretet that the test functions we had to draft, comes from when we were ask to list 3-5 core behaviors to verify. Anyway, the behaviors I tested included the Sorting Correctness, Recurrence Logic, Conflict Detection, as well as the core behaviors I listed (I put it in Claude to do part 2 of step 1 but I accidently closed the session and lost the list). These tests are important because it ensures that my systems work as it was intended to work. In my experience with coding, sometimes running a file without testing, sometimes ruin the entire program.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
Initially I had a 3/5 confidence that my Schedule Class works correctly. When I tested it with streamlit, I ran into some trouble but later fixed it. Now I'm about 4.5/5 confident it would work by how you can never be to sure it works perfectly. There may be some edge cases that might affect it, which probably like real life factors that affects the task such as missing limbs or disability and such.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    → I'm mostly satisfied with being able to structure a refine UML design, using information from previous prompts.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    → Probably my wording on prompts because sometimes AI would misinterpretet my intention or what I'm trying to do. I feel like my wording is my biggest problem.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    → Never let AI control everthing. If you depend on AI too much, you're not coding.