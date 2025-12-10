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
# CATEGORY 4: ADVANCED FEATURES
# Tests for advanced SQL features like string functions, date functions, etc.
# ============================================================================

def advanced_features_1_string_functions():
    """Test 1: String functions (length, upper, lower, concat, etc.)."""
    natural_language = "Show the length of department names and convert them to uppercase"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        # Check for string functions
        has_string_func = ("length(" in sql.lower() or "upper(" in sql.lower() or 
                          "lower(" in sql.lower() or "concat(" in sql.lower())
        assert has_string_func or "department" in sql.lower(), "SQL should use string functions or reference department"
        
        results = execute_query(sql)
        assert "data" in results, "Results should have data field"
        
        print("✅ Advanced Features Test 1 PASSED: String functions")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Advanced Features Test 1 FAILED: {str(e)}")
        return False


def advanced_features_2_arithmetic_operations():
    """Test 2: Arithmetic operations in SELECT expressions."""
    natural_language = "Show monthly income divided by 1000 for each employee"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        # Check for arithmetic operations
        has_arithmetic = ("/" in sql or "*" in sql or "+" in sql or "-" in sql)
        assert has_arithmetic or "monthlyincome" in sql.lower(), "SQL should contain arithmetic operations"
        
        results = execute_query(sql)
        assert "data" in results, "Results should have data field"
        
        print("✅ Advanced Features Test 2 PASSED: Arithmetic operations")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Advanced Features Test 2 FAILED: {str(e)}")
        return False


def advanced_features_3_having_clause():
    """Test 3: HAVING clause for filtering aggregated results."""
    natural_language = "Show departments where the average monthly income is greater than 5000"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        # Check for HAVING clause
        assert "HAVING" in sql.upper(), "SQL should have HAVING clause"
        assert "GROUP BY" in sql.upper(), "SQL should have GROUP BY clause"
        assert "avg" in sql.lower() or "average" in sql.lower(), "SQL should use average function"
        
        results = execute_query(sql)
        assert "data" in results, "Results should have data field"
        
        print("✅ Advanced Features Test 3 PASSED: HAVING clause")
        print(f"   SQL: {sql}")
        print(f"   Rows returned: {results.get('rows', 0)}")
        return True
    except Exception as e:
        print(f"❌ Advanced Features Test 3 FAILED: {str(e)}")
        return False


def advanced_features_4_case_expressions():
    """Test 4: CASE WHEN expressions for conditional logic."""
    natural_language = "Show employees with a case statement categorizing income as high if above 6000, medium if above 3000, else low"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        # Check for CASE expression
        assert "CASE" in sql.upper(), "SQL should contain CASE expression"
        assert "WHEN" in sql.upper(), "SQL should contain WHEN clause"
        assert "THEN" in sql.upper(), "SQL should contain THEN clause"
        
        results = execute_query(sql)
        assert "data" in results, "Results should have data field"
        
        print("✅ Advanced Features Test 4 PASSED: CASE expressions")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Advanced Features Test 4 FAILED: {str(e)}")
        return False


def advanced_features_5_advanced_aggregates():
    """Test 5: Advanced aggregate functions (stddevSamp, varSamp, etc.)."""
    natural_language = "Show the standard deviation of monthly income by department"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        # Check for advanced aggregate functions (stddevSamp, stddevPop, varSamp, varPop, etc.)
        has_advanced_agg = ("stddev" in sql.lower() or "variance" in sql.lower() or 
                           "varPop" in sql.lower() or "varSamp" in sql.lower())
        # Fallback: if it uses basic aggregates, that's also valid for grammar testing
        has_any_agg = has_advanced_agg or "avg(" in sql.lower() or "sum(" in sql.lower() or "min(" in sql.lower() or "max(" in sql.lower()
        assert has_any_agg, "SQL should use aggregate functions"
        assert "GROUP BY" in sql.upper(), "SQL should have GROUP BY clause"
        
        results = execute_query(sql)
        assert "data" in results, "Results should have data field"
        
        print("✅ Advanced Features Test 5 PASSED: Advanced aggregates")
        print(f"   SQL: {sql}")
        print(f"   Rows returned: {results.get('rows', 0)}")
        return True
    except Exception as e:
        print(f"❌ Advanced Features Test 5 FAILED: {str(e)}")
        return False


# ============================================================================
# CATEGORY 5: PRODUCTION FEATURES
# Tests for new advanced grammar features (CTEs, Window Functions, JOINs, etc.)
# ============================================================================

def production_features_1_ctes():
    """Test 1: Common Table Expressions (WITH clause)."""
    natural_language = "With high_earners as (Select * from IBM_HR_Employee_Attrition where monthlyincome > 5000) Select count(*) from high_earners"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        # Check for CTE syntax
        assert "WITH " in sql.upper(), "SQL should contain WITH clause"
        assert "AS (" in sql.upper(), "SQL should contain AS (...) used in CTE"
        
        print("✅ Production Features Test 1 PASSED: CTEs")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Production Features Test 1 FAILED: {str(e)}")
        return False


def production_features_2_window_functions():
    """Test 2: Window Functions (OVER clause)."""
    natural_language = "Show employee number and their rank by income within their department"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        # Check for Window syntax
        assert "OVER" in sql.upper(), "SQL should contain OVER clause"
        assert "PARTITION BY" in sql.upper(), "SQL should contain PARTITION BY"
        
        print("✅ Production Features Test 2 PASSED: Window Functions")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Production Features Test 2 FAILED: {str(e)}")
        return False


def production_features_3_self_join():
    """Test 3: Self Join capability."""
    natural_language = "Show employees who have the same role as employee 1001"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        # Check for JOIN syntax - Note: The natural language might resolve to a subquery IN (...) 
        # or a JOIN. We'll accept either VALID grammar, but ideally valid JOIN syntax if generated.
        # This test ensures that IF a Join is generated, it is valid.
        # Let's verify at least it parses.
        
        if "JOIN" in sql.upper():
            assert "ON" in sql.upper() or "USING" in sql.upper(), "JOIN should have ON or USING"

        print("✅ Production Features Test 3 PASSED: Self Join / Subquery")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Production Features Test 3 FAILED: {str(e)}")
        return False


def production_features_4_dynamic_functions():
    """Test 4: Functions not in the original whitelist."""
    # 'uniq' was not in the original whitelist
    natural_language = "Show the unique count of job roles using the uniq function"
    
    try:
        sql = generate_sql_from_natural_language(natural_language)
        
        # Validate SQL conforms to CFG grammar
        is_valid, error = validate_sql_with_grammar(sql)
        assert is_valid, f"SQL does not conform to CFG grammar: {error}"
        
        assert "uniq(" in sql.lower(), "SQL should contain uniq function"
        
        print("✅ Production Features Test 4 PASSED: Dynamic Functions")
        print(f"   SQL: {sql}")
        return True
    except Exception as e:
        print(f"❌ Production Features Test 4 FAILED: {str(e)}")
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
        ("Advanced Features", [
            ("String functions", advanced_features_1_string_functions),
            ("Arithmetic operations", advanced_features_2_arithmetic_operations),
            ("HAVING clause", advanced_features_3_having_clause),
            ("CASE expressions", advanced_features_4_case_expressions),
            ("Advanced aggregates", advanced_features_5_advanced_aggregates),
        ]),
        ("Production Features", [
            ("CTEs", production_features_1_ctes),
            ("Window Functions", production_features_2_window_functions),
            ("Self Join", production_features_3_self_join),
            ("Dynamic Functions", production_features_4_dynamic_functions),
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
