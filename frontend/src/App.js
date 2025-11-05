// src/App.js
import './App.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [editingTaskTitle, setEditingTaskTitle] = useState('');

  const API_URL = 'http://127.0.0.1:5000/tasks';

  // Fetch all tasks from backend
  const fetchTasks = async () => {
    try {
      const response = await axios.get(API_URL);
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      alert('Cannot connect to backend!');
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  // Add a new task
  const addTask = async () => {
    if (!newTaskTitle.trim()) return;
    try {
      const response = await axios.post(API_URL, { title: newTaskTitle });
      setTasks([...tasks, response.data]);
      setNewTaskTitle('');
    } catch (error) {
      console.error('Error adding task:', error);
    }
  };

  // Delete a task
  const deleteTask = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  // Start editing a task
  const startEditing = (task) => {
    setEditingTaskId(task.id);
    setEditingTaskTitle(task.title);
  };

  // Save edited task
  const saveTask = async (id) => {
    try {
      const response = await axios.put(`${API_URL}/${id}`, { title: editingTaskTitle });
      setTasks(tasks.map(task => (task.id === id ? response.data : task)));
      setEditingTaskId(null);
      setEditingTaskTitle('');
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  // Cancel editing
  const cancelEditing = () => {
    setEditingTaskId(null);
    setEditingTaskTitle('');
  };

  return (
    <div className="App">
      <h1>📝 Task Manager</h1>

      <div className="add-task">
        <input
          type="text"
          placeholder="Enter task title"
          value={newTaskTitle}
          onChange={(e) => setNewTaskTitle(e.target.value)}
        />
        <button onClick={addTask}>Add Task</button>
      </div>

      <ul className="task-list">
        {tasks.map((task) => (
          <li key={task.id}>
            {editingTaskId === task.id ? (
              <>
                <input
                  type="text"
                  value={editingTaskTitle}
                  onChange={(e) => setEditingTaskTitle(e.target.value)}
                />
                <button onClick={() => saveTask(task.id)}>💾 Save</button>
                <button onClick={cancelEditing}>❌ Cancel</button>
              </>
            ) : (
              <>
                <span>{task.title}</span>
                <button onClick={() => startEditing(task)}>✏️ Edit</button>
                <button onClick={() => deleteTask(task.id)}>🗑️ Delete</button>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
