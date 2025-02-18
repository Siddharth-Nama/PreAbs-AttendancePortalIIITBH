# 📚 PreAbs :- Attendance Portal For IIIT Bhagalpur

Check out live Website :- [**Live Demo**](https://siddharthattendanceportal.pythonanywhere.com)  
This **Attendance Website** is a robust and efficient platform designed specifically for **IIIT Bhagalpur**. It provides a streamlined system for managing attendance, enabling teachers to generate **6-digit unique codes** for classes and allowing students to mark their attendance using these codes. The app ensures accuracy, transparency, and simplicity for both teachers and students. **Role-Based Access Control (RBAC)** is implemented to secure access based on user roles (Student/Teacher).

---

## 🌟 Key Features

- **Role-Based Access Control (RBAC)**: Ensures separate access rights for teachers and students.
- **6-Digit Unique Code Generation**: Teachers can generate shareable codes (via WhatsApp or other platforms) for attendance.
- **Secure User Authentication**: Provides role-specific dashboards and features.
- **Real-Time Attendance Management**: Automatically records and stores attendance securely in the database after teacher approval.
- **User-Friendly Interface**: Intuitive design for seamless navigation across functionalities.

---

## 📁 Project Structure

Here's an overview of the key components of the project:

- **account/**: Handles user authentication and role-based access (Student/Teacher).
- **attendance/**: Manages attendance functionalities, including code generation and validation.
- **templates/**: HTML files for the user interface, including login, dashboard, and attendance pages.
- **static/**: CSS, JavaScript, and image resources for styling and interactivity.
- **media/**: Stores shareable codes and related files.

Each module is modularly designed for scalability and ease of maintenance.

---

## 🛠️ Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript (Bootstrap for responsive design)
- **Database**: SQLite (Default for Django; can be switched to PostgreSQL or MySQL for production)
- **Random Code Library**: Python's built-in `secrets` library for generating secure codes
- **Hosting**: Deployment-ready for platforms supporting Django (e.g., PythonAnywhere)

---

## 🚀 Getting Started

To set up this project locally, follow these steps:

### Prerequisites

- **Python 3.7+**: Make sure Python is installed on your system.
- **Virtual Environment**: Recommended for managing dependencies.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Siddharth-Nama/AttendenceAppForMyCollege.git
   cd AttendenceAppForMyCollege
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # macOS/Linux
   myenv\Scripts\activate     # Windows**
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

The application will be accessible at `http://127.0.0.1:8000`.

---

## 📸 Screenshots

### Login Page
![Login Page](/attendencedjango/login/static/images/loginSS.png)

### Student side Page
![Voting Page](/attendencedjango/students/static/images/studentSS.png)

### Teacher side Page
![Voting Page](/attendencedjango/teacher/static/images/teacherSS.png)

### Code Generation Page
![Admin Dashboard](/attendencedjango/teacher/static/images/CodeGenerationSS.png)

---


## 🛠️ Project Workflow

### Teacher Workflow

1. **Log In**:
   - Teachers log in using their credentials to access the teacher's dashboard.
   
2. **Generate Attendance Code**:
   - Teachers can generate a unique, 6-digit code for each class session. This code is used for students to mark their attendance.

3. **Share Attendance Code**:
   - Once the code is generated, teachers can easily share it via WhatsApp or other communication platforms with students.
   
4. **Monitor Attendance Requests**:
   - After students submit their attendance with the 6-digit code, the teacher can review the list of students who have entered the code.
   
5. **Approve Attendance**:
   - The teacher approves each student's attendance request. Once approved, the attendance is permanently recorded and stored in the database.

### Student Workflow

1. **Log In**:
   - Students log in using their credentials to access the student dashboard.
   
2. **Enter Attendance Code**:
   - On the student dashboard, a field will prompt students to enter the 6-digit code provided by the teacher.

3. **Submit Attendance Request**:
   - After entering the code, students submit their attendance request. This request is sent to the teacher for approval.

4. **Teacher Approval**:
   - The student’s attendance is pending approval until the teacher reviews and approves the request.

5. **View Attendance**:
   - After approval, students can view their attendance history and track their overall attendance records.

---

## 📚 Usage Guide

### Teacher Operations
- **Log In**: Access the teacher dashboard using role-specific credentials.
- **Generate Attendance Code**: Create a unique, 6-digit shareable code for each class session.
- **Share Code**: Share the code with students via WhatsApp or other platforms.
- **View Attendance Records**: Monitor attendance data for all classes and approve or reject attendance requests.

### Student Operations
- **Log In**: Access the student dashboard after authentication.
- **Enter Attendance Code**: Enter the provided code to mark attendance.
- **View Attendance**: Check attendance history and records after teacher approval.

---

<!-- ## 📸 Screenshots

### Login Page
![Login Page](screenshots/login.png)

### Code Generation (Teacher)
![Code Generation](screenshots/code-generation.png)

### Student Dashboard
![Student Dashboard](screenshots/student-dashboard.png)

--- -->

## 🚀 Deployment Guide

1. **Set DEBUG=False**: Configure Django to disable debug mode in production.
2. **SECRET_KEY**: Replace the default secret key with a secure, custom key.
3. **Database**: Use a production-ready database like PostgreSQL.
4. **Static Files**: Run `python manage.py collectstatic` to gather static assets.

---

## 🤝 Contributing

Contributions are welcome! Follow these steps to contribute:

1. **Fork the Repository.**
2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit Your Changes**:
   ```bash
   git commit -m "Add a brief description of your changes"
   ```
4. **Push to the Branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request.**

---

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 👥 Developed By

This project was developed by **[Siddharth Nama](https://www.linkedin.com/in/siddharth-nama-1bb967256/)** with the goal of enhancing attendance management at **IIIT Bhagalpur**.

Website: [Attendance Portal](https://siddharthattendanceportal.pythonanywhere.com)