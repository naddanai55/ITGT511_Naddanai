# Welcome to ITGT511_Naddanai

This repository is for the **ITGT511: Algorithms and AI for Computer Games**

---

### Overview Video:  
Here is a video showcasing all my work for the ITGT511: AI for Computer Games

[Click here to watch the video](https://www.youtube.com/watch?v=PtTs8VlTrkg)

---

### **Pygame Agent**  
**Features:**
1. **Multiple Agents:** 5 agents move toward a target.
2. **Interactive Target:** Players can move the target by clicking the mouse.

**Value:**

   **- Foundational in Pygame programming.**  

![Pygame Agent](https://github.com/naddanai55/ITGT511_Naddanai/blob/main/Pic/Pygame%20Agent.png)

---

### **Fish Tank Simulation**  
**Features:**
1. **Drop Food:** Left Mouse Button drops a piece of food (only one at a time).
2. **Reset Food:** Press the Spacebar to reset the food.
3. **Fish States:**
   - **Red Fish:** Indicates hunger.
   - **Blue Fish:** Indicates a normal state.
4. **Random State Change:** Every 15 seconds, blue fish will randomly change their state.
5. **Fish Eating:** Red fish turn into blue fish when they eat food.
6. **Avoid Obstacles:** Every fish avoids the skull.

**Value:**

   - Introduces concepts of behavior in Pygame.

![Fish Tank](https://github.com/naddanai55/ITGT511_Naddanai/blob/main/Pic/fish%20tank.png)

---

### **Mining Game**  
**Features:**
1. **Interactive Dirt Block:** A dirt block is placed at the center of the screen for the player to interact with using the Left Mouse Button.
2. **Digging Mechanism:** Players can click on the dirt block to dig it. There is a 50% chance that the block will break with each click.
3. **Mineral Drop Chance:** When the dirt block breaks, there is a 30% chance it will drop a mineral.
4. **Mineral Types:**  
   - **Gold**
   - **Silver**
   - **Diamond**
5. **Guaranteed Mineral Drop:** If the player fails to receive a mineral after three consecutive digs, the fourth dig will guarantee a mineral drop.

**Value:**

   - Implementing game mechanics design and random probability systems.  

![Mining Game](https://github.com/naddanai55/ITGT511_Naddanai/blob/main/Pic/mining_game.png)

---

### **FSM Zombie Behavior**  
**Features:**
**State Transitions:**
 - **Idle:** The zombie walks around randomly. It transitions to chase when it detects the target (mouse position) in its sight.
 - **Chase:** When the zombie detects the target (mouse position), it will start running toward the target.
 - **Attack:** Once the zombie gets close enough to the target (within attack range), it enters the attack state.
 - **Eat:** After attacking, if the zombie is positioned atop the target (mouse position), it transitions into the eating state and simulates eating.

**Value:**

   - Implementing a Finite State Machine in Pygame. 

![Zombie Behavior](https://github.com/naddanai55/ITGT511_Naddanai/blob/main/Pic/fsm%20pic.png)

---

### **Path Finding Algorithm**  
**Features:**
1. **Graph Traversal Visualization:** Demonstrates various pathfinding algorithms with live drawing.
2. **Algorithm Colors:**
   - **Red:** Depth-First Search
   - **Blue:** Breadth-First Search
   - **Black:** Dijkstra’s Algorithm
3. **Goal Node:** The goal node is marked in green on the grid.

**Value:**

   - Implementing pathfinding algorithms to understand the differences between search techniques. 

![Path Finding](https://github.com/naddanai55/ITGT511_Naddanai/blob/main/Pic/path%20pic.png)

---
