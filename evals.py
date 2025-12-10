"""Evaluation framework for testing CFG SQL generation."""
from sql_generator import generate_sql_from_natural_language, load_grammar
from tinybird_client import execute_query
from lark import Lark


def validate_sql_with_grammar(sql: str) -> tuple[bool, str]:
    """
    Validate that the generated SQL conforms to the CFG grammar using Lark.
    
    Returns:
        (is_valid, error_message)
    """
    try:
        grammar_text = load_grammar()
        parser = Lark(grammar_text)
        parser.parse(sql)
        return True, ""
    except Exception as e:
        return False, str(e)


# ============================================================================
# CATEGORY 1: GRAMMAR COMPLIANCE
# Tests that generated SQL conforms to the CFG grammar rules
# ============================================================================

def grammar_compliance_1_simple_select():
    """Test 1: Simple SELECT statement with basic columns."""
    natural_language = "Show me all employee numbers and their monthly income"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        print("✅ Grammar Compliance Test 1 PASSED: Simple SELECT")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Grammar Compliance Test 1 FAILED: {str(e)}")
        return False


def grammar_compliance_2_select_with_where():
    """Test 2: SELECT with WHERE clause."""
    natural_language = "Show employees in the Sales department"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        assert "WHERE" in sql.upper(), "SQL should contain WHERE clause"
        
        print("✅ Grammar Compliance Test 2 PASSED: SELECT with WHERE")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Grammar Compliance Test 2 FAILED: {str(e)}")
        return False


def grammar_compliance_3_select_with_group_by():
    """Test 3: SELECT with GROUP BY clause."""
    natural_language = "Count employees by department"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        assert "GROUP BY" in sql.upper(), "SQL should contain GROUP BY clause"
        
        print("✅ Grammar Compliance Test 3 PASSED: SELECT with GROUP BY")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Grammar Compliance Test 3 FAILED: {str(e)}")
        return False


def grammar_compliance_4_select_with_order_by_limit():
    """Test 4: SELECT with ORDER BY and LIMIT."""
    natural_language = "Show the top 5 employees by monthly income"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        assert "ORDER BY" in sql.upper(), "SQL should contain ORDER BY clause"
        assert "LIMIT" in sql.upper(), "SQL should contain LIMIT clause"
        
        print("✅ Grammar Compliance Test 4 PASSED: SELECT with ORDER BY and LIMIT")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Grammar Compliance Test 4 FAILED: {str(e)}")
        return False


def grammar_compliance_5_complex_multi_clause():
    """Test 5: Complex query with multiple clauses (WHERE, GROUP BY, ORDER BY, LIMIT)."""
    natural_language = "Show the top 3 departments by average monthly income for employees who have left"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        assert "WHERE" in sql.upper(), "SQL should contain WHERE clause"
        assert "GROUP BY" in sql.upper(), "SQL should contain GROUP BY clause"
        assert "ORDER BY" in sql.upper(), "SQL should contain ORDER BY clause"
        assert "LIMIT" in sql.upper(), "SQL should contain LIMIT clause"
        
        print("✅ Grammar Compliance Test 5 PASSED: Complex multi-clause query")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Grammar Compliance Test 5 FAILED: {str(e)}")
        return False


# ============================================================================
# CATEGORY 2: QUERY EXECUTION
# Tests that generated SQL executes successfully against the database
# ============================================================================

def query_execution_1_basic_count():
    """Test 1: Basic count query executes successfully."""
    natural_language = "How many employees are there?"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        results = execute_query(sql)
        
        assert "data" in results, "Results should have data field"
        assert "rows" in results, "Results should have rows field"
        assert results.get("rows", 0) >= 0, "Should return valid row count"
        
        print("✅ Query Execution Test 1 PASSED: Basic count query")
        print(f"   SQL: {sql}")
        print(f"   Rows returned: {results.get('rows', 0)}")
        return True
    except Exception as e:
        print(f"❌ Query Execution Test 1 FAILED: {str(e)}")
        return False


