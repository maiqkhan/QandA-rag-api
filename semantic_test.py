import requests

def test_kubernetes_query():
    response = requests.post("http://localhost:8000/query?q=What+is+Kubernetes?") 
    
    print(response.status_code)
    assert response.status_code == 200
    data = response.json()
    assert "orchestration" in data["answer"].lower(), "Answer should mention orchestration"
    assert "container" in data["answer"].lower(), "Answer should mention container"
    print("Kubernetes Query Test Passed. Answer:", data["answer"])

def test_nextwork_query():
    response = requests.post("http://localhost:8000/query?q=What+is+Nextwork?") 
    
    print(response.status_code)
    assert response.status_code == 200
    data = response.json()
    assert "platform" in data["answer"].lower(), "Answer should mention platform"
    print("Nextwork Query Test Passed. Answer:", data["answer"])


if __name__ == "__main__":
    test_kubernetes_query()
    test_nextwork_query()
    print("All tests passed successfully.")