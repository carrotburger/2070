# 2070: RPG/Visual Novel Game  

## Overview  
2070 is a role-playing game (RPG) and visual novel developed using the Pygame framework.  

## Core Architecture  
The game's architecture follows a structured, scene-based design with state-driven interactions:  

```
+---------------------+       +----------------------------+
|       Scene         | ----> | Dialog with Character 1    |
+---------------------+       +----------------------------+
         ^                    +----------------------------+
         |------------------> | Dialog with Character N    | <=====> | Global and Local Consequences |
         |                    +----------------------------+                        ^
         |                    +----------------------------+                        |
         +----------------->  | Dialog with Object N       |                        |
         ^                    +----------------------------+                        |
         |__________________________________________________________________________|
```

### Key Components  
1. **Scene System**  
   - Each game segment is implemented as a dedicated `Scene` (inheriting from the base `Scene` class).  
   - Scenes contain interactive, clickable objects that trigger contextual dialogues.  
   - Scene behavior dynamically adapts based on **local state** (scene-specific conditions) and **global state** (persistent game-wide variables).  

2. **Dialog System**  
   - Clicking objects initiates dialog sessions via classes inheriting from `BaseDialog`.  
   - Dialogs can be responded to both local and global states, enabling branching narratives.  
   - Player choices within dialogs can modify state variables, creating global consequences.  

3. **State Management**  
   - **Local State**: Governs scene-specific conditions (e.g., object availability, NPC disposition).  
   - **Global State**: Tracks cross-scene progress (e.g., story flags, available items).  
   - State changes originate from player decisions and propagate through scenes/dialogs.  

4. **Dialog Implementation**  
   - Dialogs are usually implemented as finite state machines, transitioning between nodes based on player choices.  
   - Each dialog node must ultimately return:  
     - `Text`: Display content for the current state.  
     - `Options`: Interactive choices for the player.  
   - While dialog logic varies per implementation, all sessions adhere to this output contract.  

### Workflow  
1. Player interacts with a clickable object in a `Scene`.  
2. Relevant `BaseDialog` subclass initializes, consuming current state data.  
3. Dialog processes input, updates state variables, and renders dynamic content.  
4. State changes propagate to the scene manager, influencing subsequent scenes and interactions.  

