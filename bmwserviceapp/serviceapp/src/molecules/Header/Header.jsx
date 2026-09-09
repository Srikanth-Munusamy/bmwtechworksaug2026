import Logo from "../../atoms/Logo/Logo";
import Banner from "../../atoms/Banner/Banner";

function Header() {
    return (
        <section className="flex h-50 w-full bg-black-500">
            <Logo className="flex w-80 shrink-0 items-center justify-center px-8"/>
            <Banner className="flex w-80 shrink-0 items-center justify-center px-8"/>
        </section>
    )
}

export default Header;