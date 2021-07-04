import Job from "./Job";

function Jobs() {
    return (
        <div style={{display: "flex", flexDirection: "row"}}>
            <div style={{width: "50vw"}}>
                <Job job_id={1234} expanded={true}/>
            </div>
            <div style={{width: "20vw"}}>
                Patient Set: Form <br/>
                Solver Config: Form <br/>

                <Job job_id={1234} expanded={false}/>
                <Job job_id={1234} expanded={false}/>
                <Job job_id={1234} expanded={false}/>
                <Job job_id={1234} expanded={false}/>
            </div>
        </div>
    );
}

export default Jobs