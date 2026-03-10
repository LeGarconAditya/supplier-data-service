import pytest
from app.main import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'supplier-data-service'


def test_get_all_suppliers(client):
    response = client.get('/api/suppliers')
    assert response.status_code == 200
    data = response.get_json()
    assert data['count'] >= 1
    assert 'suppliers' in data


def test_get_supplier_by_id(client):
    response = client.get('/api/suppliers/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert 'name' in data


def test_get_supplier_not_found(client):
    response = client.get('/api/suppliers/999')
    assert response.status_code == 404


def test_create_supplier(client):
    new_supplier = {
        "name": "Test Supplier",
        "category": "Testing",
        "country": "India",
        "status": "Active",
        "trust_score": 85.0
    }
    response = client.post('/api/suppliers',
                           json=new_supplier,
                           content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Test Supplier'


def test_get_active_suppliers(client):
    response = client.get('/api/suppliers/active')
    assert response.status_code == 200
    data = response.get_json()
    for supplier in data['suppliers']:
        assert supplier['status'] == 'Active'
