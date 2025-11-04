import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:5000/tasks";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [editingTask, setEditingTask] = useState(null);

  // Fetch all tasks
  const fetchTasks = async () => {
    try {
      const response = await axios.get(API_URL);
      setTasks(response.data);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  };

  // Add a new task
  const addTask = async () => {
    if (!title.trim()) return alert("Please enter a task title");

    try {
      await axios.post(API_URL, { title });
      setTitle("");
      fetchTasks();
    } catch (error) {
      console.error("Error adding task:", error);
    }
  };

  // Delete a task
  const deleteTask = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      fetchTasks();
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  };

  // Start editing
  const startEdit = (task) => {
    setEditingTask(task);
    setTitle(task.title);
  };

  // Save edited task
  const saveEdit = async () => {
    try {
      await axios.put(`${API_URL}/${editingTask.id}`, { title });
      setEditingTask(null);
      setTitle("");
      fetchTasks();
    } catch (error) {
      console.error("Error editing task:", error);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>📝 Task Manager</h1>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter task title"
      />
      {editingTask ? (
        <button onClick={saveEdit}>💾 Save</button>
      ) : (
        <button onClick={addTask}>➕ Add Task</button>
      )}

      <ul style={{ listStyle: "none", padding: 0, marginTop: "20px" }}>
        {tasks.map((task) => (
          <li key={task.id} style={{ marginBottom: "10px" }}>
            {task.title}
            <button onClick={() => startEdit(task)} style={{ marginLeft: "10px" }}>
              ✏️ Edit
            </button>
            <button onClick={() => deleteTask(task.id)} style={{ marginLeft: "10px" }}>
              🗑️ Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
