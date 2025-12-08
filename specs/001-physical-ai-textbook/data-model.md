# Data Model: Physical AI & Humanoid Robotics Textbook

## Entities

### Textbook Chapter
- **name**: String - Title of the chapter
- **number**: Integer - Chapter sequence number (1-4)
- **overview**: String - Brief description of chapter content
- **sections**: Array of Section - Collection of sections within the chapter
- **learningObjectives**: Array of String - Educational goals for the chapter
- **summary**: String - Chapter conclusion and key takeaways
- **prerequisites**: Array of String - Knowledge required before reading
- **relatedChapters**: Array of Integer - Chapters that build on or relate to this one

### Section
- **title**: String - Section heading
- **content**: String - Detailed text content (Markdown format)
- **learningObjectives**: Array of String - Goals specific to this section
- **examples**: Array of String - Real-world examples included
- **figures**: Array of String - References to diagrams or images
- **duration**: Integer - Estimated reading time in minutes

### Technical Concept
- **name**: String - Name of the concept (e.g., "Kinematics", "SLAM", "Reinforcement Learning")
- **definition**: String - Clear explanation of the concept
- **applications**: Array of String - Real-world applications
- **complexityLevel**: String - Beginner, Intermediate, or Advanced
- **relatedConcepts**: Array of String - Other concepts that connect to this one
- **examples**: Array of String - Specific examples of the concept in practice

### Learning Objective
- **description**: String - What the student should be able to do after reading
- **type**: String - Knowledge, Comprehension, Application, Analysis, Synthesis, Evaluation
- **measurable**: Boolean - Whether the objective can be assessed
- **difficulty**: String - Level of difficulty (Basic, Intermediate, Advanced)
- **chapter**: Integer - Which chapter this objective belongs to

### Real-World Example
- **name**: String - Name of the example (e.g., "Boston Dynamics Atlas")
- **description**: String - Detailed description of the example
- **relevance**: String - How the example relates to the chapter content
- **applications**: Array of String - Specific applications demonstrated
- **challenges**: Array of String - Technical challenges addressed
- **chapter**: Integer - Which chapter this example is used in

## Relationships

- **Textbook Chapter** 1 -- * contains * --> * 0..n **Section**
- **Textbook Chapter** 1 -- * has * --> * 1..n **Learning Objective**
- **Section** 1 -- * covers * --> * 0..n **Technical Concept**
- **Textbook Chapter** 1 -- * includes * --> * 0..n **Real-World Example**
- **Learning Objective** 1 -- * relates to * --> * 0..n **Technical Concept**

## Validation Rules

- Each **Textbook Chapter** must have exactly 4-6 **Section** entities
- Each **Textbook Chapter** must have 3-5 **Learning Objective** entities
- Each **Section** must have a non-empty **content** field
- Each **Learning Objective** must be measurable
- Each **Technical Concept** must have a clear **definition**
- Chapter **number** must be between 1 and 4
- **complexityLevel** must be one of: "Beginner", "Intermediate", "Advanced"
- **duration** for sections should be between 10 and 60 minutes

## State Transitions

- **Textbook Chapter**: Draft → Review → Final → Published
- **Section**: Created → In Review → Approved → Integrated
- **Learning Objective**: Proposed → Refined → Validated → Implemented