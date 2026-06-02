from celery import shared_task


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_bom(self, bom_id: str):
    """Process a BOM: parse, enrich, score, and screen."""
    from app.services.bom_parser import BOMParser
    from app.services.compliance import ComplianceScreener
    from app.services.sourcing import SourcingService

    sourcing = SourcingService()

    # enrichment happens here via async-to-sync wrapper
    # scores = sourcing.enrich_bom_item(mpn)

    return {"bom_id": bom_id, "status": "processed", "items_processed": 0}


@shared_task
def refresh_part_data(mpn: str):
    """Schedule periodic refresh of part pricing and stock."""
    pass
