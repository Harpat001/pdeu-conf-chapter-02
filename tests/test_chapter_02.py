import audit_agent


def test_prompt_requires_todo_plan_before_file_reads():
    prompt = audit_agent.SYSTEM_PROMPT
    assert "write_todos" in prompt
    assert "3-step audit plan" in prompt


def test_find_contract_locates_gujarat_steel_contract():
    path = audit_agent.find_contract("Gujarat Steel Corp")
    assert path.name == "Gujarat_Steel_Corp_Contract.txt"


def test_read_contract_extracts_penalty_clause():
    text = audit_agent.read_contract("Gujarat Steel Corp")
    assert "5% penalty" in text
    assert "exceeding 7 days" in text
