// All calls to the FastAPI server live in this file
const API = "http://127.0.0.1:8000";

export async function fetchStudents(): Promise<string[]> {
  const response = await fetch(API + "/students");
  const data = await response.json();
  return data.students;
}

export async function addStudent(name: string): Promise<void> {
  await fetch(API + "/students/" + encodeURIComponent(name), { method: "POST" });
}

export async function fetchGrades(name: string): Promise<number[]> {
  const response = await fetch(API + "/students/" + encodeURIComponent(name));
  const data = await response.json();
  return data.grades;
}
// Ask the API to delete a student (and their grades)
export async function deleteStudent(name: string): Promise<void> {
  await fetch(API + "/students/" + encodeURIComponent(name), { method: "DELETE" });
}
// Save a grade for a student. Returns false if the API rejects it (e.g. 150).
export async function addGrade(name: string, score: number): Promise<boolean> {
  const response = await fetch(
    API + "/students/" + encodeURIComponent(name) + "/grades?score=" + score,
    { method: "POST" }
  );
  return response.ok;
}