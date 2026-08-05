import Navigation from "./Navigation";
import Footer from "../components/Footer";

function Layout({ children }) {
    return (
        <>
            <Navigation />

            <main>
                {children}
            </main>

            <Footer />
        </>
    );
}

export default Layout;