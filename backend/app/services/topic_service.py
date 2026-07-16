from sqlalchemy.orm import Session

from app.models.topic import Topic
from app.models.user_topic import UserTopic
from app.schemas.topic import TopicResponse

# (code, name, discipline)
DEFAULT_TOPICS = [
    # Computer Science
    ("cs.AI", "Artificial Intelligence", "Computer Science"),
    ("cs.LG", "Machine Learning", "Computer Science"),
    ("cs.CL", "Computation and Language", "Computer Science"),
    ("cs.CV", "Computer Vision and Pattern Recognition", "Computer Science"),
    ("cs.RO", "Robotics", "Computer Science"),
    ("cs.IR", "Information Retrieval", "Computer Science"),
    ("cs.CR", "Cryptography and Security", "Computer Science"),
    ("cs.DB", "Databases", "Computer Science"),
    ("cs.DC", "Distributed, Parallel, and Cluster Computing", "Computer Science"),
    ("cs.SE", "Software Engineering", "Computer Science"),
    ("cs.NI", "Networking and Internet Architecture", "Computer Science"),
    ("cs.GR", "Graphics", "Computer Science"),
    ("cs.HC", "Human-Computer Interaction", "Computer Science"),
    ("cs.CG", "Computational Geometry", "Computer Science"),
    ("cs.MA", "Multiagent Systems", "Computer Science"),

    # Mathematics
    ("math.AG", "Algebraic Geometry", "Mathematics"),
    ("math.AP", "Analysis of PDEs", "Mathematics"),
    ("math.CO", "Combinatorics", "Mathematics"),
    ("math.NT", "Number Theory", "Mathematics"),
    ("math.PR", "Probability", "Mathematics"),
    ("math.ST", "Statistics Theory (Mathematics)", "Mathematics"),

    # Physics
    ("astro-ph", "Astrophysics", "Physics"),
    ("cond-mat", "Condensed Matter", "Physics"),
    ("gr-qc", "General Relativity and Quantum Cosmology", "Physics"),
    ("hep-ph", "High Energy Physics - Phenomenology", "Physics"),
    ("hep-th", "High Energy Physics - Theory", "Physics"),
    ("nucl-th", "Nuclear Theory", "Physics"),
    ("quant-ph", "Quantum Physics", "Physics"),

    # Statistics
    ("stat.ML", "Machine Learning (Statistics)", "Statistics"),
    ("stat.TH", "Statistics Theory", "Statistics"),
    ("stat.AP", "Statistics Applications", "Statistics"),
    ("stat.CO", "Statistics Computation", "Statistics"),

    # Quantitative Biology
    ("q-bio.BM", "Biomolecules", "Quantitative Biology"),
    ("q-bio.GN", "Genomics", "Quantitative Biology"),
    ("q-bio.NC", "Neurons and Cognition", "Quantitative Biology"),

    # Quantitative Finance
    ("q-fin.CP", "Computational Finance", "Quantitative Finance"),
    ("q-fin.EC", "Economics (Quant Finance)", "Quantitative Finance"),
    ("q-fin.MF", "Mathematical Finance", "Quantitative Finance"),

    # Economics
    ("econ.EM", "Econometrics", "Economics"),

    # Electrical Engineering and Systems Science
    ("eess.AS", "Audio and Speech Processing", "Electrical Engineering and Systems Science"),
    ("eess.IV", "Image and Video Processing", "Electrical Engineering and Systems Science"),
    ("eess.SP", "Signal Processing", "Electrical Engineering and Systems Science"),
    ("eess.SY", "Systems and Control", "Electrical Engineering and Systems Science"),
]


def seed_topics(db: Session) -> None:
    """
    Ensure every topic in DEFAULT_TOPICS exists in the database.
    Existing topics (matched by arxiv_category_code) are left in place with
    their original ID — only their discipline is backfilled if missing —
    so existing user_topics selections are never broken. New topics are
    inserted. Safe to run on every startup.
    """
    existing_topics = {t.arxiv_category_code: t for t in db.query(Topic).all()}

    for code, name, discipline in DEFAULT_TOPICS:
        existing = existing_topics.get(code)
        if existing:
            if existing.discipline != discipline:
                existing.discipline = discipline
            continue

        db.add(Topic(arxiv_category_code=code, name=name, discipline=discipline))

    db.commit()


def get_all_topics(db: Session) -> list[TopicResponse]:
    topics = db.query(Topic).order_by(Topic.discipline, Topic.name).all()
    return [
        TopicResponse(id=t.id, code=t.arxiv_category_code, name=t.name, discipline=t.discipline)
        for t in topics
    ]


def get_user_topics(db: Session, user_id: int) -> list[TopicResponse]:
    topics = (
        db.query(Topic)
        .join(UserTopic, UserTopic.topic_id == Topic.id)
        .filter(UserTopic.user_id == user_id)
        .order_by(Topic.discipline, Topic.name)
        .all()
    )
    return [
        TopicResponse(id=t.id, code=t.arxiv_category_code, name=t.name, discipline=t.discipline)
        for t in topics
    ]


def set_user_topics(db: Session, user_id: int, topic_ids: list[int]) -> None:
    """Replace a user's topic selections with the given list of topic IDs."""
    db.query(UserTopic).filter(UserTopic.user_id == user_id).delete()

    for topic_id in topic_ids:
        db.add(UserTopic(user_id=user_id, topic_id=topic_id))

    db.commit()