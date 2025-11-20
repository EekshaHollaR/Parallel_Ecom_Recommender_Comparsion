from flask import Blueprint, jsonify
from rq.job import Job
from ..tasks.worker import redis_conn

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks/<job_id>', methods=['GET'])
def get_task_status(job_id):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception:
        return jsonify({"status": "error", "message": "Job not found"}), 404

    if job.is_finished:
        return jsonify({
            "status": "finished",
            "result": job.result,
            "enqueued_at": job.enqueued_at.isoformat() if job.enqueued_at else None,
            "ended_at": job.ended_at.isoformat() if job.ended_at else None
        })
    elif job.is_failed:
        return jsonify({"status": "failed", "message": job.exc_info}), 500
    else:
        return jsonify({"status": job.get_status()}), 202
