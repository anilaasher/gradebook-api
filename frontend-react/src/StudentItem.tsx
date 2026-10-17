//the shape of the inputs this component accepts
type StudentItemProps={

    name:String;
};

// Acomponent : a functiont that takes props and retun UI

function StudentItem({name}:StudentItemProps)
{
    return(
        <li>{name} </li>
    );
}

export default StudentItem;