def query_execution_2_aggregation():
    """Test 2: Aggregation query (AVG, SUM, etc.) executes successfully."""
    natural_language = "What is the average monthly income?"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        results = execute_query(sql)
        
        assert "data" in results, "Results should have data field"
        assert results.get("rows", 0) > 0, "Should return at least one row"
        
        print("✅ Query Execution Test 2 PASSED: Aggregation query")
        print(f"   SQL: {sql}")
        print(f"   Rows returned: {results.get('rows', 0)}")
        return True
    except Exception as e:
        print(f"❌ Query Execution Test 2 FAILED: {str(e)}")
        return False


def query_execution_3_filtered_query():
    """Test 3: Filtered query with WHERE clause executes successfully."""
    natural_language = "How many employees are in the Sales department?"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        results = execute_query(sql)
        
        assert "data" in results, "Results should have data field"
        assert "rows" in results, "Results should have rows field"
        
        print("✅ Query Execution Test 3 PASSED: Filtered query")
        print(f"   SQL: {sql}")
        print(f"   Rows returned: {results.get('rows', 0)}")
        return True
    except Exception as e:
        print(f"❌ Query Execution Test 3 FAILED: {str(e)}")
        return False


def query_execution_4_grouped_query():
    """Test 4: Grouped query with GROUP BY executes successfully."""
    natural_language = "What is the average monthly income by department?"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        results = execute_query(sql)
        
        assert "data" in results, "Results should have data field"
        assert results.get("rows", 0) > 0, "Should return at least one row"
        
        print("✅ Query Execution Test 4 PASSED: Grouped query")
        print(f"   SQL: {sql}")
        print(f"   Rows returned: {results.get('rows', 0)}")
        return True
    except Exception as e:
        print(f"❌ Query Execution Test 4 FAILED: {str(e)}")
        return False


def query_execution_5_complex_query():
    """Test 5: Complex query with multiple clauses executes successfully."""
    natural_language = "Show the count of employees by gender who have left the company, ordered by count descending"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        results = execute_query(sql)
        
        assert "data" in results, "Results should have data field"
        assert results.get("rows", 0) > 0, "Should return at least one row"
        
        print("✅ Query Execution Test 5 PASSED: Complex query")
        print(f"   SQL: {sql}")
        print(f"   Rows returned: {results.get('rows', 0)}")
        return True
    except Exception as e:
        print(f"❌ Query Execution Test 5 FAILED: {str(e)}")
        return False


# ============================================================================
# CATEGORY 3: SEMANTIC ACCURACY
# Tests that generated SQL matches the intent of the natural language query
# ============================================================================

def semantic_accuracy_1_correct_columns():
    """Test 1: SQL selects the correct columns mentioned in the query."""
    natural_language = "Show me employee numbers and their monthly income"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        results = execute_query(sql)
        
        # Check that SQL contains the expected columns
        assert "employeenumber" in sql.lower(), "SQL should select employeenumber"
        assert "monthlyincome" in sql.lower(), "SQL should select monthlyincome"
        
        # Check that results contain data
        assert "data" in results, "Results should have data field"
        assert results.get("rows", 0) > 0, "Should return at least one row"
        
        print("✅ Semantic Accuracy Test 1 PASSED: Correct columns selected")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Semantic Accuracy Test 1 FAILED: {str(e)}")
        return False


def semantic_accuracy_2_correct_filtering():
    """Test 2: SQL applies correct filtering conditions."""
    natural_language = "Show employees in the Sales department who have left the company"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        results = execute_query(sql)
        
        # Check that SQL filters by both conditions
        assert "department" in sql.lower(), "SQL should filter by department"
        assert "attrition" in sql.lower(), "SQL should filter by attrition"
        assert "WHERE" in sql.upper(), "SQL should have WHERE clause"
        
        print("✅ Semantic Accuracy Test 2 PASSED: Correct filtering")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Semantic Accuracy Test 2 FAILED: {str(e)}")
        return False


def semantic_accuracy_3_correct_aggregation():
    """Test 3: SQL uses correct aggregation function."""
    natural_language = "What is the average monthly income by department?"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        results = execute_query(sql)
        
        # Check that SQL uses average/avg function
        assert "avg" in sql.lower() or "average" in sql.lower(), "SQL should use average function"
        assert "monthlyincome" in sql.lower(), "SQL should aggregate monthlyincome"
        assert "GROUP BY" in sql.upper(), "SQL should have GROUP BY clause"
        
        print("✅ Semantic Accuracy Test 3 PASSED: Correct aggregation")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Semantic Accuracy Test 3 FAILED: {str(e)}")
        return False


