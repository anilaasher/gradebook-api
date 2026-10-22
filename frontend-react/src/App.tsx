import "./App.css";
import { useEffect, useState } from "react";
import StudentItem from "./StudentItem";
import StudentCard from "./StudentCard";
import { fetchStudents, addStudent, fetchGrades, deleteStudent } from "./api";

function App() {
  // State: values React remembers and redraws the page for
  const [students, setStudents] = useState<string[]>([]);   // all student names
  const [newName, setNewName] = useState("");               // text in the input box
  const [selected, setSelected] = useState<string | null>(null);  // clicked student
  const [grades, setGrades] = useState<number[]>([]);       // grades of the selected student

  // Runs once, when the page first appears: load the student list
  useEffect(() => {
    fetchStudents().then(setStudents);
  }, []);

  useEffect(() => {
  if (!selected) return;  // nobody selected yet
  fetchGrades(selected).then(setGrades);
}, [selected]);

  // Called by the button: save a new student, then reload the list
  async function handleAddStudent() {
  if (!newName) return;  // ignore an empty box
  await addStudent(newName);
  setNewName("");                      // clear the box
  setStudents(await fetchStudents());  // reload the list
}
async function handleDeleteStudent(name: string) {
  // Ask first, because deleting is permanent
  if (!window.confirm("Delete " + name + " and all their grades?")) return;

  await deleteStudent(name);                // remove it through the API
  if (selected === name) setSelected(null); // clear the right panel if they were open
  setStudents(await fetchStudents());       // reload the list
}
  return (
  <main className="app">
    <h1>Gradebook</h1>

    <div className="layout">
      {/* Left panel: manage the students */}
      <section className="panel">
        <h2>Students</h2>

        <div className="add-student">
          <input
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            placeholder="Enter a new student name"
          />
          <button onClick={handleAddStudent}>Add Student</button>
        </div>

        <ul>
          {students.map((name) => (
            <StudentItem key={name} name={name} onSelect={setSelected}   onDelete={handleDeleteStudent}
/>
          ))}
        </ul>
      </section>

      {/* Right panel: the selected student */}
      <section className="panel">
        <h2>Selected student</h2>
        {selected ? (
          <StudentCard name={selected} grades={grades} />
        ) : (
          <p>Click a student to see their grades.</p>
        )}
      </section>
    </div>
  </main>
);
}

export default App;