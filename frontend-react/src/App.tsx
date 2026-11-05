
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useEffect, useState } from "react";
import StudentItem from "./StudentItem";
import StudentCard from "./StudentCard";
import { fetchStudents, addStudent, fetchGrades, deleteStudent,addGrade  } from "./api";

function App() {
  // State: values React remembers and redraws the page for
  const [students, setStudents] = useState<string[]>([]);   // all student names
  const [newName, setNewName] = useState("");               // text in the input box
  const [selected, setSelected] = useState<string | null>(null);  // clicked student
  const [grades, setGrades] = useState<number[]>([]);       // grades of the selected student
  const [score, setScore] = useState("");  // text typed in the grade box
const [error, setError] = useState("");  // message shown if saving fails

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
async function handleAddGrade() {
  if (!selected || score === "") return;  // need a selected student and a typed grade
  setError("");                           // clear any old message

  const ok = await addGrade(selected, Number(score));  // Number() turns "85" into 85
  if (!ok) {
    setError("Grade must be a number from 0 to 100");
    return;                               // stop here, so the box keeps what was typed
  }

  setScore("");                            // clear the box
  setGrades(await fetchGrades(selected));  // reload this student's grades
}
  return (
<main className="mx-auto max-w-4xl p-6">
      <h1 className="text-3xl font-bold">Gradebook</h1>

<div className="grid gap-8 md:grid-cols-2">
          {/* Left panel: manage the students */}
      <section >
        <h2 className="mb-3 text-xl font-semibold">Students</h2>

        <div className="mb-4  flex gap-2">
          <Input
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            placeholder="Enter a new student name"
          />
          <Button onClick={handleAddStudent}>Add Student</Button>
        </div>

        <ul className="space-y-2">
          {students.map((name) => (
            <StudentItem key={name} name={name} onSelect={setSelected}   onDelete={handleDeleteStudent}
/>
          ))}
        </ul>
      </section>

      {/* Right panel: the selected student */}
      <section >
        <h2 className="mb-3 text-xl font-semibold">Selected student</h2>
        {selected ? (
  <>
    <StudentCard name={selected} grades={grades} />

<div className="mb-4 flex gap-2">
        <Input
        type="number"
        value={score}
        onChange={(e) => setScore(e.target.value)}
        placeholder="Grade (0-100)"
      />
      <Button onClick={handleAddGrade}>Add Grade</Button>
    </div>

    {/* Show a message only if there is one */}
    {error && <p>{error}</p>}
  </>
) : (
  <p>Click a student to see their grades.</p>
)}
      </section>
    </div>
  </main>
);
}

export default App;