def semantic_accuracy_4_correct_grouping():
    """Test 4: SQL groups by the correct columns."""
    natural_language = "Count employees by gender and department"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        results = execute_query(sql)
        
        # Check that SQL groups by both columns
        assert "GROUP BY" in sql.upper(), "SQL should have GROUP BY clause"
        assert "gender" in sql.lower(), "SQL should group by gender"
        assert "department" in sql.lower(), "SQL should group by department"
        
        print("✅ Semantic Accuracy Test 4 PASSED: Correct grouping")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Semantic Accuracy Test 4 FAILED: {str(e)}")
        return False


def semantic_accuracy_5_correct_ordering():
    """Test 5: SQL orders results correctly."""
    natural_language = "Show the top 10 employees by monthly income in descending order"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        results = execute_query(sql)
        
        # Check that SQL orders by monthly income descending
        assert "ORDER BY" in sql.upper(), "SQL should have ORDER BY clause"
        assert "monthlyincome" in sql.lower(), "SQL should order by monthlyincome"
        assert "DESC" in sql.upper(), "SQL should order descending"
        assert "LIMIT" in sql.upper(), "SQL should have LIMIT clause"
        assert "10" in sql, "SQL should limit to 10"
        
        # Check that results are limited
        assert results.get("rows", 0) <= 10, "Should return at most 10 rows"
        
        print("✅ Semantic Accuracy Test 5 PASSED: Correct ordering")
        print(f"   SQL: {sql}")
        print(f"   Rows returned: {results.get('rows', 0)}")
        return True
    except Exception as e:
        print(f"❌ Semantic Accuracy Test 5 FAILED: {str(e)}")
        return False


# ============================================================================
# Test Runner
# ============================================================================

def run_all_evals():
    """Run all evaluation tests organized by category."""
    print("=" * 70)
    print("Running CFG SQL Generation Evals")
    print("=" * 70)
    print()
    
    categories = [
        ("Grammar Compliance", [
            ("Simple SELECT", grammar_compliance_1_simple_select),
            ("SELECT with WHERE", grammar_compliance_2_select_with_where),
            ("SELECT with GROUP BY", grammar_compliance_3_select_with_group_by),
            ("SELECT with ORDER BY and LIMIT", grammar_compliance_4_select_with_order_by_limit),
            ("Complex multi-clause", grammar_compliance_5_complex_multi_clause),
        ]),
        ("Query Execution", [
            ("Basic count", query_execution_1_basic_count),
            ("Aggregation", query_execution_2_aggregation),
            ("Filtered query", query_execution_3_filtered_query),
            ("Grouped query", query_execution_4_grouped_query),
            ("Complex query", query_execution_5_complex_query),
        ]),
        ("Semantic Accuracy", [
            ("Correct columns", semantic_accuracy_1_correct_columns),
            ("Correct filtering", semantic_accuracy_2_correct_filtering),
            ("Correct aggregation", semantic_accuracy_3_correct_aggregation),
            ("Correct grouping", semantic_accuracy_4_correct_grouping),
            ("Correct ordering", semantic_accuracy_5_correct_ordering),
        ]),
    ]
    
    all_results = []
    
    for category_name, tests in categories:
        print(f"\n{'=' * 70}")
        print(f"CATEGORY: {category_name}")
        print(f"{'=' * 70}")
        print()
        
        category_results = []
        for test_name, test_func in tests:
            print(f"Running: {test_name}")
            try:
                result = test_func()
                category_results.append((test_name, result))
                all_results.append((f"{category_name} - {test_name}", result))
            except Exception as e:
                print(f"❌ {test_name} FAILED with exception: {str(e)}")
                category_results.append((test_name, False))
                all_results.append((f"{category_name} - {test_name}", False))
            print()
        
        # Category summary
        passed = sum(1 for _, result in category_results if result)
        total = len(category_results)
        print(f"Category Summary: {passed}/{total} tests passed")
        print()
    
    # Overall summary
    print("=" * 70)
    print("OVERALL EVALUATION SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in all_results if result)
    total = len(all_results)
    
    for name, result in all_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed ({passed*100//total}%)")
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    run_all_evals()
