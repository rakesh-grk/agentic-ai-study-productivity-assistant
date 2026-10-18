import pytest
from pathlib import Path
from memory.manager import MemoryManager

@pytest.fixture
def temp_memory(tmp_path: Path):
    db_file = tmp_path / "test_memory.db"
    return MemoryManager(db_path=db_file)

def test_save_and_retrieve_memory(temp_memory: MemoryManager):
    mem_id = temp_memory.save_task_memory(
        goal="Study Neural Networks",
        summary="Completed 5-day schedule on backpropagation and transformers.",
        tags="deep_learning",
        details={"score": 0.95}
    )
    assert mem_id > 0
    records = temp_memory.get_all_memories()
    assert len(records) == 1
    assert records[0].goal == "Study Neural Networks"
    assert records[0].tags == "deep_learning"

def test_search_memory(temp_memory: MemoryManager):
    temp_memory.save_task_memory("Learn Python Generators", "Summary of yield statement", "python")
    temp_memory.save_task_memory("Learn React Hooks", "Summary of useState", "frontend")
    
    results = temp_memory.search_memories("Generators")
    assert len(results) == 1
    assert "Python" in results[0].goal

def test_delete_memory(temp_memory: MemoryManager):
    id1 = temp_memory.save_task_memory("Task 1", "Summary 1")
    id2 = temp_memory.save_task_memory("Task 2", "Summary 2")
    
    assert temp_memory.delete_memory(id1) is True
    records = temp_memory.get_all_memories()
    assert len(records) == 1
    assert records[0].id == id2

def test_memory_sanitizes_api_keys(temp_memory: MemoryManager):
    leaked_key = "sk-1234567890abcdef1234567890abcdef"
    mem_id = temp_memory.save_task_memory("Save task with key", f"Found secret key: {leaked_key}")
    records = temp_memory.get_all_memories()
    assert leaked_key not in records[0].summary
    assert "[REDACTED_KEY]" in records[0].summary

def test_preferences_persistence(temp_memory: MemoryManager):
    temp_memory.set_preference("theme", "dark_navy")
    assert temp_memory.get_preference("theme") == "dark_navy"
    temp_memory.set_preference("theme", "light")
    assert temp_memory.get_preference("theme") == "light"
