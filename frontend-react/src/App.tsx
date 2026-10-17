import { useEffect, useState } from "react";
import StudentItem from "./StudentItem";

const API = "http://127.0.0.1:8000";

// Ask the API for the list of student names
async function fetchStudents(): Promise<string[]> {
  const response = await fetch(API + "/students");
  const data = await response.json();
  return data.students;
}

function App() {
  const [newName, setNewName] = useState("");
  // students is the current list; setStudents replaces it and redraws the page
  const [students, setStudents] = useState<string[]>([]);

  // Runs once, when the page first loads
  useEffect(() => {
  fetchStudents().then(setStudents);
}, []);

async function addStudent() {
  if (!newName) return;  // ignore an empty box

  // Send a POST to your API, which saves the student in gradebook.db
  await fetch(API + "/students/" + encodeURIComponent(newName), { method: "POST" });

  setNewName("");                      // clear the box
  setStudents(await fetchStudents());  // reload the list from the database
}

  return (
    <div>
      <h1>Gradebook</h1>
      <input
       value={newName}
       onChange={(e) => setNewName(e.target.value)}
       placeholder="Enter a new student name"
        />
        <button onClick={addStudent}>Add Student</button>
      <ul>
        {students.map(  (name) => ( <StudentItem key={name} name={name}  />)   )}
      </ul>
    </div>
  );
}

export default App;