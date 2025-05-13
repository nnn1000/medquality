#!/bin/bash
echo "开始导入医疗质量指标..."
python scripts/import_all_indicators.py
echo ""
echo "按任意键继续..."
read -n 1 -s 