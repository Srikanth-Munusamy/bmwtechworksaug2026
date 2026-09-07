import httpx

from .config import BACKEND_URL


class BackendAPI:

    def __init__(self):

        self.base_url = (
            BACKEND_URL.rstrip("/")
        )

    def get_job(
        self,
        job_id: str
    ):

        response = httpx.get(
            f"{self.base_url}"
            f"/service-jobs/"
            f"{job_id}",
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    def get_suppliers(
        self,
        part_number: str
    ):

        response = httpx.get(
            f"{self.base_url}"
            f"/parts/"
            f"{part_number}"
            f"/suppliers",
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    def create_purchase_request(
        self,
        payload: dict
    ):

        response = httpx.post(
            f"{self.base_url}"
            f"/purchase-requests",
            json=payload,
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    def create_service_job(
        self,
        payload: dict
    ):

        response = httpx.post(
            f"{self.base_url}"
            f"/service-jobs",
            json=payload,
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    def load_demo_suppliers(
        self
    ):

        response = httpx.post(
            f"{self.base_url}"
            f"/demo/suppliers",
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    def get_purchase_requests(
        self
    ):

        response = httpx.get(
            f"{self.base_url}"
            f"/purchase-requests",
            timeout=20
        )

        response.raise_for_status()

        return response.json()