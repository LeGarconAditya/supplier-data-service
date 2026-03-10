from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__)

# In-memory supplier data (simulating MDM golden records)
suppliers = [
    {
        "id": 1,
        "name": "Acme Corporation",
        "category": "Raw Materials",
        "country": "India",
        "status": "Active",
        "trust_score": 95.5
    },
    {
        "id": 2,
        "name": "Global Tech Supplies",
        "category": "Electronics",
        "country": "USA",
        "status": "Active",
        "trust_score": 88.2
    },
    {
        "id": 3,
        "name": "Eastern Logistics",
        "category": "Logistics",
        "country": "Singapore",
        "status": "Inactive",
        "trust_score": 72.0
    }
]


@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "supplier-data-service",
        "version": "1.0.0"
    })


@api_bp.route('/api/suppliers', methods=['GET'])
def get_all_suppliers():
    return jsonify({
        "count": len(suppliers),
        "suppliers": suppliers
    })


@api_bp.route('/api/suppliers/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = next((s for s in suppliers if s["id"] == supplier_id), None)
    if supplier:
        return jsonify(supplier)
    return jsonify({"error": "Supplier not found"}), 404


@api_bp.route('/api/suppliers', methods=['POST'])
def create_supplier():
    data = request.get_json()
    new_supplier = {
        "id": len(suppliers) + 1,
        "name": data.get("name"),
        "category": data.get("category"),
        "country": data.get("country"),
        "status": data.get("status", "Active"),
        "trust_score": data.get("trust_score", 0.0)
    }
    suppliers.append(new_supplier)
    return jsonify(new_supplier), 201


@api_bp.route('/api/suppliers/active', methods=['GET'])
def get_active_suppliers():
    active = [s for s in suppliers if s["status"] == "Active"]
    return jsonify({
        "count": len(active),
        "suppliers": active
    })
