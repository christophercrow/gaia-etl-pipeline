from fastapi import APIRouter, HTTPException, Request
router = APIRouter()

@router.get("/stars/{source_id}")
def get_star_by_id(source_id: int, request: Request):
    conn = request.app.state.dbconn
    with conn.cursor() as cur:
        cur.execute(
            "SELECT source_id, ra, dec, parallax, phot_g_mean_mag FROM gaia_source WHERE source_id=%s",
            (source_id,)
        )
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"source_id": row[0], "ra": row[1], "dec": row[2], "parallax": row[3], "g_mag": row[4]}

@router.get("/stars")
def query_stars(ra: float, dec: float, radius: float, request: Request):
    conn = request.app.state.dbconn
    with conn.cursor() as cur:
        cur.execute(
            "SELECT source_id, ra, dec, phot_g_mean_mag FROM gaia_source "
            "WHERE geom IS NOT NULL AND ST_DWithin(geom, ST_SetSRID(ST_MakePoint(%s,%s),4326), %s) LIMIT 100",
            (ra, dec, radius)
        )
        rows = cur.fetchall()
    return {"count": len(rows), "results": [{"source_id": r[0], "ra": r[1], "dec": r[2], "g_mag": r[3]} for r in rows]}