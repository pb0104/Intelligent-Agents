

## **LIBRARY ROBOT**

**Author**

**Name:** Pranshul Bhatnagar
**NetID:** PB251
---

**Scenario:**

A robot in a library is tasked with organizing books and fetching requested books for users. Books can be on carts, shelves, or held by the robot. Users may request books, and the robot must fetch and deliver them. Shelves have limited space, so planning the order of reshelving is necessary.

**Entities/Objects in the Domain:**

* **Books** (b1, b2, …)
* **Shelves** (s1, s2, …)
* **Carts** (c1, …)
* **Users** (u1, u2, …)
* **Robot**

**Robot’s Goal:**

* Ensure all returned books are placed on shelves
* Deliver requested books to users

**Why Planning is Needed:**

* The robot cannot just act reflexively:

  * The robot cannot put a book on a shelf if it is full
  * The robot cannot deliver a book before picking it, must fetch before delivering to user
  * It needs to decide the order of actions (pick/move/deliver) to avoid conflicts
  
Therefore, Reflex actions are insufficient because the state changes over time and actions have preconditions



## **STRIPS Formalization**

### **Predicates / Fluents**

* `At(book, location)` → book is at a location (shelf, cart or robot)
* `Held(robot, book)` → robot is holding the book
* `ShelfAvailable(shelf)` → shelf has space
* `Request(book, user)` → user requested this book
* `Delivered(book, user)` → book delivered to user
* `OnCart(book, cart)` → book is on a cart



### **Action Schemas**

1. **Pick(book, location)**

   * **Preconditions:** `At(book, location)`, `RobotEmpty()`
   * **Add:** `Held(robot, book)`
   * **Delete:** `At(book, location)`, `RobotEmpty()`

2. **PlaceOnShelf(book, shelf)**

   * **Preconditions:** `Held(robot, book)`, `ShelfAvailable(shelf)`
   * **Add:** `At(book, shelf)`
   * **Delete:** `Held(robot, book)`


3. **FetchForUser(book, user)**

   * **Preconditions:** `At(book, shelf)`, `Request(book, user)`, `RobotEmpty()`
   * **Add:** `Held(robot, book)`
   * **Delete:** `At(book, shelf)`, `RobotEmpty()`

4. **Deliver(book, user)**

   * **Preconditions:** `Held(robot, book)`, `Request(book, user)`
   * **Add:** `Delivered(book, user)`
   * **Delete:** `Held(robot, book)`, `Request(book, user)`



## **Example Problem Instance**

Lets say we have a library robot that needs to organize returned books and deliver requested books to users. Let’s go through the problem step by step.


**Initial State:**

* `At(b1, returned_cart)`
* `At(b2, returned_cart)`
* `ShelfAvailable(s1)`
* `ShelfAvailable(s2)`
* `Request(b3, u1)`
* `At(b3, s1)`
* `RobotEmpty()`

b1 and b2 are on the returned cart i.e., these are books that have ben returned and neds to be placed on shelves. b3 is on shelf S1 and this book is requested by user u1, so it needs to be delivered. Sheves s1 and s2 both have space for one book each. The robot is not holding any book at the start. user u1 has requested book b3.

**Goal State:**

* `At(b1, s1)`
* `At(b2, s2)`
* `Delivered(b3, u1)`



The robot's goal is to complete both organisation and delivery tasks i.e., b1 should be on s1,  b2 should be on s2 and b3 should be delivered to u1



---

