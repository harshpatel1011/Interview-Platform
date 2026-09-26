# Enterprise Platform Upgrade

We are transforming the platform from a simple scheduling tool into a robust, feature-rich Interview SaaS. 

## Proposed Changes

### 1. Skill-Based Grading Matrix
Instead of a single arbitrary score, interviewers will grade candidates on specific competencies. The final score will be an automatic average.
- **Backend:** Update `Interview` model to include `technical_score`, `communication_score`, and `culture_score`. Remove the generic `score` field and replace it with a computed property or override the save method to auto-calculate the average.
- **UI:** Update the Interviewer's `ScoreForm` in the Video Room to display a beautiful slider-based grading matrix.

### 2. Role-Based Question Bank
Management can curate standard questions to ensure interview consistency.
- **Backend:** Create a new `QuestionBank` model (`role/designation`, `question_text`, `expected_answer`).
- **UI:** Add a "Question Bank" management page for admins. In the Video Room, fetch and display questions dynamically based on the current interview's Designation.

### 3. Interactive Coding Whiteboard
Embed a real code editor into the video room for technical assessments.
- **UI:** Integrate **Monaco Editor** (the engine behind VS Code) directly into `room.html`.
- **Functionality:** Include syntax highlighting for Python, JavaScript, and Java. 
- *Note:* True real-time peer-to-peer collaboration requires WebSockets (Django Channels) which is complex to set up locally. We will start by giving the interviewer and candidate side-by-side editors or a shared frontend state, depending on infrastructure limits.

### 4. Automated Email Notifications
Keep everyone in the loop automatically.
- **Backend:** Connect Django signals (`post_save`) to the `Interview` model.
- **Functionality:** When an interview is created or status changes to Cancelled/Completed, generate a beautiful branded HTML email and dispatch it to both the Candidate and the Interviewer.

### 5. Advanced Analytics Dashboard
Give management a bird's-eye view of hiring velocity.
- **Backend:** Create complex ORM aggregations (pass rates, pipeline drop-offs, interviews per month).
- **UI:** Integrate **Chart.js** into the Management Dashboard to render beautiful, animated dark-mode graphs (e.g., Pipeline Funnel, Interviewer Workload).

## Execution Strategy

Since you selected all 5 massive features, I recommend we tackle them sequentially to ensure absolute quality and stability. 

**My proposed order:**
1. **Phase 1:** Grading Matrix & Question Bank (Core Evaluation Upgrade)
2. **Phase 2:** Coding Whiteboard (Video Room Upgrade)
3. **Phase 3:** Analytics Dashboard (Management Upgrade)
4. **Phase 4:** Email Notifications (Infrastructure Upgrade)

## User Review Required
Does this execution order look good to you? Once you approve, I will immediately begin executing Phase 1 (Grading Matrix & Question Bank)!
