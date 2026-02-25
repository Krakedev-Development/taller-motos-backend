from typing import List, Tuple

class RepairRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: str | None = None) -> Tuple[List[dict], int]:
        offset = (page - 1) * limit

        repairs_query = self.db_client.table("repairs").select("*", count="exact")
        if search:
            search_pattern = f"%{search}%"
            repairs_query = repairs_query.or_(
                f"order_number.ilike.{search_pattern},"
                f"fault_description.ilike.{search_pattern},"
                f"diagnosis.ilike.{search_pattern}"
            )

        repairs_resp = repairs_query.range(offset, offset + limit - 1).execute()
        repairs = repairs_resp.data or []
        total = repairs_resp.count or 0
        if not repairs:
            return [], total

        id_mechanics = list({r.get("id_mechanic") for r in repairs if r.get("id_mechanic")})
        id_vehicles = list({r.get("id_vehicle") for r in repairs if r.get("id_vehicle")})
        id_created_by = list({r.get("id_created_by") for r in repairs if r.get("id_created_by")})
        id_updated_by = list({r.get("id_updated_by") for r in repairs if r.get("id_updated_by")})
        id_repairs = [r.get("id_repair") for r in repairs if r.get("id_repair")]

        mechanics_map: dict = {}
        vehicles_map: dict = {}
        users_map: dict = {}
        customers_map: dict = {}
        services_map: dict = {rid: [] for rid in id_repairs}

        if id_mechanics:
            m_resp = (
                self.db_client.table("mechanics")
                .select("id_mechanic,name,surname")
                .in_("id_mechanic", id_mechanics)
                .execute()
            )
            for m in (m_resp.data or []):
                mechanics_map[m["id_mechanic"]] = m

        if id_vehicles:
            v_resp = (
                self.db_client.table("vehicles")
                .select("id_vehicle,id_customer,brand,model,license_plate")
                .in_("id_vehicle", id_vehicles)
                .execute()
            )
            for v in (v_resp.data or []):
                vehicles_map[v["id_vehicle"]] = v

            id_customers = list({v.get("id_customer") for v in (v_resp.data or []) if v.get("id_customer")})
            if id_customers:
                c_resp = (
                    self.db_client.table("customers")
                    .select("id_customer,name,surname")
                    .in_("id_customer", id_customers)
                    .execute()
                )
                for c in (c_resp.data or []):
                    customers_map[c["id_customer"]] = c

        user_ids = list(set(id_created_by + id_updated_by)) if (id_created_by or id_updated_by) else []
        if user_ids:
            u_resp = (
                self.db_client.table("users")
                .select("id_user,username")
                .in_("id_user", user_ids)
                .execute()
            )
            for u in (u_resp.data or []):
                users_map[u["id_user"]] = u

        if id_repairs:
            s_resp = (
                self.db_client.table("repair_services")
                .select("*")
                .in_("id_repair", id_repairs)
                .execute()
            )
            for s in (s_resp.data or []):
                rid = s.get("id_repair")
                if rid in services_map:
                    services_map[rid].append(s)
                else:
                    services_map[rid] = [s]

        enriched: List[dict] = []
        for r in repairs:
            id_mech = r.get("id_mechanic")
            id_veh = r.get("id_vehicle")
            id_cb = r.get("id_created_by")
            id_ub = r.get("id_updated_by")
            rid = r.get("id_repair")

            mechanic = mechanics_map.get(id_mech) if id_mech else None
            vehicle = vehicles_map.get(id_veh) if id_veh else None
            created_by = users_map.get(id_cb) if id_cb else None
            updated_by = users_map.get(id_ub) if id_ub else None
            customer = customers_map.get(vehicle.get("id_customer")) if vehicle else None

            enriched.append({
                **r,
                "brand": vehicle.get("brand") if vehicle else None,
                "model": vehicle.get("model") if vehicle else None,
                "license_plate": vehicle.get("license_plate") if vehicle else None,
                "created_by_username": created_by.get("username") if created_by else None,
                "updated_by_username": updated_by.get("username") if updated_by else None,
                "services": services_map.get(rid, []),
                "customer_full_name": (f"{customer.get('name')} {customer.get('surname')}".strip() if customer else None),
                "mechanic_full_name": (f"{mechanic.get('name')} {mechanic.get('surname')}".strip() if mechanic else None),
                "vehicle_brand": vehicle.get("brand") if vehicle else None,
                "vehicle_model": vehicle.get("model") if vehicle else None,
            })

        return enriched, total


