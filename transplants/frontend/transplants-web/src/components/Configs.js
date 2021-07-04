import SolverConfig from "./SolverConfig";

function Configs() {
    return (
        <div style={{display: "flex", flexDirection: "row"}}>
            <div style={{width: "50vw"}}>
                Compatible blood group bonus: <br/>
                Incompatible blood group malus: <br/>
                Hla allele compatibility bonus: <br/>
                Max allowed antibody concentration: <br/>
                Forbidden transplants: <br/>
                Min required base score: <br/>
            </div>
            <div style={{width: "20vw"}}>
                <SolverConfig/>
                <SolverConfig/>
                <SolverConfig/>
            </div>
        </div>
    );
}

export default Configs