export default function PromptInput({ value, label, placeholder, onChange, onKeyDown, className }) {
    return (
        <textarea
            type="text"
            value={value}
            placeholder={placeholder}
            onChange={onChange}
            className={className}
            onKeyDown={onKeyDown}
            aria-label={label}
        ></textarea>
    );
}