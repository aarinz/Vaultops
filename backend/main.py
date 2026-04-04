from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine
import models, schemas
from ai_engine import analyze_risk, analyze_rollback
import random

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="VaultOps API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "VaultOps API running"}

@app.post("/releases/")
def create_release(release: schemas.ReleaseCreate, db: Session = Depends(get_db)):
    ai_result = analyze_risk(release.description)
    
    db_release = models.Release(
        name=release.name,
        description=release.description,
        risk_score=ai_result.get("risk_score", 50),
        regulatory_flags=", ".join(ai_result.get("regulatory_flags", [])),
        cost_of_delay=round(random.uniform(500, 5000), 2),
        ai_reasoning=ai_result.get("reasoning", ""),
        status="pending"
    )
    db.add(db_release)
    db.commit()
    db.refresh(db_release)
    return db_release

@app.get("/releases/")
def get_releases(db: Session = Depends(get_db)):
    return db.query(models.Release).order_by(models.Release.created_at.desc()).all()

@app.get("/releases/{release_id}")
def get_release(release_id: int, db: Session = Depends(get_db)):
    release = db.query(models.Release).filter(models.Release.id == release_id).first()
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    return release

@app.post("/releases/{release_id}/decision")
def ba_decision(release_id: int, decision: schemas.BADecision, db: Session = Depends(get_db)):
    release = db.query(models.Release).filter(models.Release.id == release_id).first()
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    release.status = decision.status
    release.ba_comment = decision.comment
    db.commit()
    db.refresh(release)
    return release

@app.post("/releases/{release_id}/rollback-check")
def rollback_check(release_id: int, metrics: schemas.MetricsCheck, db: Session = Depends(get_db)):
    result = analyze_rollback(metrics.pre_metrics, metrics.post_metrics)
    release = db.query(models.Release).filter(models.Release.id == release_id).first()
    if release and result.get("should_rollback"):
        release.status = "rolled_back"
        db.commit()
    return result

@app.get("/gate/{release_id}")
def pipeline_gate(release_id: int, db: Session = Depends(get_db)):
    release = db.query(models.Release).filter(models.Release.id == release_id).first()
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    return {
        "approved": release.status == "approved",
        "status": release.status,
        "risk_score": release.risk_score
    }