from flask import Blueprint, request, current_app
from ..utils.timing import measure_latency
from ..utils.schemas import success_response, error_response

price_compare_bp = Blueprint('price_compare', __name__)

@price_compare_bp.route('/compare_price', methods=['GET'])
@measure_latency
def compare_price():
    product_name = request.args.get('product')
    
    if not product_name:
        return error_response("Missing product parameter")
        
    scraper = current_app.config.get('SCRAPER')
    
    if not scraper:
        return error_response("Scraper service unavailable", 503)
        
    # Check for async mode
    mode = request.args.get('mode')
    if mode == 'async':
        from ..tasks.worker import q, async_compare_price
        job = q.enqueue(async_compare_price, product_name)
        return success_response({
            "job_id": job.get_id(),
            "status_url": f"/tasks/{job.get_id()}"
        }, message="Job enqueued")

    try:
        # This is a blocking call in the simple version
        # For heavy loads, we'd use the background task (to be implemented)
        data = scraper.scrape_all(product_name)
        return success_response(data)
        
    except Exception as e:
        return error_response(str(e), 500)
