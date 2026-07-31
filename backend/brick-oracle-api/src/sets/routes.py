"""API route blueprints for Brick Oracle."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..catalog.repository import list_sets, get_set

sets_bp = Blueprint("sets", __name__, url_prefix="/api/sets")


@sets_bp.route("/", methods=["GET"])
def get_sets():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 12, type=int)
    offset = (page - 1) * page_size
    sets = list_sets(limit=page_size, offset=offset)
    return jsonify([
        {
            "set_num": s.set_num,
            "name": s.name,
            "year": s.year,
            "num_parts": s.num_parts,
            "img_url": s.img_url,
        }
        for s in sets
    ])


@sets_bp.route("/<string:set_num>", methods=["GET"])
def get_set_by_num(set_num: str):
    s = get_set(set_num)
    if s is None:
        return jsonify({"error": "Set not found"}), 404
    return jsonify({
        "set_num": s.set_num,
        "name": s.name,
        "year": s.year,
        "num_parts": s.num_parts,
        "img_url": s.img_url,
        "theme_id": s.theme_id,
    })
