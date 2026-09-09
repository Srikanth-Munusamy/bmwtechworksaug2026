import Logo from "../../atoms/Logo/Logo";
import Banner from "../../atoms/Banner/Banner";

function Header() {
    return (
        <section className="flex h-20 w-full bg-black-500">
            <Logo/>
            <Banner/>
        </section>
    )
}

export default Header;