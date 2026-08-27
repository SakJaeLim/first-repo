from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    target = Path(path)
    text = target.read_text()
    if old not in text:
        raise SystemExit(f"expected snippet not found in {path}")
    target.write_text(text.replace(old, new, 1))


replace_once(
    "xazz-server/src/bin/security_api.rs",
    '#[allow(dead_code)]\n#[path = "../audit_log.rs"]',
    '#[allow(dead_code, clippy::needless_borrows_for_generic_args)]\n#[path = "../audit_log.rs"]',
)

replace_once(
    "xazz-server/src/security.rs",
    'safe_columns.iter().cloned().collect::<Vec<_>>().join(", ")',
    'safe_columns.join(", ")',
)

replace_once(
    "xazz-server/src/security.rs",
    '        assert!(report.safe_to_execute, "{:#?}", report.violations);\n        assert_eq!(report.decision, GuardDecision::Approved);',
    '        assert!(report.safe_to_execute, "{:#?}", report.violations);\n        assert!(report.warnings.is_empty(), "{:#?}", report.warnings);\n        assert_eq!(report.decision, GuardDecision::Approved);',
)

replace_once(
    "xazz-compiler/src/checker.rs",
    '''                PipelineOp::Count(Some(c))
                | PipelineOp::Sum(c)
                | PipelineOp::Mean(c)
                | PipelineOp::Min(c)
                | PipelineOp::Max(c)
                | PipelineOp::Median(c)
                | PipelineOp::Variance(c)
                | PipelineOp::Std(c) => {
                    self.check_agg_column(c, &cols);
                    pending_group = None;
                }
                PipelineOp::Count(None) => {}''',
    '''                PipelineOp::Count(Some(c)) => {
                    // count() is valid for numeric and non-numeric columns; only existence matters.
                    self.check_column(c, "count", &cols);
                    pending_group = None;
                }
                PipelineOp::Sum(c)
                | PipelineOp::Mean(c)
                | PipelineOp::Min(c)
                | PipelineOp::Max(c)
                | PipelineOp::Median(c)
                | PipelineOp::Variance(c)
                | PipelineOp::Std(c) => {
                    self.check_agg_column(c, &cols);
                    pending_group = None;
                }
                PipelineOp::Count(None) => {
                    // A row count is also a valid aggregation after groupBy.
                    pending_group = None;
                }''',
)

checker = Path("xazz-compiler/src/checker.rs")
checker_text = checker.read_text()
if "fn count_accepts_string_columns_without_numeric_warning()" not in checker_text:
    insertion = r'''

    #[test]
    fn count_accepts_string_columns_without_numeric_warning() {
        let result = check(
            r#"
            type Patient = {
                age_band: string,
                disease: string,
            }
            v raw = load("patients.csv") :: Patient
            v safe = raw |> groupBy("age_band") |> count("disease")
            "#,
        );
        assert!(result.errors.is_empty(), "{:#?}", result.errors);
        assert!(result.warnings.is_empty(), "{:#?}", result.warnings);
    }

    #[test]
    fn row_count_completes_grouped_pipeline() {
        let result = check(
            r#"
            type Patient = {
                age_band: string,
                disease: string,
            }
            v raw = load("patients.csv") :: Patient
            v safe = raw |> groupBy("age_band") |> count
            "#,
        );
        assert!(result.errors.is_empty(), "{:#?}", result.errors);
        assert!(result.warnings.is_empty(), "{:#?}", result.warnings);
    }
'''
    end = checker_text.rfind("\n}")
    if end < 0:
        raise SystemExit("checker test module closing brace not found")
    checker.write_text(checker_text[:end] + insertion + checker_text[end:])
