function Job({job_id, expanded}) {
    return (
        <div>Job {job_id} {expanded ? "T" : "F"}</div>
    );
}

export default Job