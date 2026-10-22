type StudentItemProps = {
  name: string;
  onSelect: (name: string) => void;
  onDelete: (name: string) => void;
};

function StudentItem({ name, onSelect, onDelete }: StudentItemProps) {
  return (
    <li onClick={() => onSelect(name)}>
      <span>{name}</span>
      <button
        onClick={(e) => {
          e.stopPropagation(); // don't also select the row
          onDelete(name);
        }}
      >
        Delete
      </button>
    </li>
  );
}

export default StudentItem;