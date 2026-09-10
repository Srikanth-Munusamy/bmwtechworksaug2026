export default function IconButton({ icon: Icon, label, onClick,className }) {
  return (
    <button 
    type="button"
    aria-label={label}
    onClick={onClick} 
    className={className}
    label={label}
    >
      <Icon size={24} strokeWidth={2} />
     
    </button>
  );
}