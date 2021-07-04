import {BrowserRouter as Router, Link, Route} from "react-router-dom"
import About from "./components/About";
import Patients from "./components/Patients";
import Configs from "./components/Configs";
import Jobs from "./components/Jobs";


function App() {
    return (
        <div className="envelope">
            <Router>
                <div className="menu">
                    <Link to="/about" className="link">
                        ABOUT
                    </Link>
                    <Link to="/patients" className="link">
                        PATIENTS
                    </Link>
                    <Link to="/configs" className="link">
                        CONFIGS
                    </Link>
                    <Link to="/jobs" className="link">
                        JOBS
                    </Link>
                </div>

                <div className="content">
                    <Route path="/about" exact>
                        <About/>
                    </Route>
                    <Route path="/patients" exact>
                        <Patients/>
                    </Route>
                    <Route path="/configs" exact>
                        <Configs/>
                    </Route>
                    <Route path="/jobs" exact>
                        <Jobs/>
                    </Route>
                </div>
            </Router>
        </div>
    );
}

export default App;
