import {useState} from 'react';
function NameBox(){
    const [text, setText] = useState("");
    const [names,setNames]=useState<string[]>([]); 
    
    return(
        <div>
            <input
             value={text} 
             onChange={(e)=>setText(e.target.value)}
             placeholder="Enter your name"
             />
             <button onClick={() => { setNames([...names, text]); setText(""); }}>
                Add Name
             </button>
             <button onClick={() => setText("")}>Clear Names</button>

             <ul>
                {names.map((name,Index) => (
                    <li key={Index}>{name}</li>
                ))}
             </ul>
        </div>
    );
}
export default NameBox;