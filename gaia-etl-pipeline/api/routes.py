# api/routes.py

from fastapi import APIRouter, HTTPException, Request, Query

router = APIRouter()

@router.get("/stars/{source_id}")
def get_star_by_id(source_id: int, request: Request):
    """
    Retrieve a star's information by its source_id.

    Args:
        source_id (int): Unique identifier for the star.
        request (Request): FastAPI request object with DB connection.

    Returns:
        dict: Star data including coordinates and magnitude.
    """
    conn = request.app.state.dbconn
    with conn.cursor() as cur:
        cur.execute(
            "SELECT source_id, ra, dec, parallax, phot_g_mean_mag "
            "FROM gaia_source WHERE source_id=%s",
            (source_id,)
        )
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Source not found")

    return {
        "source_id": row[0],
        "ra": row[1],
        "dec": row[2],
        "parallax": row[3],
        "g_mag": row[4],
    }

@router.get("/stars")
def query_stars(
    ra: float = Query(..., description="Right ascension in degrees"),
    dec: float = Query(..., description="Declination in degrees"),
    radius: float = Query(..., description="Search radius in degrees"),
    request: Request = None
):
    """
    Query stars within a radius of a given point using spatial filtering.

    Args:
        ra (float): Right ascension.
        dec (float): Declination.
        radius (float): Radius for spatial search.
        request (Request): FastAPI request with DB connection.

    Returns:
        dict: List of stars and total count.
    """
    conn = request.app.state.dbconn
    with conn.cursor() as cur:
        cur.execute(
            "SELECT source_id, ra, dec, phot_g_mean_mag "
            "FROM gaia_source "
            "WHERE geom IS NOT NULL AND ST_DWithin(geom, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s) "
            "LIMIT 100",
            (ra, dec, radius)
        )
        rows = cur.fetchall()

    return {
        "count": len(rows),
        "results": [
            {"source_id": r[0], "ra": r[1], "dec": r[2], "g_mag": r[3]} for r in rows
        ]
    }
