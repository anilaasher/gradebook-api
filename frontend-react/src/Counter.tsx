//useState is the component’s memory. Calling the setter changes it and reruns the component.
//useEffect does outside work after a draw, like fetching from your API, and the dependency list decides when it reruns.
import { useEffect,useState } from "react";

function Counter() {
  const [count, setCount] = useState(100);
 
  useEffect(() => {
    document.title = "Clicked " + count + " times";
  }, [count]);

  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}

export default Counter;