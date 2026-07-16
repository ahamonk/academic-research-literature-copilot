from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.cluster import ClusterPaperResponse
from app.services.clustering_service import get_clustered_papers_with_coordinates

router = APIRouter(prefix="/clusters", tags=["Clusters"])


@router.get("", response_model=list[ClusterPaperResponse])
def get_clusters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_clustered_papers_with_coordinates(db)