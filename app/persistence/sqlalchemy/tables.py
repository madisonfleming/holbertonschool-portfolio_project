from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    Date,
    DateTime,
    Enum,
    MetaData,
    ForeignKey,
)

# this is the container that stores our table definitions
metadata = MetaData()

# <--- CHILDREN --->
children = Table(
    "Child",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("name", String(100), nullable=False),
    Column("date_of_birth", Date, nullable=False),
    Column("avatar_url", String(255)),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
)

# <--- BOOKS --->
books = Table(
    "Book",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("external_id", String(100)),
    Column("source", String(50)),
    Column("title", String(255), nullable=False),
    Column("author", String(100)),
    Column("cover_url", String(255)),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
)

# <--- READING SESSIONS --->
reading_sessions = Table(
    "ReadingSession",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("child_id", String(36), ForeignKey("Child.id"), nullable=False),
    Column("external_id", String(100), nullable=False),
    Column("book_id", String(36), ForeignKey("Book.id"), nullable=False),
    Column("title", String(255), nullable=False),
    Column("cover_url", String(255)),
    Column("logged_at", DateTime, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
)

# <--- USERS --->
users = Table(
    "User",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("name", String(100), nullable=False),
    Column("email", String(255), nullable=False),
    Column("role", Enum("standard", "admin"), nullable=False, default="standard"),
    Column("firebase_uid", String(255), unique=True, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
)

# <--- RELATIONSHIPS --->
relationships = Table(
    "Relationship",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("user_id", String(36), ForeignKey("User.id"), nullable=False),
    Column("child_id", String(36), ForeignKey("Child.id"), nullable=False),
    Column("role", Enum("primary", "secondary"), nullable=False),
    Column("relationship_type", String(100)),
    Column("invited_by", String(100)),
    Column("acceptance_status", String(100)),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
)

# <--- MILESTONES --->
milestone_types = Table(
    "MilestoneType",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("name", String(100), nullable=False),
    Column("subject", String(100)),
    Column("type", String(100), nullable=False),
    Column("threshold", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
)

milestone_completions = Table(
    "MilestoneCompletion",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("child_id", String(36), ForeignKey("Child.id"), nullable=False),
    Column("milestone_id", String(36), ForeignKey("MilestoneType.id"), nullable=False),
    Column("description", String(255)),
    Column("completed_at", DateTime, nullable=False),
    Column("reward_generated_at", DateTime),
    Column("reward_url", String(255)),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
)
