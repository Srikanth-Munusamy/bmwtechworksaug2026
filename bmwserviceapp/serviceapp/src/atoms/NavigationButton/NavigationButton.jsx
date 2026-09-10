export default function NavigationButton({
  icon: Icon,
  children,
  className = "",
}) {
  return (
    <button
      type="button"
      className={`flex items-center gap-2 whitespace-nowrap text-base text-neutral-600 transition hover:text-black sm:text-lg ${className}`}
    >
      {Icon && <Icon size={23} />}
      {children}
    </button>
  );
}