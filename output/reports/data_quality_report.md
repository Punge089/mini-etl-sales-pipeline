# Data Quality Report

This report shows the basic checks from the transform step.

## Row Counts

| Metric | Count |
| --- | ---: |
| Raw rows extracted | 120 |
| Duplicate rows removed | 1 |
| Invalid rows removed after deduplication | 4 |
| Total rows removed | 5 |
| Final rows loaded | 115 |
| Rows transformed | 115 |

## Issues Found

| Check | Count | Action |
| --- | ---: | --- |
| Missing quantity values | 3 | Filled with 1 |
| Invalid or missing dates | 2 | Removed rows |
| Invalid quantity values | 0 | Removed rows |
| Non-positive quantity values | 0 | Removed rows |
| Missing or invalid unit prices | 2 | Removed rows |
| Non-positive unit prices | 0 | Removed rows |

## Missing Text Values Filled

| Column | Filled Values |
| --- | ---: |
| customer_id | 0 |
| product | 2 |
| category | 0 |
| region | 3 |

## Transformations Added

- New columns created: revenue, order_month
- Revenue was calculated as quantity multiplied by unit price.
- Order month was created from the cleaned order date.
