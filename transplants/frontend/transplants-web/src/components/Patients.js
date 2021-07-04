import Patient from "./Patient";
import PatientSet from "./PatientSet";

function Patients() {
    return (
        <div style={{display: "flex", flexDirection: "column"}}>
            <div style={{height: "7vh"}}>
                <button>Select All</button>
                <button>Deselect All</button>
                <button>Add Donor</button>
                <button>Add Recipient</button>
                <button>Create Patient Set</button>
            </div>
            <div style={{display: "flex", flexDirection: "row"}}>
                <div style={{width: "50vw"}}>
                    <div>
                        <div>
                            <Patient/>
                        </div>
                        <div>
                            <Patient/>
                            <Patient/>
                        </div>
                    </div>
                </div>
                <div style={{width: "20vw", height: "100vh"}}>
                    <PatientSet/>
                    <PatientSet/>
                    <PatientSet/>
                </div>
            </div>
        </div>
    );
}

export default Patients