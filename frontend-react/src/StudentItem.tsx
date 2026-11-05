import { Button } from "@/components/ui/button";
type StudentItemProps = {
  name: string;
  onSelect: (name: string) => void;
  onDelete: (name: string) => void;
};

function StudentItem({ name, onSelect, onDelete }: StudentItemProps) {
  return (
    <li
  className="flex cursor-pointer items-center justify-between rounded-md border px-3 py-2 hover:bg-muted"
  onClick={() => onSelect(name)}
>
      <span>{name}</span>
      <Button variant="destructive" size="sm" 
        onClick={(e) => {
          e.stopPropagation(); // don't also select the row
          onDelete(name);
        }}
      >
        Delete
      </Button>
    </li>
  );
}

export default StudentItem;