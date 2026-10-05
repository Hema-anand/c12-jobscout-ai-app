from app.db.models import Job

SEED_JOBS = [
    Job(
        title="Python Backend Developer",
        company="Northstar Labs",
        location="Bangalore",
        skills="python,fastapi,sql,docker,rest",
        description="Build backend APIs and services using Python and FastAPI.",
    ),
    Job(
        title="AI Application Engineer",
        company="BlueOrbit Systems",
        location="Hyderabad",
        skills="python,llm,rag,fastapi,docker",
        description="Build AI application workflows and integrate LLM services.",
    ),
    Job(
        title="Java Full Stack Developer",
        company="Crescent Tech",
        location="Pune",
        skills="java,spring boot,angular,sql,docker",
        description="Develop enterprise web applications with Spring Boot and Angular.",
    ),
    Job(
        title="Cloud Platform Engineer",
        company="SkyGrid",
        location="Mumbai",
        skills="aws,docker,ecs,iam,terraform",
        description="Build and operate containerized workloads on cloud platforms.",
    ),
    Job(
        title="DevOps Engineer",
        company="OrbitWorks",
        location="Bangalore",
        skills="docker,ci/cd,github actions,kubernetes,aws",
        description="Automate build, test and deployment workflows.",
    ),
    Job(
        title="Data Platform Engineer",
        company="DataSpring",
        location="Chennai",
        skills="python,sql,postgresql,aws,etl",
        description="Build data pipelines and services around PostgreSQL and cloud storage.",
    ),
    Job(
        title="Machine Learning Engineer",
        company="NovaMind",
        location="Hyderabad",
        skills="python,machine learning,pytorch,mlops",
        description="Develop and operationalize machine learning systems.",
    ),
    Job(
        title="Backend Engineer",
        company="Riverstone",
        location="Delhi",
        skills="python,fastapi,postgresql,redis,rest",
        description="Design reliable backend services and APIs.",
    ),
    Job(
        title="Platform Developer",
        company="VertexWorks",
        location="Pune",
        skills="python,docker,linux,aws,postgresql",
        description="Create internal platform services and developer tooling.",
    ),
    Job(
        title="AI Solutions Developer",
        company="InsightForge",
        location="Mumbai",
        skills="python,llm,langchain,fastapi,sql",
        description="Build practical AI solutions and service integrations.",
    ),
]


def seed_jobs(session) -> None:
    existing = session.query(Job).count()
    if existing:
        return
    session.add_all(SEED_JOBS)
    session.commit()
