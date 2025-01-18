# PropuestasPeru Backend

This is the backend for the **PropuestasPeru** platform, built using **FastAPI** and following a layered architecture. The backend is responsible for handling user authentication, managing proposals, likes, comments, and providing secure communication between the frontend and the database.

## Key features of the backend:
- **FastAPI Framework:** Fast and efficient API management using **FastAPI**, ensuring high performance and easy scalability.
- **Layered Architecture:** The backend follows a clean and modular design with separation of concerns, making it easy to maintain and scale.
  - **Presentation Layer:** Handles the interaction with the frontend, serving API endpoints.
  - **Business Layer:** Contains the core business logic for proposals, likes, and comments.
  - **Data Access Layer:** Manages interaction with the database, ensuring data consistency and security.
- **User Authentication:** Complete authentication system for user registration, login, and session management.
- **Database Integration:** Integrated with a relational database for storing user data, proposals, likes, and comments.
- **JWT Token Authentication:** Used for securing the user authentication process.

This backend provides a solid foundation for the **PropuestasPeru** platform, ensuring efficient, scalable, and secure interactions between users and the platform.

---

⚙️ **Technologies Used:**
- **FastAPI**
- **JWT Authentication**
- **SQLAlchemy**
- **PostgreSQL**
