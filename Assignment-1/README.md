

## **LIBRARY ROBOT**



### **Scenario:**

A robot in a library is tasked with organizing books and fetching requested books for users. Books can be on carts, shelves, or held by the robot. Users may request books, and the robot must fetch and deliver them. Shelves have limited space, so planning the order of reshelving is necessary.

### **Entities/Objects in the Domain:**

- **Books**: Individual books requiring management (b₁, b₂, ...)
- **Shelves**: Fixed storage locations within Library (s₁, s₂, ...)
- **Carts**: Mobile storage units for temporary book placement.
- **Users**: Library users who submit book requests (u₁, u₂, ...)
- **Robot**: Autonomous agent executing management tasks


### **Robot’s Goal:**

The robot system maintains two primary objectives:

1. Ensure all returned books are placed on shelves.
2. Deliver requested books to users.

### **Why Planning is Needed:**

The robot cannot just act reflexively:
- The robot cannot put a book on a shelf if it is full
- The robot cannot deliver a book before picking it, must fetch before delivering to user
- It needs to decide the order of actions (pick/move/deliver) to avoid conflicts
  
Therefore, Reflex actions are insufficient because the state changes over time and actions have preconditions


## **STRIPS Formalization**

### **Predicates / Fluents**
The system state is represented using the following predicates:

- `At(book, location)`: Indicates a book's current location (shelf, cart, or robot)
- `Held(robot, book)`: Indicates the robot is currently holding the specified book
- `ShelfAvailable(shelf)`: Indicates the shelf has available capacity
- `Request(book, user)`: Indicates a user has requested the specified book
- `Delivered(book, user)`: Indicates the book has been successfully delivered to the user



### **Action Schemas**

#### 1. Pick(book, location)

Retrieves a book from a specified location.

- **Preconditions**: `At(book, location)`, `RobotEmpty()`
- **Effects**: 
  - Add: `Held(robot, book)`
  - Delete: `At(book, location)`, `RobotEmpty()`

#### 2. PlaceOnShelf(book, shelf)

Places a held book onto an available shelf.

- **Preconditions**: `Held(robot, book)`, `ShelfAvailable(shelf)`
- **Effects**:
  - Add: `At(book, shelf)`
  - Delete: `Held(robot, book)`

#### 3. FetchForUser(book, user)

Retrieves a requested book from a shelf for delivery.

- **Preconditions**: `At(book, shelf)`, `Request(book, user)`, `RobotEmpty()`
- **Effects**:
  - Add: `Held(robot, book)`
  - Delete: `At(book, shelf)`, `RobotEmpty()`

#### 4. Deliver(book, user)

Delivers a held book to the requesting user.

- **Preconditions**: `Held(robot, book)`, `Request(book, user)`
- **Effects**:
  - Add: `Delivered(book, user)`
  - Delete: `Held(robot, book)`, `Request(book, user)`



## **Example Problem Instance**

Let's say we have a library robot that needs to organize returned books and deliver requested books to users. Let’s go through the problem step by step.


### **Initial State:**

```
At(b1, returned_cart)
At(b2, returned_cart)
ShelfAvailable(s1)
ShelfAvailable(s2)
Request(b3, u1)
At(b3, s1)
RobotEmpty()
```

- Books b₁ and b₂ are located on the returned cart and require shelving
- Book b₃ is currently on shelf s₁ and has been requested by user u₁
- Shelves s₁ and s₂ each have capacity for one additional book
- The robot is not currently holding any book

### **Goal State:**

```
At(b1, s1)
At(b2, s2)
Delivered(b3, u1)
```

**Objective:**
- Book b₁ must be placed on shelf s₁
- Book b₂ must be placed on shelf s₂
- Book b₃ must be delivered to user u₁

The robot must successfully complete both organizational tasks (shelving returned books) and service delivery (fulfilling the user request).

---
### **Author**
**Name:** Pranshul Bhatnagar.   
**NetID:** PB251

---

