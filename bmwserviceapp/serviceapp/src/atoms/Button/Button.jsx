import { ArrowUp } from "lucide-react";

export default function Button({ disabled, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      aria-label="Send message"
      className="grid h-14 w-14 place-items-center rounded-full bg-blue-200 text-white transition hover:-translate-y-0.5 hover:bg-blue-400 disabled:cursor-default disabled:opacity-70"
    >
      <ArrowUp size={29} strokeWidth={2.5} />
    </button>
  );
}