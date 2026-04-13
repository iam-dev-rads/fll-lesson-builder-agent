from agent.graph import content_router

def test_router_logic():
    print("\n--- Testing Graph Router Logic ---")
    
    # Case 1: Continue (No error)
    state_ok = {"error": None, "retry_count": 0}
    assert content_router(state_ok) == "continue"
    print("Continue Path: PASSED")
    
    # Case 2: Retry (Error present, count < 3)
    state_retry = {"error": "Invalid JSON", "retry_count": 1}
    assert content_router(state_retry) == "retry"
    print("Retry Path: PASSED")
    
    # Case 3: Error (Error present, count >= 3)
    state_fail = {"error": "Chronic failure", "retry_count": 3}
    assert content_router(state_fail) == "error"
    print("Error Path: PASSED")

if __name__ == "__main__":
    test_router_logic()
