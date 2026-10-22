
import "./StudentCard.css";
// Pick a style name for an average: 70+ good, 50 to 69 ok, below 50 low
function averageClass(average: number): string {
  if (average >= 70) return "average-good";
  if (average >= 50) return "average-ok";
  return "average-low";
}

// Turn an average into a letter: 80+ A, 70+ B, 60+ C, 50+ D, otherwise E
function letterGrade(average: number): string {
  if (average >= 80) return "A";
  if (average >= 70) return "B";
  if (average >= 60) return "C";
  if (average >= 50) return "D";
  return "E";
}
type StudentCardProps = {
  name: string;
  grades: number[];
};

function StudentCard({ name, grades }: StudentCardProps) {
  // Add up all the grades
  let total = 0;
  for (const g of grades) {
    total = total + g;
  }

  // Average, or null if there are no grades (avoids dividing by zero)
  const average = grades.length > 0 ? total / grades.length : null;

  return (
    <div>
      <h3>{name}</h3>
      <p>Grades: {grades.join(", ")}</p>

      <p>
  Average:{" "}
  {average === null ? (
    "No grades yet"
  ) : (
<span className={averageClass(average)}>
  {average.toFixed(1)} ({letterGrade(average)})
</span>  )}
</p>
    </div>
  );
}

export default StudentCard;